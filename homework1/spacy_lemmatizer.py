import spacy
import subprocess
import sys

def download_spacy_model(model_name):
    """Download spaCy model if not already installed"""
    try:
        subprocess.check_call([sys.executable, "-m", "spacy", "download", model_name])
        print(f"Successfully downloaded {model_name}")
    except subprocess.CalledProcessError:
        print(f"Failed to download {model_name}")
        sys.exit(1)

# Load SpaCy English model (auto-download if needed)
model_name = "en_core_web_sm"
try:
    nlp = spacy.load(model_name)
    print(f"Loaded {model_name} model")
except OSError:
    print(f"Model {model_name} not found. Downloading...")
    download_spacy_model(model_name)
    nlp = spacy.load(model_name)
    print(f"Successfully loaded {model_name} model")

# Read input words
with open("assets/sorted_types_HW1.txt", "r", encoding="utf-8") as f:
    words = [line.strip() for line in f if line.strip()]

print(f"Original words: {len(words)}")

# Lemmatize with SpaCy
lemmatized = []
lema_pairs = []

for word in words:
    doc = nlp(word)
    token = doc[0]
    lemma = token.lemma_
    lemmatized.append(lemma)
    lema_pairs.append((word, lemma, token.pos_))

# Count unique lemmas
unique_lemmas = set(lemmatized)
print(f"Unique lemmas after SpaCy lemmatization: {len(unique_lemmas)}")

# Show examples where lemmas differ
changed = [(orig, lem) for orig, lem, _ in lema_pairs if orig != lem]
print(f"Words that changed: {len(changed)}")

# Print first 20 results
print("\nFirst 20 lemmatization results:")
print(f"{'Original':15} {'Lemma':15} {'POS Tag':10}")
print("-" * 45)
for i in range(20):
    print(f"{words[i]:15} {lemmatized[i]:15} {lema_pairs[i][2]:10}")
