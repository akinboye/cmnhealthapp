# 🎨 Cure My Nation - Design System Guide

## Overview

This is a professional, production-ready design system built with **Material 3** and **responsive-first approach**. It ensures consistency across all screens (mobile, tablet, desktop) and languages.

---

## 📁 Design System Structure

```
lib/
├── core/
│   ├── theme/                          # Design tokens & theme
│   │   ├── app_theme.dart              # Material 3 theme (light/dark)
│   │   ├── colors.dart                 # Color palette
│   │   ├── typography.dart             # Font styles & sizes
│   │   ├── spacing.dart                # 8px spacing system
│   │   └── responsive.dart             # Breakpoints & responsive utilities
│   │
│   ├── widgets/                        # Reusable UI components
│   │   ├── custom_buttons.dart         # Buttons & cards
│   │   ├── adaptive_navigation.dart    # Mobile/tablet/desktop nav
│   │   └── responsive_widgets.dart     # Responsive layout widgets
│   │
│   └── constants/                      # App-wide constants
│       └── app_constants.dart          # URLs, strings, validation
│
└── features/
    ├── auth/
    ├── dashboard/
    ├── chat/
    └── ...
```

---

## 🎯 Quick Start - Using the Design System

### 1. **Use Theme Colors**

```dart
import 'package:cmn_health_app/core/theme/colors.dart';

Container(
  color: AppColors.primary,           // #1976D2
  child: Text(
    'Hello',
    style: TextStyle(color: AppColors.onPrimary),  // White
  ),
)
```

### 2. **Use Typography**

```dart
import 'package:cmn_health_app/core/theme/typography.dart';

Text(
  'Patient Rights',
  style: AppTypography.buildTextTheme().headlineLarge,  // 32px, bold
)
```

### 3. **Use Spacing**

```dart
import 'package:cmn_health_app/core/theme/spacing.dart';

Padding(
  padding: const EdgeInsets.all(AppSpacing.md),  // 16px
  child: MyWidget(),
)
```

### 4. **Create Responsive Layouts**

```dart
import 'package:cmn_health_app/core/widgets/responsive_widgets.dart';
import 'package:cmn_health_app/core/theme/responsive.dart';

class MyScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // Easy access to screen size
    if (context.isMobile) {
      return MobileLayout();
    } else if (context.isTablet) {
      return TabletLayout();
    } else {
      return DesktopLayout();
    }
  }
}

// Or use responsive widgets
ResponsiveContainer(
  child: ResponsiveGrid(
    children: [item1, item2, item3],  // Auto-adjusts columns
  ),
)
```

### 5. **Use Custom Buttons**

```dart
import 'package:cmn_health_app/core/widgets/custom_buttons.dart';

// Primary action
PrimaryButton(
  label: 'Get Started',
  onPressed: () {},
  fullWidth: true,
)

// Secondary action
SecondaryButton(
  label: 'Cancel',
  onPressed: () {},
)
```

### 6. **Use Custom Cards**

```dart
CustomCard(
  child: Column(
    children: [
      Text('Title'),
      Text('Description'),
    ],
  ),
)

// Info card
InfoCard(
  title: 'Patient Rights',
  description: 'Learn about your rights',
  icon: Icons.info,
  onTap: () {},
)

// Alert card
AlertCard(
  title: 'Success',
  message: 'Operation completed',
  type: AlertType.success,
)
```

### 7. **Use Adaptive Navigation**

```dart
import 'package:cmn_health_app/core/widgets/adaptive_navigation.dart';

AdaptiveNavigation(
  items: [
    NavigationItem(label: 'Home', icon: Icons.home, routeName: '/home'),
    NavigationItem(label: 'Chat', icon: Icons.chat, routeName: '/chat'),
    NavigationItem(label: 'Profile', icon: Icons.person, routeName: '/profile'),
  ],
  selectedIndex: 0,
  onItemSelected: (index) {},
  content: YourContent(),
  // Mobile: BottomNavigationBar
  // Tablet: NavigationRail
  // Desktop: Extended sidebar
)
```

---

## 🎨 Color Palette

### Primary Brand
- **Primary**: `#1976D2` (Professional Blue)
- **On Primary**: `#FFFFFF` (White text on primary)

