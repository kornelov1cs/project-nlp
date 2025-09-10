# Exercise 4: Vowel Duplication Analysis

## Exercise 4a Answer

### Tool Used

**Python** with regular expressions (re module)

### Regular Expression Patterns

I developed four distinct regular expression patterns to capture different types of vowel duplications used for emphasis:

#### 1. Emphatic Identical Pattern

**Regex:** `(?i)\b\w*([aeiou])\1{2,}\w*\b`

**Explanation:**

- `(?i)` = inline case-insensitive flag (matches both uppercase and lowercase)
- `\b` = word boundary (ensures we match complete words)
- `\w*` = zero or more word characters before the vowel sequence
- `([aeiou])` = capture group for any vowel (a, e, i, o, u) - matches both cases due to (?i)
- `\1{2,}` = two or more additional repetitions of the captured vowel (making 3+ total identical vowels)
- `\w*` = zero or more word characters after the vowel sequence
- `\b` = word boundary (end of word)

**Motivation:** This pattern specifically targets words with 3 or more consecutive identical vowels, which are clear indicators of emphatic expression (like "sooo", "SOOO", or "Sooo" instead of "so").

#### 2. Mixed Emphasis Pattern

**Regex:** `\b\w{1,20}(?:[aeiou]{2,}.*[aeiou]{2,})\w{0,20}\b`

**Explanation:**

- `\b\w{1,20}` = word boundary followed by 1-20 word characters (prevents matching entire paragraphs)
- `(?:...)` = non-capturing group
- `[aeiou]{2,}.*[aeiou]{2,}` = vowel duplication (2+ vowels), followed by any characters, followed by another vowel duplication
- `\w{0,20}\b` = up to 20 more word characters and word boundary

**Motivation:** Captures words with multiple vowel duplications, like "reeeeaaallllyyyy" where different vowels are emphasized within the same word.

#### 3. Long Vowel Sequences Pattern

**Regex:** `\b\w*[aeiou]{4,}\w*\b`

**Explanation:**

- `[aeiou]{4,}` = any sequence of 4 or more consecutive vowels (any combination)

**Motivation:** Identifies words with extreme emphasis using very long vowel sequences, regardless of whether they're identical vowels or mixed.

#### 4. Repeated Pairs Pattern

**Regex:** `\b\w*([aeiou])\1{3,}\w*\b`

**Explanation:**

- `([aeiou])\1{3,}` = a vowel followed by 3+ more identical vowels (4+ total identical vowels)

**Motivation:** Captures words with extreme emphasis using 4 or more identical consecutive vowels (like "soooooo").

### Filtering Strategy

To focus on true emphatic duplications rather than normal English words, I implemented:

1. **Common word exclusion:** Filtered out frequent English words that naturally contain double vowels (like "good", "been", "see", "too", etc.)
2. **Length limiting:** Limited matches to 30 characters or less to avoid capturing entire sentences or paragraphs
3. **Multiple validation:** For mixed emphasis patterns, verified that words actually contain multiple vowel duplications

### Key Findings

The analysis of 650 blog files revealed:

#### Most Common Emphatic Duplications:

1. **"sooo"** - 78 occurrences across 53 files (most common)
2. **"soooo"** - 54 occurrences across 43 files
3. **"sooooo"** - 38 occurrences across 30 files
4. **"iii"** - 19 occurrences across 13 files
5. **"weeee"** - 4 occurrences across 4 files
6. **"noooooo"** - 4 occurrences across 4 files

#### Summary Statistics:

- **Emphatic Identical Vowels:** 413 unique words, 1,179 total occurrences
- **Mixed Emphasis:** 264 unique words, 374 total occurrences
- **Long Vowel Sequences:** 304 unique words, 599 total occurrences
- **Repeated Pairs:** 200 unique words, 467 total occurrences

### Analysis Insights

1. **"So" variations dominate:** The word "so" with various levels of emphasis (sooo, soooo, sooooo, etc.) is by far the most common emphatic duplication pattern

