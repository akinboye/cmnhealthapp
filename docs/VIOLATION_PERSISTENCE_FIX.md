# Violation Persistence Fix

## Problem
When users logged out and logged back in, their previously reported violations were showing as 0. The violations were only stored in memory and were lost when the app was closed or restarted.

## Root Cause
Violations were stored in static variables that were initialized as empty lists:
- `Map<String, List<Violation>> _violations = {}` - in-memory per-user storage
- `List<Violation> _globalViolations = []` - in-memory global storage

These were reset every time the app ran, causing data loss between sessions.

## Solution
Implemented persistent storage using `SharedPreferences`:

### Changes Made

#### 1. **lib/services/violation_service.dart**
Added persistence mechanism:

- **New imports**: Added `shared_preferences` and `dart:convert` imports
- **Storage keys**: 
  - `_violationsStorageKey` - stores per-user violations
  - `_globalViolationsStorageKey` - stores global violations for admins
- **New methods**:
  - `initialize()` - Loads violations from persistent storage on app startup
  - `_loadViolationsFromStorage()` - Retrieves violations from SharedPreferences
  - `_saveViolationsToStorage()` - Saves violations to SharedPreferences
- **Updated methods**:
  - `createViolation()` - Now calls `_saveViolationsToStorage()` after creating
  - `updateViolationStatus()` - Now calls `_saveViolationsToStorage()` after updating

#### 2. **lib/main.dart**
Integrated persistence initialization:

- **New import**: Added `import 'services/violation_service.dart'`
- **Updated initState**: 
  - Created `_initializeServices()` async method
  - Calls `ViolationService.initialize()` to load violations from storage
  - Then calls `_checkAuthStatus()` to authenticate user
- **Initialization order**: Ensures violations are loaded before UI is built

### How It Works

**On App Startup:**
1. App initializes `_CMNHealthAppState`
2. `initState()` calls `_initializeServices()`
3. `ViolationService.initialize()` loads all violations from SharedPreferences
4. Both `_violations` (per-user) and `_globalViolations` (global) are populated
5. User authentication check proceeds normally
6. Dashboard now displays correct violation count

**When Violation is Created:**
1. Violation is created and added to both storage maps
2. `_saveViolationsToStorage()` is called
3. Violations are serialized to JSON and saved to SharedPreferences
4. Data persists across app restarts

**When Violation Status is Updated (by Admin):**
1. Violation is updated in both maps
2. `_saveViolationsToStorage()` is called
3. Updated violations are serialized and saved
4. Changes persist across app restarts

### Data Flow Diagram

```
App Startup
    ↓
_initializeServices()
    ↓
ViolationService.initialize()
    ↓
_loadViolationsFromStorage()
    ↓
SharedPreferences.getString(keys)
    ↓
Deserialize JSON → Populate _violations & _globalViolations
    ↓
Dashboard shows correct violation count
```

### Storage Format

Violations are stored as JSON in SharedPreferences:

**Global Violations (admin access):**
```json
[
  {
    "id": "VIOL_user123_1_1234567890",
    "userId": "user123",
    "type": "ViolationType.medicalMalpractice",
    "hospitalName": "City Hospital",
    "status": "ViolationStatus.reported",
    ...
  }
]
```

**Per-User Violations:**
```json
{
  "user123": [
    {
      "id": "VIOL_user123_1_1234567890",
      ...
    }
  ],
  "user456": [...]
}
```

### Benefits

✅ **Persistent Storage**: Violations now persist across app restarts  
✅ **Dual Access**: Users see their violations, admins see all violations  
✅ **Data Sync**: Both storage mechanisms stay synchronized  
✅ **Automatic Loading**: No manual reload required  
✅ **Logging**: Console shows when violations are loaded and saved  

### Testing Steps

1. **Submit a Violation** as user@cmnhealth.com
   - Check console for: `✓ Violation created and stored`
   - Check console for: `💾 Violations saved to persistent storage`

2. **Close and Reopen App**
   - Check console for: `📁 Initializing ViolationService from persistent storage...`
   - Check console for: `✓ Loaded N violations from global storage`

3. **Login Again** as user@cmnhealth.com
   - Check Dashboard: Violation count should show 1 (or more if multiple submitted)
   - Violation should appear in violations list

4. **Login as Admin** (admin@cmnhealth.com)
   - Go to Admin → Violations
   - Should see user@cmnhealth.com's violation in the list
   - Should persist even after app restart

### Verification in Console

**On violation creation:**
```
✓ Violation created and stored: VIOL_user123_1_1234567890
  - Total violations in global list: 1
  - Hospital: City Hospital
💾 Violations saved to persistent storage
```

**On app startup:**
```
📁 Initializing ViolationService from persistent storage...
  ✓ Loaded 1 violations from global storage
  ✓ Loaded per-user violations for 1 users
✓ ViolationService initialized. Global violations: 1
```

**When admin retrieves violations:**
```
📋 getAllViolations() called
  - Total in global list: 1
    • VIOL_user123_1_1234567890 - City Hospital
```

### Files Modified

1. `lib/services/violation_service.dart` - Core persistence logic
2. `lib/main.dart` - Initialize violations on startup

### Dependencies Used

- `shared_preferences: ^2.2.2` (already in pubspec.yaml)
- `dart:convert` - JSON serialization
- Violation model's existing `toJson()` and `fromJson()` methods

### No Database Required

This implementation uses SharedPreferences for simplicity and doesn't require:
- SQLite setup
- Database migrations
- Complex queries

It's ideal for a Flutter app with moderate data requirements.
