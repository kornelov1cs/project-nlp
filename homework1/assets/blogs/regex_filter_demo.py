import re

r"[aeiouAEIOU]{2,}"

def demo_regex_patterns():
    """
    Demonstrate different regular expression patterns to filter out words with excessive vowel duplications.
    """

    # Sample text with various vowel duplications
    sample_text = """
    This is a normal sentence with regular words.
    But then we have words like reeeeaaallly, sooooooo, and WOOOHOOOOO!
    Some more examples: hellooo, byeeeee, waaaaay, huuuuge, III, and cooool.
    Mixed with normal words like: really, so, hello, bye, way, huge, I, and cool.
    """

    print("🎯 REGEX PATTERNS FOR FILTERING VOWEL DUPLICATIONS")
    print("="*70)

    # Pattern 1: Basic pattern for 3+ consecutive same vowels
    print("\n📌 PATTERN 1: Basic - 3+ consecutive identical vowels")
    pattern1 = r'\b\w*[aeiouAEIOU]{3,}\w*\b'
    print(f"Pattern: {pattern1}")
    print("Explanation: \\b = word boundary, \\w* = any word chars, [aeiouAEIOU]{{3,}} = 3+ same vowels")

    matches1 = re.findall(pattern1, sample_text)
    print(f"Matches: {matches1}")

    # Pattern 2: More specific - exactly same vowel repeated 3+ times
    print("\n📌 PATTERN 2: More Specific - Same vowel repeated 3+ times")
    pattern2 = r'\b\w*([aeiouAEIOU])\1{2,}\w*\b'
    print(f"Pattern: {pattern2}")
    print("Explanation: ([aeiouAEIOU]) captures a vowel, \\1{{2,}} matches that same vowel 2+ more times")

    matches2 = re.findall(pattern2, sample_text)
    words2 = re.findall(r'\b\w*([aeiouAEIOU])\1{2,}\w*\b', sample_text)
    print(f"Captured vowels: {matches2}")
    print(f"Full words: {words2}")

    # Pattern 3: Case-insensitive version
    print("\n📌 PATTERN 3: Case-insensitive")
    pattern3 = r'\b\w*([aeiou])\1{2,}\w*\b'
    print(f"Pattern: {pattern3}")
    print("Explanation: Only lowercase vowels, use re.IGNORECASE flag")

    matches3 = re.findall(pattern3, sample_text, re.IGNORECASE)
    words3 = re.findall(r'\b\w*[aeiou]{3,}\w*\b', sample_text, re.IGNORECASE)
    pattern3_full = r'\b\w*([aeiou])\1{2,}\w*\b'
    matches3_iter = [match.group() for match in re.finditer(pattern3_full, sample_text, re.IGNORECASE)]
    print(f"Words found: {matches3_iter}")

    return pattern1, pattern2, pattern3

def filter_text_examples():
    """
    Show practical examples of filtering text using the regex patterns.
    """
    print("\n\n🔧 PRACTICAL FILTERING EXAMPLES")
    print("="*70)

    sample_sentences = [
        "I reeeeaaally love this sooooooo much!",
        "This is a normal sentence without issues.",
        "WOOOHOOOOO that was amaaaazing!",
        "Hello there, how are you today?",
        "Byeeeeeee everyone, see you laterrrr!",
        "The cooool breeze feels niiiiice."
    ]

    # Method 1: Remove words with excessive vowels
    print("\n📝 METHOD 1: Remove problematic words entirely")
    pattern = r'\b\w*([aeiouAEIOU])\1{2,}\w*\b'

    for sentence in sample_sentences:
        filtered = re.sub(pattern, '[FILTERED]', sentence)
        print(f"Original:  {sentence}")
        print(f"Filtered:  {filtered}")
        print()

    # Method 2: Fix the duplications (reduce to 2 of same vowel max)
    print("\n📝 METHOD 2: Fix duplications (reduce to max 2 consecutive)")

    def fix_vowel_duplications(text):
        """Reduce excessive vowel duplications to maximum of 2 consecutive."""
        # Pattern to find 3+ consecutive same vowels
        pattern = r'([aeiouAEIOU])\1{2,}'
        # Replace with just 2 of the same vowel
        fixed = re.sub(pattern, r'\1\1', text)
        return fixed

    for sentence in sample_sentences:
        fixed = fix_vowel_duplications(sentence)
        print(f"Original:  {sentence}")
        print(f"Fixed:     {fixed}")
        print()

    # Method 3: Identify and flag for manual review
    print("\n📝 METHOD 3: Identify and flag for manual review")

    pattern = r'\b\w*([aeiouAEIOU])\1{2,}\w*\b'

    for i, sentence in enumerate(sample_sentences, 1):
        problematic_words = re.findall(pattern, sentence)
        if problematic_words:
            print(f"Sentence {i}: ⚠️  CONTAINS ISSUES")
            print(f"  Text: {sentence}")
            matches = re.finditer(pattern, sentence)
            for match in matches:
                print(f"  Problematic word: '{match.group()}'")
        else:
            print(f"Sentence {i}: ✅ Clean")
            print(f"  Text: {sentence}")
        print()

