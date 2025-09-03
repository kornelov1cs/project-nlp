import os
import re
import glob
from collections import defaultdict

# Regex pattern to match words with 2+ consecutive identical vowels
VOWEL_DUPLICATION_PATTERN = r'\b\w*([aeiouAEIOU])\1{1,}\w*\b'

def clean_word(word):
    """
    Clean word by removing punctuation and URLs, keeping only letters.
    """
    # Remove urlLink patterns and other non-letter characters
    word = re.sub(r'urlLink|[^a-zA-Z]', '', word)
    return word

def process_text_files(directory_path):
    """
    Process all .txt files in the given directory and find words with excessive vowel duplication.
    """
    results = defaultdict(set)  # Use set to avoid duplicates
    total_files = 0
    total_words_checked = 0
    total_duplicates_found = 0

    # Get all .txt files in the directory
    txt_files = glob.glob(os.path.join(directory_path, "*.txt"))

    print(f"Processing {len(txt_files)} text files...")
    print("-" * 60)

    for file_path in txt_files:
        total_files += 1
        filename = os.path.basename(file_path)

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()

            # Find all words with vowel duplications using regex
            duplicated_words = [match.group() for match in re.finditer(VOWEL_DUPLICATION_PATTERN, content)]

            # Clean and process the matches
            for word in duplicated_words:
                cleaned_word = clean_word(word)
                if len(cleaned_word) > 2:  # Only check words with more than 2 letters
                    results[filename].add(cleaned_word)
                    total_duplicates_found += 1

            # Count total words for statistics
            total_words_checked += len(content.split())

            if duplicated_words:
                print(f"📁 {filename}: {len(set(duplicated_words))} unique words with vowel duplications found")

        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")

    return results, total_files, total_words_checked, total_duplicates_found

def display_results(results, total_files, total_words_checked, total_duplicates_found):
    """
    Display the results in a formatted way.
    """
    print("\n" + "="*80)
    print("🔍 VOWEL DUPLICATION ANALYSIS RESULTS")
    print("="*80)

    if not results:
        print("✅ No excessive vowel duplications found in any files!")
        return

    # Count total unique words across all files
    all_words = set()
    for words in results.values():
        all_words.update(words)

    print(f"\n📊 SUMMARY:")
    print(f"   • Files processed: {total_files}")
    print(f"   • Words analyzed: {total_words_checked:,}")
    print(f"   • Files with duplications: {len(results)}")
    print(f"   • Total unique words with duplications: {len(all_words)}")
    print(f"   • Total duplicate instances found: {total_duplicates_found}")

    print(f"\n📝 DETAILED FINDINGS:")
    print("-" * 60)

    for filename, words in results.items():
        print(f"\n🗂️  FILE: {filename}")
        print(f"   Words with vowel duplications ({len(words)} unique):")

        # Sort words for consistent display
        sorted_words = sorted(words)
        for word in sorted_words:
            # Show which vowel patterns are found
            vowel_matches = re.findall(r'([aeiouAEIOU])\1{1,}', word)
            if vowel_matches:
                unique_vowels = list(set(v.lower() for v in vowel_matches))
                print(f"   └── '{word}' (vowels: {', '.join(unique_vowels)})")
            else:
                print(f"   └── '{word}'")

    print(f"\n💡 REGEX PATTERN USED:")
    print(f"   • Pattern: {VOWEL_DUPLICATION_PATTERN}")
    print(f"   • Finds words with 2+ consecutive identical vowels")
    print(f"   • Examples: 'cool', 'reeeeaaallllyyyy', 'sooooooo', 'WOOOHOOOOO'")

def main():
    """
    Main function to run the vowel duplication finder.
    """
    # Get the directory path (current directory where script is located)
    script_dir = os.path.dirname(os.path.abspath(__file__))

    print("🎯 Vowel Duplication Finder")
    print(f"📂 Searching in: {script_dir}")
    print("🔍 Looking for words with 2+ consecutive identical vowels...")
    print()

    # Process all text files
    results, total_files, total_words_checked, total_duplicates_found = process_text_files(script_dir)

    # Display results
    display_results(results, total_files, total_words_checked, total_duplicates_found)

    print(f"\n✨ Analysis complete!")

if __name__ == "__main__":
    main()
