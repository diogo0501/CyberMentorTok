import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/feed_provider.dart';
import 'feed_screen.dart';

/// Shows the video feed filtered to a specific category or concept.
/// Uses its own scoped [FeedProvider] so it doesn't disturb the main feed.
class CategoryFeedScreen extends StatefulWidget {
  final String title;
  final String? category;
  final String? conceptId;

  const CategoryFeedScreen({
    super.key,
    required this.title,
    this.category,
    this.conceptId,
  });

  @override
  State<CategoryFeedScreen> createState() => _CategoryFeedScreenState();
}

class _CategoryFeedScreenState extends State<CategoryFeedScreen> {
  late final FeedProvider _feedProvider;

  @override
  void initState() {
    super.initState();
    _feedProvider = FeedProvider();
    _feedProvider.loadFeed(category: widget.category, conceptId: widget.conceptId);
  }

  @override
  void dispose() {
    _feedProvider.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider<FeedProvider>.value(
      value: _feedProvider,
      child: Scaffold(
        backgroundColor: Colors.black,
        appBar: AppBar(
          backgroundColor: Colors.black,
          elevation: 0,
          leading: const BackButton(color: Colors.white),
          title: Text(
            widget.title,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 18,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
        body: const FeedScreen(),
      ),
    );
  }
}