def advanced_patterns():
    """
    Show more advanced regex patterns for specific use cases.
    """
    print("\n\n🚀 ADVANCED REGEX PATTERNS")
    print("="*70)

    # Pattern for different thresholds
    print("\n📌 CONFIGURABLE THRESHOLD PATTERNS")

    test_words = ["cool", "coool", "cooool", "coooool", "sooo", "soooooo", "realy", "reeally", "reeeally"]

    # Different thresholds
    thresholds = [3, 4, 5]

    for threshold in thresholds:
        print(f"\n🎯 Threshold: {threshold}+ consecutive vowels")
        pattern = rf'\b\w*([aeiouAEIOU])\1{{{threshold-1},}}\w*\b'
        print(f"Pattern: {pattern}")

        matches = []
        for word in test_words:
            if re.search(pattern, word):
                matches.append(word)
        print(f"Matches from test words: {matches}")

    # Pattern for specific vowels only
    print(f"\n📌 SPECIFIC VOWEL PATTERNS")

    # Only 'o' vowels
    pattern_o = r'\b\w*o{3,}\w*\b'
    print(f"Only 'o' vowels (3+): {pattern_o}")
    o_matches = [word for word in test_words if re.search(pattern_o, word)]
    print(f"Matches: {o_matches}")

    # Only 'e' vowels
    pattern_e = r'\b\w*e{3,}\w*\b'
    print(f"Only 'e' vowels (3+): {pattern_e}")
    e_matches = [word for word in test_words if re.search(pattern_e, word)]
    print(f"Matches: {e_matches}")

        # Multiple different vowel duplications in same word
    print(f"\n📌 MULTIPLE DUPLICATIONS IN SAME WORD")
    complex_words = ["reeeeaaallly", "sooouuuul", "aaaaeeeeiiiii", "hello", "normal"]

    # Pattern for words with multiple vowel duplications (any vowel 3+ times, multiple times in word)
    pattern_multi = r'\b\w*([aeiouAEIOU])\1{2,}.*([aeiouAEIOU])\2{2,}\w*\b'
    print(f"Multiple duplications: {pattern_multi}")

    for word in complex_words:
        if re.search(pattern_multi, word):
            print(f"  ⚠️  '{word}' has multiple vowel duplications")
        else:
            # Check for single duplication
            single_dup = r'\b\w*([aeiouAEIOU])\1{2,}\w*\b'
            if re.search(single_dup, word):
                print(f"  ⚠️  '{word}' has single vowel duplication")
            else:
                print(f"  ✅ '{word}' is clean")

def create_filter_function():
    """
    Create a reusable function for filtering text.
    """
    print("\n\n⚙️ REUSABLE FILTER FUNCTION")
    print("="*70)

    def filter_excessive_vowels(text, method='remove', threshold=3, replacement='[FILTERED]'):
        """
        Filter text to handle excessive vowel duplications.

        Args:
            text (str): Input text to filter
            method (str): 'remove', 'fix', or 'flag'
            threshold (int): Minimum consecutive vowels to consider excessive
            replacement (str): What to replace with if method='remove'

        Returns:
            str: Filtered text
        """
        pattern = rf'\b\w*([aeiouAEIOU])\1{{{threshold-1},}}\w*\b'

        if method == 'remove':
            return re.sub(pattern, replacement, text)
        elif method == 'fix':
            def fix_match(match):
                word = match.group()
                # Reduce any sequence of 3+ same vowels to just 2
                fixed = re.sub(r'([aeiouAEIOU])\1{2,}', r'\1\1', word)
                return fixed
            return re.sub(pattern, fix_match, text)
        elif method == 'flag':
            matches = re.findall(pattern, text)
            if matches:
                return f"⚠️ FLAGGED: {text} (Contains: {set(matches)})"
            return f"✅ CLEAN: {text}"
        else:
            return text

    # Test the function
    test_texts = [
        "I reeeeaaally love this sooooooo much!",
        "This is completely normal text.",
        "WOOOHOOOOO that was amaaaazing!",
    ]

    print("🧪 Testing the filter function:")

    for method in ['remove', 'fix', 'flag']:
        print(f"\n📋 Method: {method}")
        for text in test_texts:
            result = filter_excessive_vowels(text, method=method)
            print(f"  Input:  {text}")
            print(f"  Output: {result}")
            print()

    return filter_excessive_vowels

if __name__ == "__main__":
    # Run all demonstrations
    demo_regex_patterns()
    filter_text_examples()
    advanced_patterns()
    filter_func = create_filter_function()

    print("\n" + "="*70)
    print("🎉 SUMMARY OF KEY PATTERNS:")
    print("="*70)
    print("1. Basic (3+ same vowels):     " + r"\b\w*([aeiouAEIOU])\1{2,}\w*\b")
    print("2. Configurable threshold:     " + r"\b\w*([aeiouAEIOU])\1{n-1,}\w*\b")
    print("3. Case-insensitive:           Use re.IGNORECASE flag")
    print("4. Specific vowels only:       " + r"\b\w*[o]{3,}\w*\b" + " (for 'o' only)")
    print("5. Remove: re.sub(pattern, replacement, text)")
    print("6. Fix: re.sub(pattern, lambda m: fix_function(m.group()), text)")
