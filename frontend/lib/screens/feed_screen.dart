import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/feed_provider.dart';
import '../widgets/lesson_card.dart';

class FeedScreen extends StatefulWidget {
  const FeedScreen({super.key});

  @override
  State<FeedScreen> createState() => _FeedScreenState();
}

class _FeedScreenState extends State<FeedScreen> {
  final PageController _pageController = PageController();

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<FeedProvider>().loadInitialFeed();
    });
  }

  @override
  void dispose() {
    _pageController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: Consumer<FeedProvider>(
        builder: (context, feed, _) {
          if (feed.isLoading && feed.lessons.isEmpty) {
            return const Center(
              child: CircularProgressIndicator(color: Color(0xFFFE2C55)),
            );
          }

          if (feed.lessons.isEmpty) {
            return Center(
              child: feed.error != null
                  ? Padding(
                      padding: const EdgeInsets.all(32),
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          const Icon(Icons.cloud_off, color: Colors.white38, size: 48),
                          const SizedBox(height: 16),
                          const Text(
                            'Could not load videos',
                            style: TextStyle(color: Colors.white, fontSize: 18),
                          ),
                          const SizedBox(height: 8),
                          Text(
                            feed.error!,
                            textAlign: TextAlign.center,
                            style: const TextStyle(color: Color(0xFF8E8E93), fontSize: 13),
                          ),
                          const SizedBox(height: 16),
                          ElevatedButton(
                            onPressed: () => context.read<FeedProvider>().loadInitialFeed(),
                            child: const Text('Retry'),
                          ),
                        ],
                      ),
                    )
                  : const Text('No lessons available', style: TextStyle(color: Color(0xFF8E8E93))),
            );
          }

          return Stack(
            children: [
              PageView.builder(
                controller: _pageController,
                scrollDirection: Axis.vertical,
                itemCount: feed.lessons.length,
                onPageChanged: (index) {
                  feed.setIndex(index);
                  if (index >= feed.lessons.length - 2) {
                    feed.loadMore();
                  }
                },
                itemBuilder: (context, index) {
                  final lesson = feed.lessons[index];
                  return LessonCard(lesson: lesson);
                },
              ),
              Positioned(
                left: 0,
                right: 0,
                top: 0,
                child: _TikTokTopChrome(
                  current: feed.currentIndex + 1,
                  total: feed.lessons.length,
                ),
              ),
            ],
          );
        },
      ),
    );
  }
}

class _TikTokTopChrome extends StatelessWidget {
  final int current;
  final int total;

  const _TikTokTopChrome({required this.current, required this.total});

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      bottom: false,
      child: Padding(
        padding: const EdgeInsets.fromLTRB(16, 8, 14, 0),
        child: Row(
          children: [
            SizedBox(
              width: 42,
              child: Text(
                '$current/$total',
                style: const TextStyle(
                  color: Color(0xCCFFFFFF),
                  fontSize: 12,
                  fontWeight: FontWeight.w700,
                  shadows: [Shadow(color: Colors.black, blurRadius: 8)],
                ),
              ),
            ),
            const Expanded(
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    'Following',
                    style: TextStyle(
                      color: Color(0x99FFFFFF),
                      fontSize: 16,
                      fontWeight: FontWeight.w700,
                      shadows: [Shadow(color: Colors.black, blurRadius: 8)],
                    ),
                  ),
                  SizedBox(width: 18),
                  Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(
                        'For You',
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 17,
                          fontWeight: FontWeight.w800,
                          shadows: [Shadow(color: Colors.black, blurRadius: 8)],
                        ),
                      ),
                      SizedBox(height: 4),
                      SizedBox(
                        width: 22,
                        height: 3,
                        child: DecoratedBox(
                          decoration: BoxDecoration(
                            color: Colors.white,
                            borderRadius: BorderRadius.all(Radius.circular(2)),
                          ),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
            const SizedBox(
              width: 42,
              child: Align(
                alignment: Alignment.centerRight,
                child: Icon(Icons.search, color: Colors.white, size: 26),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
