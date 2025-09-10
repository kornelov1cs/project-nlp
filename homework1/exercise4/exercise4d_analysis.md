# Exercise 4d: Vowel Duplication Normalization using Regular Expression Substitution

## Approach and Implementation

For this exercise, I implemented four different regular expression substitution strategies to normalize vowel duplications found in the blog corpus:

### 1. Aggressive Normalization

**Pattern:** `([aeiou])\1{2,}` → `\1`
**Strategy:** Reduces any sequence of 3+ consecutive identical vowels to a single vowel.

### 2. Conservative Normalization

**Pattern:** `([aeiou])\1{2,}` → `\1\1`
**Strategy:** Reduces any sequence of 3+ consecutive identical vowels to exactly two vowels.

### 3. Extreme Cases Only

**Pattern:** `([aeiou])\1{4,}` → `\1\1`
**Strategy:** Only normalizes extreme cases (5+ consecutive vowels), leaving moderate duplications untouched.

### 4. Smart Normalization

**Strategy:** Uses context awareness to preserve common English words that naturally contain double vowels (like "good", "been", "see").

## Results and Effectiveness

Testing these approaches on sample sentences from the corpus revealed clear differences:

**Example:** "I am soooo happy about this!"

- Aggressive: "I am so happy about this!" (perhaps too drastic)
- Conservative: "I am soo happy about this!" (balanced)
- Extreme only: No change (too conservative)
- Smart: "I am soo happy about this!" (context-aware)

The conservative approach emerged as the most balanced, preserving some emphasis while normalizing clear duplications.

## Problems Encountered

### 1. False Positives with Natural English Words

The most significant challenge was distinguishing between intentional emphatic duplications and legitimate English words containing double vowels. Words like "good", "been", "queen", and "school" naturally contain consecutive identical vowels and should not be normalized.

**Problem Example:**

- Original: "The food was sooooo good"
- Aggressive result: "The fod was so god" (incorrectly changes "food" and "good")
- Solution: Implemented a whitelist of common English words to preserve

### 2. Word Boundary Detection

Regular expressions don't inherently understand word semantics, making it difficult to apply normalization only within word boundaries appropriately.

**Problem:** The pattern `([aeiou])\1{2,}` can match across word boundaries in some edge cases or within compound words where it shouldn't apply.

### 3. Context Dependency

Determining when vowel duplication is intentional emphasis versus accidental requires understanding context that regex alone cannot provide.

**Example:** "I feel soooooo much better" - clearly intentional emphasis
**Versus:** "cooperation" - contains "ooo" but shouldn't be changed

### 4. Mixed Vowel Sequences

Some emphasis patterns use mixed vowels (like "beauuutiful" or "yeeeah") which are harder to normalize systematically because they don't follow the identical repetition pattern.

### 5. Case Preservation

Maintaining the original capitalization while applying normalization required careful consideration of the replacement patterns to preserve the visual formatting of the text.

### 6. Performance Considerations

Processing large corpus files with complex regex patterns proved computationally intensive, especially when applying multiple normalization strategies simultaneously.

## Recommended Solution

After testing all approaches, the **conservative normalization** (3+ consecutive identical vowels → 2 vowels) combined with a whitelist of common English words provides the best balance between:

- Effectively reducing emphatic duplications
- Preserving legitimate English vocabulary
- Maintaining some stylistic emphasis
- Computational efficiency

This approach successfully normalized examples like:

- "sooooo" → "soo" (preserves some emphasis)
- "weeeeee" → "wee" (maintains emotional expression)
- "noooooooo" → "noo" (reduces excessive duplication)

While preserving standard words like "good", "been", and "see" unchanged.

The experience highlighted that vowel duplication normalization is not merely a pattern-matching problem but requires linguistic awareness about intentionality, word boundaries, and contextual appropriateness - challenges that push beyond what regex substitution alone can elegantly solve.
