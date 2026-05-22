/// Example: How to integrate the chatbot into your existing screens
/// 
/// This file shows example implementations for adding the chatbot to different screens

import 'package:flutter/material.dart';
import '../screens/chatbot/chatbot_screen.dart';
import '../widgets/chatbot_floating_button.dart';

/// Example 1: Add chatbot as Floating Action Button
class ExampleHomeScreen extends StatelessWidget {
  final String language;

  const ExampleHomeScreen({
    Key? key,
    this.language = 'en',
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Home'),
      ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            // Your existing home content here
            Container(
              padding: const EdgeInsets.all(16),
              child: const Text('Welcome to Health App'),
            ),
          ],
        ),
      ),
      // Add chatbot FAB
      floatingActionButton: ChatbotFloatingButton(
        onPressed: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => ChatbotScreen(language: language),
            ),
          );
        },
        label: 'Ask Health Assistant',
      ),
    );
  }
}

/// Example 2: Add chatbot as Menu Item / Button
class ExampleResourcesScreen extends StatelessWidget {
  final String language;

  const ExampleResourcesScreen({
    Key? key,
    this.language = 'en',
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Resources'),
      ),
      body: ListView(
        children: [
          // Your existing resources
          ListTile(
            title: const Text('Health Information'),
            onTap: () {},
          ),
          ListTile(
            title: const Text('Patient Rights'),
            onTap: () {},
          ),
          const Divider(),
          // Chatbot button
          Padding(
            padding: const EdgeInsets.all(16),
            child: ElevatedButton.icon(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => ChatbotScreen(language: language),
                  ),
                );
              },
              icon: const Icon(Icons.chat),
              label: const Text('Ask Health Assistant'),
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF1976D2),
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(vertical: 12),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

/// Example 3: Add chatbot as Card/Widget
class ExampleDashboardWidget extends StatelessWidget {
  final String language;
  final VoidCallback onChatTapped;

  const ExampleDashboardWidget({
    Key? key,
    this.language = 'en',
    required this.onChatTapped,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.all(12),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            const Icon(Icons.help_outline, size: 48, color: Color(0xFF1976D2)),
            const SizedBox(height: 12),
            const Text(
              'Need Help?',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            const Text(
              'Ask our Health Assistant about patient rights and healthcare information',
              textAlign: TextAlign.center,
              style: TextStyle(color: Colors.grey),
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: onChatTapped,
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF1976D2),
                foregroundColor: Colors.white,
              ),
              child: const Text('Start Chat'),
            ),
          ],
        ),
      ),
    );
  }
}

/// Example 4: Implementation in main.dart
void exampleMainDartImplementation() {
  // In your routes configuration:
  
  // Add to your route definitions:
  /*
  routes: {
    '/home': (context) => const HomeScreen(),
    '/chatbot': (context) => const ChatbotScreen(),
    '/resources': (context) => const ResourcesScreen(),
  },
  */

  // Or use named routes:
  /*
  Navigator.pushNamed(context, '/chatbot');
  */
}

/// Example 5: Integration with existing navigation
class ExampleMainApp extends StatelessWidget {
  const ExampleMainApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Cure My Nation Health App',
      theme: ThemeData(
        primaryColor: const Color(0xFF1976D2),
        useMaterial3: true,
      ),
      home: const ExampleHomeWithChatbot(),
      // Add named route for chatbot
      routes: {
        '/chatbot': (context) => const ChatbotScreen(language: 'en'),
      },
    );
  }
}

class ExampleHomeWithChatbot extends StatefulWidget {
  const ExampleHomeWithChatbot({Key? key}) : super(key: key);

  @override
  State<ExampleHomeWithChatbot> createState() => _ExampleHomeWithChatbotState();
}

class _ExampleHomeWithChatbotState extends State<ExampleHomeWithChatbot> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Cure My Nation'),
      ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            // Dashboard content
            const Padding(
              padding: EdgeInsets.all(16),
              child: Text('Welcome to Health App'),
            ),
            // Add the chatbot card widget
            ExampleDashboardWidget(
              onChatTapped: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => const ChatbotScreen(),
                  ),
                );
              },
            ),
          ],
        ),
      ),
      // Or add floating action button
      floatingActionButton: ChatbotFloatingButton(
        onPressed: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => const ChatbotScreen(),
            ),
          );
        },
      ),
    );
  }
}

/// Usage Guidelines:
/// 
/// 1. **Floating Action Button** (Best for primary feature)
///    - Use when chat is main feature
///    - Always visible and accessible
///    - Good for frequent users
/// 
/// 2. **Menu Item / Button** (Good for secondary feature)
///    - Place in app navigation
///    - Not always visible
///    - Clean UI
/// 
/// 3. **Card Widget** (Best for dashboard)
///    - Eye-catching
///    - Can provide context
///    - Works well on home screen
/// 
/// 4. **Bottom Navigation** (Alternative)
///    - Add to bottom nav bar
///    - Consistent placement
///    - Works for equal-priority features
///
/// Implementation Checklist:
/// - [x] Import ChatbotScreen and ChatbotFloatingButton
/// - [x] Add navigation to ChatbotScreen
/// - [x] Configure language support
/// - [x] Test on device
/// - [x] Ensure backend is running
/// - [x] Update API endpoint in ChatbotConfig
