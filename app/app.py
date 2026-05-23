"""
Cure My Nation — Web Application
Flask backend serving HTML pages + REST API, PostgreSQL database
"""

from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail
from werkzeug.middleware.proxy_fix import ProxyFix
from pathlib import Path
import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv(override=True)

# ─── LangChain imports (chatbot) ────────────────────────────────────────────
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PDFPlumberLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage

# ─── Database + blueprints ──────────────────────────────────────────────────
from models import db, init_db, User, Violation
from auth import auth_bp
from violations import violations_bp
from blogs import blogs_bp
from events import events_bp
from live_chat import live_chat_bp

# ─── App setup ──────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
app = Flask(__name__, template_folder='templates', static_folder='static')

# Handle reverse-proxy subdirectory (e.g. /healthapp on cPanel)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Restrict CORS to configured origins (default: localhost only)
_allowed_origins = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:5000,http://127.0.0.1:5000').split(',')
CORS(app, resources={r"/api/*": {"origins": _allowed_origins}}, supports_credentials=True)

# Rate limiter — keyed by remote IP
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[],          # no global limit; apply per-route
    storage_uri='memory://',
)

# ─── Configuration ──────────────────────────────────────────────────────────
database_url = os.getenv('DATABASE_URL', 'mysql+pymysql://root:password@localhost:3306/curemynation')
# Normalise mysql:// → mysql+pymysql://
if database_url.startswith('mysql://') and not database_url.startswith('mysql+'):
    database_url = database_url.replace('mysql://', 'mysql+pymysql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'change-me-in-production')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY') or os.getenv('SECRET_KEY', 'jwt-change-me-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)
# Allow JWT from Authorization header OR cookie named 'access_token'
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']
app.config['JWT_COOKIE_SECURE'] = False          # set True in production (HTTPS)
app.config['JWT_COOKIE_SAMESITE'] = 'Lax'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False    # simplified for SPA usage

# Flask-Mail
app.config['MAIL_SERVER']   = os.getenv('MAIL_SERVER', 'curemynation.org')
app.config['MAIL_PORT']     = int(os.getenv('MAIL_PORT', 465))
app.config['MAIL_USE_SSL']  = os.getenv('MAIL_USE_SSL', 'True') == 'True'
app.config['MAIL_USE_TLS']  = os.getenv('MAIL_USE_TLS', 'False') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', '')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', '')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'Cure My Nation <healthappuser@curemynation.org>')
app.config['APP_URL'] = os.getenv('APP_URL', 'http://localhost:5000')
mail = Mail(app)

if database_url.startswith('mysql'):
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'pool_size': 10,
        'max_overflow': 20,
    }
    print(f'[OK] MySQL configured: {database_url.split("@")[-1]}')
elif database_url.startswith('postgresql') or database_url.startswith('postgres'):
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'pool_size': 10,
        'max_overflow': 20,
    }
    print(f'[OK] PostgreSQL configured: {database_url.split("@")[-1]}')
else:
    print(f'[OK] Database configured: {database_url}')

db.init_app(app)
jwt = JWTManager(app)

# ─── Template globals ────────────────────────────────────────────────────────
@app.context_processor
def inject_app_base():
    # request.script_root is set automatically by Passenger (SCRIPT_NAME)
    # or by ProxyFix (X-Forwarded-Prefix). Empty string on plain localhost.
    app_base = request.script_root
    print(f'[DEBUG] inject_app_base: script_root={app_base}, path={request.path}')
    return dict(APP_BASE=app_base)

# ─── Security headers ───────────────────────────────────────────────────────
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    # Only send HSTS on HTTPS
    if request.is_secure:
        response.headers['Strict-Transport-Security'] = 'max-age=63072000; includeSubDomains'
    # CSP: allow Tailwind CDN, SheetJS CDN, same-origin scripts/styles
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com https://cdn.sheetjs.com; "
        "style-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data: https:; "
        "connect-src 'self' https://translate.googleapis.com; "
        "frame-ancestors 'none';"
    )
    return response

app.register_blueprint(auth_bp)
app.register_blueprint(violations_bp)
app.register_blueprint(blogs_bp)
app.register_blueprint(events_bp)
app.register_blueprint(live_chat_bp)

# ─── Per-route rate limits ───────────────────────────────────────────────────
# Apply after registration so the view functions exist
from auth import login, register, forgot_password
limiter.limit('10 per minute')(login)
limiter.limit('5 per hour')(register)
limiter.limit('5 per hour')(forgot_password)

