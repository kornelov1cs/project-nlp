#!/usr/bin/env python3
"""
Exercise 4b: Refined Vowel-Specific Duplication Analysis

This script analyzes emphatic vowel duplications (3+ consecutive identical vowels)
and provides the top 3 most frequent word types for each vowel (a,e,i,o,u).

Author: NLP Course Exercise
"""

import re
import os
import glob
from collections import defaultdict, Counter
from typing import Dict, List, Tuple
import json


class RefinedVowelAnalyzer:
    """Analyzes emphatic vowel duplications by individual vowel."""

    def __init__(self, corpus_path: str):
        """
        Initialize the analyzer.

        Args:
            corpus_path: Path to the directory containing blog text files
        """
        self.corpus_path = corpus_path
        self.vowels = ['a', 'e', 'i', 'o', 'u']

        # Dictionary to store word types by vowel
        # Structure: {vowel: {base_word: total_frequency}}
        self.vowel_word_frequencies = {vowel: defaultdict(int) for vowel in self.vowels}

        # Words to exclude from analysis
        self.exclude_words = {
            'invisiblenodetrexample'
        }

    def extract_base_word_and_vowel(self, emphatic_word: str) -> Tuple[str, str]:
        """
        Extract base word and identify which vowel is duplicated for emphatic words.

        Args:
            emphatic_word: Word containing emphatic vowel duplications (3+ consecutive)

        Returns:
            Tuple of (base_word, duplicated_vowel) or None if no clear pattern
        """
        # Find emphatic duplications (3+ consecutive identical vowels)
        for vowel in self.vowels:
            pattern = f'({vowel})\\1{{2,}}'  # 3+ consecutive identical vowels
            match = re.search(pattern, emphatic_word, re.IGNORECASE)

            if match:
                # Replace the emphatic sequence with single vowel to get base word
                base_word = re.sub(pattern, vowel, emphatic_word, flags=re.IGNORECASE)
                return (base_word.lower(), vowel)

        return None

    def find_emphatic_duplications_in_text(self, text: str) -> None:
        """
        Find emphatic vowel duplications in text (3+ consecutive identical vowels).

        Args:
            text: The text to search
        """
        # Use same pattern as 4a: emphatic duplications with 3+ consecutive identical vowels
        pattern = r'(?i)\b\w*([aeiou])\1{2,}\w*\b'

        for match in re.finditer(pattern, text):
            word = match.group(0).lower()

            # Filter out excluded words and very long matches
            if len(word) <= 30 and word not in self.exclude_words:
                result = self.extract_base_word_and_vowel(word)

                if result:
                    base_word, duplicated_vowel = result
                    # Only count if there was actual emphatic duplication and base word is not excluded
                    if base_word != word and base_word not in self.exclude_words:
                        self.vowel_word_frequencies[duplicated_vowel][base_word] += 1
    def process_corpus(self) -> None:
        """Process all text files in the corpus directory."""
        pattern = os.path.join(self.corpus_path, '*.txt')
        files = glob.glob(pattern)

        print(f"Processing {len(files)} files from {self.corpus_path}")
        print("Analyzing emphatic vowel duplications by individual vowel...")

        processed_count = 0
        for filepath in files:
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                    text = file.read()
                    self.find_emphatic_duplications_in_text(text)
                    processed_count += 1

                    if processed_count % 100 == 0:
                        print(f"Processed {processed_count} files...")

            except Exception as e:
                print(f"Error processing {filepath}: {e}")

        print(f"Completed processing {processed_count} files.")

    def get_top_3_for_each_vowel(self) -> Dict[str, List[Tuple[str, int]]]:
        """
        Get top 3 most frequent word types for each vowel.

        Returns:
            Dictionary with vowel as key and list of (word, frequency) tuples as value
        """
        results = {}

        for vowel in self.vowels:
            # Sort by frequency (descending) and take top 3
            sorted_words = sorted(
                self.vowel_word_frequencies[vowel].items(),
                key=lambda x: x[1],
                reverse=True
            )
            results[vowel] = sorted_words[:3]

        return results

    def find_example_duplications(self, base_word: str, vowel: str, max_examples: int = 3) -> List[str]:
        """
        Find example emphatic duplications for a base word.

        Args:
            base_word: The base word to find examples for
            vowel: The vowel that gets duplicated
            max_examples: Maximum number of examples to return

        Returns:
            List of example duplicated forms
        """
        examples = set()
        pattern = os.path.join(self.corpus_path, '*.txt')
        files = glob.glob(pattern)

        # Search through files to find examples
        for filepath in files[:50]:  # Check first 50 files for efficiency
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                    text = file.read()

                    # Look for emphatic duplications
                    duplication_pattern = r'(?i)\b\w*([aeiou])\1{2,}\w*\b'
                    for match in re.finditer(duplication_pattern, text):
                        word = match.group(0).lower()
                        if word not in self.exclude_words:
                            result = self.extract_base_word_and_vowel(word)
                            if result:
                                bw, v = result
                                if bw == base_word and v == vowel and bw not in self.exclude_words:
                                    examples.add(word)
                                    if len(examples) >= max_examples:
                                        return list(examples)

            except Exception:
                continue

        return list(examples)

    def print_results(self) -> None:
        """Print the analysis results for 4b."""
        print("\n" + "="*80)
        print("EXERCISE 4B: TOP 3 WORD TYPES BY EMPHATIC VOWEL DUPLICATION")
        print("="*80)
        print("Note: Only analyzing emphatic duplications (3+ consecutive identical vowels)")

        top_3_results = self.get_top_3_for_each_vowel()

        for vowel in self.vowels:
            print(f"\nVowel '{vowel.upper()}' - Top 3 most frequent word types with '{vowel}' duplication:")
            print("-" * 65)

            if not top_3_results[vowel]:
                print("  No word types found with this vowel duplication.")
                continue

            for i, (base_word, frequency) in enumerate(top_3_results[vowel], 1):
                print(f"  {i}. '{base_word}' - {frequency} total occurrences")

                # Show some examples of the duplicated forms
                examples = self.find_example_duplications(base_word, vowel)
                if examples:
                    example_str = ", ".join(f"'{ex}'" for ex in sorted(examples))
                    print(f"     Examples: {example_str}")

            # Show total statistics for this vowel
            total_word_types = len(self.vowel_word_frequencies[vowel])
            total_occurrences = sum(self.vowel_word_frequencies[vowel].values())
            print(f"  Total word types with '{vowel}' duplication: {total_word_types}")
            print(f"  Total occurrences: {total_occurrences}")

    def save_results_to_file(self, output_file: str) -> None:
        """Save results to a JSON file for further analysis."""
        top_3_results = self.get_top_3_for_each_vowel()

        # Convert to serializable format with examples
        results_dict = {}
        for vowel, word_list in top_3_results.items():
            results_dict[vowel] = []
            for word, freq in word_list:
                examples = self.find_example_duplications(word, vowel)
                results_dict[vowel].append({
                    "word": word,
                    "frequency": freq,
                    "examples": examples
                })

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results_dict, f, indent=2, ensure_ascii=False)

        print(f"\nResults saved to {output_file}")


def main():
    """Main function to run the refined vowel-specific analysis for 4b."""
    # Path to the blog corpus
    corpus_path = "/Users/kornelovics/EIT/UT/NLP/project-nlp/homework1/assets/blogs"

    print("Exercise 4b: Refined Vowel-Specific Duplication Analysis")
    print("="*65)
    print(f"Corpus: {corpus_path}")

    # Create and run the analyzer
    analyzer = RefinedVowelAnalyzer(corpus_path)
    analyzer.process_corpus()
    analyzer.print_results()

    # Save results to file
    output_file = "/Users/kornelovics/EIT/UT/NLP/project-nlp/homework1/exercise4/exercise4b_refined_results.json"
    analyzer.save_results_to_file(output_file)


if __name__ == "__main__":
    main()
