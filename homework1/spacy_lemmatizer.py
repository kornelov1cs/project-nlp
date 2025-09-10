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

# Save results to file
output_filename = "assets/spacy_lemmatized_results.txt"
with open(output_filename, "w", encoding="utf-8") as output_file:
    # Write header to both console and file
    header = "{0:20}{1:20}".format("--Original--", "--Lemma--")
    print(f"\n{header}")
    output_file.write(header + "\n")

    # Write all lemmatization results (without POS tag)
    for word, lemma in zip(words, lemmatized):
        line = "{0:20}{1:20}".format(word, lemma)
        print(line)
        output_file.write(line + "\n")

    # Write summary to file
    output_file.write(f"\nTotal rows: {len(words)}\n")
    output_file.write(f"Unique lemmas: {len(unique_lemmas)}\n")

# Print summary
print(f"\nTotal rows: {len(words)}")
print(f"Unique lemmas: {len(unique_lemmas)}")
print(f"Results saved to: {output_filename}")

# Print the list of unique lemmatized words
print(f"\nList of unique lemmatized words:")
print("-" * 40)
sorted_unique_lemmas = sorted(unique_lemmas)
for i, lemma in enumerate(sorted_unique_lemmas, 1):
    print(f"{i:4}. {lemma}")

# Show examples where lemmas differ
changed = [(orig, lem) for orig, lem, _ in lema_pairs if orig != lem]
print(f"\nWords that changed: {len(changed)}")
