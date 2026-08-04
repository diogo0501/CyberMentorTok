import 'package:flutter/material.dart';
import '../models/lesson.dart';
import '../services/api_service.dart';

class FeedProvider extends ChangeNotifier {
  final ApiService _api = ApiService();
  List<LessonModel> _lessons = [];
  int _currentIndex = 0;
  bool _isLoading = false;
  bool _hasMore = true;
  String? _nextCursor;
  String? _error;
  String? _category;
  String? _conceptId;

  List<LessonModel> get lessons => _lessons;
  int get currentIndex => _currentIndex;
  bool get isLoading => _isLoading;
  bool get hasMore => _hasMore;
  String? get error => _error;

  LessonModel? get currentLesson =>
      _lessons.isNotEmpty ? _lessons[_currentIndex] : null;

  Future<void> loadInitialFeed() => loadFeed();

  Future<void> loadFeed({String? category, String? conceptId}) async {
    _category = category ?? _category;
    _conceptId = conceptId ?? _conceptId;
    _isLoading = true;
    _error = null;
    _currentIndex = 0;
    _nextCursor = null;
    _hasMore = true;
    notifyListeners();

    try {
      final data = await _api.getAnonymousFeed(
        category: _category,
        conceptId: _conceptId,
      );
      _lessons = _parseFeedItems(data);
      _nextCursor = data['next_cursor'];
      _hasMore = data['has_more'] ?? false;
    } catch (e) {
      _error = 'Failed to load feed: $e';
      _lessons = [];
      _hasMore = false;
    }
    _isLoading = false;
    notifyListeners();
  }

  Future<void> loadMore() async {
    if (_isLoading || !_hasMore) return;
    _isLoading = true;
    notifyListeners();

    try {
      final data = await _api.getAnonymousFeed(
        cursor: _nextCursor,
        category: _category,
        conceptId: _conceptId,
      );
      final more = _parseFeedItems(data);
      _lessons.addAll(more);
      _nextCursor = data['next_cursor'];
      _hasMore = data['has_more'] ?? false;
    } catch (e) {
      _hasMore = false;
    }
    _isLoading = false;
    notifyListeners();
  }

  /// Only keeps items that have a video or mask (video lessons only).
  List<LessonModel> _parseFeedItems(Map<String, dynamic> data) {
    final items = data['items'] as List? ?? [];
    return items
        .whereType<Map<String, dynamic>>()
        .map((e) => LessonModel.fromJson(e))
        .where((l) =>
            (l.videoUrl != null && l.videoUrl!.isNotEmpty) ||
            (l.maskUrl != null && l.maskUrl!.isNotEmpty))
        .toList();
  }

  void nextLesson() {
    if (_currentIndex < _lessons.length - 1) {
      _currentIndex++;
      notifyListeners();
    } else {
      loadMore();
    }
  }

  void previousLesson() {
    if (_currentIndex > 0) {
      _currentIndex--;
      notifyListeners();
    }
  }

  void setIndex(int index) {
    _currentIndex = index;
    notifyListeners();
  }
}
