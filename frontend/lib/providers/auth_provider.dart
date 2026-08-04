import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class AuthProvider extends ChangeNotifier {
  bool _isLoading = true;
  bool _isAuthenticated = false;
  String? _token;
  String? _userId;
  String? _username;

  bool get isLoading => _isLoading;
  bool get isAuthenticated => _isAuthenticated;
  String? get token => _token;
  String? get userId => _userId;
  String? get username => _username;

  AuthProvider() {
    _loadToken();
  }

  Future<void> _loadToken() async {
    final prefs = await SharedPreferences.getInstance();
    _token = prefs.getString('auth_token');
    _userId = prefs.getString('user_id');
    _username = prefs.getString('username');
    if (_token == null) {
      // Demo auto-login so the app opens straight on the video feed.
      _token = 'demo_token';
      _userId = 'demo_user';
      _username = 'student';
      await prefs.setString('auth_token', _token!);
      await prefs.setString('user_id', _userId!);
      await prefs.setString('username', _username!);
    }
    _isAuthenticated = true;
    _isLoading = false;
    notifyListeners();
  }

  Future<bool> login(String email, String password) async {
    try {
      // In production, call actual API
      // final response = await http.post(Uri.parse('$baseUrl/auth/login'), ...);
      _token = 'mock_token_$email';
      _userId = 'user_123';
      _username = email.split('@').first;
      _isAuthenticated = true;

      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('auth_token', _token!);
      await prefs.setString('user_id', _userId!);
      await prefs.setString('username', _username!);

      notifyListeners();
      return true;
    } catch (e) {
      return false;
    }
  }

  Future<bool> register(String email, String username, String password) async {
    try {
      _token = 'mock_token_$email';
      _userId = 'user_new';
      _username = username;
      _isAuthenticated = true;

      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('auth_token', _token!);
      await prefs.setString('user_id', _userId!);
      await prefs.setString('username', _username!);

      notifyListeners();
      return true;
    } catch (e) {
      return false;
    }
  }

  Future<void> logout() async {
    _token = null;
    _userId = null;
    _username = null;
    _isAuthenticated = false;

    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('auth_token');
    await prefs.remove('user_id');
    await prefs.remove('username');

    notifyListeners();
  }
}
