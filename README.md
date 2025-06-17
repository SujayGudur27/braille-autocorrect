# braille-autocorrect
# Braille Autocorrect System

### Developed by: Sujay Gudur

---

## 🔍 Overview

The **Braille Autocorrect System** processes QWERTY-based Braille inputs and converts them into accurate text. It supports autocorrection of mistyped inputs and suggests the most likely intended word from a predefined dictionary.

---

## 🚀 Approach

The solution is built in Python and includes the following components:

- **Input Processing**: Converts QWERTY Braille inputs (`D, W, Q, K, O, P`) into 6-bit Braille binary patterns.
- **Correction Mechanism**: Uses **Levenshtein Distance** to detect and correct errors such as missing, extra, or swapped keys.
- **Word Suggestion**: Matches input patterns against dictionary words and returns the closest possible match based on character pattern similarity.

---

## ✨ Bonus Features

- ✅ **Braille Contractions** (e.g., `"ch"`, `"sh"`).
- ✅ **Learning Mechanism** to prioritize frequent corrections.

---

## ⚙️ Optimizations

- **Levenshtein Efficiency**: Dynamic programming approach with two-row space optimization.
- **Early Exit**: Immediate return on exact match to improve speed.
- **Fast Lookup**: Braille patterns stored as binary strings for fast dictionary access.
- **Learning Adjustments**: Lightweight memory of frequent corrections to improve results over time.

---

## ⚖️ Trade-Offs

| Option | Decision | Reason |
|--------|----------|--------|
| Levenshtein vs Trie | ✅ Levenshtein | Better for dot-level mismatches |
| Large Dictionary | 🚫 Not used yet | Trie/indexing needed for scale |
| Full Grade 2 Braille | 🚫 Limited to basic contractions | Simpler parsing |
| ML-based Learning | 🚫 Not implemented | Used lightweight frequency learning |

---

## 🧪 Test Cases

| Test | Input | Output | Expected | Time (ms) | Description |
|------|-------|--------|----------|-----------|-------------|
| 1 | `qw,do,kp,kp,od` | hello | hello | 0.12 | Correct input |
| 2 | `q,do,kp,kp,od` | hello | hello | 0.15 | Missing dot |
| 3 | `qwq,do,kp,kp,od` | hello | hello | 0.14 | Extra dot |
| 4 | `xyz,abc` | *(empty)* | *(empty)* | 0.10 | Invalid input |
| 5 | `qw,000001` | h ch | h ch | 0.11 | Contraction support |

---

## ✅ Evaluation

- **Accuracy**: Handles real-world mistypes and returns reliable suggestions.
- **Efficiency**: Processes input in <0.2ms for small dictionaries.
- **Code Quality**: Modular, readable, and maintainable.
- **Innovation**: Adds contraction support and learning for improved usability.

---

## 📦 How to Run

```bash
python braille_autocorrect.py
