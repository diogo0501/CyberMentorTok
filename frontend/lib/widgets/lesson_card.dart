import 'dart:async';
import 'package:flutter/material.dart';
import 'package:video_player/video_player.dart';
import 'package:visibility_detector/visibility_detector.dart';
import '../models/lesson.dart';
import '../services/api_service.dart';

/// Plays a lesson as: a shared background video (muted, looping) with the
/// transparent mask overlay and separate lesson audio. If the mask cannot be
/// loaded, it falls back to the baked full.mp4 or, as a last resort, the old
/// native character/subtitle overlay.
class LessonCard extends StatefulWidget {
  final LessonModel lesson;

  const LessonCard({super.key, required this.lesson});

  @override
  State<LessonCard> createState() => _LessonCardState();
}

class _LessonCardState extends State<LessonCard> {
  VideoPlayerController? _bgController;
  VideoPlayerController? _maskController;
  VideoPlayerController? _audioController;
  Timer? _timer;
  bool _initializing = true;
  bool _error = false;
  bool _usingFallback = false;
  bool _visible = false;

  @override
  void initState() {
    super.initState();
    _initVideos();
  }

  Future<void> _initVideos() async {
    final bgUrl = widget.lesson.backgroundUrl;
    final maskUrl = widget.lesson.maskUrl;
    final audioUrl = widget.lesson.audioUrl;
    final fallbackUrl = widget.lesson.videoUrl;

    // Background (muted, looping) — non-blocking.
    if (bgUrl != null && bgUrl.isNotEmpty) {
      _loadBackground(bgUrl);
    }

    // Preferred mode: separate audio + transparent mask overlay.
    if (audioUrl != null && audioUrl.isNotEmpty) {
      final audio = VideoPlayerController.networkUrl(
        Uri.parse(ApiService.resolveUrl(audioUrl)),
      );
      _audioController = audio;
      try {
        await audio.initialize();
        await audio.setVolume(1);
        await audio.setLooping(false);
        _usingFallback = false;
        if (maskUrl != null && maskUrl.isNotEmpty) {
          unawaited(_loadMask(maskUrl));
        }
        if (mounted) {
          setState(() => _initializing = false);
          _maybePlay();
        }
        return;
      } catch (e) {
        _audioController = null;
      }
    }

    // Fallback: baked full video (single layer with audio).
    if (fallbackUrl != null && fallbackUrl.isNotEmpty) {
      final fb = VideoPlayerController.networkUrl(
        Uri.parse(ApiService.resolveUrl(fallbackUrl)),
      );
      _audioController = fb;
      try {
        await fb.initialize();
        await fb.setLooping(true);
        await fb.setVolume(1);
        _usingFallback = true;
        if (mounted) {
          setState(() => _initializing = false);
          _maybePlay();
        }
        return;
      } catch (e) {
        _audioController = null;
      }
    }

    if (mounted) {
      setState(() {
        _initializing = false;
        _error = true;
      });
    }
  }

  Future<void> _loadBackground(String bgUrl) async {
    final bg = VideoPlayerController.networkUrl(
      Uri.parse(ApiService.resolveUrl(bgUrl)),
    );
    _bgController = bg;
    try {
      await bg.initialize();
      await bg.setLooping(true);
      await bg.setVolume(0); // audio comes from the separate track
      if (mounted) {
        setState(() {});
        _maybePlay();
      }
    } catch (_) {
      _bgController = null;
    }
  }

  Future<void> _loadMask(String maskUrl) async {
    final mask = VideoPlayerController.networkUrl(
      Uri.parse(ApiService.resolveUrl(maskUrl)),
    );
    _maskController = mask;
    try {
      await mask.initialize();
      await mask.setLooping(false);
      await mask.setVolume(0);
      if (mounted) {
        setState(() {});
        _maybePlay();
      }
    } catch (_) {
      _maskController?.dispose();
      _maskController = null;
    }
  }

  @override
  void dispose() {
    _timer?.cancel();
    _timer = null;
    _bgController?.dispose();
    _bgController = null;
    _maskController?.dispose();
    _maskController = null;
    _audioController?.dispose();
    _audioController = null;
    super.dispose();
  }

