import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

# Download required resources
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger_eng')

def get_wordnet_pos(word):
    """Map POS tag to WordNet POS format"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)

# Initialize lemmatizer
wnl = WordNetLemmatizer()

# Read input file
with open("assets/sorted_types_HW1.txt", "r", encoding="utf-8") as f:
    words = [line.strip() for line in f if line.strip()]

print(f"Original words: {len(words)}")

# Perform lemmatization with automatic POS tagging
lemmatized_words = []
lemmatization_pairs = []

for word in words:
    pos = get_wordnet_pos(word)  # Get correct POS automatically
    lemma = wnl.lemmatize(word, pos)
    lemmatized_words.append(lemma)
    lemmatization_pairs.append((word, lemma))

# Count unique lemmas
unique_lemmas = set(lemmatized_words)
print(f"Unique lemmas after lemmatization: {len(unique_lemmas)}")

# Show examples of changes
changed_words = [(orig, lemma) for orig, lemma in lemmatization_pairs if orig != lemma]
print(f"Words that changed: {len(changed_words)}")

# Print first 20 lemmatization results
print("\nFirst 20 lemmatization results:")
print("{0:15}{1:15}{2:10}".format("Original", "Lemma", "POS Tag"))
print("-" * 40)
for i in range(20):
    word = words[i]
    lemma = lemmatized_words[i]
    pos_tag = nltk.pos_tag([word])[0][1]
    print("{0:15}{1:15}{2:10}".format(word, lemma, pos_tag))
