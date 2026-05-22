# CMN Health Rights Application - Setup & Development Guide

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

1. **Flutter SDK** (3.13.0 or higher)
   - Download from: https://flutter.dev/docs/get-started/install
   
2. **Dart** (3.0 or higher)
   - Comes bundled with Flutter
   
3. **IDE/Editor**
   - Visual Studio Code (recommended)
   - Android Studio
   - XCode (for macOS/iOS)
   
4. **Platform Requirements**
   - **Web:** Chrome, Firefox, Edge (modern browser)
   - **Android:** Android SDK, Android emulator or physical device
   - **iOS:** macOS with Xcode, iPhone simulator or physical device

## 🚀 Quick Start

### 1. Project Setup

```bash
# Navigate to project directory
cd cmnhealthapp

# Get all dependencies
flutter pub get

# (Optional) Upgrade packages
flutter pub upgrade
```

### 2. Running the Application

#### For Web (Browser)
```bash
# Run in Chrome
flutter run -d chrome

# Run in Firefox
flutter run -d firefox
```

The app will typically run at: `http://localhost:8000` or `http://localhost:5985`

#### For Android
```bash
# Ensure Android emulator is running
flutter emulators --launch emulator-name

# Run app
flutter run -d android

# Or run on physical device
flutter run
```

#### For iOS (macOS/iOS)
```bash
# Pod setup (first time)
cd ios
pod install
cd ..

# Run simulation
flutter run -d ios

# Run on device
flutter run -d ios --release
```

#### For macOS Desktop
```bash
flutter run -d macos -v
```

### 3. Building for Production

#### Web Build
```bash
# Build for web
flutter build web --release

# Output will be in: build/web/
```

#### Android Build (APK)
```bash
# Build APK
flutter build apk --release

# Build App Bundle (Play Store)
flutter build appbundle --release
```

#### iOS Build
```bash
# Build for iOS
flutter build ios --release

# Archive for App Store
flutter build ios --release -v
```

## 📁 Project Structure Explanation

```
lib/
├── main.dart
│   └── Application entry point with main app widget and navigation logic
│
├── constants/
│   ├── app_colors.dart
│   │   └── Color palette, theme configuration (light/dark)
│   └── app_strings.dart
│       └── 500+ translated strings in 10 languages
│
├── models/
│   ├── user_model.dart (User profile data)
│   ├── violation_model.dart (Violation types and status)
│   ├── resource_model.dart (Healthcare resources and tips)
│   └── support_model.dart (Chat messages and support tickets)
│
├── services/
│   ├── auth_service.dart
│   │   └── Authentication, registration, password management
│   ├── violation_service.dart
│   │   └── Violation CRUD operations, statistics
│   ├── resource_service.dart
│   │   └── Resource retrieval, search, save favorites
│   └── support_service.dart
│       └── Ticket creation, chat messaging, support info
│
├── widgets/
│   └── custom_widgets.dart
│       ├── CustomButton - Reusable button with loading states
│       ├── CustomTextField - Input with validation
│       ├── CustomCard - Card container
│       ├── StatisticCard - Metric display
│       ├── LoadingSpinner - Progress indicator
│       ├── SuccessDialog - Success confirmation
│       ├── Header - AppBar with subtitle
│       └── InfoCard - Info display card
│
└── screens/
    ├── auth/
    │   ├── login_screen.dart (Email/password login)
    │   └── signup_screen.dart (User registration with validation)
    │
    ├── home/
    │   └── home_screen.dart (Landing page for non-authenticated users)
    │
    ├── dashboard/
    │   └── dashboard_screen.dart (Main dashboard with stats & quick actions)
    │
    ├── violation/
    │   ├── violation_reporting_screen.dart (Report new violation form)
    │   └── violations_dashboard_screen.dart (Analytics & statistics)
    │
    ├── resources/
    │   └── resources_screen.dart (Healthcare education & resources)
    │
    ├── support/
    │   └── support_center_screen.dart (24/7 support & tickets)
    │
    └── profile/
        └── profile_settings_screen.dart (User profile & settings)
```

## 🔧 Development Workflows

### Adding a New Screen

1. **Create the screen file** in appropriate directory:
   ```dart
   lib/screens/category/my_screen.dart
   ```

2. **Define the widget**:
   ```dart
   class MyScreen extends StatefulWidget {
     final String language;
     
     const MyScreen({Key? key, required this.language}) : super(key: key);
     
     @override
     State<MyScreen> createState() => _MyScreenState();
   }
   
   class _MyScreenState extends State<MyScreen> {
     @override
     Widget build(BuildContext context) {
       return Scaffold(
         appBar: Header(
           title: AppStrings.get('screen_title', language: widget.language),
         ),
         body: // Your content here
       );
     }
   }
   ```

3. **Update navigation** in `main.dart`:
   ```dart
   case 'my_screen':
     return MyScreen(language: _currentLanguage);
   ```

### Adding a New Service

1. **Create service file** `lib/services/my_service.dart`:
   ```dart
   class MyService {
     static Future<List<MyData>> getData() async {
       try {
         // Your logic
         return data;
       } catch (e) {
         return [];
       }
     }
   }
   ```

