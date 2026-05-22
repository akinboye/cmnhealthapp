# Cure My Nation RAG Chatbot - Complete Implementation Guide

## Overview

This is a complete RAG (Retrieval-Augmented Generation) chatbot system for the Cure My Nation health app. It provides intelligent responses to user questions about patient rights, healthcare services, and health information.

## Architecture

```
┌─────────────────┐
│   Flutter App   │
│  (Mobile/Web)   │
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────────────────┐
│    Flask Backend API        │
│  (Python + LangChain)       │
├─────────────────────────────┤
│ • Chat Endpoint             │
│ • Document Retrieval        │
│ • Document Upload           │
│ • System Status             │
└─────────┬───────────────────┘
          │
    ┌─────┴─────┬──────────────┐
    ▼           ▼              ▼
┌─────────┐ ┌────────────┐ ┌──────────┐
│ FAISS   │ │ OpenAI API │ │Documents │
│ Vector  │ │ (GPT-3.5)  │ │(PDFs,TXT)│
│ Store   │ │            │ │          │
└─────────┘ └────────────┘ └──────────┘
```

## Features

✅ **RAG Technology**
- Retrieves relevant documents from knowledge base
- Augments queries with context
- Generates accurate responses using LLM

✅ **Multi-Document Support**
- PDF documents
- Text files
- Website scraping
- Easy document management

✅ **Multi-Language**
- English, Yoruba, Hausa, Igbo
- Easy to extend

✅ **User-Friendly Interface**
- Real-time chat
- Message history
- Typing indicator
- Source citations

✅ **Production Ready**
- Error handling
- Rate limiting support
- Cloud deployment ready
- Scalable architecture

## Quick Start

### For Flutter Developers

1. **Copy the chatbot files to your Flutter project:**
   ```
   lib/
   ├── screens/
   │   └── chatbot/
   │       └── chatbot_screen.dart
   ├── services/
   │   └── chatbot_service.dart
   ├── models/
   │   └── chatbot_message_model.dart
   ├── widgets/
   │   └── chatbot_floating_button.dart
   └── config/
       └── chatbot_config.dart
   ```

2. **Add HTTP package to pubspec.yaml:**
   ```yaml
   dependencies:
     http: ^1.1.0
   ```

3. **Add navigation to chatbot:**
   ```dart
   FloatingActionButton(
     onPressed: () {
       Navigator.push(
         context,
         MaterialPageRoute(
           builder: (context) => ChatbotScreen(language: 'en'),
         ),
       );
     },
     child: Icon(Icons.chat),
   )
   ```

4. **Update API endpoint in `chatbot_config.dart`**

### For Backend Developers

1. **Set up Python backend:**
   ```bash
   cd chatbot_backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   echo "OPENAI_API_KEY=sk-your-key" > .env
   ```

3. **Add documents:**
   ```bash
   # Place PDFs/text files in documents/ folder
   python document_processor.py  # Optional: scrape websites
   ```

4. **Run locally:**
   ```bash
   python app.py
   ```

5. **Deploy to cloud:**
   See deployment section in backend README

## File Structure

```
cmnhealthapp/
├── lib/
│   ├── screens/
│   │   └── chatbot/
│   │       └── chatbot_screen.dart          # Main chat UI
│   ├── services/
│   │   └── chatbot_service.dart             # API communication
│   ├── models/
│   │   └── chatbot_message_model.dart       # Message data model
│   ├── widgets/
│   │   └── chatbot_floating_button.dart     # FAB widget
│   └── config/
│       └── chatbot_config.dart              # Configuration
│
└── chatbot_backend/
    ├── app.py                               # Flask application
    ├── document_processor.py                # Document handling
    ├── requirements.txt                     # Python dependencies
    ├── README.md                            # Backend setup guide
    └── documents/                           # Knowledge base
        ├── patient_bill_of_rights_nigeria.pdf
        └── curemynation_website.txt
```

## Document Management

### Adding Documents

**Option 1: Place in folder (recommended)**
```bash
# Copy PDFs or text files to documents/ folder
cp patient_rights.pdf chatbot_backend/documents/
cp health_info.txt chatbot_backend/documents/
# Restart app - vector store rebuilds automatically
```

**Option 2: Upload via API**
```bash
curl -X POST http://localhost:5000/api/upload \
  -F "file=@document.pdf" \
  -F "document_name=Patient Rights" \
  -F "document_type=pdf"
```

**Option 3: Scrape website**
```bash
python chatbot_backend/document_processor.py
```

### Included Documents

- **patient_bill_of_rights_nigeria.pdf** - Complete PBOR guide
- **curemynation_website.txt** - Website content (auto-scraped)

### Adding More Documents

When you have additional PDFs:

1. Convert to text or keep as PDF
2. Place in `chatbot_backend/documents/`
3. Restart backend
4. Vector store automatically indexes them

## API Endpoints

### Chat
```
POST /api/chat
Content-Type: application/json

{
  "query": "What are my patient rights?",
  "language": "en",
  "documentSources": []
}

Response:
{
  "response": "Patient rights include...",
  "sources": ["document1.pdf", "document2.txt"],
  "language": "en",
  "timestamp": "2024-05-18T..."
}
```

