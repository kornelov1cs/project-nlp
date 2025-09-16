#!/usr/bin/env python3
"""
Exercise 4d: Vowel Duplication Normalization using Regular Expression Substitution

This script attempts to normalize emphatic vowel duplications in the blog corpus
using regular expression substitution as described in Section 2.7.7.

The goal is to convert emphatic duplications like "sooooo" back to "so",
while documenting the challenges and problems encountered.

Author: NLP Course Exercise
"""

import re
import os
import glob
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Set
import json


class VowelNormalizationExperiment:
    """Experiments with regex-based vowel duplication normalization."""

    def __init__(self, corpus_path: str):
        """
        Initialize the normalization experiment.

        Args:
            corpus_path: Path to the directory containing blog text files
        """
        self.corpus_path = corpus_path
        self.vowels = ['a', 'e', 'i', 'o', 'u']

        # Track statistics
        self.stats = {
            'total_files_processed': 0,
            'total_substitutions': 0,
            'substitutions_by_vowel': {vowel: 0 for vowel in self.vowels},
            'problematic_cases': [],
            'before_after_examples': [],
            'unique_transformations': set()
        }

        # Different normalization strategies to try
        self.strategies = {
            'simple': self._simple_normalization,
            'conservative': self._conservative_normalization,
            'contextual': self._contextual_normalization,
            'threshold_based': self._threshold_based_normalization
        }

    def _simple_normalization(self, text: str) -> str:
        """
        Strategy 1: Simple approach - replace any 2+ consecutive vowels with single vowel.
        This will have many false positives with legitimate English words.
        """
        normalized = text
        substitution_count = 0

        for vowel in self.vowels:
            # Pattern: 2+ consecutive identical vowels
            pattern = f'({vowel})\\1+'
            # Replace with single vowel
            matches = re.findall(pattern, normalized, re.IGNORECASE)
            if matches:
                substitution_count += len(matches)
                self.stats['substitutions_by_vowel'][vowel] += len(matches)

            normalized = re.sub(pattern, vowel, normalized, flags=re.IGNORECASE)

        self.stats['total_substitutions'] += substitution_count
        return normalized

    def _conservative_normalization(self, text: str) -> str:
        """
        Strategy 2: Conservative - only normalize 3+ consecutive vowels.
        This should avoid most legitimate English words.
        """
        normalized = text
        substitution_count = 0

        for vowel in self.vowels:
            # Pattern: 3+ consecutive identical vowels
            pattern = f'({vowel})\\1{{2,}}'
            # Replace with single vowel
            matches = re.findall(pattern, normalized, re.IGNORECASE)
            if matches:
                substitution_count += len(matches)
                self.stats['substitutions_by_vowel'][vowel] += len(matches)

            normalized = re.sub(pattern, vowel, normalized, flags=re.IGNORECASE)

        self.stats['total_substitutions'] += substitution_count
        return normalized

    def _contextual_normalization(self, text: str) -> str:
        """
        Strategy 3: Contextual - only normalize within word boundaries and preserve common words.
        """
        normalized = text
        substitution_count = 0

        # Common English words with legitimate double vowels (incomplete list)
        legitimate_words = {
            'good', 'book', 'look', 'took', 'cool', 'pool', 'room', 'soon', 'moon', 'noon',
            'been', 'seen', 'keep', 'deep', 'sleep', 'meet', 'feet', 'feel', 'need', 'free',
            'tree', 'three', 'green', 'sweet', 'speed', 'agree', 'coffee'
        }

        for vowel in self.vowels:
            # Find words with 2+ consecutive vowels
            word_pattern = rf'\b\w*({vowel})\1+\w*\b'

            def replacement_func(match):
                word = match.group(0).lower()
                # Don't normalize if it's a legitimate English word
                if word in legitimate_words:
                    return match.group(0)  # Return unchanged
                else:
                    # Normalize the vowel duplication
                    inner_pattern = f'({vowel})\\1+'
                    normalized_word = re.sub(inner_pattern, vowel, word, flags=re.IGNORECASE)
                    # Track the transformation
                    if word != normalized_word:
                        self.stats['unique_transformations'].add(f"{word} -> {normalized_word}")
                        self.stats['substitutions_by_vowel'][vowel] += 1
                        nonlocal substitution_count
                        substitution_count += 1
                    return normalized_word

            normalized = re.sub(word_pattern, replacement_func, normalized, flags=re.IGNORECASE)

        self.stats['total_substitutions'] += substitution_count
        return normalized

    def _threshold_based_normalization(self, text: str) -> str:
        """
        Strategy 4: Threshold-based - normalize based on length of duplication.
        Short duplications (2-3) might be legitimate, longer ones (4+) are likely emphatic.
        """
        normalized = text
        substitution_count = 0

        for vowel in self.vowels:
            # Pattern for 4+ consecutive identical vowels (very likely emphatic)
            long_pattern = f'({vowel})\\1{{3,}}'
            matches = re.findall(long_pattern, normalized, re.IGNORECASE)
            if matches:
                substitution_count += len(matches)
                self.stats['substitutions_by_vowel'][vowel] += len(matches)
            normalized = re.sub(long_pattern, vowel, normalized, flags=re.IGNORECASE)

        self.stats['total_substitutions'] += substitution_count
        return normalized

    def analyze_original_text(self, text: str) -> Dict:
        """Analyze the original text to understand vowel duplication patterns."""
        analysis = {
            'vowel_duplications_found': [],
            'word_examples': [],
            'patterns': defaultdict(int)
        }

        # Find all words with vowel duplications
        pattern = r'(?i)\b\w*([aeiou])\1+\w*\b'

        for match in re.finditer(pattern, text):
            word = match.group(0)
            vowel = match.group(1).lower()

            analysis['vowel_duplications_found'].append({
                'word': word,
                'vowel': vowel,
                'position': match.span()
            })

            # Count pattern length
            vowel_sequence_pattern = f'({vowel})\\1+'
            vowel_matches = re.findall(vowel_sequence_pattern, word, re.IGNORECASE)
            if vowel_matches:
                sequence_match = re.search(vowel_sequence_pattern, word, re.IGNORECASE)
                if sequence_match:
                    sequence_length = len(sequence_match.group(0))
                    analysis['patterns'][f'{vowel}_{sequence_length}'] += 1

        return analysis

    def test_normalization_strategies(self, sample_text: str) -> Dict:
        """Test all normalization strategies on a sample text."""
        results = {
            'original': sample_text,
            'original_analysis': self.analyze_original_text(sample_text)
        }

        for strategy_name, strategy_func in self.strategies.items():
            # Reset stats for this strategy
            old_stats = self.stats.copy()
            self.stats['total_substitutions'] = 0
            self.stats['substitutions_by_vowel'] = {vowel: 0 for vowel in self.vowels}
            self.stats['unique_transformations'] = set()

            # Apply normalization
            normalized = strategy_func(sample_text)

            results[strategy_name] = {
                'normalized_text': normalized,
                'substitutions_made': self.stats['total_substitutions'],
                'substitutions_by_vowel': self.stats['substitutions_by_vowel'].copy(),
                'transformations': list(self.stats['unique_transformations'])
            }

            # Restore stats
            self.stats = old_stats

        return results

    def process_sample_files(self, max_files: int = 10) -> None:
        """Process a sample of files to demonstrate the normalization approaches."""
        pattern = os.path.join(self.corpus_path, '*.txt')
        files = glob.glob(pattern)[:max_files]

        print(f"Testing normalization strategies on {len(files)} sample files...")

        all_results = []

        for i, filepath in enumerate(files):
            print(f"\nProcessing file {i+1}/{len(files)}: {os.path.basename(filepath)}")

            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                    text = file.read()

                # Test all strategies on this text
                results = self.test_normalization_strategies(text)
                results['filename'] = os.path.basename(filepath)
                all_results.append(results)

                # Show a summary for this file
                original_duplications = len(results['original_analysis']['vowel_duplications_found'])
                if original_duplications > 0:
                    print(f"  Found {original_duplications} vowel duplications")
                    for strategy in ['simple', 'conservative', 'contextual', 'threshold_based']:
                        subs = results[strategy]['substitutions_made']
                        print(f"  {strategy.capitalize()} strategy: {subs} substitutions")

                        # Show some examples
                        if results[strategy]['transformations']:
                            examples = results[strategy]['transformations'][:3]
                            print(f"    Examples: {', '.join(examples)}")

            except Exception as e:
                print(f"Error processing {filepath}: {e}")

        return all_results

    def demonstrate_problems(self) -> None:
        """Demonstrate specific problems with regex normalization."""
        print("\n" + "="*80)
        print("DEMONSTRATION OF PROBLEMS WITH REGEX NORMALIZATION")
        print("="*80)

        # Test cases that highlight different problems
        test_cases = [
            {
                'name': 'Legitimate English Words',
                'text': 'I need to book a room. The coffee tastes good. I agree completely.',
                'problem': 'Simple regex would incorrectly normalize legitimate double vowels'
            },
            {
                'name': 'Mixed Emphatic and Legitimate',
                'text': 'The book was sooooo good! I totally agree with youuuu.',
                'problem': 'Need to distinguish between emphatic and legitimate duplications'
            },
            {
                'name': 'Context Dependency',
                'text': 'Coooool! vs cool temperature. Meeting at noon vs noooooo way!',
                'problem': 'Same word can be emphatic or legitimate depending on context'
            },
            {
                'name': 'Edge Cases',
                'text': 'Woooohooooo! Yeeeaaaahhh! Hmmmmmm... Arrrrgh!',
                'problem': 'Complex patterns, mixed vowels, non-standard expressions'
            },
            {
                'name': 'Capitalization and Punctuation',
                'text': 'SOOOOO excited!!! Whaaaat?!? Oh nooooo...',
                'problem': 'Case sensitivity and punctuation handling'
            }
        ]

        for i, test_case in enumerate(test_cases, 1):
            print(f"\n{i}. {test_case['name']}:")
            print(f"   Problem: {test_case['problem']}")
            print(f"   Original: {test_case['text']}")

            # Test each strategy
            for strategy_name in ['simple', 'conservative', 'contextual', 'threshold_based']:
                strategy_func = self.strategies[strategy_name]
                # Reset stats
                self.stats['total_substitutions'] = 0
                self.stats['substitutions_by_vowel'] = {vowel: 0 for vowel in self.vowels}
                self.stats['unique_transformations'] = set()

                normalized = strategy_func(test_case['text'])
                subs = self.stats['total_substitutions']

                print(f"   {strategy_name.capitalize()}: {normalized} ({subs} substitutions)")

    def write_analysis_report(self) -> str:
        """Write a comprehensive analysis report."""
        report = """
VOWEL DUPLICATION NORMALIZATION ANALYSIS REPORT
===============================================

OBJECTIVE:
Normalize emphatic vowel duplications in blog text using regular expression
substitution, while documenting challenges and problems encountered.

APPROACHES TESTED:

1. SIMPLE NORMALIZATION:
   - Pattern: Replace any 2+ consecutive identical vowels with single vowel
   - Regex: (vowel)\\1+ → vowel
   - Pros: Catches all duplications
   - Cons: High false positive rate with legitimate English words

2. CONSERVATIVE NORMALIZATION:
   - Pattern: Replace only 3+ consecutive identical vowels
   - Regex: (vowel)\\1{2,} → vowel
   - Pros: Avoids most legitimate words
   - Cons: Misses some emphatic 2-vowel cases

3. CONTEXTUAL NORMALIZATION:
   - Pattern: Word-boundary aware with whitelist of legitimate words
   - Logic: Check against known legitimate double-vowel words
   - Pros: More accurate distinction
   - Cons: Requires comprehensive word list, still imperfect

4. THRESHOLD-BASED NORMALIZATION:
   - Pattern: Normalize based on duplication length (4+ vowels)
   - Logic: Longer duplications are more likely emphatic
   - Pros: Good balance of precision/recall
   - Cons: May miss shorter emphatic cases

MAJOR PROBLEMS ENCOUNTERED:

1. LEGITIMATE vs EMPHATIC DISAMBIGUATION:
   The biggest challenge is distinguishing between legitimate English words
   with natural double vowels (book, cool, been, agree) and emphatic
   duplications (sooo, coool). Simple regex cannot understand linguistic
   context or word validity.

2. CONTEXT DEPENDENCY:
   The same sequence can be legitimate or emphatic depending on context:
   - "cool weather" vs "coool story!"
   - "noon meeting" vs "noooo way!"

3. INCOMPLETE WORD KNOWLEDGE:
   Creating a comprehensive list of all legitimate English words with
   double vowels is impractical and language-dependent.

4. MIXED PATTERNS:
   Complex expressions like "Woooohooooo!" or "Yeeeaaaahhh!" contain
   multiple vowel types and don't fit simple patterns.

5. CASE AND PUNCTUATION:
   Capitalization and surrounding punctuation complicate pattern matching:
   - "SOOOOO" vs "sooooo"
   - "What?!?" vs "whaaaat"

6. FALSE NEGATIVES vs FALSE POSITIVES TRADE-OFF:
   - Conservative approach misses some emphatic cases
   - Aggressive approach incorrectly normalizes legitimate words
   - No single regex strategy achieves perfect balance

RECOMMENDATIONS:

1. HYBRID APPROACH:
   Combine regex with linguistic resources (dictionaries, NLP libraries)
   to make informed decisions about word legitimacy.

2. LENGTH-BASED HEURISTICS:
   Use duplication length as a strong indicator:
   - 2 vowels: Likely legitimate, proceed with caution
   - 3 vowels: Context-dependent, check word validity
   - 4+ vowels: Very likely emphatic, safe to normalize

3. MACHINE LEARNING APPROACH:
   Train a classifier on labeled examples of emphatic vs legitimate
   duplications, using features like context, word frequency, length.

CONCLUSION:

Pure regex substitution for vowel normalization faces fundamental limitations
due to the complexity of natural language. While regex can identify patterns,
it cannot understand meaning, context, or linguistic validity. The most
effective approach would combine regex pattern matching with additional
linguistic knowledge and contextual analysis.

The threshold-based approach (normalizing 4+ consecutive vowels) provides
the best balance for this specific task, achieving reasonable precision
while avoiding most false positives with legitimate English words.
        """
        return report.strip()

    def save_results(self, results: List[Dict], output_file: str) -> None:
        """Save detailed results to JSON file."""
        # Convert sets to lists for JSON serialization
        serializable_results = []
        for result in results:
            serialized = {}
            for key, value in result.items():
                if key == 'original_analysis':
                    # Handle the analysis dict
                    serialized[key] = {
                        'vowel_duplications_found': value['vowel_duplications_found'],
                        'patterns': dict(value['patterns']),
                        'total_duplications': len(value['vowel_duplications_found'])
                    }
                else:
                    serialized[key] = value
            serializable_results.append(serialized)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'analysis_report': self.write_analysis_report(),
                'sample_results': serializable_results,
                'summary': {
                    'total_files_tested': len(results),
                    'strategies_compared': list(self.strategies.keys())
                }
            }, f, indent=2, ensure_ascii=False)

        print(f"Detailed results saved to {output_file}")


def main():
    """Main function to run the vowel normalization experiment."""
    # Path to the blog corpus
    corpus_path = "/Users/kornelovics/EIT/UT/NLP/project-nlp/homework1/assets/blogs"

    print("Exercise 4d: Vowel Duplication Normalization using Regex Substitution")
    print("="*75)
    print(f"Corpus: {corpus_path}")

    # Create the experiment
    experiment = VowelNormalizationExperiment(corpus_path)

    # Demonstrate problems with different test cases
    experiment.demonstrate_problems()

    # Process sample files to show real-world application
    print("\n" + "="*80)
    print("TESTING ON SAMPLE CORPUS FILES")
    print("="*80)

    sample_results = experiment.process_sample_files(max_files=5)

    # Display the analysis report
    print("\n" + "="*80)
    print(experiment.write_analysis_report())

    # Save results to file
    output_file = "/Users/kornelovics/EIT/UT/NLP/project-nlp/homework1/exercise4/exercise4d_normalization_results.json"
    experiment.save_results(sample_results, output_file)


if __name__ == "__main__":
    main()
