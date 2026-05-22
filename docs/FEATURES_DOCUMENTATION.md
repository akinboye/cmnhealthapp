# CMN Health Rights App - Features Documentation

## 📋 Complete Feature List

### 1. Authentication & User Management

#### Registration (Signup)
- **Fields:**
  - Email (required, validated)
  - Username (required)
  - First Name (required)
  - Last Name (required)
  - Phone (required)
  - Address (required)
  - State (dropdown with 36 Nigerian states)
  - Password (minimum 6 characters)
  - Confirm Password (must match)

- **Features:**
  - Form validation with error messages
  - Success confirmation dialog
  - Redirect to login after signup
  - Account creation timestamp
  - Automatic profile creation

- **Security:**
  - Password hashing
  - Duplicate email prevention
  - Required field validation

#### Login
- **Fields:**
  - Email (required)
  - Password (required)
  - Forgot Password link

- **Features:**
  - Email/password validation
  - JWT token generation
  - Session management
  - Remember me capability (future)
  - Error handling with user feedback

- **Security:**
  - Password verification with hashed value
  - User existence check
  - Token expiration (7 days)

#### Profile Management
- **Edit Profile:**
  - Update first name, last name
  - Update phone, address, state
  - Email is not editable (for security)
  - Update button with confirmation

- **Password Management:**
  - Change current password
  - Verify old password before change
  - New password confirmation
  - Secure password storage

- **Account Deletion:**
  - Confirmation dialog with warning
  - Complete data removal
  - Automatic logout
  - Cannot be undone

### 2. Home/Landing Screen

**Purpose:** Introduce application to guest users

**Sections:**
1. **Hero Section**
   - Large health icon
   - App title and subtitle
   - Prominent call-to-action (Get Started)
   - Primary color background

2. **Information Cards**
   - Patient Rights Information
   - Healthcare Violation Reporting
   - Educational Resources Access
   - 24/7 Support Information

3. **Key Features Highlight**
   - Structured Violation Reporting
   - AI Chatbot Support
   - Real-time Dashboard
   - Multilingual Support

4. **Expected Impact Section**
   - 1000+ Healthcare Professionals
   - 50,000+ Patient Consultations
   - 28 States Nationwide Coverage
   - 24/7 Support Availability

5. **Call-to-Action**
   - Sign Up Now button
   - Alternative login link

**Navigation:**
- Get Started → Signup Screen
- Sign In → Login Screen

### 3. User Dashboard

**Purpose:** Main hub for authenticated users

**Components:**

1. **Welcome Section**
   - User avatar with initials
   - Personalized greeting ("Welcome back, [Name]!")
   - User email display
   - Member since date

2. **Key Metrics Grid (4 cards)**
   - **Violations Reported** (blue card with report icon)
   - **Resolved Cases** (green card with checkmark)
   - **In Progress Cases** (orange card with hourglass)
   - **Resolution Rate** (purple card with percentage)

3. **Quick Actions (3 buttons)**
   - Report Violation (primary action)
   - View Resources (secondary action)
   - Contact Support (success color)

4. **Healthcare Tips Section**
   - Displays 4 quick healthcare tips
   - Each tip shows title and content
   - Updated dynamically

**Floating Action Button:**
- "Report Violation" button for quick access
- Only visible on dashboard tab

### 4. Violation Reporting System

**Purpose:** Allow users to report healthcare violations

**Form Fields:**

1. **Violation Type** (Dropdown)
   - Medical Malpractice
   - Denial of Treatment
   - Negligence
   - Over Charging
   - Infection Control
   - Privacy Violation
   - Mistreated
   - Other

2. **Date of Incident**
   - Date picker interface
   - Limited to past dates (validation)
   - Defaults to today

3. **Hospital/Clinic Name**
   - Text field with validation
   - Required field

4. **Description** (Multiline)
   - 4-line text area
   - Detailed explanation of violation
   - Required field

5. **Evidence Attachment**
   - File picker interface
   - Support for multiple files
   - Document, image, or video

6. **Priority Level** (Dropdown)
   - Low (green)
   - Medium (orange)
   - High (red)
   - Critical (dark red)

**Features:**
- Full form validation
- Error messages for invalid inputs
- Submit and Cancel buttons
- Success confirmation dialog
- Violation ID generation (VIOL_[UserID]_[Counter]_[Timestamp])

**Data Stored:**
- Violation ID
- User ID
- Type, Date, Hospital Name
- Description, Evidence, Priority
- Status (initially "Reported")
- Date Reported
- User's state

### 5. Violations Dashboard

**Purpose:** Analytics and aggregated violation data

**Sections:**

1. **Overall Statistics** (4 metric cards)
   - Total Violations (global)
   - Resolved Cases (count)
   - In Progress (count)
   - Pending Cases (count)