### Retrieve Documents
```
POST /api/retrieve
{
  "query": "patient confidentiality",
  "top_k": 5
}

Response:
{
  "documents": [
    {
      "content": "...",
      "source": "document.pdf",
      "score": 0.95
    }
  ]
}
```

### Upload Document
```
POST /api/upload (multipart/form-data)
- file: [file]
- document_name: "Name"
- document_type: "pdf"
```

### System Status
```
GET /api/status

Response:
{
  "status": "ready",
  "documents_loaded": 2,
  "vector_store_exists": true,
  "timestamp": "2024-05-18T..."
}
```

### Health Check
```
GET /health

Response:
{
  "status": "ok"
}
```

## Configuration

### Flutter (chatbot_config.dart)

```dart
// Change environment
static const String environment = 'development';

// Update API endpoint
static const Map<String, String> baseUrls = {
  'development': 'http://localhost:5000',
  'production': 'https://your-api-domain.com',
};

// Adjust LLM settings
static const String model = 'gpt-3.5-turbo';
static const double temperature = 0.7;
```

### Backend (.env)

```env
OPENAI_API_KEY=sk-your-api-key
FLASK_ENV=development
```

## Integration Examples

### Add Chatbot to Home Screen

```dart
import 'package:flutter/material.dart';
import 'screens/chatbot/chatbot_screen.dart';
import 'widgets/chatbot_floating_button.dart';

class HomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Home')),
      body: Center(child: Text('Welcome')),
      floatingActionButton: ChatbotFloatingButton(
        onPressed: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => ChatbotScreen(language: 'en'),
            ),
          );
        },
      ),
    );
  }
}
```

### Add to Navigation Menu

```dart
ListTile(
  leading: Icon(Icons.chat),
  title: Text('Health Assistant'),
  onTap: () {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => ChatbotScreen()),
    );
  },
)
```

See `CHATBOT_INTEGRATION_EXAMPLES.md` for more examples.

## Deployment

### Local Development

```bash
# Terminal 1: Backend
cd chatbot_backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py

# Terminal 2: Flutter
cd ..
flutter run -d chrome  # or your device
```

### Production - Google Cloud Run

```bash
cd chatbot_backend

# Create Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
EOF

# Deploy
gcloud run deploy cure-my-nation-chatbot \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=sk-your-key
```

Update Flutter API endpoint to the Cloud Run URL.

## Testing

### Test Backend Locally

```bash
# Start backend
python chatbot_backend/app.py

# Test chat
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the right to privacy?",
    "language": "en"
  }'

# Test status
curl http://localhost:5000/api/status
```

### Test Flutter App

1. Ensure backend is running
2. Update API endpoint in `chatbot_config.dart` to `http://localhost:5000`
3. Run: `flutter run`
4. Click chatbot button
5. Send a message

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Connection refused" | Ensure backend is running on port 5000 |
| "No documents loaded" | Place PDFs in `chatbot_backend/documents/` |
| "Invalid API key" | Check OPENAI_API_KEY in `.env` file |
| "Empty responses" | Vector store may be empty, add documents |
| "CORS error" | Ensure Flask-CORS is installed and enabled |

## Cost Management

OpenAI API usage (example):
- Embeddings: ~$0.00002 per 1K tokens
- GPT-3.5-turbo: ~$0.0005 per 1K prompt tokens
- Average chat: $0.01-$0.02

**Cost reduction tips:**
1. Use document chunking efficiently
2. Implement response caching
3. Use GPT-3.5-turbo instead of GPT-4
4. Set max_tokens appropriately

## Performance Optimization

1. **Vector Store Caching**: Preload vector store on startup
2. **Response Caching**: Cache common queries
3. **Batch Processing**: Process multiple queries together
4. **Document Indexing**: Index documents efficiently

## Security Considerations

1. **API Key Protection**: Store OPENAI_API_KEY securely
2. **CORS**: Configure CORS for your domain
3. **Rate Limiting**: Implement in production
4. **Input Validation**: Sanitize user inputs
5. **HTTPS**: Use HTTPS in production

## Monitoring

Monitor these metrics:
- Response time
- Document retrieval accuracy
- API token usage
- Error rates
- User satisfaction

## Roadmap

- [ ] Fine-tune embeddings
- [ ] Add voice input
- [ ] Implement feedback loop
- [ ] Multi-user chat history
- [ ] Admin dashboard
- [ ] Analytics dashboard
- [ ] Response quality scoring

## Support & Resources

**Documentation:**
- [Backend Setup](chatbot_backend/README.md)
- [Integration Examples](CHATBOT_INTEGRATION_EXAMPLES.md)

**References:**
- [LangChain Docs](https://python.langchain.com/)
- [OpenAI API](https://platform.openai.com/docs/)
- [FAISS](https://github.com/facebookresearch/faiss)
- [Flutter Navigation](https://flutter.dev/docs/development/navigation)

## License

This chatbot is part of the Cure My Nation Health App.

## Contributors

- AI/LLM Team
- Flutter Development Team
- Backend Infrastructure Team

---

Last Updated: May 18, 2024
Version: 1.0.0