### Secondary
- **Secondary**: `#03DAC6` (Teal)
- **Tertiary**: `#EF7B2F` (Orange)

### Semantic Colors
- **Success**: `#2E7D32` (Green)
- **Warning**: `#F57C00` (Orange)
- **Error**: `#B3261E` (Red)
- **Info**: `#0288D1` (Light Blue)

### Grayscale
```
Gray 900: #1A1C1E (Almost black)
Gray 800: #313033
Gray 700: #49454E
Gray 600: #625B71
Gray 500: #79747E (Mid gray)
Gray 400: #938F96
Gray 300: #CAC7D0
Gray 200: #E8DEF8
Gray 100: #F5EFF7
Gray 50:  #FAF8FD (Almost white)
```

**Usage:**
```dart
Text('Body text', style: TextStyle(color: AppColors.gray700))
Divider(color: AppColors.gray300)
```

---

## 📝 Typography System

### Hierarchy

| Style | Size | Weight | Use Case |
|-------|------|--------|----------|
| Display Large | 57px | 400 | App title/hero |
| Headline Large | 32px | 600 | Page titles |
| Title Large | 22px | 600 | Section headers |
| Body Large | 16px | 400 | Main content |
| Body Small | 12px | 400 | Secondary text |
| Label Large | 14px | 500 | Buttons/tags |

**Usage:**

```dart
// Headlines
Text('Page Title', style: AppTypography.buildTextTheme().headlineLarge)

// Body text
Text('Description', style: AppTypography.buildTextTheme().bodyMedium)

// Labels
Text('Submit', style: AppTypography.buildTextTheme().labelLarge)
```

---

## 📐 Spacing System (8px Base)

| Token | Value | Use Case |
|-------|-------|----------|
| xs | 4px | Minimal gaps |
| sm | 8px | Component padding |
| md | 16px | Default spacing |
| lg | 24px | Section spacing |
| xl | 32px | Large gaps |
| xxl | 40px | Extra large |

**Usage:**

```dart
// 8px base unit
Padding(padding: const EdgeInsets.all(AppSpacing.md))  // 16px
SizedBox(height: AppSpacing.lg)  // 24px gap
```

---

## 📱 Responsive Breakpoints

| Device | Width | Navigation |
|--------|-------|-----------|
| Mobile | 0-450px | Bottom Navigation |
| Tablet | 451-800px | Navigation Rail |
| Desktop | 801-1920px | Sidebar |
| Ultra-wide | 1921px+ | Extended Sidebar |

**Check Device Type:**

```dart
if (context.isMobile) {
  // Mobile layout
} else if (context.isTablet) {
  // Tablet layout
} else {
  // Desktop layout
}

// Direct access
bool mobile = context.screenSize.isMobile;
double width = context.width;
```

---

## 🔘 Button States

### Primary Button
```dart
PrimaryButton(
  label: 'Submit',
  onPressed: () {},
  isLoading: false,
  fullWidth: false,
  icon: Icons.check,
)
```

### Secondary Button
```dart
SecondaryButton(
  label: 'Cancel',
  onPressed: () {},
  fullWidth: false,
)
```

### Tertiary Button (Text)
```dart
TertiaryButton(
  label: 'Learn More',
  onPressed: () {},
)
```

---

## 🧩 Common Components

### Responsive Container
```dart
ResponsiveContainer(
  maxWidth: 1200,
  padding: const EdgeInsets.all(16),
  child: MyContent(),  // Centered, responsive padding
)
```

### Responsive Grid
```dart
ResponsiveGrid(
  children: items,  // Auto: 1 col (mobile), 2 cols (tablet), 3 cols (desktop)
)
```

### Info Card
```dart
InfoCard(
  title: 'Patient Rights',
  description: 'Learn your healthcare rights',
  icon: Icons.gavel,
  iconColor: AppColors.primary,
  onTap: () => navigator.push(...),
)
```

### Alert Card
```dart
AlertCard(
  title: 'Success',
  message: 'Your profile was updated',
  type: AlertType.success,
  onDismiss: () {},
)
```

---

## 🎬 Animation Durations

