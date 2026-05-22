import 'package:flutter/material.dart';
import '../../models/user_model.dart';
import '../../models/admin_role_model.dart';
import '../../services/auth_service.dart';
import '../../widgets/custom_widgets.dart';

class AdminManagementScreen extends StatefulWidget {
  const AdminManagementScreen({Key? key}) : super(key: key);

  @override
  State<AdminManagementScreen> createState() => _AdminManagementScreenState();
}

class _AdminManagementScreenState extends State<AdminManagementScreen> {
  List<User> _admins = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadAdmins();
  }

  void _loadAdmins() async {
    setState(() => _isLoading = true);
    try {
      final admins = await AuthService.getAllAdmins();
      setState(() => _admins = admins);
    } catch (e) {
      print('Error loading admins: $e');
    } finally {
      setState(() => _isLoading = false);
    }
  }

  void _showCreateAdminDialog() {
    showDialog(
      context: context,
      builder: (context) => CreateAdminDialog(
        onAdminCreated: _loadAdmins,
      ),
    );
  }

  void _showEditAdminDialog(User admin) {
    showDialog(
      context: context,
      builder: (context) => EditAdminDialog(
        admin: admin,
        onAdminUpdated: _loadAdmins,
      ),
    );
  }

  void _showDeleteConfirmation(User admin) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Delete Admin'),
        content: Text('Are you sure you want to delete ${admin.fullName}?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text('Cancel'),
          ),
          TextButton(
            onPressed: () async {
              final result = await AuthService.deleteAdminAccount(
                adminEmail: admin.email,
              );
              Navigator.pop(context);
              if (result['success']) {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('Admin deleted successfully')),
                );
                _loadAdmins();
              } else {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text(result['message'] ?? 'Error deleting admin')),
                );
              }
            },
            child: Text('Delete', style: TextStyle(color: Colors.red)),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Admin Management'),
        backgroundColor: Color(0xFF1E3A8A),
        elevation: 0,
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Header
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    'Admin Accounts',
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: Color(0xFF1E3A8A),
                    ),
                  ),
                  ElevatedButton.icon(
                    onPressed: _showCreateAdminDialog,
                    icon: Icon(Icons.add),
                    label: Text('Create Admin'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Color(0xFFF97316),
                      foregroundColor: Colors.white,
                    ),
                  ),
                ],
              ),
              SizedBox(height: 16),

              // Admin list
              if (_isLoading)
                Center(
                  child: CircularProgressIndicator(),
                )
              else if (_admins.isEmpty)
                Center(
                  child: Padding(
                    padding: EdgeInsets.symmetric(vertical: 32),
                    child: Text(
                      'No admin accounts found',
                      style: TextStyle(fontSize: 16, color: Colors.grey),
                    ),
                  ),
                )
              else
                ListView.builder(
                  shrinkWrap: true,
                  physics: NeverScrollableScrollPhysics(),
                  itemCount: _admins.length,
                  itemBuilder: (context, index) {
                    final admin = _admins[index];
                    return CustomCard(
                      padding: EdgeInsets.fromLTRB(16, 16, 16, 12),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          // Name and role
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      admin.fullName,
                                      style: TextStyle(
                                        fontSize: 16,
                                        fontWeight: FontWeight.bold,
                                        color: Color(0xFF1E3A8A),
                                      ),
                                    ),
                                    SizedBox(height: 4),
                                    Text(
                                      admin.email,
                                      style: TextStyle(
                                        fontSize: 13,
                                        color: Colors.grey[600],
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                              Container(
                                padding: EdgeInsets.symmetric(
                                  horizontal: 12,
                                  vertical: 6,
                                ),
                                decoration: BoxDecoration(
                                  color: Color(0xFFF97316).withOpacity(0.1),
                                  borderRadius: BorderRadius.circular(4),
                                  border: Border.all(
                                    color: Color(0xFFF97316),
                                  ),
                                ),
                                child: Text(
                                  admin.adminRole?.toUpperCase() ?? 'ADMIN',
                                  style: TextStyle(
                                    fontSize: 12,
                                    fontWeight: FontWeight.w600,
                                    color: Color(0xFFF97316),
                                  ),
                                ),
                              ),
                            ],
                          ),
                          SizedBox(height: 12),

                          // Privileges
                          Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                'Privileges:',
                                style: TextStyle(
                                  fontSize: 12,
                                  fontWeight: FontWeight.w600,
                                  color: Colors.grey[700],
                                ),
                              ),
                              SizedBox(height: 8),
                              Wrap(
                                spacing: 8,
                                runSpacing: 8,
                                children: (admin.adminPrivileges ?? [])
                                    .map((privilege) {
                                  return Container(
                                    padding: EdgeInsets.symmetric(
                                      horizontal: 8,
                                      vertical: 4,
                                    ),
                                    decoration: BoxDecoration(
                                      color: Colors.blue[100],
                                      borderRadius: BorderRadius.circular(4),
                                    ),
                                    child: Text(
                                      privilege.replaceAll('_', ' '),
                                      style: TextStyle(
                                        fontSize: 11,
                                        color: Colors.blue[800],
                                      ),
                                    ),
                                  );
                                }).toList(),
                              ),
                            ],
                          ),
                          SizedBox(height: 12),

                          // Actions
                          Row(
                            mainAxisAlignment: MainAxisAlignment.end,
                            children: [
                              TextButton.icon(
                                onPressed: () => _showEditAdminDialog(admin),
                                icon: Icon(Icons.edit, size: 16),
                                label: Text('Edit'),
                                style: TextButton.styleFrom(
                                  foregroundColor: Colors.blue,
                                ),
                              ),
                              SizedBox(width: 8),
                              if (admin.adminRole != 'superAdmin')
                                TextButton.icon(
                                  onPressed: () => _showDeleteConfirmation(admin),
                                  icon: Icon(Icons.delete, size: 16),
                                  label: Text('Delete'),
                                  style: TextButton.styleFrom(
                                    foregroundColor: Colors.red,
                                  ),
                                ),
                            ],
                          ),
                        ],
                      ),
                    );
                  },
                ),
            ],
          ),
        ),
      ),
    );
  }
}

