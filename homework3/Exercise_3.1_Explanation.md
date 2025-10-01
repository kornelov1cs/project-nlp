# Exercise 3.1 - Complete Explanation and Solution

## What Exercise 3.1 Asks For

Exercise 3.1 requires you to:

1. **Choose an NLP application** (e.g., summarization, Q&A, classification)
2. **Select appropriate model(s)** (Seq2Seq encoder-decoder OR Causal decoder-only)
3. **Justify your choice** with technical reasoning
4. **Document constraints** (computational, quality, practical)

## Solution Summary

### ✅ Application Chosen: **Text Summarization with Audience Adaptation**

**Why this is a good choice:**

- Clear, measurable task
- Real-world application (science communication, education)
- Allows comparison between model architectures
- Has objective evaluation criteria (factual accuracy, readability)

### ✅ Models Selected: **Both Architectures (for comparison)**

#### 1. **FLAN-T5-Small** (Seq2Seq / Encoder-Decoder)

**Architecture:**

```
Input → Encoder (reads full context) → Hidden State → Decoder (generates summary) → Output
```

**Why it's good for summarization:**

- ✅ **Bidirectional context**: The encoder can look at the entire input at once
- ✅ **Designed for transformation**: Naturally maps input text → different output text
- ✅ **Instruction-tuned**: Pre-trained specifically on tasks like "summarize this"
- ✅ **Faithful to source**: Less likely to hallucinate facts
- ✅ **Length control**: Can follow specific length constraints

**When to use:**

- Need high factual accuracy
- Input and output are clearly different (translation, summarization)
- Want extractive-style summaries

#### 2. **TinyLlama-1.1B-Chat** (Causal / Decoder-Only)

**Architecture:**

```
Prompt + Input → Decoder (generates continuation) → Output
```

**Why it's good for summarization:**

- ✅ **Natural generation**: Produces more fluent, human-like text
- ✅ **Style adaptation**: Better at changing tone for different audiences
- ✅ **Instruction following**: Chat-tuned models understand complex prompts
- ✅ **Single-pass efficiency**: Faster inference
- ✅ **Creative phrasing**: Can rephrase concepts in engaging ways

**When to use:**

- Need engaging, natural-sounding summaries
- Want to adapt style for different audiences
- Free-form generation tasks

### ✅ Constraints Documented

#### **Computational Constraints:**

- **Hardware**: CPU-only (M1/M2 Mac or standard laptop)
- **Memory**: ~8GB RAM limitation
- **Model Size**: Must use models < 2B parameters
  - FLAN-T5-Small: 80M parameters
  - TinyLlama: 1.1B parameters
- **Speed**: Target < 10 seconds per summary

#### **Quality Constraints:**

- **Factual Accuracy**: Summaries must preserve key facts
- **Consistency**: Similar inputs should produce similar outputs
- **Readability**: Clear, well-structured text
- **Control**: Must be able to adjust length and style

#### **Practical Constraints:**

- **Local deployment**: No API calls (privacy, cost)
- **Reproducibility**: Need consistent results for evaluation
- **Scalability**: Should work for batch processing

---

## Key Concepts to Understand

### 🔑 Seq2Seq vs. Causal: The Fundamental Difference

| Feature            | Seq2Seq (Encoder-Decoder)                 | Causal (Decoder-Only)                    |
| ------------------ | ----------------------------------------- | ---------------------------------------- |
| **Context Access** | Sees entire input at once (bidirectional) | Sees only left-to-right (unidirectional) |
| **Architecture**   | Two networks: encoder + decoder           | One network: decoder only                |
| **Task Design**    | Transform input → different output        | Continue/complete the input              |
| **Summarization**  | Natural: "compress this"                  | Learned: "continue with a summary"       |
| **Example Models** | T5, BART, FLAN-T5                         | GPT, LLaMA, Mistral                      |

### 🔑 Why Architecture Matters for Summarization

**Seq2Seq Advantages:**

1. **Full context understanding**: Encoder sees the entire abstract before generating
2. **Compression mindset**: Trained to transform long → short
3. **Factual preservation**: Less likely to add information not in source
4. **Length control**: Naturally handles "summarize in N words"

