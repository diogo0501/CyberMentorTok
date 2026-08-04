// Basic smoke test for the CyberMentorTok app shell.

import 'package:flutter_test/flutter_test.dart';

import 'package:cybermentortok/main.dart';

void main() {
  testWidgets('App builds without crashing', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(const CyberMentorTokApp());

    // The MaterialApp should be present.
    expect(find.byType(CyberMentorTokApp), findsOneWidget);
  });
}
