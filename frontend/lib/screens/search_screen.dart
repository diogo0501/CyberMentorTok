import 'package:flutter/material.dart';
import '../services/api_service.dart';
import 'category_feed_screen.dart';

/// TikTok-style dark palette (matches the feed).
const _tRed = Color(0xFFFE2C55);
const _tCard = Color(0xFF1C1C1E);
const _tCard2 = Color(0xFF2C2C2E);
const _tLabel = Colors.white;
const _tSub = Color(0xFF8E8E93);

class SearchScreen extends StatefulWidget {
  const SearchScreen({super.key});

  @override
  State<SearchScreen> createState() => _SearchScreenState();
}

class _SearchScreenState extends State<SearchScreen> {
  final _searchController = TextEditingController();
  final ApiService _api = ApiService();

  List<Map<String, dynamic>> _results = [];
  List<Map<String, dynamic>> _categories = [];
  Map<String, int> _videoCountByCategory = {};
  bool _isSearching = false;
  bool _loadingCategories = true;

  static const Map<String, Map<String, dynamic>> _categoryMeta = {
    'networking': {'name': 'Networking', 'icon': Icons.wifi, 'color': Color(0xFF2196F3)},
    'security-architecture': {'name': 'Security Architecture', 'icon': Icons.shield, 'color': Color(0xFF4CAF50)},
    'security-fundamentals': {'name': 'Security Fundamentals', 'icon': Icons.verified_user, 'color': Color(0xFF009688)},
    'fundamentals': {'name': 'Fundamentals', 'icon': Icons.school, 'color': Color(0xFF9C27B0)},
    'linux': {'name': 'Linux', 'icon': Icons.terminal, 'color': Color(0xFFFF9800)},
    'windows': {'name': 'Windows', 'icon': Icons.desktop_windows, 'color': Color(0xFF00BCD4)},
    'blue-team': {'name': 'Blue Team', 'icon': Icons.visibility, 'color': Color(0xFF3F51B5)},
    'red-team': {'name': 'Red Team', 'icon': Icons.bug_report, 'color': Color(0xFFF44336)},
    'cloud': {'name': 'Cloud', 'icon': Icons.cloud, 'color': Color(0xFFAB47BC)},
    'advanced': {'name': 'Advanced', 'icon': Icons.code, 'color': Color(0xFFFFC107)},
    'programming': {'name': 'Programming', 'icon': Icons.code, 'color': Color(0xFF607D8B)},
  };