  void _onVisibilityChanged(VisibilityInfo info) {
    if (!mounted) return;
    final visible = info.visibleFraction >= 0.8;
    _visible = visible;
    if (visible) {
      _play();
    } else if (info.visibleFraction <= 0.2) {
      _pause();
    }
  }

  /// Start playback once we're on screen AND the controllers are initialized.
  /// The visibility callback can fire before initialization finishes, so each
  /// init path calls this to (re)start playback when it becomes ready.
  void _maybePlay() {
    if (mounted && _visible) _play();
  }

  void _play() {
    if (!mounted) return;
    final bg = _bgController;
    if (bg != null && bg.value.isInitialized && !bg.value.isPlaying) {
      bg.play();
    }
    final mask = _maskController;
    if (mask != null && mask.value.isInitialized && !mask.value.isPlaying) {
      mask.play();
    }
    final audio = _audioController;
    if (audio != null && audio.value.isInitialized && !audio.value.isPlaying) {
      audio.play();
    }
    _timer?.cancel();
    _timer = Timer.periodic(const Duration(milliseconds: 120), (_) {
      if (mounted) setState(() {});
    });
  }

  void _pause() {
    _timer?.cancel();
    _timer = null;
    if (!mounted) return;
    final bg = _bgController;
    if (bg != null && bg.value.isInitialized && bg.value.isPlaying) {
      bg.pause();
    }
    final mask = _maskController;
    if (mask != null && mask.value.isInitialized && mask.value.isPlaying) {
      mask.pause();
    }
    final audio = _audioController;
    if (audio != null && audio.value.isInitialized && audio.value.isPlaying) {
      audio.pause();
    }
  }

  /// The timing entry active at the current audio position (or null).
  Map<String, dynamic>? get _currentLine {
    final audio = _audioController;
    if (audio == null || !audio.value.isInitialized) return null;
    final pos = audio.value.position.inMilliseconds / 1000.0;
    for (final t in widget.lesson.timing) {
      final start = (t['start_s'] as num?)?.toDouble() ?? 0;
      final end = (t['end_s'] as num?)?.toDouble() ?? 0;
      if (pos >= start && pos <= end) return t;
    }
    return null;
  }

  Widget _video(VideoPlayerController? controller) {
    if (controller == null) return const SizedBox.shrink();
    final size = controller.value.size;
    return SizedBox.expand(
      child: FittedBox(
        fit: BoxFit.cover,
        child: SizedBox(
          width: size.width > 0 ? size.width : 1080,
          height: size.height > 0 ? size.height : 1920,
          child: VideoPlayer(controller),
        ),
      ),
    );
  }

  bool get _showMaskOverlay =>
      !_usingFallback && _maskController != null && _maskController!.value.isInitialized;

