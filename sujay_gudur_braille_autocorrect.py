import time
from collections import defaultdict

# QWERTY to Braille dot mapping
BRAILLE_QWERTY_MAP = {
    'd': 1, 'w': 2, 'q': 3, 'k': 4, 'o': 5, 'p': 6
}

# Braille dictionary
BRAILLE_DICT = {
    '100000': 'a', '110000': 'b', '101000': 'c', '100100': 'd', '100010': 'e',
    '110100': 'f', '110010': 'g', '110110': 'h', '010100': 'i', '010110': 'j',
    '101100': 'k', '111100': 'l', '101110': 'm', '101010': 'n', '100101': 'o',
    '111110': 'p', '111011': 'q', '101111': 'r', '011110': 's', '011011': 't',
    '101001': 'u', '111001': 'v', '100110': 'w', '101011': 'x', '101101': 'y',
    '100111': 'z'
}

# Optional contractions
BRAILLE_CONTRACTIONS = {
    '000001': 'ch', '000011': 'sh', '010011': 'th', '011001': 'wh'
}

# Include 'braille' explicitly
WORD_DICT = ['hello', 'braille', 'world', 'data', 'code']

CORRECTION_HISTORY = defaultdict(lambda: defaultdict(int))

def qwerty_to_braille(qwerty_input):
    if len(qwerty_input) == 6 and set(qwerty_input).issubset({'0', '1'}):
        return qwerty_input
    dots = set()
    for char in qwerty_input.lower():
        if char not in BRAILLE_QWERTY_MAP:
            return '000000'
        dots.add(BRAILLE_QWERTY_MAP[char])
    return ''.join('1' if i + 1 in dots else '0' for i in range(6))

def braille_to_char(braille_pattern):
    return BRAILLE_CONTRACTIONS.get(braille_pattern, BRAILLE_DICT.get(braille_pattern, ''))

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def braille_word_to_text(qwerty_inputs):
    result = []
    for q in qwerty_inputs:
        braille_pattern = qwerty_to_braille(q)
        char = braille_to_char(braille_pattern)
        if char:
            result.append(char)
    if any(q in BRAILLE_CONTRACTIONS for q in qwerty_inputs):
        return ' '.join(result)
    return ''.join(result)

def suggest_correction(qwerty_inputs, dictionary=WORD_DICT):
    valid_inputs = [q for q in qwerty_inputs if qwerty_to_braille(q) != '000000']
    input_patterns = [qwerty_to_braille(q) for q in valid_inputs]
    min_distance = float('inf')
    best_match = None

    char_to_braille = {v: k for k, v in BRAILLE_DICT.items()}

    for word in dictionary:
        try:
            word_braille = [char_to_braille[c] for c in word]
        except KeyError:
            continue
        if len(word_braille) != len(input_patterns):
            continue
        distance = sum(levenshtein_distance(p, w) for p, w in zip(input_patterns, word_braille))
        if distance == 0:
            return word, 0
        if distance < min_distance:
            min_distance = distance
            best_match = word

    if best_match:
        input_text = ''.join(braille_to_char(qwerty_to_braille(q)) for q in valid_inputs)
        CORRECTION_HISTORY[input_text][best_match] += 1
    return best_match, min_distance if best_match else (None, float('inf'))

def autocorrect_system(qwerty_input_string, dictionary=WORD_DICT):
    words = qwerty_input_string.strip().split()
    corrected_words = []
    for word_inputs in words:
        char_inputs = word_inputs.split(',')
        if not char_inputs:
            continue
        corrected_word, _ = suggest_correction(char_inputs, dictionary)
        corrected_words.append(corrected_word if corrected_word else braille_word_to_text(char_inputs))
    return ' '.join(corrected_words)

def run_test_cases():
    test_cases = [
        ("qw,od,kp,kp,od", "hello", "Correct 'hello' input"),
        ("dw,dkp,d,wq,kp,kp,od", "braille", "Correct 'braille' input"),
        ("qw,od,kp,kp,od dw,dkp,d,wq,kp,kp,od", "hello braille", "Full phrase")
    ]
    results = []
    for i, (input_str, expected, desc) in enumerate(test_cases, 1):
        start_time = time.perf_counter()
        result = autocorrect_system(input_str)
        elapsed = (time.perf_counter() - start_time) * 1000
        results.append((i, input_str, result, expected, f"{elapsed:.2f}", desc))
    return results

if __name__ == "__main__":
    input_str = "qw,od,kp,kp,od dw,dkp,d,wq,kp,kp,od"
    print(f"Input: {input_str}")
    print(f"Output: {autocorrect_system(input_str)}")
    print("\nTest Cases:")
    for i, inp, out, exp, t, desc in run_test_cases():
        print(f"Test {i}: Input: {inp}, Output: {out}, Expected: {exp}, Time: {t}ms, Desc: {desc}")