```dart
const Duration fastAnimation = Duration(milliseconds: 300);
const Duration normalAnimation = Duration(milliseconds: 500);
const Duration slowAnimation = Duration(milliseconds: 800);

// Usage
AnimatedContainer(
  duration: AppConstants.normalAnimationDuration,
  child: MyWidget(),
)
```

---

## ✅ Design System Best Practices

### ✅ DO:
- Use theme colors from `AppColors`
- Use typography styles from `AppTypography`
- Use spacing from `AppSpacing`
- Use responsive widgets for layouts
- Check `context.isMobile` for device-specific logic
- Use `ResponsiveContainer` for max-width constraints
- Use elevation for depth (AppSpacing.elevationSmall, Medium, Large)

### ❌ DON'T:
- Don't hardcode colors (use AppColors)
- Don't hardcode font sizes (use AppTypography)
- Don't hardcode padding/margins (use AppSpacing)
- Don't design mobile-only then stretch to web
- Don't use arbitrary responsive breakpoints
- Don't forget about tablet layouts
- Don't use too many different colors

---

## 🌍 Multi-Language Support

```dart
import 'package:cmn_health_app/core/constants/app_constants.dart';

// Supported languages
SupportedLanguages.codes  // ['en', 'yo', 'ha', 'ig']

// Example usage
// Use localization package with these language codes
```

---

## 🚀 Material 3 Features Used

✅ **Modern Color System**
- 13 color slots (primary, secondary, tertiary, etc.)
- Automatic light/dark variants

✅ **Rounded Corners**
- Small: 4px
- Medium: 8px
- Large: 12px
- Extra Large: 16px

✅ **Typography Scale**
- 3 display styles
- 3 headline styles
- 3 title styles
- 3 body styles
- 3 label styles

✅ **Elevation System**
- Small: 2px
- Medium: 4px
- Large: 8px

---

## 📱 Responsive Design Examples

### Mobile First (450px max)
```dart
ResponsiveContainer(
  child: Column(
    children: [
      Text('Title', style: AppTypography.buildTextTheme().headlineSmall),
      SizedBox(height: AppSpacing.md),
      PrimaryButton(label: 'Action', onPressed: () {}, fullWidth: true),
    ],
  ),
)
```

### Tablet (451-800px)
```dart
ResponsiveGrid(
  children: [
    InfoCard(title: 'Item 1', description: 'Desc'),
    InfoCard(title: 'Item 2', description: 'Desc'),
  ],
)
```

### Desktop (801px+)
```dart
ResponsiveGrid(
  children: [
    InfoCard(title: 'Item 1', description: 'Desc'),
    InfoCard(title: 'Item 2', description: 'Desc'),
    InfoCard(title: 'Item 3', description: 'Desc'),
  ],
)
```

---

## 🔍 Advanced Tips

### Custom Responsive Text Size
```dart
Text(
  'Dynamic Text',
  style: TextStyle(
    fontSize: AppTypography.responsiveFontSize(
      baseFontSize: 16,
      screenWidth: context.width,
    ),
  ),
)
```

### Device-Specific Styling
```dart
Container(
  padding: EdgeInsets.all(context.screenSize.responsivePadding),
  child: MyContent(),
)
```

### Grid Columns Based on Device
```dart
int columns = context.screenSize.gridColumns;  // 1, 2, 3, or 4
```

---

## 📚 File Structure Reference

When creating new screens:

```dart
// Good structure
lib/
├── features/
│   └── auth/
│       ├── screens/
│       │   └── login_screen.dart
│       ├── widgets/
│       │   └── login_form.dart
│       ├── models/
│       │   └── auth_state.dart
│       └── services/
│           └── auth_service.dart
```

---

## 🎓 Learning Resources

- **Material 3 Spec**: https://m3.material.io/
- **Flutter Material**: https://flutter.dev/docs/development/ui/widgets/material
- **Responsive Design**: https://flutter.dev/docs/development/ui/layout/responsive
- **Theme Data**: https://api.flutter.dev/flutter/material/ThemeData-class.html

---

## 📞 Support

For design system questions:
1. Check this guide
2. Look at existing screens for examples
3. Review `core/` folder structure

---

**Version**: 1.0.0  
**Last Updated**: May 18, 2024  
**Status**: Production Ready ✅
