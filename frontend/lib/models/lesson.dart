import 'package:flutter/material.dart';

class LessonModel {
  final String id;
  final String conceptId;
  final String title;
  final String slug;
  final String? description;
  final int difficulty;
  final String? hook;
  final String? problem;
  final String? explanation;
  final String? realWorldExample;
  final String? summary;
  final String? curiosityHook;
  final List<DialogueLine> dialogue;
  final List<String> learningObjectives;
  final List<QuizQuestion> quizQuestions;
  final int estimatedDurationSeconds;
  final bool aiGenerated;
  final double? aiConfidence;
  final bool approved;
  final int totalWatches;
  final double averageCompletion;
  final String? videoUrl;
  final String? maskUrl;
  final String? audioUrl;
  final String? backgroundUrl;
  final List<Map<String, dynamic>> timing;
  final String? thumbnailUrl;
  final String? concept;
  final String? conceptSlug;
  final String? category;

  LessonModel({
    required this.id,
    required this.conceptId,
    required this.title,
    required this.slug,
    this.description,
    required this.difficulty,
    this.hook,
    this.problem,
    this.explanation,
    this.realWorldExample,
    this.summary,
    this.curiosityHook,
    required this.dialogue,
    required this.learningObjectives,
    required this.quizQuestions,
    required this.estimatedDurationSeconds,
    required this.aiGenerated,
    this.aiConfidence,
    required this.approved,
    required this.totalWatches,
    required this.averageCompletion,
    this.videoUrl,
    this.maskUrl,
    this.audioUrl,
    this.backgroundUrl,
    this.timing = const [],
    this.thumbnailUrl,
    this.concept,
    this.conceptSlug,
    this.category,
  });

  factory LessonModel.fromJson(Map<String, dynamic> json) {
    return LessonModel(
      id: json['id'],
      conceptId: json['concept_id'],
      title: json['title'],
      slug: json['slug'],
      description: json['description'],
      difficulty: json['difficulty'] ?? 1,
      hook: json['hook'],
      problem: json['problem'],
      explanation: json['explanation'],
      realWorldExample: json['real_world_example'],
      summary: json['summary'],
      curiosityHook: json['curiosity_hook'],
      dialogue: (json['dialogue'] as List? ?? [])
          .map((d) => DialogueLine.fromJson(d))
          .toList(),
      learningObjectives: List<String>.from(json['learning_objectives'] ?? []),
      quizQuestions: (json['quiz_questions'] as List? ?? [])
          .map((q) => QuizQuestion.fromJson(q))
          .toList(),
      estimatedDurationSeconds: json['estimated_duration_seconds'] ?? 90,
      aiGenerated: json['ai_generated'] ?? false,
      aiConfidence: json['ai_confidence']?.toDouble(),
      approved: json['approved'] ?? false,
      totalWatches: json['total_watches'] ?? 0,
      averageCompletion: (json['average_completion'] ?? 0.0).toDouble(),
      videoUrl: json['video_url'],
      maskUrl: json['mask_url'],
      audioUrl: json['audio_url'],
      backgroundUrl: json['background_url'],
      timing: (json['timing'] as List? ?? [])
          .whereType<Map<String, dynamic>>()
          .toList(),
      thumbnailUrl: json['thumbnail_url'],
      concept: json['concept'],
      conceptSlug: json['concept_slug'],
      category: json['category'],
    );
  }

  String get difficultyLabel {
    switch (difficulty) {
      case 1: return 'Beginner';
      case 2: return 'Elementary';
      case 3: return 'Intermediate';
      case 4: return 'Advanced';
      case 5: return 'Expert';
      case 6: return 'Master';
      default: return 'Unknown';
    }
  }

  Color get difficultyColor {
    switch (difficulty) {
      case 1: return Colors.green;
      case 2: return Colors.teal;
      case 3: return Colors.blue;
      case 4: return Colors.orange;
      case 5: return Colors.red;
      case 6: return Colors.purple;
      default: return Colors.grey;
    }
  }
}

class DialogueLine {
  final String speaker;
  final String text;

  DialogueLine({required this.speaker, required this.text});

  factory DialogueLine.fromJson(Map<String, dynamic> json) {
    return DialogueLine(
      speaker: json['speaker'],
      text: json['text'],
    );
  }

  bool get isStewie => speaker == 'Stewie';
  bool get isPeter => speaker == 'Peter';
}

class QuizQuestion {
  final String question;
  final List<QuizAnswer> answers;
  final String? explanation;

  QuizQuestion({
    required this.question,
    required this.answers,
    this.explanation,
  });

  factory QuizQuestion.fromJson(Map<String, dynamic> json) {
    return QuizQuestion(
      question: json['question'],
      answers: (json['answers'] as List)
          .map((a) => QuizAnswer.fromJson(a))
          .toList(),
      explanation: json['explanation'],
    );
  }
}

class QuizAnswer {
  final String id;
  final String text;
  final bool correct;

  QuizAnswer({
    required this.id,
    required this.text,
    required this.correct,
  });

  factory QuizAnswer.fromJson(Map<String, dynamic> json) {
    return QuizAnswer(
      id: json['id'],
      text: json['text'],
      correct: json['correct'] ?? false,
    );
  }
}
