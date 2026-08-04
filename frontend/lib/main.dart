import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'providers/auth_provider.dart';
import 'providers/feed_provider.dart';
import 'providers/progress_provider.dart';
import 'screens/feed_screen.dart';
import 'screens/login_screen.dart';
import 'screens/profile_screen.dart';
import 'screens/progress_screen.dart';
import 'screens/search_screen.dart';
import 'utils/ios_colors.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const CyberMentorTokApp());
}

class CyberMentorTokApp extends StatelessWidget {
  const CyberMentorTokApp({super.key});

  @override
  Widget build(BuildContext context) {
    // System fonts instead of google_fonts: no runtime CDN fetch, faster startup.
    final textTheme = ThemeData.dark().textTheme;
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AuthProvider()),
        ChangeNotifierProvider(create: (_) => FeedProvider()),
        ChangeNotifierProvider(create: (_) => ProgressProvider()),
      ],
      child: MaterialApp(
        title: 'CyberMentorTok',
        debugShowCheckedModeBanner: false,
        // Constrain to a mobile viewport on desktop (TikTok-like)
        builder: (context, child) => Center(
          child: Container(
            constraints: const BoxConstraints(maxWidth: 430),
            child: child!,
          ),
        ),
        theme: ThemeData(
          brightness: Brightness.dark,
          scaffoldBackgroundColor: iOS.background,
          colorScheme: const ColorScheme.dark(
            primary: Color(0xFFFE2C55),
            secondary: Color(0xFFFE2C55),
            surface: Color(0xFF121212),
            onSurface: Colors.white,
          ),
          textTheme: textTheme,
          appBarTheme: const AppBarTheme(
            backgroundColor: Colors.black,
            foregroundColor: Colors.white,
            elevation: 0,
            centerTitle: false,
          ),
          // TikTok-style input fields
          inputDecorationTheme: InputDecorationTheme(
            filled: true,
            fillColor: const Color(0xFF1C1C1E),
            hintStyle: const TextStyle(color: Color(0xFF8E8E93)),
            contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 14),
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(10),
              borderSide: BorderSide.none,
            ),
            enabledBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(10),
              borderSide: BorderSide.none,
            ),
            focusedBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(10),
              borderSide: const BorderSide(color: Color(0xFFFE2C55), width: 2),
            ),
          ),
          elevatedButtonTheme: ElevatedButtonThemeData(
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFFFE2C55),
              foregroundColor: Colors.white,
              elevation: 0,
              minimumSize: const Size.fromHeight(50),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              textStyle: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
            ),
          ),
          cardTheme: CardThemeData(
            color: const Color(0xFF121212),
            elevation: 0,
            margin: EdgeInsets.zero,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          ),
          navigationBarTheme: NavigationBarThemeData(
            backgroundColor: Colors.transparent,
            indicatorColor: iOS.blue.withOpacity(0.18),
            iconTheme: WidgetStateProperty.resolveWith((states) {
              return IconThemeData(
                color: states.contains(WidgetState.selected) ? iOS.blue : iOS.gray,
              );
            }),
            labelTextStyle: WidgetStateProperty.resolveWith((states) {
              return TextStyle(
                fontSize: 10,
                fontWeight: FontWeight.w600,
                color: states.contains(WidgetState.selected) ? iOS.blue : iOS.gray,
              );
            }),
          ),
        ),
        home: const AuthWrapper(),
      ),
    );
  }
}

class AuthWrapper extends StatelessWidget {
  const AuthWrapper({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<AuthProvider>(
      builder: (context, auth, _) {
        if (auth.isLoading) {
          return const Scaffold(
            body: Center(child: CircularProgressIndicator(color: iOS.blue)),
          );
        }
        if (auth.isAuthenticated) {
          return const MainNavigation();
        }
        return const LoginScreen();
      },
    );
  }
}

class MainNavigation extends StatefulWidget {
  const MainNavigation({super.key});

  @override
  State<MainNavigation> createState() => _MainNavigationState();
}

class _MainNavigationState extends State<MainNavigation> {
  int _currentIndex = 0;

  final List<Widget> _screens = const [
    FeedScreen(),
    SearchScreen(),
    ProgressScreen(),
    ProfileScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      extendBody: true,
      body: _screens[_currentIndex],
      bottomNavigationBar: _IosTabBar(
        currentIndex: _currentIndex,
        onSelected: (index) => setState(() => _currentIndex = index),
      ),
    );
  }
}

/// TikTok-style bottom tab bar (faint translucent overlay).
class _IosTabBar extends StatelessWidget {
  final int currentIndex;
  final ValueChanged<int> onSelected;

  const _IosTabBar({required this.currentIndex, required this.onSelected});

  @override
  Widget build(BuildContext context) {
    const items = [
      (0, Icons.home_outlined, Icons.home, 'Home'),
      (1, Icons.search, Icons.search, 'Search'),
      (-1, Icons.add, Icons.add, ''),
      (2, Icons.bar_chart_outlined, Icons.bar_chart, 'Progress'),
      (3, Icons.person_outline, Icons.person, 'Profile'),
    ];

    return ClipRect(
      child: BackdropFilter(
        filter: ImageFilter.blur(sigmaX: 28, sigmaY: 28),
        child: Container(
          decoration: BoxDecoration(
            color: Colors.black.withOpacity(0.62),
            border: const Border(top: BorderSide(color: Color(0x1CFFFFFF), width: 0.5)),
            boxShadow: const [
              BoxShadow(color: Color(0x66000000), blurRadius: 22, offset: Offset(0, -8)),
            ],
          ),
          child: SafeArea(
            top: false,
            child: Padding(
              padding: const EdgeInsets.fromLTRB(8, 6, 8, 5),
              child: Row(
                children: List.generate(items.length, (i) {
                  final item = items[i];
                  final index = item.$1;
                  final isCreate = index == -1;
                  final selected = index == currentIndex;
                  return Expanded(
                    child: GestureDetector(
                      behavior: HitTestBehavior.opaque,
                      onTap: () => onSelected(isCreate ? 1 : index),
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          if (isCreate)
                            Container(
                              width: 46,
                              height: 30,
                              decoration: BoxDecoration(
                                color: Colors.white,
                                borderRadius: BorderRadius.circular(8),
                                boxShadow: const [
                                  BoxShadow(color: Color(0xFF25F4EE), offset: Offset(-4, 0)),
                                  BoxShadow(color: Color(0xFFFE2C55), offset: Offset(4, 0)),
                                ],
                              ),
                              child: const Icon(Icons.add, color: Colors.black, size: 24),
                            )
                          else ...[
                            Icon(
                              selected ? item.$3 : item.$2,
                              size: 24,
                              color: selected ? Colors.white : const Color(0xFFB7B7B7),
                            ),
                            const SizedBox(height: 2),
                            Text(
                              item.$4,
                              style: TextStyle(
                                fontSize: 10,
                                fontWeight: selected ? FontWeight.w700 : FontWeight.w500,
                                color: selected ? Colors.white : const Color(0xFFB7B7B7),
                              ),
                            ),
                          ],
                        ],
                      ),
                    ),
                  );
                }),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
