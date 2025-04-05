import fitz

def rebuild_pdf(input_pdf, translated_blocks, output_pdf):
    doc = fitz.open(input_pdf)

    for block in translated_blocks:
        page = doc[block["page"]]
        x0, y0, x1, y1 = block["bbox"]
        rect = fitz.Rect(x0, y0, x1, y1)

        # White out the original text
        page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))

        # Extract styling (with fallback defaults)
        fontname = block.get("font", "helv")
        fontsize = block.get("size", 10)
        color = tuple(block.get("color", (0, 0, 0)))  # RGB
        alignment = block.get("align", "left")
        text = block["translated_text"]

        # Compute x-position based on alignment
        text_width = fitz.get_text_length(text, fontname=fontname, fontsize=fontsize)
        if alignment == "center":
            x = (x0 + x1) / 2 - text_width / 2
        elif alignment == "right":
            x = x1 - text_width
        else:  # left or unknown
            x = x0

        # Insert translated text at adjusted position
        page.insert_text(
            fitz.Point(x, y0),
            text,
            fontsize=fontsize,
            fontname=fontname,
            color=color,
        )

    doc.save(output_pdf)
    doc.close()
    print(f"✅ Saved translated PDF to {output_pdf}")
