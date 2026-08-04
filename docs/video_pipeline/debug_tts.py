import asyncio
import edge_tts

async def main():
    c = edge_tts.Communicate("Hello world, this is a test.", "en-US-GuyNeural", rate="+50%")
    types_seen = set()
    words = []
    async for chunk in c.stream():
        t = chunk["type"]
        types_seen.add(t)
        if t == "WordBoundary":
            words.append(chunk)
            print(f"  WordBoundary: offset={chunk['offset']} dur={chunk['duration']} text='{chunk['text']}'")
        elif t == "Metadata":
            pass
    print(f"\nTypes seen: {types_seen}")
    print(f"Total words: {len(words)}")

asyncio.run(main())