2. **Emotional expression:** These duplications appear to be primarily used for emotional emphasis, excitement, or frustration (like "weeee" for excitement, "noooooo" for dismay)

3. **Graduated emphasis:** Users employ different lengths of duplication to indicate different intensity levels (so → sooo → soooo → sooooo)

4. **Limited vocabulary:** Most emphatic duplications occur on a relatively small set of common words (so, we, no, oh, etc.) rather than across the entire vocabulary

### Conclusion

The regular expression approach successfully identified genuine vowel duplications used for emphasis in the blog corpus. The patterns capture the online spelling variation phenomenon where users duplicate vowels to convey emotional intensity or emphasis, distinguishing these from natural English words that happen to contain double vowels.

The Python script with its refined regex patterns and filtering mechanisms provides a robust tool for analyzing emphatic vowel duplications in informal text like blogs and social media content.

## Exercise 4b Answer

### Methodology

For 4b, I analyzed the emphatic vowel duplications found in 4a to determine the top 3 most frequent word types for each vowel. The approach involved:

1. **Base Word Extraction**: Converting emphatic duplications back to their base forms (e.g., "sooo", "soooo", "sooooo" → "so")
2. **Frequency Calculation**: Summing all instances of each base word type across the corpus
3. **Vowel-Specific Analysis**: Grouping results by which vowel is duplicated
4. **Case Folding**: Using lowercase normalization to combine capitalized and non-capitalized variants

### Top 3 Most Frequent Word Types by Vowel Duplication

#### Vowel 'A' - Top 3 word types with 'a' duplication:

1. **"way"** - 8 total occurrences
2. **"ah"** - 7 total occurrences (examples: "aaaaaaaaah")
3. **"a"** - 5 total occurrences (examples: "aaa")

_Total: 92 word types, 142 total occurrences_

#### Vowel 'E' - Top 3 word types with 'e' duplication:

1. **"we"** - 17 total occurrences (examples: "weee", "weeee")
2. **"invisiblenodetrexample"** - 10 total occurrences
3. **"e"** - 7 total occurrences

_Total: 62 word types, 122 total occurrences_

#### Vowel 'I' - Top 3 word types with 'i' duplication:

1. **"i"** - 20 total occurrences (examples: "iii")
2. **"right"** - 5 total occurrences (examples: "riiiiight")
3. **"ffvi"** - 3 total occurrences

_Total: 13 word types, 44 total occurrences_

#### Vowel 'O' - Top 3 word types with 'o' duplication:

1. **"so"** - 211 total occurrences (examples: "sooo", "soooo", "sooooooooo")
2. **"o"** - 25 total occurrences (examples: "ooo", "oooo", "ooooooo")
3. **"no"** - 22 total occurrences (examples: "nooooo", "noooooooo", "nooooooooooooooooooooooo")

_Total: 92 word types, 442 total occurrences_

#### Vowel 'U' - Top 3 word types with 'u' duplication:

1. **"huge"** - 6 total occurrences (examples: "huuuuge", "huuuuuge")
2. **"nyu"** - 2 total occurrences
3. **"lurrrve"** - 2 total occurrences

_Total: 20 word types, 27 total occurrences_

### Key Insights

1. **Vowel 'O' Dominance**: The vowel 'o' shows the highest frequency of emphatic duplications (442 total occurrences), primarily driven by the word "so" and its variations.

2. **"So" as Primary Target**: The word "so" accounts for 211 occurrences, making it by far the most frequently emphasized word through vowel duplication in the corpus.

3. **Emotional Expression Patterns**: The results confirm that emphatic vowel duplication is primarily used for:

   - Emphasis ("sooo good")
   - Emotional expression ("aaaaaaaaah", "nooooo")
   - Interjections ("weee", "ooo")

4. **Limited Vocabulary**: Emphatic duplication targets a small set of common, emotionally-charged words rather than the entire vocabulary.

### Technical Implementation

The analysis was implemented using Python with regular expressions, building on the 4a methodology but reorganizing results by individual vowels. The script (`exercise4b_refined.py`) processes the same blog corpus and uses the same filtering criteria as 4a to ensure consistency.