2. **Violations by Type** (Progress bars)
   - Lists all violation types
   - Shows count and percentage
   - Progress bar visualization
   - Ordered by frequency

3. **Top States Analysis** (Top 8)
   - State name with violation count
   - Progress bars for comparison
   - Sorted by highest count
   - Geographic distribution view

4. **Status Breakdown** (Color-coded)
   - Reported: Blue
   - In Progress: Orange
   - Resolved: Green
   - On Hold: Red

**Data Aggregation:**
- Real-time calculations
- Filtered by status
- Grouped by violation type
- Geographic filtering
- Trend analysis preparation

### 6. Healthcare Resources & Education

**Purpose:** Provide comprehensive healthcare information

**Featured Categories (7 total):**

1. **Patient Rights in Nigeria**
   - Right to Information
   - Right to Dignity and Respect
   - Right to Quality Healthcare
   - Right to Complaint and Redressal

2. **Signs of Medical Malpractice**
   - Common warning signs (6 types)
   - How to document issues
   - Steps to take

3. **Healthcare Consumer Protection Act**
   - Coverage details
   - Consumer protections
   - Filing complaints (3 levels)
   - Compensation types

4. **Medication Safety Guidelines**
   - Before taking medicine
   - During treatment
   - Red flags to watch
   - Questions to ask

5. **Hospital Rights and Responsibilities**
   - Your rights as patient
   - Your responsibilities
   - Hospital responsibilities

6. **Mental Health Rights**
   - Treatment rights
   - Right to dignity
   - Legal protections
   - Getting help resources

7. **Additional Healthcare Resources**
   - Government resources
   - Emergency contacts
   - Complaint authorities
   - Support organizations

**Features:**

1. **Search Functionality**
   - Real-time search as you type
   - Searches title, description, content
   - Case-insensitive matching

2. **Category Filtering**
   - "All Categories" option
   - Filter by single category
   - Dynamic resource updating

3. **Resource Cards**
   - Title and category display
   - Description preview truncated
   - Save/bookmark functionality
   - Read More link

4. **Full Resource View**
   - Modal dialog with full content
   - Markdown formatted content
   - Close button

5. **Save for Later**
   - Bookmark icon (outline or filled)
   - Persists across sessions
   - View saved resources separately

6. **Healthcare Tips Section**
   - 4 quick tips displayed
   - Currently: Keep records, Ask questions, Verify meds, Know rights
   - Icon-based presentation
   - Category indicators

### 7. 24/7 Support Center

**Purpose:** Provide customer support and assistance

**Two Main Sections:**

**A. AI Chatbot Support**

Features:
- Support information card
- AI Chatbot availability info
- Simulation of bot responses
- Message sending interface
- Chat history

Bot Features:
- Automated response simulation
- Context-aware responses
- Message persistence
- Loading indicators

**B. Support Tickets**

Features:
- Create new support ticket
- View existing tickets
- Ticket status (Open/Closed)
- Subject and description
- Ticket ID for reference
- Support history view

Ticket Form:
- Subject field
- Description field
- Form validation
- Success confirmation

**C. Helpline Information**

- Toll-free number: 1800-CMN-HELP
- 24/7 availability
- Multilingual support (10 languages)
- Direct calling capability

**D. Multilingual Support**

Supported languages in support:
1. English
2. Yorùbá
3. Hausa
4. Igbo
5. Français
6. Hindi
7. Tamil
8. Telugu
9. Kannada
10. Malayalam

### 8. Patient Profile & Settings

**Purpose:** User account management and preferences

**Four Tabs:**

**Tab 1: Profile Information**
- Avatar display with initials
- Email address (read-only)
- Editable fields:
  - First Name
  - Last Name
  - Phone
  - Address
  - State
- Update button

**Tab 2: Preferences**
- Language selection (10 languages)
- Notification preferences:
  - Email notifications (toggle)
  - SMS alerts (toggle)
  - News & Advocacy updates (toggle)

**Tab 3: Privacy & Security**
- Change Password section:
  - Old password field
  - New password field
  - Confirm password field
  - Validation and confirmation
- Delete Account section:
  - Warning dialog
  - Confirmation required
  - Permanent deletion

**Tab 4: About**
- App icon display
- App title and version
- Company mission statement
- Mission: "Empowering patients and protecting healthcare rights across nations"
- Copyright notice (© 2024 Cure my Nation)
- Logout button

### 9. Multilingual Support (10 Languages)

**Supported Languages:**
1. English
2. Yorùbá (Nigerian)
3. Hausa (Nigerian)
4. Igbo (Nigerian)
5. Français (French)
6. Pidgin (Nigerian)
7. Fulfulde (Nigerian)
8. Arabic
9. Swahili
10. Portuguese

**Translation Coverage:**
- 500+ translatable strings
- All UI labels
- Button texts
- Dialog messages
- Error messages
- Tooltips and hints

