import nltk

# Download required NLTK resources if not already present
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')

# Read words from the file
with open("assets/sorted_types_HW1.txt", "r", encoding="utf-8") as f:
    words = [line.strip() for line in f if line.strip()]

# Get POS tags for each word
tagged_words = nltk.pos_tag(words)

# Print only the first 20 words with their POS tags
print("{0:15}{1:10}{2:10}".format("Word", "POS Tag", "First letter of POS tag"))
print("-" * 25)
for word, tag in tagged_words[:20]:
    print("{0:15}{1:10}{2:10}".format(word, tag, tag[0]))