**Causal Model Advantages:**

1. **Natural language**: Produces more fluent, engaging text
2. **Style flexibility**: Better at tone adaptation (technical vs. simple)
3. **Instruction following**: Chat models understand complex prompts
4. **Efficiency**: Single-pass generation (faster)

### 🔑 Trade-offs to Consider

```
More Accurate ←------------------------→ More Natural
More Extractive ←----------------------→ More Creative
More Faithful ←------------------------→ More Fluent
Seq2Seq                                   Causal

              [Ideal Sweet Spot]
                    ↓
            Use both and compare!
```

---

## What I Added to Your Notebook

I've added **three new cells** after Cell 86 (Exercise 3.1):

### **Cell 87** (Markdown):

Comprehensive answer explaining:

- The chosen application (summarization)
- Why FLAN-T5 is suited (encoder-decoder advantages)
- Why TinyLlama is suited (causal advantages)
- All constraints (computational, quality, practical)

### **Cell 88** (Code):

Sample scientific abstract and setup code that:

- Provides a concrete example text
- Prepares for Exercise 3.2 experiments
- Shows you'll test both models

### **Cell 89** (Markdown):

Educational content explaining:

- How Seq2Seq vs. Causal models work
- Comparison table of their strengths
- What makes a good Exercise 3.1 answer

---

## How to Present This Exercise

When submitting, make sure you:

1. ✅ **Clearly state your application**

   - "I chose text summarization with audience adaptation"

2. ✅ **Explain your model choice(s)**

   - "I'm testing both Seq2Seq (FLAN-T5) and Causal (TinyLlama)"
   - "Seq2Seq because it's designed for text transformation..."
   - "Causal because it generates more natural language..."

3. ✅ **Justify with architecture details**

   - "The encoder-decoder architecture allows bidirectional context..."
   - "The decoder-only model can better adapt style because..."

4. ✅ **Document realistic constraints**

   - "Running on CPU with 8GB RAM"
   - "Models must be < 1B parameters for inference speed"
   - "Need factual accuracy, so monitoring hallucinations"

5. ✅ **Set up for Exercise 3.2**
   - "In Exercise 3.2, I'll test these models with different prompting techniques"

---

## Common Mistakes to Avoid

❌ **DON'T**: Just say "I chose summarization"
✅ **DO**: Explain _what type_ of summarization and _why it's interesting_

❌ **DON'T**: Say "I chose T5 because it's good"
✅ **DO**: Explain the encoder-decoder architecture advantage

❌ **DON'T**: Ignore constraints
✅ **DO**: Acknowledge hardware, speed, and quality trade-offs

❌ **DON'T**: Only choose one model arbitrarily
✅ **DO**: Either justify why one is clearly better, OR test both to compare

---

## Connection to Exercise 3.2

Exercise 3.1 is the **setup/justification** phase.
Exercise 3.2 is the **experimental/empirical** phase.

In 3.2, you'll:

- Test different prompting techniques (zero-shot, few-shot, chain-of-thought, etc.)
- Run both models with the same prompts
- Compare outputs
- Evaluate which prompting technique + model combination works best

**Your Exercise 3.1 answer sets the foundation for why you're testing what you're testing in 3.2!**

---

## Summary

You've now completed Exercise 3.1 by:

1. ✅ Choosing **text summarization with audience adaptation** as your application
2. ✅ Selecting **both FLAN-T5 (Seq2Seq) and TinyLlama (Causal)** for comparison
3. ✅ Justifying each with **technical architecture details**
4. ✅ Documenting **computational, quality, and practical constraints**
5. ✅ Understanding the **fundamental differences** between model architectures

The solution in your notebook now includes all required components with clear explanations and educational context!

---

## Next Steps

1. **Run the cells** I added (87-89) to see the output
2. **Read through** the explanations to understand the concepts
3. **Move to Exercise 3.2** where you'll implement different prompting techniques
4. **Compare results** empirically between the two models

Good luck with your assignment! 🚀
