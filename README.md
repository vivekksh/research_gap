# LOOPX  
### Literature-Oriented Open Problem Explorer

LOOPX is an AI-based research assistant that automatically discovers
persistent research gaps and open problems from academic literature.

---

## 🔍 What LOOPX Does
- Extracts limitation and challenge statements from research papers
- Cleans and reconstructs academic text for reliability
- Groups recurring unresolved issues using semantic clustering
- Presents evidence-backed research gaps in a clear, interpretable format
- Handles low-data and edge cases conservatively (no hallucination)

---

## 🧠 Why LOOPX is Different
- Evidence-driven (no invented gaps)
- Conservative by design
- Domain-agnostic
- Researcher-trust focused

---

## ⚙️ Tech Stack
- Python
- Sentence Transformers
- Scikit-learn
- PyMuPDF
- NLTK
- Streamlit

---

## 🚀 How to Run

```bash
# create venv
python -m venv venv
venv\Scripts\activate

# install dependencies
pip install -r requirements.txt

# run UI
streamlit run app.py