# ─── Chatbot setup ──────────────────────────────────────────────────────────
DOCS_DIR = str(BASE_DIR / 'documents')
VECTOR_DIR = str(BASE_DIR / 'vector_store')
os.makedirs(DOCS_DIR, exist_ok=True)
os.makedirs(VECTOR_DIR, exist_ok=True)

embeddings = llm = qa_retriever = None

HEALTH_PROMPT = PromptTemplate(
    template="""You are an expert health information assistant for the Cure My Nation Initiative.
You provide information about patient rights, healthcare services, and health education in Nigeria.
Use the context below to answer the question. Be empathetic, clear and actionable.
If you don't know the answer, say so clearly.

Context:
{context}

Conversation History:
{history}

Current Question: {question}

Answer:""",
    input_variables=["context", "history", "question"],
)

try:
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        print(f'[DEBUG] Initializing OpenAI with key: {api_key[:20]}...')
        embeddings = OpenAIEmbeddings(
            openai_api_key=api_key,
            model='text-embedding-3-small',
        )
        llm = ChatOpenAI(
            openai_api_key=api_key,
            model_name='gpt-3.5-turbo',
            temperature=0.7,
            max_tokens=1024,
        )
        print('[OK] OpenAI initialized successfully')
    else:
        print('[WARN] OPENAI_API_KEY not found in environment')
except Exception as e:
    print(f'[ERROR] OpenAI init failed: {type(e).__name__}: {e}')


def load_documents():
    docs = []
    for fp in Path(DOCS_DIR).glob('*'):
        try:
            if fp.suffix.lower() == '.pdf':
                docs.extend(PDFPlumberLoader(str(fp)).load())
            elif fp.suffix.lower() == '.txt':
                docs.extend(TextLoader(str(fp)).load())
        except Exception as e:
            print(f'[WARN] Error loading {fp}: {e}')
    return docs


def init_vector_store():
    global qa_retriever
    print(f'[DEBUG] init_vector_store called: embeddings={bool(embeddings)}, llm={bool(llm)}')
    if not embeddings or not llm:
        print('[ERROR] Cannot initialize vector store: OpenAI not ready')
        return
    try:
        print(f'[DEBUG] Attempting to load vector store from {VECTOR_DIR}')
        vs = FAISS.load_local(VECTOR_DIR, embeddings, allow_dangerous_deserialization=True)
        print('[OK] Loaded existing vector store')
    except Exception as e:
        print(f'[DEBUG] Creating new vector store: {type(e).__name__}: {e}')
        documents = load_documents()
        print(f'[DEBUG] Loaded {len(documents)} document(s)')
        if not documents:
            print('[ERROR] No documents found — chatbot disabled')
            return
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(documents)
        print(f'[DEBUG] Split into {len(chunks)} chunks')
        vs = FAISS.from_documents(chunks, embeddings)
        vs.save_local(VECTOR_DIR)
        print(f'[OK] Created vector store from {len(documents)} document(s)')
    qa_retriever = vs.as_retriever(search_kwargs={'k': 5})
    print('[OK] Chatbot retriever ready')


# ─── Seed default users ─────────────────────────────────────────────────────
def seed_default_users():
    from uuid import uuid4
    defaults = [
        dict(email='healthappadmin@curemynation.org', old_email='admin@cmnhealth.com',
             firstName='Super', lastName='Admin',
             phone='+234123456789', state='Lagos', password='@healthappadmin123456_',
             isAdmin=True, adminRole='superAdmin',
             adminPrivileges=['manage_admins', 'create_blog', 'edit_blog',
                              'delete_blog', 'publish_blog', 'view_analytics',
                              'manage_users', 'moderate_comments']),
        dict(email='healthappuser@curemynation.org', old_email='user@cmnhealth.com',
             firstName='John', lastName='Doe',
             phone='+234987654321', state='Abuja', password='@healthappuser123456_',
             isAdmin=False, adminRole=None, adminPrivileges=[]),
    ]
    created = 0
    for d in defaults:
        # Migrate old email to new email if old account exists
        old = User.query.filter_by(email=d['old_email']).first()
        if old:
            old.email = d['email']
            old.set_password(d['password'])
            db.session.commit()
            print(f'[OK] Updated credentials for {d["email"]}')
            continue
        if not User.query.filter_by(email=d['email']).first():
            u = User(
                id=str(uuid4()),
                email=d['email'],
                firstName=d['firstName'],
                lastName=d['lastName'],
                phone=d['phone'],
                state=d['state'],
                isAdmin=d['isAdmin'],
                adminRole=d['adminRole'],
                adminPrivileges=json.dumps(d['adminPrivileges']) if d['adminPrivileges'] else None,
            )
            u.set_password(d['password'])
            db.session.add(u)
            created += 1
    if created:
        db.session.commit()
        print(f'[OK] Seeded {created} default user(s)')


