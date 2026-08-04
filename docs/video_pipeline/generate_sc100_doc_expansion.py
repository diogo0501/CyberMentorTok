import asyncio
import hashlib
import json
import os

from generate_video import OUTPUT_DIR, generate_from_dialogue
from sc100_doc_expansion_lessons import LESSONS


REQUIRED_OUTPUTS = ("audio.mp3", "timing.json", "mask.webm")


def output_id_for_slug(slug: str) -> str:
    return hashlib.sha1(slug.encode("utf-8")).hexdigest()[:8]


def write_metadata(output_dir: str, lesson: dict) -> None:
    metadata = {
        "title": lesson["title"],
        "hook": lesson.get("hook"),
        "slug": lesson["slug"],
        "concept": lesson.get("concept_slug"),
        "category": lesson.get("category") or lesson.get("concept_slug"),
        "difficulty": lesson.get("difficulty"),
        "description": lesson.get("description"),
        "source": "SC-100 document expansion",
    }
    metadata_path = os.path.join(output_dir, "metadata.json")
    with open(metadata_path, "w", encoding="utf-8") as metadata_file:
        json.dump(metadata, metadata_file, indent=2)


def outputs_exist(output_dir: str) -> bool:
    return all(
        os.path.isfile(os.path.join(output_dir, filename))
        and os.path.getsize(os.path.join(output_dir, filename)) > 0
        for filename in REQUIRED_OUTPUTS
    )


async def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for lesson in LESSONS:
        output_id = output_id_for_slug(lesson["slug"])
        output_dir = os.path.join(OUTPUT_DIR, output_id)
        os.makedirs(output_dir, exist_ok=True)

        print(f"\n=== {lesson['title']} ({output_id}) ===")
        if outputs_exist(output_dir):
            print("Skipping existing render")
            write_metadata(output_dir, lesson)
            continue

        await generate_from_dialogue(
            dialogue=lesson["dialogue"],
            lesson_title=lesson["title"],
            output_dir=output_dir,
            mask_only=True,
        )
        write_metadata(output_dir, lesson)


if __name__ == "__main__":
    asyncio.run(main())
