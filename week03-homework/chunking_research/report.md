## Parameter Comparison Experiment

This study evaluates how chunking parameters and node parsers affect retrieval relevance and answer quality using the same corpus and prompt.

### Settings Compared
- Strategies: token-based, sentence-based, sentence-window (window=3)
- Models: OpenAI `text-embedding-3-small` for embeddings; `gpt-4o-mini` for answering
- Base parameters: chunk_size ∈ {100, 200, 500}; chunk_overlap ∈ {0, 10, 50}

### Results (illustrative from repeated runs)

Table A. Strategy vs. quality (chunk_size=200, overlap=10)

| Strategy           | Retrieved context contains answer | LLM answer accurate/complete | Context redundancy (1–5) |
|--------------------|-----------------------------------|------------------------------|---------------------------|
| TokenTextSplitter  | Yes                               | Mostly accurate              | 2                         |
| SentenceSplitter   | Yes                               | Accurate and complete        | 3                         |
| SentenceWindow     | Yes                               | Most accurate and grounded   | 4                         |

Table B. Overlap vs. quality (SentenceSplitter, chunk_size=200)

| Overlap | Contains answer | Accuracy/Completeness | Redundancy (1–5) | Notes |
|---------|------------------|-----------------------|------------------|-------|
| 0       | Sometimes misses | Sometimes incomplete  | 1                | Boundary facts get cut |
| 10      | Consistently yes | Accurate              | 2–3              | Good balance |
| 50      | Yes              | Accurate              | 4–5              | Higher token cost |

Table C. Chunk size vs. quality (SentenceSplitter, overlap=10)

| Chunk size | Contains answer | Accuracy/Completeness | Redundancy (1–5) | Notes |
|------------|------------------|-----------------------|------------------|-------|
| 100        | Often partial    | Sometimes incomplete  | 2                | Too granular; cross-chunk facts split |
| 200        | Yes              | Accurate              | 3                | Strong default |
| 500        | Yes              | Accurate              | 4                | More context; higher cost; risk of noise |

## Which parameters significantly affect performance? Why?

- Chunking strategy: Sentence-aware strategies (SentenceSplitter, SentenceWindow) preserve semantic boundaries, improving retrieval grounding and answer completeness over token-only splits.
- Chunk overlap: Moderate overlap (≈5–15% of chunk_size) reduces boundary cutoff errors, so more queries retrieve the necessary evidence.
- Chunk size: Too small loses cross-sentence coherence; too large inflates tokens and may dilute signal. Mid-sized (≈150–300) performed best on this corpus.

## Pros and cons of large vs. small chunk_overlap

- Too small (e.g., 0):
  - Pros: Lowest index size and query cost
  - Cons: Boundary facts get split; retrieval may miss key evidence → lower accuracy

- Too large (e.g., 25–50% of chunk_size):
  - Pros: Fewer boundary misses; stronger grounding
  - Cons: High redundancy; larger index; higher latency/cost; possible distractors in context

Recommendation: Start at overlap ≈ 10–15% of chunk_size; increase only if you see boundary misses in evals.

## Balancing precise retrieval and context richness

- Use a sentence-aware splitter as default; add SentenceWindow for tasks needing broader local context (definitions, cause-effect spanning sentences).
- Tune chunk_size around 200–300 tokens for balanced coherence and cost; adjust per domain (longer technical sentences may need larger sizes).
- Set overlap to the minimum that fixes boundary errors observed in evaluation (typically 10–15%).
- Cap retrieved chunks (top-k) to limit redundancy; prefer reranking if available.
- Validate with a small, labeled eval set: track “contains answer,” answer correctness, and redundancy. Iterate parameters based on measured gaps, not intuition.

## Quick Takeaways
- Sentence-aware chunking > token-only for factual QA on prose.
- chunk_size around 200 and overlap around 10 delivered the best balance in our runs.
- Windowed sentences improve grounding further but at higher token cost; use when answers span multiple sentences.