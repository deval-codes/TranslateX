import google.generativeai as genai
import time
import json
from tenacity import retry, stop_after_attempt, wait_fixed

# Configure the Gemini model
genai.configure(api_key="")
model = genai.GenerativeModel("gemini-1.5-flash")

# Retry logic for robust translation
@retry(stop=stop_after_attempt(5), wait=wait_fixed(5))
def translate_text(text, target_lang="Hindi"):
    prompt = f"Translate this to {target_lang} and preserve tone, line breaks, and formatting:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text.strip()

# Translate blocks with styling info
def translate_blocks(blocks, target_lang="Hindi"):
    translated_blocks = []
    for i, block in enumerate(blocks):
        try:
            original = block["text"]
            translated = translate_text(original, target_lang)

            translated_blocks.append({
                "page": block["page"],
                "bbox": block["bbox"],
                "original": original,
                "translated_text": translated,
                "font": block.get("font", "helv"),
                "size": block.get("size", 10),
                "alignment": block.get("alignment", "left")
            })

            print(f"✅ Translated block {i + 1}/{len(blocks)}")
            time.sleep(4.5)  # ~13 requests/min limit
        except Exception as e:
            print(f"⚠️ Error at block {i}: {e}")
            translated_blocks.append({
                "page": block["page"],
                "bbox": block["bbox"],
                "original": block["text"],
                "translated_text": block["text"],
                "font": block.get("font", "helv"),
                "size": block.get("size", 10),
                "alignment": block.get("alignment", "left")
            })
    return translated_blocks

# Save output to JSON
def save_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"📦 Saved to {filename}")