// Dialog to create new admin
class CreateAdminDialog extends StatefulWidget {
  final Function()? onAdminCreated;

  const CreateAdminDialog({Key? key, this.onAdminCreated}) : super(key: key);

  @override
  State<CreateAdminDialog> createState() => _CreateAdminDialogState();
}

class _CreateAdminDialogState extends State<CreateAdminDialog> {
  final _formKey = GlobalKey<FormState>();

  late TextEditingController _emailController;
  late TextEditingController _passwordController;
  late TextEditingController _firstNameController;
  late TextEditingController _lastNameController;
  String _selectedRole = 'admin';
  List<String> _selectedPrivileges = [];
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _emailController = TextEditingController();
    _passwordController = TextEditingController();
    _firstNameController = TextEditingController();
    _lastNameController = TextEditingController();
  }

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    _firstNameController.dispose();
    _lastNameController.dispose();
    super.dispose();
  }

  void _updatePrivilegesForRole(String role) {
    setState(() {
      _selectedRole = role;
      _selectedPrivileges =
          AdminPrivilege.getPrivilegesForRole(_stringToAdminRole(role));
    });
  }

  AdminRole _stringToAdminRole(String role) {
    return AdminRole.values.firstWhere(
      (r) => r.toString().split('.').last == role,
      orElse: () => AdminRole.admin,
    );
  }

  void _submitForm() async {
    if (_formKey.currentState!.validate()) {
      setState(() => _isLoading = true);

      try {
        final result = await AuthService.createAdminAccount(
          email: _emailController.text,
          password: _passwordController.text,
          firstName: _firstNameController.text,
          lastName: _lastNameController.text,
          adminRole: _selectedRole,
          privileges: _selectedPrivileges,
        );

        if (result['success']) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Admin created successfully')),
          );
          widget.onAdminCreated?.call();
          Navigator.pop(context);
        } else {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(result['message'] ?? 'Error creating admin')),
          );
        }
      } catch (e) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: $e')),
        );
      } finally {
        setState(() => _isLoading = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: Text('Create New Admin'),
      content: SingleChildScrollView(
        child: Form(
          key: _formKey,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextFormField(
                controller: _firstNameController,
                decoration: InputDecoration(
                  labelText: 'First Name',
                  border: OutlineInputBorder(),
                ),
                validator: (value) {
                  if (value?.isEmpty ?? true) return 'Required';
                  return null;
                },
              ),
              SizedBox(height: 12),
              TextFormField(
                controller: _lastNameController,
                decoration: InputDecoration(
                  labelText: 'Last Name',
                  border: OutlineInputBorder(),
                ),
                validator: (value) {
                  if (value?.isEmpty ?? true) return 'Required';
                  return null;
                },
              ),
              SizedBox(height: 12),
              TextFormField(
                controller: _emailController,
                decoration: InputDecoration(
                  labelText: 'Email',
                  border: OutlineInputBorder(),
                ),
                validator: (value) {
                  if (value?.isEmpty ?? true) return 'Required';
                  if (!value!.contains('@')) return 'Invalid email';
                  return null;
                },
              ),
              SizedBox(height: 12),
              TextFormField(
                controller: _passwordController,
                decoration: InputDecoration(
                  labelText: 'Password',
                  border: OutlineInputBorder(),
                ),
                obscureText: true,
                validator: (value) {
                  if (value?.isEmpty ?? true) return 'Required';
                  if ((value?.length ?? 0) < 6) return 'Min 6 characters';
                  return null;
                },
              ),
              SizedBox(height: 12),
              DropdownButtonFormField<String>(
                initialValue: _selectedRole,
                items: ['superAdmin', 'admin', 'editor', 'moderator']
                    .map((role) => DropdownMenuItem(
                          value: role,
                          child: Text(role.replaceAllMapped(
                            RegExp(r'^(.)'),
                            (m) => m.group(0)!.toUpperCase(),
                          )),
                        ))
                    .toList(),
                onChanged: (value) {
                  if (value != null) {
                    _updatePrivilegesForRole(value);
                  }
                },
                decoration: InputDecoration(
                  labelText: 'Admin Role',
                  border: OutlineInputBorder(),
                ),
              ),
            ],
          ),
        ),
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context),
          child: Text('Cancel'),
        ),
        ElevatedButton(
          onPressed: _isLoading ? null : _submitForm,
          style: ElevatedButton.styleFrom(
            backgroundColor: Color(0xFF1E3A8A),
          ),
          child: _isLoading
              ? SizedBox(
                  height: 20,
                  width: 20,
                  child: CircularProgressIndicator(
                    strokeWidth: 2,
                    valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                  ),
                )
              : Text('Create'),
        ),
      ],
    );
  }
}

