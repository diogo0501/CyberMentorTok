import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = 'http://localhost:8000/api/v1';
  static const String rootUrl = 'http://localhost:8000';
  String? _token;

  /// Resolve a relative media path (e.g. "/videos/abc/full.mp4") to an absolute URL.
  static String resolveUrl(String path) {
    if (path.startsWith('http')) return path;
    return '$rootUrl$path';
  }

  void setToken(String? token) => _token = token;

  Map<String, String> get _headers => {
        'Content-Type': 'application/json',
        if (_token != null) 'Authorization': 'Bearer $_token',
      };

  Future<Map<String, dynamic>> get(String path, {Map<String, String>? params}) async {
    final uri = Uri.parse('$baseUrl$path').replace(queryParameters: params);
    final response = await http.get(uri, headers: _headers);
    return _handleResponse(response);
  }

  Future<Map<String, dynamic>> post(String path, {Map<String, dynamic>? body}) async {
    final response = await http.post(
      Uri.parse('$baseUrl$path'),
      headers: _headers,
      body: body != null ? jsonEncode(body) : null,
    );
    return _handleResponse(response);
  }

  Future<Map<String, dynamic>> patch(String path, {Map<String, dynamic>? body}) async {
    final response = await http.patch(
      Uri.parse('$baseUrl$path'),
      headers: _headers,
      body: body != null ? jsonEncode(body) : null,
    );
    return _handleResponse(response);
  }

  Future<void> delete(String path) async {
    final response = await http.delete(Uri.parse('$baseUrl$path'), headers: _headers);
    if (response.statusCode >= 400) {
      throw Exception('Failed to delete');
    }
  }

  Map<String, dynamic> _handleResponse(http.Response response) {
    if (response.statusCode >= 400) {
      throw Exception('API Error: ${response.statusCode}');
    }
    return jsonDecode(response.body);
  }

  // Auth
  Future<Map<String, dynamic>> login(String email, String password) =>
      post('/auth/login', body: {'email': email, 'password': password});

  Future<Map<String, dynamic>> register(String email, String username, String password) =>
      post('/auth/register', body: {'email': email, 'username': username, 'password': password});

  // Feed
  Future<Map<String, dynamic>> getFeed({String? cursor, String? category, int? difficulty}) =>
      get('/videos/feed', params: {
        if (cursor != null) 'cursor': cursor,
        if (category != null) 'category': category,
        if (difficulty != null) 'difficulty': difficulty.toString(),
      });

  // Anonymous feed - no auth required, returns only video lessons
  Future<Map<String, dynamic>> getAnonymousFeed({String? cursor, String? category, String? conceptId, int? difficulty}) =>
      get('/videos/feed/anonymous', params: {
        if (cursor != null) 'cursor': cursor,
        if (category != null) 'category': category,
        if (conceptId != null) 'concept_id': conceptId,
        if (difficulty != null) 'difficulty': difficulty.toString(),
      });

  // Concepts
  Future<Map<String, dynamic>> getConcepts({String? category, int? difficulty}) =>
      get('/concepts/', params: {
        if (category != null) 'category': category,
        if (difficulty != null) 'difficulty': difficulty.toString(),
      });

  Future<Map<String, dynamic>> getConceptGraph({String? category}) =>
      get('/concepts/graph', params: {if (category != null) 'category': category});

  // Lessons
  Future<Map<String, dynamic>> getLesson(String id) => get('/lessons/$id');
  Future<Map<String, dynamic>> getLessonFeed(String id) => get('/lessons/$id/feed');

  // Progress
  Future<Map<String, dynamic>> getProgress(String lessonId) => get('/progress/lesson/$lessonId');
  Future<Map<String, dynamic>> updateProgress(Map<String, dynamic> data) =>
      post('/progress/lesson', body: data);
  Future<Map<String, dynamic>> getDashboard() => get('/progress/dashboard');

  // Quizzes
  Future<Map<String, dynamic>> getQuizzes(String lessonId) => get('/quizzes/lesson/$lessonId');
  Future<Map<String, dynamic>> submitQuiz(Map<String, dynamic> data) =>
      post('/quizzes/submit', body: data);

  // Bookmarks
  Future<List<dynamic>> getBookmarks({String? folder}) async {
    final result = await get('/bookmarks/', params: {if (folder != null) 'folder': folder});
    return result['bookmarks'] ?? [];
  }

  Future<void> createBookmark(Map<String, dynamic> data) => post('/bookmarks/', body: data);
  Future<void> deleteBookmark(String id) => delete('/bookmarks/$id');

  // Search
  Future<Map<String, dynamic>> search(String query, {String? type}) =>
      get('/search/', params: {'q': query, if (type != null) 'type': type});

  Future<Map<String, dynamic>> autocomplete(String query) =>
      get('/search/autocomplete', params: {'q': query});

  // Categories (with video counts)
  Future<Map<String, dynamic>> getCategories() => get('/search/categories');

  // User
  Future<Map<String, dynamic>> getProfile() => get('/users/me');
  Future<Map<String, dynamic>> getStats() => get('/users/me/stats');
}