**Language Switching:**
- Dropdown in login/signup screens
- Preferences tab on profile
- Immediate UI update
- Preference persistence

**Translations Included:**
- Authentication screens
- Navigation labels
- Form labels and placeholders
- Success/error messages
- Screen titles
- Menu items
- Help text

### 10. Responsive Design

**Breakpoints:**
- Mobile: < 600px
- Tablet: 600px - 1000px
- Desktop: > 1000px

**Responsive Features:**

1. **Layout Adaptation**
   - Single column on mobile
   - Multi-column on larger screens
   - Flexible grid layouts
   - Adaptive padding and margins

2. **Navigation**
   - Bottom navigation for mobile
   - Bottom nav bar for tablet
   - Full navigation for desktop

3. **Components**
   - Touch-friendly sizing
   - Adaptive font sizes
   - Responsive images
   - Flexible containers

4. **Forms**
   - Full width on mobile
   - Constrained width on web
   - Proper spacing
   - Accessible inputs

5. **Cards & Modals**
   - Responsive grid layouts
   - Scrollable on small screens
   - Full-screen modals on mobile
   - Dialog modals on large screens

### 11. Data Visualization

**Charts & Statistics:**

1. **Metric Cards**
   - Large number display
   - Category label
   - Color coding
   - Icon indicators

2. **Progress Bars**
   - Linear progress indicators
   - Color-coded status
   - Percentage display
   - Category labels

3. **Status Indicators**
   - Reported: Blue (#2196F3)
   - In Progress: Orange (#FFC107)
   - Resolved: Green (#4CAF50)
   - On Hold: Dark Orange (#FF9800)

4. **Priority Indicators**
   - Low: Green
   - Medium: Orange
   - High: Red
   - Critical: Dark Red (#8B0000)

5. **Category Breakdown**
   - Violation type counts
   - Percentage calculations
   - Visual representations
   - Top statistics display

### 12. Navigation System

**App Navigation Flow:**

```
Login → Dashboard
      ├── Dashboard Tab
      ├── Violations Tab
      ├── Resources Tab
      ├── Support Tab
      └── Profile Tab
         └── Logout
         
Quick Actions:
├── Report Violation
├── View Resources
└── Contact Support
```

**Navigation Methods:**
1. Bottom Navigation Bar (5 items)
2. Floating Action Button
3. Quick Action Buttons
4. Inline Navigation Links
5. Dialog/Modal navigation

**Protected Routes:**
- All authenticated screens require login
- Automatic redirect to login if not authenticated
- Session validation
- Token verification

## 🎨 UI/UX Features

### Color Scheme
- **Primary:** #1976D2 (Blue) - Main actions
- **Secondary:** #00897B (Teal) - Alternative actions
- **Accent:** #FFB300 (Amber) - Highlights
- **Success:** #4CAF50 (Green) - Positive actions
- **Error:** #F44336 (Red) - Negative actions
- **Warning:** #FFC107 (Orange) - Cautions

### Typography
- **Headings:** Various sizes (24px - 32px)
- **Body Text:** 14px - 16px
- **Small Text:** 12px
- **Font:** Roboto (system default for platforms not specified)

### Spacing
- Standard padding: 16px
- Medium spacing: 24px
- Large spacing: 32px
- Component gaps: 8px - 16px

### Animations
- Smooth page transitions
- Button hover effects
- Loading indicators
- Fade-in animations (future)

## 🔄 User Workflows

### User Registration Flow
1. Open app → See login screen
2. Click "Sign Up"
3. Fill registration form
4. Submit
5. See success confirmation
6. Redirect to login
7. Login with new credentials

### Violation Reporting Workflow
1. Dashboard → Click "Report Violation" or FAB
2. Fill violation form
3. Select type, date, hospital, priority
4. Add description and evidence
5. Submit form
6. See success confirmation
7. Violation tracked in dashboard

### Resource Discovery Workflow
1. Dashboard → Resources tab
2. Search by keyword (optional)
3. Filter by category (optional)
4. Browse resource cards
5. Click "Read More" to view full content
6. Save for later (bookmark)
7. View saved resources

### Support Request Workflow
1. Dashboard → Support tab
2. Choose between chatbot or create ticket
3. For chatbot: Send message, receive response
4. For ticket: Fill subject and description, submit
5. View tickets list
6. Track ticket status

## 📱 Platform-Specific Features

### Web
- Responsive layout
- Dropdown menus
- Full-width content
- Keyboard shortcuts (future)
- Browser storage

### Android
- Material Design
- Native navigation gestures
- Back button handling
- Android-specific permissions
- APK installation

### iOS
- Cupertino Design (future)
- iOS gestures
- iOS-specific permissions
- App Store distribution
- iOS app signing

---

**Complete Feature Documentation**
**Version:** 1.0.0
**Last Updated:** March 2026
