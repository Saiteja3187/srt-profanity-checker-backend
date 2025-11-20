import pysrt
from better_profanity import profanity
from collections import Counter
import re

# Load default profanity words
profanity.load_censor_words()

def analyze_srt(file_path):
    subs = pysrt.open(file_path)
    word_counter = Counter()
    profane_line_count = 0

    for sub in subs:
        text = sub.text.strip()

        # Remove HTML tags
        cleaned = re.sub(r"<.*?>", "", text)

        # SAFETY: Ensure cleaned is a string
        cleaned_str = str(cleaned)

        # SAFETY WRAPPER to prevent crashing on Render
        try:
            has_profane = profanity.contains_profanity(cleaned_str)
        except Exception as e:
            print("Profanity line check failed:", e)
            has_profane = False

        if has_profane:
            profane_line_count += 1

            # Find words safely
            words = re.findall(r"\b\w+\b", cleaned_str.lower())

            for word in words:
                try:
                    if profanity.contains_profanity(word):
                        word_counter[word] += 1
                except Exception as e:
                    print("Profanity word check failed:", e)
                    continue

    return {
        "total_profane_lines": profane_line_count,
        "word_counts": word_counter.most_common()
    }
