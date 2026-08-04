import copy
import re


def _clean(text):
    return " ".join(str(text or "").replace("\n", " ").split())


def _sentences(text, limit=4):
    cleaned = _clean(text)
    if not cleaned:
        return []
    parts = re.split(r"(?<=[.!?])\s+", cleaned)
    results = []
    for part in parts:
        part = part.strip(" -")
        if not part:
            continue
        words = part.split()
        if len(words) > 28:
            part = " ".join(words[:28]).rstrip(",;:") + "."
        results.append(part)
        if len(results) >= limit:
            break
    merged = []
    for part in results:
        if merged and len(merged[-1].split()) < 6:
            merged[-1] = f"{merged[-1].rstrip('.')}." + f" {part}"
        else:
            merged.append(part)
    return merged[:limit]


def _objectives_text(objectives):
    items = []
    for item in objectives or []:
        cleaned = _clean(item).rstrip(".")
        if not cleaned:
            continue
        items.append(cleaned[:1].lower() + cleaned[1:])
    if not items:
        return ""
    if len(items) == 1:
        return items[0] + "."
    if len(items) == 2:
        return f"{items[0]}, and {items[1]}."
    return f"{items[0]}, {items[1]}, and {items[2]}."


def _opening_question(title):
    title = _clean(title)
    if not title:
        return "What am I really supposed to understand here?"
    return f'I keep hearing "{title}". What am I really supposed to understand here?'


def _hook_answer(lesson):
    for key in ("hook", "description", "summary"):
        value = _clean(lesson.get(key))
        if value:
            return value
    return "This topic matters because it changes how you design, defend, and explain security decisions."


def _problem_answer(lesson):
    value = _clean(lesson.get("problem"))
    if value:
        return value
    return "Teams usually struggle because the concept sounds simple until it collides with real systems, real tradeoffs, and real attackers."


def _summary_answer(lesson):
    for key in ("summary", "curiosity_hook", "description"):
        value = _clean(lesson.get(key))
        if value:
            return value
    return "The important thing is not memorizing the label but understanding the design logic behind it."


def _example_answer(lesson):
    value = _clean(lesson.get("real_world_example"))
    if value:
        return value
    return ""


def _concept_points(lesson):
    points = _sentences(lesson.get("explanation"), limit=4)
    if points:
        return points
    fallback = []
    for key in ("description", "summary"):
        fallback.extend(_sentences(lesson.get(key), limit=2))
    return fallback[:3]


def build_lesson_dialogue(lesson):
    points = _concept_points(lesson)
    objectives = _objectives_text(lesson.get("learning_objectives"))
    example = _example_answer(lesson)

    dialogue = [
        {"speaker": "Peter", "text": _opening_question(lesson.get("title"))},
        {"speaker": "Stewie", "text": _hook_answer(lesson)},
        {"speaker": "Peter", "text": "What problem does this solve in the real world, not just in exam language?"},
        {"speaker": "Stewie", "text": _problem_answer(lesson)},
    ]

    prompt_cycle = [
        "Break the core idea down for me. What is first thing to get straight?",
        "Okay, but what is particular technical detail that people usually miss?",
        "How does that change the way you actually design or operate systems?",
        "Where do teams usually get this wrong when they try to apply it?",
    ]

    for index, point in enumerate(points[:4]):
        dialogue.append({"speaker": "Peter", "text": prompt_cycle[index]})
        dialogue.append({"speaker": "Stewie", "text": point})

    if example:
        dialogue.append({"speaker": "Peter", "text": "Can you anchor that in concrete example so I can remember it?"})
        dialogue.append({"speaker": "Stewie", "text": example})

    if objectives:
        dialogue.append({"speaker": "Peter", "text": "If I really learned this lesson, what should I be able to explain back to you?"})
        dialogue.append({"speaker": "Stewie", "text": f"By end, you should be able to {objectives}"})

    dialogue.append({"speaker": "Peter", "text": "So what is takeaway I should keep in my head when this topic comes up again?"})
    dialogue.append({"speaker": "Stewie", "text": _summary_answer(lesson)})

    return dialogue


def rewrite_lessons_dialogues(lessons):
    rewritten = []
    for lesson in lessons:
        updated = copy.deepcopy(lesson)
        updated["dialogue"] = build_lesson_dialogue(updated)
        rewritten.append(updated)
    return rewritten
