#!/usr/bin/env python3
"""
Exercise 4c: Gender-Separated Vowel-Specific Duplication Analysis

This script analyzes emphatic vowel duplications (3+ consecutive identical vowels)
separately for male and female bloggers, and provides the top 3 most frequent
word types for each vowel (a,e,i,o,u) by gender.

Female blogger files start with 'F-', male blogger files start with 'M-'.

Author: NLP Course Exercise
"""

import re
import os
import glob
from collections import defaultdict, Counter
from typing import Dict, List, Tuple
import json


class GenderSeparatedVowelAnalyzer:
    """Analyzes emphatic vowel duplications by individual vowel, separated by blogger gender."""

    def __init__(self, corpus_path: str):
        """
        Initialize the analyzer.

        Args:
            corpus_path: Path to the directory containing blog text files
        """
        self.corpus_path = corpus_path
        self.vowels = ['a', 'e', 'i', 'o', 'u']

        # Dictionary to store word types by vowel and gender
        # Structure: {gender: {vowel: {base_word: total_frequency}}}
        self.vowel_word_frequencies = {
            'female': {vowel: defaultdict(int) for vowel in self.vowels},
            'male': {vowel: defaultdict(int) for vowel in self.vowels}
        }

        # Words to exclude from analysis
        self.exclude_words = {
            'invisiblenodetrexample'
        }

        # Statistics tracking
        self.file_counts = {'female': 0, 'male': 0, 'unknown': 0}

    def get_gender_from_filename(self, filepath: str) -> str:
        """
        Determine blogger gender from filename.

        Args:
            filepath: Path to the blog file

        Returns:
            'female', 'male', or 'unknown'
        """
        filename = os.path.basename(filepath)
        if filename.startswith('F-'):
            return 'female'
        elif filename.startswith('M-'):
            return 'male'
        else:
            return 'unknown'

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

    def find_emphatic_duplications_in_text(self, text: str, gender: str) -> None:
        """
        Find emphatic vowel duplications in text (3+ consecutive identical vowels).

        Args:
            text: The text to search
            gender: The gender of the blogger ('female' or 'male')
        """
        # Use same pattern as 4b: emphatic duplications with 3+ consecutive identical vowels
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
                        self.vowel_word_frequencies[gender][duplicated_vowel][base_word] += 1

    def process_corpus(self) -> None:
        """Process all text files in the corpus directory, separating by gender."""
        pattern = os.path.join(self.corpus_path, '*.txt')
        files = glob.glob(pattern)

        print(f"Processing {len(files)} files from {self.corpus_path}")
        print("Analyzing emphatic vowel duplications by gender and individual vowel...")

        processed_count = 0
        for filepath in files:
            try:
                gender = self.get_gender_from_filename(filepath)

                if gender == 'unknown':
                    self.file_counts['unknown'] += 1
                    continue  # Skip files that don't match F- or M- pattern

                self.file_counts[gender] += 1

                with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                    text = file.read()
                    self.find_emphatic_duplications_in_text(text, gender)
                    processed_count += 1

                    if processed_count % 100 == 0:
                        print(f"Processed {processed_count} files...")

            except Exception as e:
                print(f"Error processing {filepath}: {e}")

        print(f"Completed processing {processed_count} files.")
        print(f"Female bloggers: {self.file_counts['female']} files")
        print(f"Male bloggers: {self.file_counts['male']} files")
        if self.file_counts['unknown'] > 0:
            print(f"Unknown gender: {self.file_counts['unknown']} files (skipped)")

    def get_top_3_for_each_vowel_by_gender(self) -> Dict[str, Dict[str, List[Tuple[str, int]]]]:
        """
        Get top 3 most frequent word types for each vowel by gender.

        Returns:
            Dictionary with gender as key, then vowel as key, and list of (word, frequency) tuples as value
        """
        results = {}

        for gender in ['female', 'male']:
            results[gender] = {}
            for vowel in self.vowels:
                # Sort by frequency (descending) and take top 3
                sorted_words = sorted(
                    self.vowel_word_frequencies[gender][vowel].items(),
                    key=lambda x: x[1],
                    reverse=True
                )
                results[gender][vowel] = sorted_words[:3]

        return results

    def find_example_duplications(self, base_word: str, vowel: str, gender: str, max_examples: int = 3) -> List[str]:
        """
        Find example emphatic duplications for a base word in specified gender's files.

        Args:
            base_word: The base word to find examples for
            vowel: The vowel that gets duplicated
            gender: The gender to search in ('female' or 'male')
            max_examples: Maximum number of examples to return

        Returns:
            List of example duplicated forms
        """
        examples = set()
        pattern = os.path.join(self.corpus_path, '*.txt')
        files = glob.glob(pattern)

        # Filter files by gender
        gender_files = [f for f in files if self.get_gender_from_filename(f) == gender]

        # Search through files to find examples
        for filepath in gender_files[:25]:  # Check first 25 files of this gender for efficiency
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
        """Print the analysis results for 4c."""
        print("\n" + "="*80)
        print("EXERCISE 4C: TOP 3 WORD TYPES BY EMPHATIC VOWEL DUPLICATION - BY GENDER")
        print("="*80)
        print("Note: Only analyzing emphatic duplications (3+ consecutive identical vowels)")
        print("Female bloggers: files starting with 'F-'")
        print("Male bloggers: files starting with 'M-'")

        top_3_results = self.get_top_3_for_each_vowel_by_gender()

        for gender in ['female', 'male']:
            print(f"\n{'='*60}")
            print(f"RESULTS FOR {gender.upper()} BLOGGERS ({self.file_counts[gender]} files)")
            print(f"{'='*60}")

            for vowel in self.vowels:
                print(f"\nVowel '{vowel.upper()}' - Top 3 most frequent word types with '{vowel}' duplication:")
                print("-" * 65)

                if not top_3_results[gender][vowel]:
                    print(f"  No word types found with this vowel duplication.")
                    continue

                for i, (base_word, frequency) in enumerate(top_3_results[gender][vowel], 1):
                    print(f"  {i}. '{base_word}' - {frequency} total occurrences")

                    # Show some examples of the duplicated forms
                    examples = self.find_example_duplications(base_word, vowel, gender)
                    if examples:
                        example_str = ", ".join(f"'{ex}'" for ex in sorted(examples))
                        print(f"     Examples: {example_str}")

                # Show total statistics for this vowel and gender
                total_word_types = len(self.vowel_word_frequencies[gender][vowel])
                total_occurrences = sum(self.vowel_word_frequencies[gender][vowel].values())
                print(f"  Total word types with '{vowel}' duplication: {total_word_types}")
                print(f"  Total occurrences: {total_occurrences}")

    def analyze_gender_differences(self) -> None:
        """Analyze and discuss differences between male and female bloggers."""
        print("\n" + "="*80)
        print("GENDER COMPARISON ANALYSIS")
        print("="*80)

        top_3_results = self.get_top_3_for_each_vowel_by_gender()

        print(f"Dataset composition:")
        print(f"- Female bloggers: {self.file_counts['female']} files")
        print(f"- Male bloggers: {self.file_counts['male']} files")

        # Calculate overall statistics
        total_stats = {
            'female': {'word_types': 0, 'total_occurrences': 0},
            'male': {'word_types': 0, 'total_occurrences': 0}
        }

        for gender in ['female', 'male']:
            for vowel in self.vowels:
                total_stats[gender]['word_types'] += len(self.vowel_word_frequencies[gender][vowel])
                total_stats[gender]['total_occurrences'] += sum(self.vowel_word_frequencies[gender][vowel].values())

        print(f"\nOverall Statistics:")
        print(f"Female bloggers: {total_stats['female']['word_types']} unique word types, {total_stats['female']['total_occurrences']} total occurrences")
        print(f"Male bloggers: {total_stats['male']['word_types']} unique word types, {total_stats['male']['total_occurrences']} total occurrences")

        # Calculate rates per file
        if self.file_counts['female'] > 0:
            female_rate = total_stats['female']['total_occurrences'] / self.file_counts['female']
        else:
            female_rate = 0

        if self.file_counts['male'] > 0:
            male_rate = total_stats['male']['total_occurrences'] / self.file_counts['male']
        else:
            male_rate = 0

        print(f"Average emphatic duplications per file:")
        print(f"- Female bloggers: {female_rate:.2f}")
        print(f"- Male bloggers: {male_rate:.2f}")

        # Vowel-by-vowel comparison
        print(f"\nVowel-by-vowel comparison:")
        vowel_comparison = {}

        for vowel in self.vowels:
            female_total = sum(self.vowel_word_frequencies['female'][vowel].values())
            male_total = sum(self.vowel_word_frequencies['male'][vowel].values())

            vowel_comparison[vowel] = {
                'female': female_total,
                'male': male_total,
                'diff': female_total - male_total
            }

            print(f"  Vowel '{vowel}': Female={female_total}, Male={male_total}, Diff={female_total - male_total}")

        # Find most distinctive words by gender
        print(f"\nMost distinctive words by gender:")
        self._find_distinctive_words(top_3_results)

        # Discussion
        print(f"\nDISCUSSION OF FINDINGS:")
        print("-" * 40)

        if female_rate > male_rate * 1.2:
            print("• Female bloggers show significantly more emphatic vowel duplications")
        elif male_rate > female_rate * 1.2:
            print("• Male bloggers show significantly more emphatic vowel duplications")
        else:
            print("• Similar rates of emphatic vowel duplications between genders")

        # Find most emphasized vowel by gender
        max_vowel_female = max(vowel_comparison, key=lambda v: vowel_comparison[v]['female'])
        max_vowel_male = max(vowel_comparison, key=lambda v: vowel_comparison[v]['male'])

        print(f"• Most emphasized vowel by females: '{max_vowel_female}' ({vowel_comparison[max_vowel_female]['female']} occurrences)")
        print(f"• Most emphasized vowel by males: '{max_vowel_male}' ({vowel_comparison[max_vowel_male]['male']} occurrences)")

        if max_vowel_female != max_vowel_male:
            print(f"• Different vowel preferences detected between genders")
        else:
            print(f"• Both genders show similar vowel emphasis patterns")

    def _find_distinctive_words(self, top_3_results: Dict[str, Dict[str, List[Tuple[str, int]]]]) -> None:
        """Find words that appear prominently in one gender but not the other."""
        female_words = set()
        male_words = set()

        # Collect all prominent words by gender
        for vowel in self.vowels:
            for word, freq in top_3_results['female'][vowel]:
                female_words.add((word, freq))
            for word, freq in top_3_results['male'][vowel]:
                male_words.add((word, freq))

        female_only = []
        male_only = []

        # Find gender-distinctive words
        for word, freq in female_words:
            if not any(w == word for w, _ in male_words):
                female_only.append((word, freq))

        for word, freq in male_words:
            if not any(w == word for w, _ in female_words):
                male_only.append((word, freq))

        # Sort by frequency
        female_only.sort(key=lambda x: x[1], reverse=True)
        male_only.sort(key=lambda x: x[1], reverse=True)

        print("  Female-distinctive words (top 3):")
        for i, (word, freq) in enumerate(female_only[:3], 1):
            print(f"    {i}. '{word}' ({freq} occurrences)")

        print("  Male-distinctive words (top 3):")
        for i, (word, freq) in enumerate(male_only[:3], 1):
            print(f"    {i}. '{word}' ({freq} occurrences)")

    def save_results_to_file(self, output_file: str) -> None:
        """Save results to a JSON file for further analysis."""
        top_3_results = self.get_top_3_for_each_vowel_by_gender()

        # Convert to serializable format with examples
        results_dict = {
            'metadata': {
                'file_counts': self.file_counts,
                'description': 'Gender-separated emphatic vowel duplication analysis'
            },
            'results_by_gender': {}
        }

        for gender in ['female', 'male']:
            results_dict['results_by_gender'][gender] = {}
            for vowel, word_list in top_3_results[gender].items():
                results_dict['results_by_gender'][gender][vowel] = []
                for word, freq in word_list:
                    examples = self.find_example_duplications(word, vowel, gender)
                    results_dict['results_by_gender'][gender][vowel].append({
                        "word": word,
                        "frequency": freq,
                        "examples": examples
                    })

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results_dict, f, indent=2, ensure_ascii=False)

        print(f"\nResults saved to {output_file}")


def main():
    """Main function to run the gender-separated vowel-specific analysis for 4c."""
    # Path to the blog corpus
    corpus_path = "/Users/kornelovics/EIT/UT/NLP/project-nlp/homework1/assets/blogs"

    print("Exercise 4c: Gender-Separated Vowel-Specific Duplication Analysis")
    print("="*75)
    print(f"Corpus: {corpus_path}")

    # Create and run the analyzer
    analyzer = GenderSeparatedVowelAnalyzer(corpus_path)
    analyzer.process_corpus()
    analyzer.print_results()
    analyzer.analyze_gender_differences()

    # Save results to file
    output_file = "/Users/kornelovics/EIT/UT/NLP/project-nlp/homework1/exercise4/exercise4c_results.json"
    analyzer.save_results_to_file(output_file)


if __name__ == "__main__":
    main()
