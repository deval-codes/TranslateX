from extract_blocks import extract_text_blocks # type: ignore
from translate_pdf import translate_blocks
from rebuild_pdf_with_translations import rebuild_pdf
from translate_pdf import save_json

SOURCE_PDF = "sample_invoice.pdf"
OUTPUT_PDF = "translated_invoice_french.pdf"

print("🔍 Extracting...")
blocks = extract_text_blocks(SOURCE_PDF)
save_json(blocks, "blocks_raw.json")


print("🌐 Translating...")
translated_blocks = translate_blocks(blocks, target_lang="French")

save_json(translated_blocks, "blocks_translated.json")


print("🛠️ Rebuilding PDF...")
rebuild_pdf(SOURCE_PDF, translated_blocks, OUTPUT_PDF)