# ─── Page routes ────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/forgot-password')
def forgot_password_page():
    return render_template('forgot_password.html')


@app.route('/reset-password')
def reset_password_page():
    return render_template('reset_password.html')


@app.route('/register')
def register_page():
    return render_template('register.html')


@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')


@app.route('/violations')
def violations_page():
    return render_template('violations.html')


@app.route('/violations/new')
def violation_new_page():
    return render_template('violations_new.html')


@app.route('/chatbot')
def chatbot_page():
    return render_template('chatbot.html')


@app.route('/resources')
def resources_page():
    return render_template('resources.html')


@app.route('/blog/<blog_id>')
def blog_post_page(blog_id):
    return render_template('blog_post.html', blog_id=blog_id)


@app.route('/profile')
def profile_page():
    return render_template('profile.html')


@app.route('/admin')
def admin_page():
    return render_template('admin/dashboard.html')


@app.route('/admin/violations')
def admin_violations_page():
    return render_template('admin/violations.html')


@app.route('/admin/blog')
def admin_blog_page():
    return render_template('admin/blog.html')


@app.route('/blog')
def blog_page():
    return render_template('blog.html')


@app.route('/events')
def events_page():
    return render_template('events.html')


@app.route('/admin/users')
def admin_users_page():
    return render_template('admin/users.html')


@app.route('/admin/events')
def admin_events_page():
    return render_template('admin/events.html')


@app.route('/admin/chat')
def admin_chat_page():
    return render_template('admin/chat.html')


# ─── Chat API ────────────────────────────────────────────────────────────────
@app.route('/api/chat', methods=['POST'])
@limiter.limit('20 per minute')
def chat():
    try:
        data = request.get_json(silent=True) or {}
        query = (data.get('query') or '').strip()
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        if len(query) > 500:
            return jsonify({'error': 'Query too long (max 500 characters)'}), 400
        if not qa_retriever:
            return jsonify({
                'error': 'Chatbot not available',
                'message': 'OpenAI API key not configured or no documents loaded',
            }), 503
        # Build conversation history string from last 6 turns
        raw_history = data.get('history') or []
        if isinstance(raw_history, list):
            history_lines = []
            for turn in raw_history[-6:]:
                role = turn.get('role', '')
                content = (turn.get('content') or '').strip()[:400]
                if role == 'user':
                    history_lines.append(f'User: {content}')
                elif role == 'ai':
                    history_lines.append(f'Assistant: {content}')
            history_text = '\n'.join(history_lines) if history_lines else 'None'
        else:
            history_text = 'None'
        source_docs = qa_retriever.invoke(query)
        context = '\n\n'.join(d.page_content for d in source_docs)
        prompt_text = HEALTH_PROMPT.format(context=context, history=history_text, question=query)
        ai_response = llm.invoke([HumanMessage(content=prompt_text)])
        sources = [{'content': d.page_content[:200], 'source': d.metadata.get('source', 'Unknown')}
                   for d in source_docs[:3]]
        return jsonify({
            'response': ai_response.content,
            'sources': sources,
        }), 200
    except Exception as e:
        print(f'[ERROR] Chat: {e}')
        return jsonify({'error': 'An error occurred processing your request'}), 500


# ─── Status API ──────────────────────────────────────────────────────────────
@app.route('/api/status')
def status():
    try:
        with app.app_context():
            users = User.query.count()
            violations = Violation.query.count()
        return jsonify({
            'status': 'operational',
            'database': 'connected',
            'users': users,
            'violations': violations,
            'chatbot': 'ready' if qa_retriever else 'disabled',
            'timestamp': datetime.utcnow().isoformat(),
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(_):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Endpoint not found'}), 404
    return render_template('index.html'), 404


@app.errorhandler(500)
def internal_error(_):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Internal server error'}), 500
    return render_template('index.html'), 500


# ─── Bootstrap ───────────────────────────────────────────────────────────────
def init_app():
    with app.app_context():
        init_db(app)
        seed_default_users()
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        print(f'[DEBUG] OPENAI_API_KEY is set ({len(api_key)} chars)')
        init_vector_store()
    else:
        print('[ERROR] OPENAI_API_KEY not set — chatbot disabled')


if __name__ == '__main__':
    init_app()
    port = int(os.getenv('PORT', 5000))
    print(f'\n{"=" * 60}')
    print('  Cure My Nation — Web Application')
    print(f'  http://localhost:{port}')
    print(f'  Database: {database_url.split("@")[-1] if "@" in database_url else database_url}')
    print(f'{"=" * 60}\n')
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_ENV') == 'development')
