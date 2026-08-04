import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/auth_provider.dart';
import '../providers/progress_provider.dart';

/// TikTok-style dark palette.
const _tRed = Color(0xFFFE2C55);
const _tCyan = Color(0xFF25F4EE);
const _tCard = Color(0xFF1C1C1E);
const _tLabel = Colors.white;
const _tSub = Color(0xFF8E8E93);

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: SafeArea(
        child: Consumer2<AuthProvider, ProgressProvider>(
          builder: (context, auth, progress, _) {
            return ListView(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              children: [
                const SizedBox(height: 12),
                // TikTok-style large title
                const Text(
                  'Profile',
                  style: TextStyle(
                    color: _tLabel,
                    fontSize: 32,
                    fontWeight: FontWeight.w800,
                  ),
                ),
                const SizedBox(height: 16),
                // Header: avatar + name
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: _tCard,
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: Row(
                    children: [
                      Container(
                        width: 64,
                        height: 64,
                        decoration: const BoxDecoration(
                          shape: BoxShape.circle,
                          gradient: LinearGradient(
                            begin: Alignment.topLeft,
                            end: Alignment.bottomRight,
                            colors: [_tRed, _tCyan],
                          ),
                        ),
                        child: Center(
                          child: Text(
                            (auth.username ?? 'U')[0].toUpperCase(),
                            style: const TextStyle(
                              color: Colors.white,
                              fontSize: 28,
                              fontWeight: FontWeight.w700,
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(width: 16),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              auth.username ?? 'User',
                              style: const TextStyle(
                                color: _tLabel,
                                fontSize: 22,
                                fontWeight: FontWeight.w700,
                              ),
                            ),
                            const SizedBox(height: 4),
                            Text(
                              'Level ${progress.conceptsMastered ~/ 5 + 1}',
                              style: const TextStyle(color: _tRed, fontSize: 15),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 24),
                const _SectionHeader('Learning Stats'),
                const SizedBox(height: 6),
                Container(
                  decoration: BoxDecoration(
                    color: _tCard,
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Column(
                    children: [
                      _buildStatRow(Icons.access_time, 'Total Hours', '${progress.totalHoursLearned}h'),
                      _buildDivider(),
                      _buildStatRow(Icons.check_circle, 'Concepts Mastered', '${progress.conceptsMastered}'),
                      _buildDivider(),
                      _buildStatRow(Icons.local_fire_department, 'Current Streak', '${progress.currentStreak} days'),
                      _buildDivider(),
                      _buildStatRow(Icons.quiz, 'Avg Quiz Score', '${(progress.averageQuizScore * 100).toInt()}%'),
                    ],
                  ),
                ),
                const SizedBox(height: 24),
                const _SectionHeader('Settings'),
                const SizedBox(height: 6),
                Container(
                  decoration: BoxDecoration(
                    color: _tCard,
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Column(
                    children: [
                      _buildSettingsTile(Icons.notifications_outlined, 'Notifications', () {}),
                      _buildDivider(),
                      _buildSettingsTile(Icons.dark_mode_outlined, 'Theme', () {}),
                      _buildDivider(),
                      _buildSettingsTile(Icons.download_outlined, 'Downloads', () {}),
                      _buildDivider(),
                      _buildSettingsTile(Icons.bookmark_outline, 'Bookmarks', () {}),
                      _buildDivider(),
                      _buildSettingsTile(Icons.help_outline, 'Help & Support', () {}),
                      _buildDivider(),
                      _buildSettingsTile(
                        Icons.logout,
                        'Logout',
                        () => auth.logout(),
                        color: _tRed,
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 20),
              ],
            );
          },
        ),
      ),
    );
  }

  Widget _buildDivider() =>
      const Divider(height: 1, indent: 16, endIndent: 16, color: Colors.white24);

  Widget _buildStatRow(IconData icon, String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      child: Row(
        children: [
          Icon(icon, color: _tRed, size: 20),
          const SizedBox(width: 14),
          Expanded(child: Text(label, style: const TextStyle(color: _tLabel, fontSize: 16))),
          Text(
            value,
            style: const TextStyle(
              color: _tSub,
              fontSize: 15,
              fontWeight: FontWeight.w500,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSettingsTile(IconData icon, String label, VoidCallback onTap, {Color? color}) {
    return ListTile(
      leading: Icon(icon, color: color ?? _tRed, size: 22),
      title: Text(
        label,
        style: TextStyle(color: color ?? _tLabel, fontSize: 16),
      ),
      trailing: const Icon(Icons.chevron_right, size: 18, color: _tSub),
      onTap: onTap,
    );
  }
}

class _SectionHeader extends StatelessWidget {
  final String title;
  const _SectionHeader(this.title);

  @override
  Widget build(BuildContext context) {
    return Text(
      title.toUpperCase(),
      style: const TextStyle(
        color: _tSub,
        fontSize: 13,
        fontWeight: FontWeight.w600,
        letterSpacing: 0.6,
      ),
    );
  }
}
