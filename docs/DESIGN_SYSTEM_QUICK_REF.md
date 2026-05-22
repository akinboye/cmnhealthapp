# ⚡ Design System Quick Reference

## One-Minute Overview

```dart
// 1. Colors
AppColors.primary              // Blue #1976D2
AppColors.secondary            // Teal #03DAC6
AppColors.error                // Red #B3261E
AppColors.gray700              // Dark gray

// 2. Typography
AppTypography.buildTextTheme().headlineLarge   // 32px bold
AppTypography.buildTextTheme().bodyMedium      // 14px regular
AppTypography.buildTextTheme().labelSmall      // 11px medium

// 3. Spacing (8px base)
AppSpacing.xs   // 4px
AppSpacing.sm   // 8px
AppSpacing.md   // 16px (most common)
AppSpacing.lg   // 24px
AppSpacing.xl   // 32px

// 4. Responsive
context.isMobile      // true if width < 450
context.isTablet      // true if 451 < width < 800
context.isDesktop     // true if width > 800
context.width         // Screen width
context.height        // Screen height
```

---

## Common Patterns

### Basic Screen
```dart
class MyScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Title')),
      body: ResponsiveContainer(
        child: Column(
          children: [
            Text('Content', style: AppTypography.buildTextTheme().bodyLarge),
            SizedBox(height: AppSpacing.lg),
            PrimaryButton(label: 'Action', onPressed: () {}),
          ],
        ),
      ),
    );
  }
}
```

### Responsive Grid
```dart
ResponsiveGrid(
  spacing: AppSpacing.md,
  children: items.map((item) => InfoCard(...)).toList(),
)
// Mobile: 1 column
// Tablet: 2 columns
// Desktop: 3 columns
```

### Device-Specific Layout
```dart
if (context.isMobile) {
  return MobileLayout();
} else {
  return DesktopLayout();
}
```

### Button Variations
```dart
PrimaryButton(label: 'Submit', onPressed: () {})
SecondaryButton(label: 'Cancel', onPressed: () {})
TertiaryButton(label: 'Learn More', onPressed: () {})
```

### Alert/Info Cards
```dart
InfoCard(icon: Icons.info, title: 'Title', description: 'Desc')
AlertCard(title: 'Error', message: 'Error message', type: AlertType.error)
```

---

## Spacing Cheat Sheet

```
xs:   4px   → Minimal gaps
sm:   8px   → Padding between elements
md:   16px  → Default padding (most used)
lg:   24px  → Section spacing
xl:   32px  → Large sections
xxl:  40px  → Extra large spacing
```

---

## Color Quick Reference

| Color | Hex | Usage |
|-------|-----|-------|
| Primary | #1976D2 | Buttons, highlights |
| Secondary | #03DAC6 | Accents |
| Tertiary | #EF7B2F | Warnings |
| Success | #2E7D32 | Success states |
| Error | #B3261E | Errors, alerts |
| Gray500 | #79747E | Disabled text |

---

## Don't Forget!

✅ Always import from `core/`  
✅ Use `context.isMobile` for responsive logic  
✅ Use `AppSpacing.md` instead of hardcoding `16`  
✅ Use `AppColors.primary` instead of `0xFF1976D2`  
✅ Wrap long layouts in `ResponsiveContainer`  
✅ Use `ResponsiveGrid` for multi-column layouts  

---

## File Import Shortcuts

```dart
// Colors
import 'package:cmn_health_app/core/theme/colors.dart';

// Typography
import 'package:cmn_health_app/core/theme/typography.dart';

// Spacing
import 'package:cmn_health_app/core/theme/spacing.dart';

// Responsive
import 'package:cmn_health_app/core/theme/responsive.dart';

// Buttons & Cards
import 'package:cmn_health_app/core/widgets/custom_buttons.dart';

// Responsive Widgets
import 'package:cmn_health_app/core/widgets/responsive_widgets.dart';

// Navigation
import 'package:cmn_health_app/core/widgets/adaptive_navigation.dart';
```

---

## Responsive Breakpoints

| Device | Width | Nav |
|--------|-------|-----|
| Mobile | 0-450 | Bottom |
| Tablet | 451-800 | Rail |
| Desktop | 801+ | Sidebar |

---

That's it! Check `DESIGN_SYSTEM_GUIDE.md` for more details.
