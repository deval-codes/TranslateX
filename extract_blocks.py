import fitz  # PyMuPDF

def extract_text_blocks(pdf_path):
    doc = fitz.open(pdf_path)
    blocks = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        raw_blocks = page.get_text("dict")["blocks"]

        for b in raw_blocks:
            if "lines" not in b:
                continue
            for line in b["lines"]:
                for span in line["spans"]:
                    block = {
                        "page": page_num,
                        "text": span["text"],
                        "bbox": span["bbox"],
                        "font": span["font"],
                        "size": span["size"],
                        "color": span["color"],  # RGB as integer
                        "flags": span["flags"],  # style flag (e.g., bold, italic)
                    }
                    blocks.append(block)
    
    doc.close()
    return blocks