  @override
  Widget build(BuildContext context) {
    return VisibilityDetector(
      key: Key('lesson_video_${widget.lesson.id}'),
      onVisibilityChanged: _onVisibilityChanged,
      child: Container(
        width: double.infinity,
        height: double.infinity,
        color: Colors.black,
        child: Stack(
          fit: StackFit.expand,
          children: [
            // Hidden audio track (separate audio mode) — the VideoPlayer widget
            // MUST be in the tree for its HTML element to exist on Flutter web,
            // otherwise the audio never plays. Rendered first (behind the full
            // screen background) at 1x1 so it's covered. No Opacity wrapper:
            // HtmlElementViews are dropped when composited with opacity on web.
            if (!_usingFallback &&
                _audioController != null &&
                _audioController!.value.isInitialized)
              Positioned(
                left: 0,
                top: 0,
                child: SizedBox(
                  width: 1,
                  height: 1,
                  child: VideoPlayer(_audioController!),
                ),
              ),
            // Background video (muted, looping)
            if (_bgController != null && _bgController!.value.isInitialized)
              _video(_bgController),
            // Fallback: baked full video
            if (_usingFallback &&
                _audioController != null &&
                _audioController!.value.isInitialized)
              _video(_audioController),

            if (_showMaskOverlay) _video(_maskController),

            // Bottom gradient for caption readability.
            Positioned(
              left: 0,
              right: 0,
              bottom: 0,
              child: Container(
                height: 260,
                decoration: const BoxDecoration(
                  gradient: LinearGradient(
                    begin: Alignment.topCenter,
                    end: Alignment.bottomCenter,
                    colors: [Colors.transparent, Color(0x66000000), Colors.black],
                  ),
                ),
              ),
            ),
            Positioned(
              left: 0,
              right: 0,
              top: 0,
              child: Container(
                height: 120,
                decoration: const BoxDecoration(
                  gradient: LinearGradient(
                    begin: Alignment.topCenter,
                    end: Alignment.bottomCenter,
                    colors: [Color(0x77000000), Colors.transparent],
                  ),
                ),
              ),
            ),

            if (_initializing)
              const Center(child: CircularProgressIndicator(color: Colors.white)),
            if (_error) _buildBackgroundPattern(),

            // Native character + subtitle overlay only if the mask could not load.
            if (!_usingFallback && !_showMaskOverlay) _buildOverlay(),

            _buildSidebar(),
            _buildCaption(),
          ],
        ),
      ),
    );
  }

