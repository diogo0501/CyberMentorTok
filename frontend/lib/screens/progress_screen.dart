import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/progress_provider.dart';

/// TikTok-style dark palette.
const _tRed = Color(0xFFFE2C55);
const _tCyan = Color(0xFF25F4EE);
const _tCard = Color(0xFF1C1C1E);
const _tLabel = Colors.white;
const _tSub = Color(0xFF8E8E93);
const _tGreen = Color(0xFF00C853);
const _tOrange = Color(0xFFFF9800);

class ProgressScreen extends StatefulWidget {
  const ProgressScreen({super.key});

  @override
  State<ProgressScreen> createState() => _ProgressScreenState();
}

class _ProgressScreenState extends State<ProgressScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<ProgressProvider>().loadProgress();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: SafeArea(
        child: Consumer<ProgressProvider>(
          builder: (context, progress, _) {
            return ListView(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              children: [
                const SizedBox(height: 12),
                const Text(
                  'Progress',
                  style: TextStyle(
                    color: _tLabel,
                    fontSize: 32,
                    fontWeight: FontWeight.w800,
                  ),
                ),
                const SizedBox(height: 16),
                // Stats row
                _buildStatsRow(progress),
                const SizedBox(height: 24),
                // Streak card
                _buildStreakCard(progress),
                const SizedBox(height: 24),
                // Domain progress
                const _SectionHeader('Domain Mastery'),
                const SizedBox(height: 6),
                _buildDomainProgress(progress),
                const SizedBox(height: 24),
                // Upcoming reviews
                const _SectionHeader('Upcoming Reviews'),
                const SizedBox(height: 6),
                _buildUpcomingReviews(progress),
                const SizedBox(height: 24),
                // Recent activity
                const _SectionHeader('Recent Activity'),
                const SizedBox(height: 6),
                _buildRecentActivity(progress),
                const SizedBox(height: 20),
              ],
            );
          },
        ),
      ),
    );
  }

  Widget _buildStatsRow(ProgressProvider progress) {
    return Row(
      children: [
        _buildStatCard(Icons.access_time, '${progress.totalHoursLearned}h', 'Learned', _tCyan),
        const SizedBox(width: 12),
        _buildStatCard(Icons.check_circle, '${progress.conceptsMastered}', 'Mastered', _tGreen),
        const SizedBox(width: 12),
        _buildStatCard(Icons.quiz, '${(progress.averageQuizScore * 100).toInt()}%', 'Quiz', _tOrange),
      ],
    );
  }

  Widget _buildStatCard(IconData icon, String value, String label, Color color) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 8),
        decoration: BoxDecoration(
          color: _tCard,
          borderRadius: BorderRadius.circular(14),
        ),
        child: Column(
          children: [
            Icon(icon, color: color, size: 26),
            const SizedBox(height: 8),
            Text(
              value,
              style: TextStyle(color: _tLabel, fontSize: 20, fontWeight: FontWeight.w700),
            ),
            Text(label, style: const TextStyle(color: _tSub, fontSize: 12)),
          ],
        ),
      ),
    );
  }

  Widget _buildStreakCard(ProgressProvider progress) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: _tCard,
        borderRadius: BorderRadius.circular(14),
      ),
      child: Row(
        children: [
          const Icon(Icons.local_fire_department, color: _tOrange, size: 44),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  '${progress.currentStreak} Day Streak!',
                  style: const TextStyle(
                    color: _tOrange,
                    fontSize: 20,
                    fontWeight: FontWeight.w700,
                  ),
                ),
                const SizedBox(height: 4),
                const Text(
                  'Keep learning daily to maintain your streak',
                  style: TextStyle(color: _tSub, fontSize: 12),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildDomainProgress(ProgressProvider progress) {
    final colors = [_tRed, _tCyan, _tGreen, _tOrange, Color(0xFF7C4DFF), Color(0xFF00BCD4)];
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: _tCard,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        children: progress.domainProgress.entries.map((entry) {
          final color = colors[progress.domainProgress.keys.toList().indexOf(entry.key) % colors.length];
          return Padding(
            padding: const EdgeInsets.only(bottom: 12),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(entry.key, style: const TextStyle(color: _tLabel, fontSize: 14)),
                    Text('${(entry.value * 100).toInt()}%', style: TextStyle(color: color, fontSize: 14)),
                  ],
                ),
                const SizedBox(height: 8),
                ClipRRect(
                  borderRadius: BorderRadius.circular(4),
                  child: LinearProgressIndicator(
                    value: entry.value,
                    backgroundColor: Colors.white12,
                    valueColor: AlwaysStoppedAnimation(color),
                    minHeight: 6,
                  ),
                ),
              ],
            ),
          );
        }).toList(),
      ),
    );
  }

  Widget _buildUpcomingReviews(ProgressProvider progress) {
    if (progress.upcomingReviews.isEmpty) {
      return const Text('No reviews scheduled', style: TextStyle(color: _tSub));
    }
    return Container(
      decoration: BoxDecoration(
        color: _tCard,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        children: progress.upcomingReviews.asMap().entries.map((entry) {
          final review = entry.value;
          final confidence = review['confidence'] as int? ?? 0;
          return Column(
            children: [
              if (entry.key > 0) const Divider(height: 1, indent: 16, endIndent: 16, color: Colors.white24),
              ListTile(
                title: Text(review['concept'] ?? '', style: const TextStyle(color: _tLabel)),
                subtitle: Text(
                  review['reviewAt']?.toString() ?? '',
                  style: const TextStyle(color: _tSub, fontSize: 12),
                ),
                trailing: Text(
                  '$confidence%',
                  style: TextStyle(
                    color: confidence > 70 ? _tGreen : _tOrange,
                    fontWeight: FontWeight.w700,
                  ),
                ),
              ),
            ],
          );
        }).toList(),
      ),
    );
  }

  Widget _buildRecentActivity(ProgressProvider progress) {
    return Container(
      decoration: BoxDecoration(
        color: _tCard,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        children: progress.recentActivity.asMap().entries.map((entry) {
          final activity = entry.value;
          final status = activity['status']?.toString() ?? '';
          final statusColor = status == 'mastered'
              ? _tGreen
              : status == 'practicing'
                  ? _tCyan
                  : _tOrange;
          return Column(
            children: [
              if (entry.key > 0) const Divider(height: 1, indent: 16, endIndent: 16, color: Colors.white24),
              ListTile(
                leading: Container(
                  width: 8,
                  height: 8,
                  decoration: BoxDecoration(shape: BoxShape.circle, color: statusColor),
                ),
                title: Text(activity['concept']?.toString() ?? '', style: const TextStyle(color: _tLabel)),
                subtitle: Text(
                  '${activity['status']} • ${activity['date']}',
                  style: const TextStyle(color: _tSub, fontSize: 12),
                ),
                trailing: Text(
                  '${activity['score'] ?? '0'}%',
                  style: TextStyle(color: statusColor, fontWeight: FontWeight.w700),
                ),
              ),
            ],
          );
        }).toList(),
      ),
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
