import 'package:flutter/material.dart';

class ProgressProvider extends ChangeNotifier {
  int _totalHoursLearned = 0;
  int _conceptsMastered = 0;
  int _currentStreak = 0;
  double _averageQuizScore = 0.0;
  Map<String, double> _domainProgress = {};
  List<Map<String, dynamic>> _recentActivity = [];
  List<Map<String, dynamic>> _upcomingReviews = [];

  int get totalHoursLearned => _totalHoursLearned;
  int get conceptsMastered => _conceptsMastered;
  int get currentStreak => _currentStreak;
  double get averageQuizScore => _averageQuizScore;
  Map<String, double> get domainProgress => _domainProgress;
  List<Map<String, dynamic>> get recentActivity => _recentActivity;
  List<Map<String, dynamic>> get upcomingReviews => _upcomingReviews;

  Future<void> loadProgress() async {
    // Mock data - in production, fetch from API
    _totalHoursLearned = 12;
    _conceptsMastered = 8;
    _currentStreak = 5;
    _averageQuizScore = 0.85;
    _domainProgress = {
      'Networking': 0.75,
      'Linux': 0.60,
      'Windows': 0.40,
      'Security Fundamentals': 0.55,
      'Blue Team': 0.30,
      'Red Team': 0.20,
    };
    _recentActivity = [
      {'concept': 'DNS', 'status': 'mastered', 'score': 95, 'date': '2 hours ago'},
      {'concept': 'TCP/IP', 'status': 'practicing', 'score': 78, 'date': '5 hours ago'},
      {'concept': 'Linux Permissions', 'status': 'learning', 'score': 60, 'date': '1 day ago'},
    ];
    _upcomingReviews = [
      {'concept': 'HTTP/HTTPS', 'reviewAt': 'In 2 days', 'confidence': 65},
      {'concept': 'SSH', 'reviewAt': 'In 4 days', 'confidence': 72},
    ];
    notifyListeners();
  }

  void recordLessonCompletion(String conceptId, double score) {
    _averageQuizScore = (_averageQuizScore + score) / 2;
    notifyListeners();
  }

  void incrementStreak() {
    _currentStreak++;
    notifyListeners();
  }
}