  @override
  void initState() {
    super.initState();
    _loadCategories();
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  String _categoryName(String slug) =>
      _categoryMeta[slug]?['name'] as String? ?? _toTitleCase(slug);

  String _toTitleCase(String s) =>
      s.isEmpty ? s : s.split('-').map((w) => w.isEmpty ? w : w[0].toUpperCase() + w.substring(1)).join(' ');

  Future<void> _loadCategories() async {
    setState(() => _loadingCategories = true);
    try {
      final data = await _api.getCategories();
      final cats = (data['categories'] as List? ?? []).whereType<Map<String, dynamic>>().toList();
      setState(() {
        // Only categories that actually have video lessons
        _categories = cats.where((c) => (c['video_count'] ?? 0) > 0).toList();
        _videoCountByCategory = {
          for (final c in _categories) (c['name'] as String? ?? '') : (c['video_count'] as num? ?? 0).toInt(),
        };
        _loadingCategories = false;
      });
    } catch (e) {
      setState(() {
        _categories = [];
        _videoCountByCategory = {};
        _loadingCategories = false;
      });
    }
  }

  Future<void> _performSearch(String query) async {
    if (query.trim().isEmpty) {
      setState(() {
        _results = [];
        _isSearching = false;
      });
      return;
    }

    setState(() => _isSearching = true);
    try {
      final data = await _api.search(query.trim());
      final results = (data['results'] as List? ?? []).whereType<Map<String, dynamic>>().toList();
      // Keep lessons (which have videos) and concepts whose category has videos
      final filtered = results.where((r) {
        if (r['type'] == 'lesson') return true;
        if (r['type'] == 'concept') {
          final cat = r['category']?.toString() ?? '';
          return (_videoCountByCategory[cat] ?? 0) > 0;
        }
        return false;
      }).toList();
      setState(() {
        _results = filtered;
        _isSearching = false;
      });
    } catch (e) {
      setState(() {
        _results = [];
        _isSearching = false;
      });
    }
  }

  void _openCategory(String slug) {
    if (slug.isEmpty) return;
    Navigator.of(context).push(MaterialPageRoute(
      builder: (_) => CategoryFeedScreen(title: _categoryName(slug), category: slug),
    ));
  }

  void _openConcept(Map<String, dynamic> concept) {
    _openCategory(concept['category']?.toString() ?? '');
  }

  void _openLesson(Map<String, dynamic> lesson) {
    final conceptId = lesson['concept_id']?.toString();
    final concept = lesson['concept']?.toString() ?? 'Lesson';
    Navigator.of(context).push(MaterialPageRoute(
      builder: (_) => CategoryFeedScreen(title: concept, conceptId: conceptId),
    ));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: SafeArea(
        child: Column(
          children: [
            // TikTok-style search bar (rounded gray pill)
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 12, 16, 8),
              child: TextField(
                controller: _searchController,
                onChanged: _performSearch,
                style: const TextStyle(color: _tLabel, fontSize: 16),
                decoration: InputDecoration(
                  hintText: 'Search lessons, topics…',
                  hintStyle: const TextStyle(color: _tSub, fontSize: 16),
                  prefixIcon: const Icon(Icons.search, color: _tSub, size: 20),
                  suffixIcon: _searchController.text.isNotEmpty
                      ? IconButton(
                          icon: const Icon(Icons.cancel, color: _tSub, size: 18),
                          onPressed: () {
                            _searchController.clear();
                            _performSearch('');
                          },
                        )
                      : null,
                  filled: true,
                  fillColor: _tCard,
                  isDense: true,
                  contentPadding: const EdgeInsets.symmetric(vertical: 12),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                    borderSide: BorderSide.none,
                  ),
                ),
              ),
            ),
            // Results or categories
            Expanded(
              child: _isSearching
                  ? const Center(child: CircularProgressIndicator(color: _tRed))
                  : _results.isNotEmpty
                      ? _buildSearchResults()
                      : _buildCategories(),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSearchResults() {
    return ListView.builder(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      itemCount: _results.length,
      itemBuilder: (context, index) {
        final result = _results[index];
        final isConcept = result['type'] == 'concept';
        final title = result['name']?.toString() ?? result['title']?.toString() ?? '';
        final subtitle = isConcept
            ? '${_categoryName(result['category']?.toString() ?? '')} • ${_videoCountByCategory[result['category']?.toString()] ?? 0} videos'
            : '${result['concept']?.toString() ?? ''} • Difficulty ${result['difficulty']}';

        return Card(
          color: _tCard,
          margin: const EdgeInsets.only(bottom: 8),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          child: ListTile(
            onTap: () => isConcept ? _openConcept(result) : _openLesson(result),
            leading: Container(
              width: 40,
              height: 40,
              decoration: BoxDecoration(
                color: isConcept ? _tRed.withOpacity(0.18) : Colors.white.withOpacity(0.12),
                borderRadius: BorderRadius.circular(10),
              ),
              child: Icon(
                isConcept ? Icons.lightbulb_outline : Icons.play_circle_outline,
                color: isConcept ? _tRed : Colors.white,
                size: 22,
              ),
            ),
            title: Text(title, style: const TextStyle(color: _tLabel)),
            subtitle: Text(subtitle, style: const TextStyle(color: _tSub, fontSize: 12)),
            trailing: const Icon(Icons.chevron_right, color: _tSub, size: 20),
          ),
        );
      },
    );
  }

  Widget _buildCategories() {
    if (_loadingCategories) {
      return const Center(child: CircularProgressIndicator(color: _tRed));
    }
    if (_categories.isEmpty) {
      return const Center(
        child: Text(
          'No video categories available',
          style: TextStyle(color: _tSub),
        ),
      );
    }
    return ListView(
      padding: const EdgeInsets.symmetric(horizontal: 16),
      children: [
        const _SectionHeader('Browse by Category'),
        const SizedBox(height: 16),
        GridView.builder(
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 2,
            crossAxisSpacing: 12,
            mainAxisSpacing: 12,
            childAspectRatio: 1.5,
          ),
          itemCount: _categories.length,
          itemBuilder: (context, index) {
            final cat = _categories[index];
            final slug = cat['name']?.toString() ?? '';
            final meta = _categoryMeta[slug] ?? const {};
            final color = (meta['color'] as Color?) ?? _tRed;
            final icon = (meta['icon'] as IconData?) ?? Icons.category;
            final videoCount = (cat['video_count'] ?? 0).toString();
            return InkWell(
              onTap: () => _openCategory(slug),
              borderRadius: BorderRadius.circular(14),
              child: Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: _tCard,
                  borderRadius: BorderRadius.circular(14),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Icon(icon, color: color, size: 26),
                        const Icon(Icons.chevron_right, color: _tSub, size: 18),
                      ],
                    ),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          _categoryName(slug),
                          style: const TextStyle(
                            color: _tLabel,
                            fontSize: 14,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                        Text(
                          '$videoCount videos',
                          style: const TextStyle(color: _tSub, fontSize: 11),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            );
          },
        ),
        const SizedBox(height: 24),
        const _SectionHeader('Popular Searches'),
        const SizedBox(height: 12),
        Wrap(
          spacing: 8,
          runSpacing: 8,
          children: [
            _buildPopularTag('DNS'),
            _buildPopularTag('TCP/IP'),
            _buildPopularTag('TLS'),
            _buildPopularTag('Cryptography'),
            _buildPopularTag('Cloud'),
            _buildPopularTag('OSI'),
            _buildPopularTag('Firewall'),
            _buildPopularTag('Encryption'),
            _buildPopularTag('Security'),
          ],
        ),
      ],
    );
  }

  Widget _buildPopularTag(String tag) {
    return ActionChip(
      label: Text(tag, style: const TextStyle(color: _tLabel, fontSize: 12)),
      backgroundColor: _tCard2,
      side: BorderSide.none,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(18)),
      onPressed: () {
        _searchController.text = tag;
        _performSearch(tag);
      },
    );
  }
}

/// TikTok-style section header (small, uppercase, gray).
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

