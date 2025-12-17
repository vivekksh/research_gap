from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from collections import Counter, defaultdict
import re
import json

# ---------------- CONFIG ----------------
INPUT_PATH = Path("output/all_limitations.txt")
TEXT_OUTPUT = Path("output/gap_results.txt")
JSON_OUTPUT = Path("output/gap_results.json")

NUM_CLUSTERS = 6
MIN_WORDS = 10
MIN_CLUSTER_SIZE = 3

# Conceptual mapping for gap titles
CONCEPT_MAP = {
    "attention": "Attention Noise and Context Management",
    "context": "Long-Context Understanding Limitations",
    "bert": "Encoder Architecture Limitations",
    "encoder": "Encoder Architecture Limitations",
    "scaling": "Performance Saturation with Scaling",
    "scale": "Performance Saturation with Scaling",
    "compute": "Computational Inefficiency",
    "data": "Data Inefficiency and Bias",
    "training": "Training Cost and Data Dependence",
    "prompt": "Limitations of Prompt-Based Methods",
    "reasoning": "Reasoning and Generalization Failures",
    "evaluation": "Evaluation and Benchmarking Gaps",
    "hallucination": "Hallucination and Reliability Issues"
}

NEGATIVE_CUES = (
    "limitation", "challenge", "difficult", "fails",
    "cannot", "unable", "insufficient", "problem",
    "issue", "inefficient", "lack", "trade-off",
    "concern", "risk", "drawback", "costly",
    "expensive", "bias", "unclear", "open problem",
    "future work", "remains", "still", "yet"
)

# ---------------- HELPERS ----------------
def repair_sentence(s: str) -> str:
    s = s.replace("-\n", "")
    s = re.sub(r"\s+", " ", s).strip()
    if s and s[0].islower():
        s = s[0].upper() + s[1:]
    return s


def is_valid_limitation(s: str) -> bool:
    if len(s.split()) < MIN_WORDS:
        return False
    if s.upper() == s:
        return False
    if not any(cue in s.lower() for cue in NEGATIVE_CUES):
        return False
    if len(re.findall(r"[a-zA-Z]", s)) < 15:
        return False
    return True


def load_sentences(path):
    sentences = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = repair_sentence(line.strip())
            if not line:
                continue
            if is_valid_limitation(line):
                sentences.append(line)
    return sentences


def infer_gap_title(sentences):
    text = " ".join(sentences).lower()
    for key, title in CONCEPT_MAP.items():
        if key in text:
            return title
    words = re.findall(r"[a-zA-Z]{5,}", text)
    common = [w for w, _ in Counter(words).most_common(3)]
    return " ".join(common).title()


def generate_description(title, freq):
    return (
        f"This research gap represents a recurring unresolved challenge related to **{title}**. "
        f"It is supported by **{freq} limitation statement(s)** extracted from the literature. "
        "While evidence is limited, the issue indicates a potential direction for future research."
    )

# ---------------- MAIN ----------------
def main():
    sentences = load_sentences(INPUT_PATH)

    # ---------- EDGE CASE: VERY LOW DATA ----------
    if len(sentences) < 2:
        print("⚠️ Very limited limitation evidence detected.")
        print("⚠️ Skipping clustering and generating a conservative single-gap report.")

        title = infer_gap_title(sentences)
        desc = generate_description(title, len(sentences))

        with open(TEXT_OUTPUT, "w", encoding="utf-8") as f:
            f.write("AUTOMATICALLY DISCOVERED RESEARCH GAPS\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"GAP 1: {title}\n")
            f.write("-" * 60 + "\n")
            f.write(desc + "\n\n")
            f.write("Representative Evidence:\n")
            for s in sentences:
                f.write(f"- {s}\n")

        with open(JSON_OUTPUT, "w", encoding="utf-8") as jf:
            json.dump([{
                "gap_id": 1,
                "title": title,
                "description": desc,
                "frequency": len(sentences),
                "evidence": sentences
            }], jf, indent=2)

        print("✅ Conservative single-gap report generated.")
        return

    # ---------- NORMAL PIPELINE ----------
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(sentences)

    n_clusters = min(NUM_CLUSTERS, max(2, len(sentences) // 2))
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(embeddings)

    clusters = defaultdict(list)
    for sent, label in zip(sentences, labels):
        clusters[label].append(sent)

    results = []

    with open(TEXT_OUTPUT, "w", encoding="utf-8") as f:
        f.write("AUTOMATICALLY DISCOVERED RESEARCH GAPS\n")
        f.write("=" * 60 + "\n\n")

        gap_id = 1
        for sents in clusters.values():
            if len(sents) < MIN_CLUSTER_SIZE:
                continue

            title = infer_gap_title(sents)
            desc = generate_description(title, len(sents))

            f.write(f"GAP {gap_id}: {title}\n")
            f.write("-" * 60 + "\n")
            f.write(desc + "\n\n")
            f.write("Representative Evidence:\n")
            for s in sents[:5]:
                f.write(f"- {s}\n")
            f.write("\n\n")

            results.append({
                "gap_id": gap_id,
                "title": title,
                "description": desc,
                "frequency": len(sents),
                "evidence": sents[:5]
            })

            gap_id += 1

    with open(JSON_OUTPUT, "w", encoding="utf-8") as jf:
        json.dump(results, jf, indent=2)

    print("✅ Research-gap analysis completed successfully.")


if __name__ == "__main__":
    main()
