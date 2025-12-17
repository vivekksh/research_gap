import nltk
from pathlib import Path

INPUT_PATH = Path("output/sample_text.txt")
OUTPUT_PATH = Path("output/limitations.txt")

# Keywords that usually signal limitations or future work
LIMITATION_KEYWORDS = [
    "limitation",
    "limitations",
    "future work",
    "future research",
    "we leave",
    "however",
    "remains an open",
    "not addressed",
    "still challenging"
]

def extract_limitation_sentences(text):
    sentences = nltk.sent_tokenize(text)
    limitation_sentences = []

    for sent in sentences:
        sent_lower = sent.lower()
        if any(keyword in sent_lower for keyword in LIMITATION_KEYWORDS):
            limitation_sentences.append(sent.strip())

    return limitation_sentences

def main():
    text = INPUT_PATH.read_text(encoding="utf-8", errors="ignore")
    limitations = extract_limitation_sentences(text)

    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for i, sent in enumerate(limitations, 1):
            f.write(f"{i}. {sent}\n\n")

    print(f"✅ Extracted {len(limitations)} limitation sentences")
    print(f"Saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
