import sys
import fitz  # PyMuPDF

def extract_text_with_style_and_spacing(pdf_path):
    doc = fitz.open(pdf_path) # type: ignore
    output_text = ""

    for page in doc:
        blocks = page.get_text("blocks")
        blocks.sort(key=lambda block: (block[1], block[0]))  # sort by y, then x coordinates

        for block in blocks:
            block_text = block[4].strip()

            if block_text:
                output_text += block_text + "\n"

    return output_text

if __name__ == "__main__":
    pdf_path = sys.argv[1]
    extracted_text = extract_text_with_style_and_spacing(pdf_path)

    with open("output.txt", "w", encoding="utf-8") as output_file:
        output_file.write(extracted_text)
