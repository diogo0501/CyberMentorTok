import asyncio
import edge_tts

async def main():
    c = edge_tts.Communicate("Hello world, this is a test of word boundaries.", "en-US-GuyNeural", rate="+50%")
    audio_data = b""
    all_chunks = []
    async for chunk in c.stream():
        all_chunks.append(chunk)
        if chunk["type"] == "audio":
            audio_data += chunk["data"]

    print(f"Total chunks: {len(all_chunks)}")
    for i, chunk in enumerate(all_chunks):
        if chunk["type"] != "audio":
            print(f"  [{i}] type={chunk['type']} keys={list(chunk.keys())}")
            if "text" in chunk:
                print(f"       text={chunk['text']}")
            # Print all non-audio keys
            for k, v in chunk.items():
                if k not in ("type", "data"):
                    print(f"       {k}={v}")

asyncio.run(main())
