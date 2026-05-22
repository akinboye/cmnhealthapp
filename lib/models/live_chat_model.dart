
class LiveChatMessage {
  final String id;
  final String conversationId;
  final String senderId;
  final String senderName;
  final String senderType; // 'user' or 'admin'
  final String message;
  final DateTime timestamp;
  final bool isRead;
  final String? attachmentUrl;

  LiveChatMessage({
    required this.id,
    required this.conversationId,
    required this.senderId,
    required this.senderName,
    required this.senderType,
    required this.message,
    required this.timestamp,
    this.isRead = false,
    this.attachmentUrl,
  });

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'conversationId': conversationId,
      'senderId': senderId,
      'senderName': senderName,
      'senderType': senderType,
      'message': message,
      'timestamp': timestamp.toIso8601String(),
      'isRead': isRead,
      'attachmentUrl': attachmentUrl,
    };
  }

  factory LiveChatMessage.fromJson(Map<String, dynamic> json) {
    return LiveChatMessage(
      id: json['id'] ?? '',
      conversationId: json['conversationId'] ?? '',
      senderId: json['senderId'] ?? '',
      senderName: json['senderName'] ?? 'Anonymous',
      senderType: json['senderType'] ?? 'user',
      message: json['message'] ?? '',
      timestamp: json['timestamp'] != null
          ? DateTime.parse(json['timestamp'])
          : DateTime.now(),
      isRead: json['isRead'] ?? false,
      attachmentUrl: json['attachmentUrl'],
    );
  }
}

class LiveChatConversation {
  final String id;
  final String userId;
  final String userName;
  final String userEmail;
  final String status; // 'active', 'resolved', 'pending'
  final DateTime createdAt;
  final DateTime? updatedAt;
  final String? lastMessage;
  final int unreadCount;
  final String? assignedAdminId;
  final String? assignedAdminName;

  LiveChatConversation({
    required this.id,
    required this.userId,
    required this.userName,
    required this.userEmail,
    this.status = 'active',
    required this.createdAt,
    this.updatedAt,
    this.lastMessage,
    this.unreadCount = 0,
    this.assignedAdminId,
    this.assignedAdminName,
  });

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'userId': userId,
      'userName': userName,
      'userEmail': userEmail,
      'status': status,
      'createdAt': createdAt.toIso8601String(),
      'updatedAt': updatedAt?.toIso8601String(),
      'lastMessage': lastMessage,
      'unreadCount': unreadCount,
      'assignedAdminId': assignedAdminId,
      'assignedAdminName': assignedAdminName,
    };
  }

  factory LiveChatConversation.fromJson(Map<String, dynamic> json) {
    return LiveChatConversation(
      id: json['id'] ?? '',
      userId: json['userId'] ?? '',
      userName: json['userName'] ?? 'Anonymous',
      userEmail: json['userEmail'] ?? '',
      status: json['status'] ?? 'active',
      createdAt: json['createdAt'] != null
          ? DateTime.parse(json['createdAt'])
          : DateTime.now(),
      updatedAt:
          json['updatedAt'] != null ? DateTime.parse(json['updatedAt']) : null,
      lastMessage: json['lastMessage'],
      unreadCount: json['unreadCount'] ?? 0,
      assignedAdminId: json['assignedAdminId'],
      assignedAdminName: json['assignedAdminName'],
    );
  }
}
