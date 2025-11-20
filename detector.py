import pysrt
from better_profanity import profanity
from collections import Counter
import re

profanity.load_censor_words()

def analyze_srt(file_path):
    subs = pysrt.open(file_path)
    word_counter = Counter()
    profane_line_count = 0

    for sub in subs:
        text = sub.text.strip()
        cleaned = re.sub(r"<.*?>", "", text)

        if profanity.contains_profanity(cleaned):
            profane_line_count += 1
            for word in re.findall(r"\b\w+\b", cleaned.lower()):
                if profanity.contains_profanity(word):
                    word_counter[word] += 1

    return {
        "total_profane_lines": profane_line_count,
        "word_counts": word_counter.most_common()
    }
