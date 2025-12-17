import fitz  # PyMuPDF
from pathlib import Path

PDF_PATH = Path("data/papers/sample.pdf")
OUTPUT_PATH = Path("output/sample_text.txt")

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def main():
    text = extract_text_from_pdf(PDF_PATH)
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(text)
    print("✅ Text extracted successfully!")
    print(f"Saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