  /// TikTok-style right sidebar (difficulty badge, likes, comments, share, save).
  Widget _buildSidebar() {
    final lesson = widget.lesson;
    return Positioned(
      right: 10,
      bottom: 132 + MediaQuery.of(context).padding.bottom,
      child: Column(
        children: [
          Stack(
            clipBehavior: Clip.none,
            alignment: Alignment.center,
            children: [
              Container(
                width: 50,
                height: 50,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  border: Border.all(color: Colors.white, width: 2),
                  gradient: const LinearGradient(
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                    colors: [Color(0xFF25F4EE), Color(0xFFFE2C55)],
                  ),
                ),
                child: Center(
                  child: Text(
                    lesson.difficultyLabel.substring(0, 1),
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 18,
                      fontWeight: FontWeight.w900,
                      shadows: [Shadow(color: Colors.black, blurRadius: 4)],
                    ),
                  ),
                ),
              ),
              Positioned(
                bottom: -7,
                child: Container(
                  width: 20,
                  height: 20,
                  decoration: BoxDecoration(
                    color: const Color(0xFFFE2C55),
                    shape: BoxShape.circle,
                    border: Border.all(color: Colors.black, width: 2),
                  ),
                  child: const Icon(Icons.add, color: Colors.white, size: 14),
                ),
              ),
            ],
          ),
          const SizedBox(height: 20),
          _sidebarIcon(Icons.favorite, '${_formatCount(lesson.totalWatches)}'),
          const SizedBox(height: 18),
          _sidebarIcon(Icons.mode_comment, '${(lesson.averageCompletion * 100).toInt()}%'),
          const SizedBox(height: 18),
          _sidebarIcon(Icons.bookmark, 'Save'),
          const SizedBox(height: 18),
          _sidebarIcon(Icons.reply, 'Share'),
          const SizedBox(height: 18),
          _spinningDisc(),
        ],
      ),
    );
  }

  Widget _spinningDisc() {
    return Container(
      width: 46,
      height: 46,
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        gradient: const SweepGradient(
          colors: [Color(0xFF111111), Color(0xFF4A4A4A), Color(0xFF111111)],
        ),
        border: Border.all(color: const Color(0x66FFFFFF), width: 1),
        boxShadow: const [BoxShadow(color: Color(0x80000000), blurRadius: 10)],
      ),
      child: Center(
        child: Container(
          width: 16,
          height: 16,
          decoration: const BoxDecoration(
            color: Color(0xFFE8E8E8),
            shape: BoxShape.circle,
          ),
        ),
      ),
    );
  }

  Widget _sidebarIcon(IconData icon, String label) {
    return SizedBox(
      width: 58,
      child: Column(
        children: [
          Icon(
            icon,
            color: Colors.white,
            size: 32,
            shadows: const [Shadow(color: Colors.black, blurRadius: 8)],
          ),
          const SizedBox(height: 4),
          Text(
            label,
            maxLines: 1,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 11,
              fontWeight: FontWeight.w800,
              shadows: [Shadow(color: Colors.black, blurRadius: 6)],
            ),
            overflow: TextOverflow.ellipsis,
          ),
        ],
      ),
    );
  }

  /// TikTok-style bottom caption (concept name, lesson title, hook, difficulty).
  Widget _buildCaption() {
    final lesson = widget.lesson;
    return Positioned(
      left: 14,
      right: 78,
      bottom: 86 + MediaQuery.of(context).padding.bottom,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            '@${lesson.concept ?? lesson.conceptId}',
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 16,
              fontWeight: FontWeight.w800,
              shadows: [Shadow(color: Colors.black, blurRadius: 8)],
            ),
          ),
          const SizedBox(height: 6),
          Text(
            lesson.title,
            maxLines: 2,
            overflow: TextOverflow.ellipsis,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 15,
              height: 1.25,
              fontWeight: FontWeight.w600,
              shadows: [Shadow(color: Colors.black, blurRadius: 8)],
            ),
          ),
          if (lesson.hook != null && lesson.hook!.isNotEmpty) ...[
            const SizedBox(height: 6),
            Text(
              lesson.hook!,
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
              style: const TextStyle(
                color: Color(0xE6FFFFFF),
                fontSize: 14,
                height: 1.25,
                shadows: [Shadow(color: Colors.black, blurRadius: 8)],
              ),
            ),
          ],
          const SizedBox(height: 10),
          ClipRRect(
            borderRadius: BorderRadius.circular(14),
            child: Container(
              height: 28,
              padding: const EdgeInsets.symmetric(horizontal: 10),
              color: const Color(0x33FFFFFF),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Icon(Icons.music_note, color: Colors.white, size: 14),
                  const SizedBox(width: 6),
                  Flexible(
                    child: Text(
                      '${lesson.difficultyLabel} - Cyber lesson',
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 12,
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  /// Renders the active speaker's character + the subtitle, synced to audio.
  Widget _buildOverlay() {
    final line = _currentLine;
    if (line == null) return const SizedBox.shrink();

    final speaker = (line['speaker']?.toString() ?? '').toLowerCase();
    final text = line['text']?.toString() ?? '';
    final isPeter = speaker.contains('peter');
    final charPath = isPeter ? '/characters/peter.png' : '/characters/stewie.png';

    return Stack(
      children: [
        // Subtitle
        Positioned(
          left: 24,
          right: 24,
          top: MediaQuery.of(context).size.height * 0.40,
          child: Text(
            text,
            textAlign: TextAlign.center,
            style: TextStyle(
              color: Colors.white,
              fontSize: 36,
              fontWeight: FontWeight.w800,
              height: 1.25,
              shadows: List.generate(
                4,
                (i) => Shadow(color: Colors.black, blurRadius: 2, offset: Offset(0, 0)),
              ),
            ),
          ),
        ),
        // Character
        Positioned(
          left: isPeter ? 16 : null,
          right: isPeter ? null : 16,
          bottom: 150,
          child: Image.network(
            ApiService.resolveUrl(charPath),
            width: MediaQuery.of(context).size.width * 0.39,
            fit: BoxFit.contain,
            errorBuilder: (_, __, ___) => const SizedBox.shrink(),
          ),
        ),
      ],
    );
  }

  Widget _buildBackgroundPattern() {
    return Center(
      child: Container(
        width: 200,
        height: 200,
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          border: Border.all(color: Colors.green.withOpacity(0.2), width: 2),
        ),
        child: Icon(
          Icons.security,
          size: 80,
          color: Colors.green.withOpacity(0.15),
        ),
      ),
    );
  }

  String _formatCount(int count) {
    if (count >= 1000000) return '${(count / 1000000).toStringAsFixed(1)}M';
    if (count >= 1000) return '${(count / 1000).toStringAsFixed(1)}K';
    return count.toString();
  }
}