// Dialog to edit admin privileges
class EditAdminDialog extends StatefulWidget {
  final User admin;
  final Function()? onAdminUpdated;

  const EditAdminDialog({
    Key? key,
    required this.admin,
    this.onAdminUpdated,
  }) : super(key: key);

  @override
  State<EditAdminDialog> createState() => _EditAdminDialogState();
}

class _EditAdminDialogState extends State<EditAdminDialog> {
  late String _selectedRole;
  late List<String> _selectedPrivileges;
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _selectedRole = widget.admin.adminRole ?? 'admin';
    _selectedPrivileges = List.from(widget.admin.adminPrivileges ?? []);
  }

  void _updatePrivilegesForRole(String role) {
    setState(() {
      _selectedRole = role;
      _selectedPrivileges =
          AdminPrivilege.getPrivilegesForRole(_stringToAdminRole(role));
    });
  }

  AdminRole _stringToAdminRole(String role) {
    return AdminRole.values.firstWhere(
      (r) => r.toString().split('.').last == role,
      orElse: () => AdminRole.admin,
    );
  }

  void _submitForm() async {
    setState(() => _isLoading = true);

    try {
      final result = await AuthService.updateAdminPrivileges(
        adminEmail: widget.admin.email,
        adminRole: _selectedRole,
        privileges: _selectedPrivileges,
      );

      if (result['success']) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Admin updated successfully')),
        );
        widget.onAdminUpdated?.call();
        Navigator.pop(context);
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(result['message'] ?? 'Error updating admin')),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e')),
      );
    } finally {
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: Text('Edit Admin: ${widget.admin.fullName}'),
      content: SingleChildScrollView(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text('Email: ${widget.admin.email}'),
            SizedBox(height: 16),
            DropdownButtonFormField<String>(
              initialValue: _selectedRole,
              items: ['superAdmin', 'admin', 'editor', 'moderator']
                  .map((role) => DropdownMenuItem(
                        value: role,
                        child: Text(role.replaceAllMapped(
                          RegExp(r'^(.)'),
                          (m) => m.group(0)!.toUpperCase(),
                        )),
                      ))
                  .toList(),
              onChanged: (value) {
                if (value != null) {
                  _updatePrivilegesForRole(value);
                }
              },
              decoration: InputDecoration(
                labelText: 'Admin Role',
                border: OutlineInputBorder(),
              ),
            ),
            SizedBox(height: 16),
            Text(
              'Privileges for ${_selectedRole.replaceAllMapped(
                RegExp(r'^(.)'),
                (m) => m.group(0)!.toUpperCase(),
              )}:',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 8),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: _selectedPrivileges.isEmpty
                  ? [
                      Container(
                        padding:
                            EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                        decoration: BoxDecoration(
                          color: Colors.grey[100],
                          borderRadius: BorderRadius.circular(4),
                        ),
                        child: Text(
                          'No privileges assigned',
                          style: TextStyle(color: Colors.grey[600]),
                        ),
                      ),
                    ]
                  : _selectedPrivileges
                      .map((privilege) => Container(
                            padding: EdgeInsets.symmetric(
                              horizontal: 8,
                              vertical: 4,
                            ),
                            decoration: BoxDecoration(
                              color: Colors.blue[100],
                              borderRadius: BorderRadius.circular(4),
                            ),
                            child: Text(
                              privilege.replaceAll('_', ' '),
                              style: TextStyle(
                                fontSize: 12,
                                color: Colors.blue[800],
                              ),
                            ),
                          ))
                      .toList(),
            ),
          ],
        ),
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context),
          child: Text('Cancel'),
        ),
        ElevatedButton(
          onPressed: _isLoading ? null : _submitForm,
          style: ElevatedButton.styleFrom(
            backgroundColor: Color(0xFF1E3A8A),
          ),
          child: _isLoading
              ? SizedBox(
                  height: 20,
                  width: 20,
                  child: CircularProgressIndicator(
                    strokeWidth: 2,
                    valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                  ),
                )
              : Text('Update'),
        ),
      ],
    );
  }
}
