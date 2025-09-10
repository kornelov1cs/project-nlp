import nltk
from nltk.stem import WordNetLemmatizer
nltk.download("wordnet")
nltk.download("omw-1.4")

# Initialize wordnet lemmatizer
wnl = WordNetLemmatizer()

# Example inflections to reduce
with open("./assets/sorted_types_HW1.txt", "r", encoding="utf-8") as f:
    example_words = [line.strip() for line in f if line.strip()]


# Sets to collect unique lemmas
unique_lemmas_v = set()
unique_lemmas_n = set()

# Open output file for writing
with open("assets/lemmatized_results.txt", "w", encoding="utf-8") as output_file:
    # Write header to both console and file
    header = "{0:20}{1:20}{2:20}".format("--Word--", "--Lemma (v)--", "--Lemma (n)--")
    print(header)
    output_file.write(header + "\n")

    # Perform lemmatization and print/write 3 columns: word -- lemma (pos=v) -- lemma (pos=n)
    for word in example_words:
        lemma_v = wnl.lemmatize(word, pos="v")
        lemma_n = wnl.lemmatize(word, pos="n")

        # Add to unique sets
        unique_lemmas_v.add(lemma_v)
        unique_lemmas_n.add(lemma_n)

        # Format the line
        line = "{0:20}{1:20}{2:20}".format(word, lemma_v, lemma_n)
        print(line)
        output_file.write(line + "\n")

    # Write summary to file
    output_file.write(f"\nTotal rows: {len(example_words)}\n")
    output_file.write(f"Unique lemmas (pos=v): {len(unique_lemmas_v)}\n")
    output_file.write(f"Unique lemmas (pos=n): {len(unique_lemmas_n)}\n")

print(f"\nTotal rows: {len(example_words)}")
print(f"Unique lemmas (pos=v): {len(unique_lemmas_v)}")
print(f"Unique lemmas (pos=n): {len(unique_lemmas_n)}")
print(f"\nResults saved to: assets/lemmatized_results.txt")
