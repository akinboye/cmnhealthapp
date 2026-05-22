# Admin Role & Privilege System Documentation

## Overview

The CMN Health App now supports a comprehensive role-based access control (RBAC) system that allows SuperAdmins to create multiple admin accounts with different privilege levels. This enables better delegation of responsibilities and access control.

## Admin Roles

### 1. SuperAdmin (Full Access)
- **Name**: Super Admin
- **Description**: Full access - manage admins and all content
- **Key Capabilities**:
  - Create, edit, and delete blog posts
  - Publish/unpublish content
  - Create and manage other admin accounts
  - Modify admin privileges and roles
  - Delete admin accounts
  - View analytics
  - Manage users
  - Moderate comments
  - Access admin management panel

### 2. Admin (Full Blog Management)
- **Name**: Admin
- **Description**: Create, edit and delete blog posts
- **Key Capabilities**:
  - Create new blog posts
  - Edit existing blog posts
  - Delete blog posts
  - Publish/unpublish content
  - View analytics
  - **Cannot**: Manage other admins

### 3. Editor (Limited Editing)
- **Name**: Editor
- **Description**: Edit existing blog posts only
- **Key Capabilities**:
  - Edit existing blog posts
  - Publish/unpublish content
  - **Cannot**: Create or delete blog posts

### 4. Moderator (Viewing & Moderation)
- **Name**: Moderator
- **Description**: View and moderate content
- **Key Capabilities**:
  - View analytics
  - Moderate comments
  - **Cannot**: Create, edit, or delete blog posts

## Admin Privileges

The system uses a privilege-based model where each role has a set of permissions:

| Privilege | SuperAdmin | Admin | Editor | Moderator |
|-----------|-----------|-------|---------|-----------|
| manage_admins | ✓ | ✗ | ✗ | ✗ |
| create_blog | ✓ | ✓ | ✗ | ✗ |
| edit_blog | ✓ | ✓ | ✓ | ✗ |
| delete_blog | ✓ | ✓ | ✗ | ✗ |
| publish_blog | ✓ | ✓ | ✓ | ✗ |
| view_analytics | ✓ | ✓ | ✗ | ✓ |
| manage_users | ✓ | ✗ | ✗ | ✗ |
| moderate_comments | ✓ | ✗ | ✗ | ✓ |

## Default SuperAdmin Account

The default SuperAdmin account is created automatically on first initialization:

- **Email**: admin@cmnhealth.com
- **Password**: admin123
- **Role**: SuperAdmin (Full Access)

## Managing Admin Accounts

### For SuperAdmins Only

#### Accessing Admin Management
1. Log in as SuperAdmin
2. Go to Admin Dashboard
3. Click "Manage Admins" button

#### Creating a New Admin Account
1. Click "Create Admin" button
2. Fill in the form:
   - **First Name**: Admin's first name
   - **Last Name**: Admin's last name
   - **Email**: Unique email address for the admin
   - **Password**: Secure password (min 6 characters)
   - **Admin Role**: Select from SuperAdmin, Admin, Editor, or Moderator
   - **Privileges**: Automatically assigned based on selected role
3. Click "Create" to save the new admin account

#### Editing Admin Privileges
1. Find the admin in the list
2. Click the "Edit" button
3. Modify the role (privileges update automatically)
4. Click "Update" to save changes

#### Deleting Admin Accounts
1. Find the admin in the list
2. Click the "Delete" button
3. Confirm the deletion
4. The admin account is permanently removed

## API Methods

### AuthService Methods

```dart
// Create a new admin account (SuperAdmin only)
Future<Map<String, dynamic>> createAdminAccount({
  required String email,
  required String password,
  required String firstName,
  required String lastName,
  required String adminRole,
  required List<String> privileges,
})

// Get all admin accounts (SuperAdmin only)
Future<List<User>> getAllAdmins()

// Update admin privileges (SuperAdmin only)
Future<Map<String, dynamic>> updateAdminPrivileges({
  required String adminEmail,
  required String adminRole,
  required List<String> privileges,
})

// Delete admin account (SuperAdmin only)
Future<Map<String, dynamic>> deleteAdminAccount({
  required String adminEmail,
})

// Check if current user has specific privilege
bool hasPrivilege(String privilege)

// Check if current user is SuperAdmin
bool isSuperAdmin()
```

## User Model Updates

The User model now includes:

```dart
final String? adminRole; // 'superAdmin', 'admin', 'editor', 'moderator'
final List<String>? adminPrivileges; // List of privilege strings
```

## Security Considerations

1. **SuperAdmin Protection**: 
   - SuperAdmins cannot delete their own accounts
   - SuperAdmins cannot change their own role

2. **Password Security**:
   - Minimum 6 characters required
   - Passwords are hashed before storage

3. **Role Restrictions**:
   - Only SuperAdmins can create, edit, or delete admin accounts
   - Privilege changes are immediately enforced

4. **Email Uniqueness**:
   - Each admin must have a unique email address
   - Duplicate emails are rejected

## Role Decision Matrix

Use this matrix to determine which role to assign:

| Scenario | Recommended Role |
|----------|------------------|
| Need full control | SuperAdmin |
| Trust to manage all blog content | Admin |
| Only review/edit articles | Editor |
| Only moderate and view analytics | Moderator |
| Limited content creation | Admin with future custom roles |

## Best Practices

1. **Creation Policy**:
   - Create SuperAdmin accounts sparingly
   - Use Admin role for most staff
   - Assign more restrictive roles for junior staff

2. **Onboarding**:
   - Create account with minimum permissions first
   - Increase permissions only when needed
   - Document who has what access

3. **Monitoring**:
   - Regularly review admin accounts
   - Remove inactive admins
   - Update privileges based on role changes

4. **Security**:
   - Use strong passwords (longer than minimum)
   - Change passwords periodically
   - Delete admin accounts when staff leaves

## Future Enhancements

Potential additions to the system:

1. Custom role creation
2. Permission templates
3. Audit logs for admin actions
4. Two-factor authentication
5. API tokens for admin accounts
6. Bulk operations
7. Admin activity dashboard
8. Permission inheritance
