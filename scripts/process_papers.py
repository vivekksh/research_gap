# from pathlib import Path
# import fitz  # PyMuPDF
# import re
# import nltk

# nltk.download("punkt", quiet=True)

# # ---------------- CONFIG ----------------
# PAPERS_DIR = Path("data/papers")
# OUTPUT_FILE = Path("output/all_limitations.txt")

# LIMITATION_CUES = (
#     "limitation", "challenge", "problem", "issue",
#     "difficult", "fails", "cannot", "unable",
#     "insufficient", "lack", "trade-off",
#     "concern", "risk", "drawback",
#     "future work", "remains", "still", "yet"
# )

# MIN_SENTENCE_WORDS = 10


# # ---------------- TEXT CLEANING ----------------
# def extract_text_from_pdf(pdf_path: Path) -> str:
#     doc = fitz.open(pdf_path)
#     text = []
#     for page in doc:
#         text.append(page.get_text("text"))
#     return "\n".join(text)


# def reconstruct_paragraphs(text: str) -> str:
#     """
#     Merge broken PDF lines into coherent paragraphs.
#     This is the MOST important step for trust.
#     """
#     lines = text.split("\n")
#     paragraphs = []
#     buffer = ""

#     for line in lines:
#         line = line.strip()

#         if not line:
#             if buffer:
#                 paragraphs.append(buffer.strip())
#                 buffer = ""
#             continue

#         # join lines unless previous ends sentence
#         if buffer and not buffer.endswith((".", "?", "!", ":")):
#             buffer += " " + line
#         else:
#             buffer += " " + line

#     if buffer:
#         paragraphs.append(buffer.strip())

#     return "\n\n".join(paragraphs)


# def clean_text(text: str) -> str:
#     text = re.sub(r"-\s+", "", text)  # fix hyphen splits
#     text = re.sub(r"\s+", " ", text)
#     return text.strip()


# # ---------------- SENTENCE FILTERING ----------------
# def looks_complete(sentence: str) -> bool:
#     if len(sentence.split()) < MIN_SENTENCE_WORDS:
#         return False
#     if sentence.endswith(("such as", "including", "and", "or", "in")):
#         return False
#     if sentence.isupper():
#         return False
#     return True


# def is_limitation_sentence(sentence: str) -> bool:
#     s = sentence.lower()
#     return any(cue in s for cue in LIMITATION_CUES)


# # ---------------- MAIN PIPELINE ----------------
# def main():
#     OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

#     all_limitations = []

#     for pdf in PAPERS_DIR.glob("*.pdf"):
#         print(f"Processing: {pdf.name}")

#         raw_text = extract_text_from_pdf(pdf)
#         paragraphs = reconstruct_paragraphs(raw_text)
#         paragraphs = clean_text(paragraphs)

#         sentences = nltk.sent_tokenize(paragraphs)

#         for sent in sentences:
#             sent = sent.strip()

#             if looks_complete(sent) and is_limitation_sentence(sent):
#                 all_limitations.append(sent)

#     with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
#         for s in all_limitations:
#             f.write(s + "\n")

#     print(f"\n✅ Extracted {len(all_limitations)} high-quality limitation statements")
#     print(f"Saved to {OUTPUT_FILE}")


# if __name__ == "__main__":
#     main()



# scripts/process_papers.py

import os
import fitz  # PyMuPDF
import nltk

# Download tokenizer safely (Streamlit compatible)
nltk.download("punkt", quiet=True)


def process_papers(papers_dir: str, output_file: str):
    """
    Extracts text from PDFs, reconstructs paragraphs,
    and writes clean sentences to a file.
    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    all_sentences = []

    for filename in os.listdir(papers_dir):
        if not filename.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(papers_dir, filename)
        doc = fitz.open(pdf_path)

        full_text = ""
        for page in doc:
            full_text += page.get_text("text") + "\n"

        sentences = nltk.sent_tokenize(full_text)
        for s in sentences:
            s = s.strip()
            if len(s.split()) >= 6:  # basic quality filter
                all_sentences.append(s)

    with open(output_file, "w", encoding="utf-8") as f:
        for s in all_sentences:
            f.write(s + "\n")
