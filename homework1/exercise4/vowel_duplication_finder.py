#!/usr/bin/env python3
"""
Exercise 4: Vowel Duplication Finder

This script finds words with duplicated vowels (a,e,i,o,u) in the blog corpus.
It's designed to identify spelling variations used for emphasis online, such as
"reeeeaaallllyyyy?!".

Author: NLP Course Exercise
Tool: Python with regular expressions
"""

import re
import os
import glob
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Set


class VowelDuplicationFinder:
    """Finds and analyzes vowel duplications in text files."""

    def __init__(self, corpus_path: str):
        """
        Initialize the vowel duplication finder.

        Args:
            corpus_path: Path to the directory containing blog text files
        """
        self.corpus_path = corpus_path
        self.vowels = 'aeiou'

        # Common English words with natural double vowels to exclude
        self.common_words = {
            'good', 'been', 'see', 'too', 'feel', 'school', 'need', 'look',
            'week', 'keep', 'cool', 'took', 'looking', 'soon', 'sleep', 'room',
            'seems', 'feeling', 'free', 'three', 'you', 'out', 'about', 'really',
            'your', 'would', 'people', 'going', 'our', 'because', 'their', 'could',
            'again', 'said', 'being', 'beautiful', 'seeing', 'seriously', 'serious',
            'obviously', 'quiet', 'previous', 'beauty', 'various', 'obvious',
            'religious', 'hilarious', 'precious', 'queen', 'delicious', 'gorgeous'
        }

        # Regular expression patterns for vowel duplication (with inline case-insensitive flag)
        # Pattern 1: Emphatic duplications - 3+ identical vowels (clearly for emphasis)
        self.emphatic_identical_pattern = r'(?i)\b\w*([aeiou])\1{2,}\w*\b'

        # Pattern 2: Multiple vowel sequences in one word (mixed emphasis)
        self.mixed_emphasis_pattern = r'(?i)\b\w{1,20}(?:[aeiou]{2,}.*[aeiou]{2,})\w{0,20}\b'

        # Pattern 3: Long vowel sequences (4+ vowels, regardless of type)
        self.long_vowel_pattern = r'(?i)\b\w*[aeiou]{4,}\w*\b'

        # Pattern 4: Repeated vowel pairs (like "aaaa", "eeee", "oooo")
        self.repeated_pairs_pattern = r'(?i)\b\w*([aeiou])\1{3,}\w*\b'

        self.results = {
            'emphatic_identical': defaultdict(list),
            'mixed_emphasis': defaultdict(list),
            'long_vowels': defaultdict(list),
            'repeated_pairs': defaultdict(list)
        }

    def get_regex_explanations(self) -> Dict[str, str]:
        """
        Return explanations of the regular expression patterns used.

        Returns:
            Dictionary with pattern names and their explanations
        """
        return {
            'emphatic_identical_pattern': (
                r'(?i)\b\w*([aeiou])\1{2,}\w*\b - Finds words with 3+ consecutive identical vowels (clear emphasis).\n'
                r'  (?i) = inline case-insensitive flag\n'
                r'  \b = word boundary\n'
                r'  \w* = zero or more word characters before\n'
                r'  ([aeiou]) = capture group for a vowel (matches both upper and lowercase due to (?i))\n'
                r'  \1{2,} = two or more additional repetitions of the captured vowel (3+ total)\n'
                r'  \w* = zero or more word characters after\n'
                r'  \b = word boundary'
            ),
            'mixed_emphasis_pattern': (
                r'(?i)\b\w{1,20}(?:[aeiou]{2,}.*[aeiou]{2,})\w{0,20}\b - Finds words with multiple vowel duplications.\n'
                r'  (?i) = inline case-insensitive flag\n'
                r'  \w{1,20} = 1-20 word characters (prevents matching entire paragraphs)\n'
                r'  (?:...) = non-capturing group\n'
                r'  [aeiou]{2,}.*[aeiou]{2,} = vowel duplication, any chars, another vowel duplication'
            ),
            'long_vowel_pattern': (
                r'(?i)\b\w*[aeiou]{4,}\w*\b - Finds words with 4+ consecutive vowels (extreme emphasis).\n'
                r'  (?i) = inline case-insensitive flag\n'
                r'  [aeiou]{4,} = any vowel sequence of 4 or more characters'
            ),
            'repeated_pairs_pattern': (
                r'(?i)\b\w*([aeiou])\1{3,}\w*\b - Finds words with 4+ identical consecutive vowels.\n'
                r'  (?i) = inline case-insensitive flag\n'
                r'  ([aeiou])\1{3,} = a vowel followed by 3+ more of the same (4+ total identical vowels)'
            )
        }

    def find_duplications_in_text(self, text: str, filename: str) -> None:
        """
        Find vowel duplications in a single text string.

        Args:
            text: The text to search
            filename: Name of the file being processed (for tracking)
        """
        # Patterns now use (?i) inline flag, so no need for text.lower() or re.IGNORECASE

        # Pattern 1: Emphatic identical vowels (3+ consecutive identical vowels)
        for match in re.finditer(self.emphatic_identical_pattern, text):
            word = match.group(0).lower()  # Still lowercase for consistent storage
            # Filter out common English words and very long matches (likely paragraphs)
            if word not in self.common_words and len(word) <= 30:
                self.results['emphatic_identical'][word].append(filename)

        # Pattern 2: Mixed emphasis (multiple vowel duplications in same word)
        for match in re.finditer(self.mixed_emphasis_pattern, text):
            word = match.group(0).lower()  # Still lowercase for consistent storage
            # Ensure it's not a common word and not too long (to avoid paragraphs)
            if word not in self.common_words and len(word) <= 30:
                # Additional check to ensure it actually has multiple duplications
                vowel_sequences = re.findall(r'(?i)[aeiou]{2,}', word)
                if len(vowel_sequences) >= 2:
                    self.results['mixed_emphasis'][word].append(filename)

        # Pattern 3: Long vowel sequences (4+ consecutive vowels)
        for match in re.finditer(self.long_vowel_pattern, text):
            word = match.group(0).lower()  # Still lowercase for consistent storage
            if word not in self.common_words and len(word) <= 30:
                self.results['long_vowels'][word].append(filename)

        # Pattern 4: Repeated pairs (4+ identical consecutive vowels)
        for match in re.finditer(self.repeated_pairs_pattern, text):
            word = match.group(0).lower()  # Still lowercase for consistent storage
            if word not in self.common_words and len(word) <= 30:
                self.results['repeated_pairs'][word].append(filename)

    def process_corpus(self) -> None:
        """Process all text files in the corpus directory."""
        pattern = os.path.join(self.corpus_path, '*.txt')
        files = glob.glob(pattern)

        print(f"Processing {len(files)} files from {self.corpus_path}")

        processed_count = 0
        for filepath in files:
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                    text = file.read()
                    filename = os.path.basename(filepath)
                    self.find_duplications_in_text(text, filename)
                    processed_count += 1

                    if processed_count % 100 == 0:
                        print(f"Processed {processed_count} files...")

            except Exception as e:
                print(f"Error processing {filepath}: {e}")

        print(f"Completed processing {processed_count} files.")

    def print_results(self) -> None:
        """Print the analysis results."""
        print("\n" + "="*80)
        print("VOWEL DUPLICATION ANALYSIS RESULTS")
        print("="*80)

        # Print regex explanations
        print("\nREGULAR EXPRESSION PATTERNS USED:")
        print("-"*50)
        for pattern_name, explanation in self.get_regex_explanations().items():
            print(f"\n{pattern_name}:")
            print(explanation)

        # Print results for each category
        categories = [
            ('emphatic_identical', 'Emphatic Identical Vowels (3+ consecutive identical vowels)'),
            ('mixed_emphasis', 'Mixed Emphasis (multiple vowel duplications in same word)'),
            ('long_vowels', 'Long Vowel Sequences (4+ consecutive vowels)'),
            ('repeated_pairs', 'Repeated Pairs (4+ identical consecutive vowels)')
        ]

        for category_key, category_title in categories:
            print(f"\n{category_title}")
            print("-" * len(category_title))

            category_results = self.results[category_key]
            if not category_results:
                print("No matches found.")
                continue

            # Sort by frequency (number of files containing the word)
            sorted_words = sorted(category_results.items(),
                                key=lambda x: len(x[1]), reverse=True)

            print(f"Total unique words found: {len(sorted_words)}")
            print(f"Top 20 most frequent words:")

            for i, (word, files) in enumerate(sorted_words[:20]):
                file_count = len(set(files))  # Unique files
                total_occurrences = len(files)  # Total occurrences
                print(f"  {i+1:2d}. '{word}' - in {file_count} files, {total_occurrences} total occurrences")

            if len(sorted_words) > 20:
                print(f"  ... and {len(sorted_words) - 20} more words")

    def get_summary_statistics(self) -> Dict[str, int]:
        """Get summary statistics about the findings."""
        stats = {}
        for category in self.results:
            stats[f"{category}_unique_words"] = len(self.results[category])
            stats[f"{category}_total_occurrences"] = sum(len(files) for files in self.results[category].values())

        return stats


def main():
    """Main function to run the vowel duplication analysis."""
    # Path to the blog corpus
    corpus_path = "/Users/kornelovics/EIT/UT/NLP/project-nlp/homework1/assets/blogs"

    print("Exercise 4: Finding Vowel Duplications in Blog Corpus")
    print("="*60)
    print("Tool: Python with regular expressions")
    print(f"Corpus: {corpus_path}")

    # Create and run the finder
    finder = VowelDuplicationFinder(corpus_path)
    finder.process_corpus()
    finder.print_results()

    # Print summary statistics
    stats = finder.get_summary_statistics()
    print(f"\n{'='*80}")
    print("SUMMARY STATISTICS")
    print("="*80)
    for stat_name, stat_value in stats.items():
        print(f"{stat_name}: {stat_value}")


if __name__ == "__main__":
    main()
