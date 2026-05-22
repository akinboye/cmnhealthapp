import '../models/live_chat_model.dart';

class LiveChatService {
  static const String baseUrl = 'http://localhost:5000/api'; // Update with your API
  static const String timeout = '30000'; // 30 seconds

  // Local storage for demo
  static final List<LiveChatConversation> _conversations = [];
  static final Map<String, List<LiveChatMessage>> _messages = {};

  // ========== USER METHODS ==========

  /// Create a new conversation (user initiates chat)
  static Future<LiveChatConversation> createConversation({
    required String userId,
    required String userName,
    required String userEmail,
  }) async {
    try {
      final conversationId =
          'conv_${DateTime.now().millisecondsSinceEpoch}_$userId';

      final conversation = LiveChatConversation(
        id: conversationId,
        userId: userId,
        userName: userName,
        userEmail: userEmail,
        status: 'pending',
        createdAt: DateTime.now(),
      );

      _conversations.add(conversation);
      _messages[conversationId] = [];

      // In production, call API:
      // final response = await http.post(
      //   Uri.parse('$baseUrl/conversations'),
      //   headers: {'Content-Type': 'application/json'},
      //   body: jsonEncode(conversation.toJson()),
      // ).timeout(Duration(seconds: 30));

      return conversation;
    } catch (e) {
      rethrow;
    }
  }

  /// Send a message as user
  static Future<LiveChatMessage> sendUserMessage({
    required String conversationId,
    required String userId,
    required String userName,
    required String message,
  }) async {
    try {
      final messageId = 'msg_${DateTime.now().millisecondsSinceEpoch}';

      final chatMessage = LiveChatMessage(
        id: messageId,
        conversationId: conversationId,
        senderId: userId,
        senderName: userName,
        senderType: 'user',
        message: message,
        timestamp: DateTime.now(),
      );

      if (!_messages.containsKey(conversationId)) {
        _messages[conversationId] = [];
      }
      _messages[conversationId]!.add(chatMessage);

      // Update conversation's last message
      final convIndex =
          _conversations.indexWhere((c) => c.id == conversationId);
      if (convIndex != -1) {
        _conversations[convIndex] = LiveChatConversation(
          id: _conversations[convIndex].id,
          userId: _conversations[convIndex].userId,
          userName: _conversations[convIndex].userName,
          userEmail: _conversations[convIndex].userEmail,
          status: 'active',
          createdAt: _conversations[convIndex].createdAt,
          updatedAt: DateTime.now(),
          lastMessage: message,
          unreadCount: _conversations[convIndex].unreadCount,
          assignedAdminId: _conversations[convIndex].assignedAdminId,
          assignedAdminName: _conversations[convIndex].assignedAdminName,
        );
      }

      // In production, call API:
      // final response = await http.post(
      //   Uri.parse('$baseUrl/messages'),
      //   headers: {'Content-Type': 'application/json'},
      //   body: jsonEncode(chatMessage.toJson()),
      // ).timeout(Duration(seconds: 30));

      return chatMessage;
    } catch (e) {
      rethrow;
    }
  }

  /// Get conversation for user
  static Future<LiveChatConversation?> getUserConversation(String userId) async {
    try {
      final conversation = _conversations.firstWhere(
        (c) => c.userId == userId,
        orElse: () => LiveChatConversation(
          id: '',
          userId: userId,
          userName: '',
          userEmail: '',
          createdAt: DateTime.now(),
        ),
      );

      return conversation.id.isNotEmpty ? conversation : null;
    } catch (e) {
      rethrow;
    }
  }

  /// Get messages for a conversation
  static Future<List<LiveChatMessage>> getConversationMessages(
      String conversationId) async {
    try {
      return _messages[conversationId] ?? [];
    } catch (e) {
      rethrow;
    }
  }

  // ========== ADMIN METHODS ==========

  /// Get all conversations (admin view)
  static Future<List<LiveChatConversation>> getAllConversations() async {
    try {
      return _conversations;
    } catch (e) {
      rethrow;
    }
  }

  /// Get unresolved conversations
  static Future<List<LiveChatConversation>> getUnresolvedConversations() async {
    try {
      return _conversations
          .where((c) => c.status == 'active' || c.status == 'pending')
          .toList();
    } catch (e) {
      rethrow;
    }
  }

  /// Assign conversation to admin
  static Future<void> assignConversation(
    String conversationId,
    String adminId,
    String adminName,
  ) async {
    try {
      final convIndex =
          _conversations.indexWhere((c) => c.id == conversationId);
      if (convIndex != -1) {
        final conv = _conversations[convIndex];
        _conversations[convIndex] = LiveChatConversation(
          id: conv.id,
          userId: conv.userId,
          userName: conv.userName,
          userEmail: conv.userEmail,
          status: 'active',
          createdAt: conv.createdAt,
          updatedAt: DateTime.now(),
          lastMessage: conv.lastMessage,
          unreadCount: conv.unreadCount,
          assignedAdminId: adminId,
          assignedAdminName: adminName,
        );
      }
    } catch (e) {
      rethrow;
    }
  }

  /// Send a message as admin
  static Future<LiveChatMessage> sendAdminMessage({
    required String conversationId,
    required String adminId,
    required String adminName,
    required String message,
  }) async {
    try {
      final messageId = 'msg_${DateTime.now().millisecondsSinceEpoch}';

      final chatMessage = LiveChatMessage(
        id: messageId,
        conversationId: conversationId,
        senderId: adminId,
        senderName: adminName,
        senderType: 'admin',
        message: message,
        timestamp: DateTime.now(),
      );

      if (!_messages.containsKey(conversationId)) {
        _messages[conversationId] = [];
      }
      _messages[conversationId]!.add(chatMessage);

      return chatMessage;
    } catch (e) {
      rethrow;
    }
  }

  /// Mark conversation as resolved
  static Future<void> resolveConversation(String conversationId) async {
    try {
      final convIndex =
          _conversations.indexWhere((c) => c.id == conversationId);
      if (convIndex != -1) {
        final conv = _conversations[convIndex];
        _conversations[convIndex] = LiveChatConversation(
          id: conv.id,
          userId: conv.userId,
          userName: conv.userName,
          userEmail: conv.userEmail,
          status: 'resolved',
          createdAt: conv.createdAt,
          updatedAt: DateTime.now(),
          lastMessage: conv.lastMessage,
          unreadCount: conv.unreadCount,
          assignedAdminId: conv.assignedAdminId,
          assignedAdminName: conv.assignedAdminName,
        );
      }
    } catch (e) {
      rethrow;
    }
  }

  /// Get messages for admin panel
  static Future<List<LiveChatMessage>> getMessagesForAdmin(
      String conversationId) async {
    try {
      return _messages[conversationId] ?? [];
    } catch (e) {
      rethrow;
    }
  }
}