2. **Use in screens**:
   ```dart
   FutureBuilder(
     future: MyService.getData(),
     builder: (context, snapshot) {
       // Build UI with data
     },
   )
   ```

### Adding Languages

1. **Update `app_strings.dart`**:
   ```dart
   'es': {  // Spanish
     'app_title': 'Título de la Aplicación',
     'login': 'Iniciar sesión',
     // ... more translations
   }
   ```

2. **Add to language list**:
   ```dart
   static List<String> get supportedLanguages => 
     ['en', 'yo', 'ha', 'ig', 'fr', 'hi', 'ta', 'te', 'kn', 'ml', 'es'];
   ```

3. **Add language name**:
   ```dart
   'es': 'Español',
   ```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
flutter test

# Run specific test file
flutter test test/my_test.dart

# Run with coverage
flutter test --coverage
```

### Manual Testing Checklist

- [ ] Login/Signup flow
- [ ] Navigation between screens
- [ ] Language switching
- [ ] Form validation
- [ ] Data persistence
- [ ] Error handling
- [ ] Responsive layouts (web, mobile)
- [ ] All UI components render correctly

## 🐛 Debugging

### Enable Debug Logging
```dart
// In any service
print('[DEBUG] Message: $value');

// Or use debugPrint (recommended)
import 'package:flutter/foundation.dart';
debugPrint('Debug message');
```

### Debug Mode
```bash
# Run with verbose output
flutter run -v

# Attach debugger
flutter attach

# Show widget tree
flutter run --profile
```

### DevTools
```bash
# Open DevTools
flutter pub global activate devtools
devtools

# Or from IDE: Run > Open DevTools
```

## 📦 Dependencies

Current dependencies in `pubspec.yaml`:

```yaml
flutter:
  sdk: flutter
flutter_localizations:
  sdk: flutter
intl: ^0.19.0           # Localization support
http: ^1.1.0            # HTTP requests (for future API integration)
crypto: ^3.0.3          # Password hashing
jwt_decoder: ^2.0.1     # JWT token handling
provider: ^6.0.0        # State management (optional)
shared_preferences:     # Local storage
file_picker: ^6.0.0     # File selection
image_picker: ^1.0.4    # Image upload
```

### Adding New Dependencies
```bash
# Add package
flutter pub add package_name

# Add dev dependency
flutter pub add -d package_name

# Get specific version
flutter pub add package_name:^1.0.0
```

## 🔐 Security Best Practices

1. **Never commit sensitive data** (API keys, tokens)
2. **Use environment variables** for configuration
3. **Validate all user inputs** before processing
4. **Hash passwords** before storage
5. **Use HTTPS** for API calls
6. **Implement rate limiting** on backend
7. **Secure local storage** with encryption

## 📊 Performance Optimization

1. **Use `const` constructors** wherever possible
2. **Implement lazy loading** for lists
3. **Cache API responses** appropriately
4. **Use `.take()`** to limit displayed items
5. **Optimize image sizes** before loading
6. **Profile app** using DevTools

## 🚀 Deployment

### Web Deployment

**Firebase Hosting:**
```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Initialize
firebase init hosting

# Build and deploy
flutter build web
firebase deploy
```

**Other platforms:** Netlify, Vercel, GitHub Pages

### Mobile Deployment

**Google Play Store:**
1. Create Google Play Console account
2. Build app bundle: `flutter build appbundle`
3. Upload to Play Console
4. Fill app details, privacy policy, etc.
5. Submit for review

**App Store (iOS):**
1. Create Apple Developer account
2. Build for iOS: `flutter build ios`
3. Use Xcode to archive and submit
4. Fill App Store Connect details
5. Submit for review

## 📞 Troubleshooting

### Common Issues

**Issue: "Doctor summary says Flutter is not installed"**
```bash
flutter doctor
# Follow the instructions to fix any issues
```

**Issue: "No device available"**
```bash
# List available devices
flutter devices

# Create new emulator
flutter emulators --create
```

**Issue: "Build fails with dependency errors"**
```bash
# Clean and rebuild
flutter clean
flutter pub get
flutter run
```

**Issue: "Hot reload not working"**
- Try hot restart: `R` in terminal
- Or rebuild: `flutter run`

## 📚 Useful Resources

- Flutter Documentation: https://flutter.dev/docs
- Dart Language Guide: https://dart.dev/guides
- Material Design: https://material.io/design
- Flutter Community: https://flutter.dev/community

## 📝 Notes for Contributors

1. **Code Style:** Follow Flutter conventions
2. **Naming:** Use camelCase for variables, PascalCase for classes
3. **Comments:** Add comments for complex logic
4. **Testing:** Write tests for new features
5. **Documentation:** Update README when needed
6. **Commits:** Use descriptive commit messages

## 🎯 Next Steps

1. Verify the app runs locally
2. Test all screens and features
3. Build for your target platform
4. Deploy to app stores/hosting
5. Gather user feedback
6. Plan future enhancements

---

**Happy Coding! 🚀**

For detailed Flutter information, visit: https://flutter.dev/
