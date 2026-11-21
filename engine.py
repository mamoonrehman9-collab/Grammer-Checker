import re
from spellchecker import SpellChecker

spell = SpellChecker()

# Words that are fine even if the dictionary doesn't know them
CUSTOM_WORDS = {"nlp", "fastapi", "python", "github", "api"}
spell.word_frequency.load_words(CUSTOM_WORDS)

# Common wrong -> right phrases
COMMON_MISTAKES = {
    "alot": "a lot",
    "could of": "could have",
    "should of": "should have",
    "would of": "would have",
    "should of": "should have",
    "dont": "don't",
    "cant": "can't",
    "wont": "won't",
    "didnt": "didn't",
    "doesnt": "doesn't",
    "im": "I'm",
    "ive": "I've",
    "your welcome": "you're welcome",
    "less people": "fewer people",
}

WORD_RE = re.compile(r"[A-Za-z']+")


def check_spelling(text):
    issues = []
    for m in WORD_RE.finditer(text):
        word = m.group()
        clean = word.strip("'")
        if len(clean) < 2 or clean.lower() in CUSTOM_WORDS:
            continue
        if clean.lower() in spell.unknown([clean.lower()]):
            fix = spell.correction(clean.lower())
            issues.append({
                "type": "spelling",
                "start": m.start(),
                "end": m.end(),
                "text": word,
                "suggestion": fix if fix and fix != clean.lower() else None,
                "message": f"Possible spelling mistake: '{word}'",
            })
    return issues


def check_grammar(text):
    issues = []

    # 1. a / an
    for m in re.finditer(r"\b(a|an)\s+([A-Za-z]+)", text, re.IGNORECASE):
        article, nxt = m.group(1), m.group(2)
        starts_vowel = nxt[0].lower() in "aeiou"
        if article.lower() == "a" and starts_vowel:
            correct = "an"
        elif article.lower() == "an" and not starts_vowel:
            correct = "a"
        else:
            continue
        issues.append({
            "type": "grammar",
            "start": m.start(1),
            "end": m.end(1),
            "text": article,
            "suggestion": correct,
            "message": f"Use '{correct}' before '{nxt}'",
        })

    # 2. repeated words ("the the")
    for m in re.finditer(r"\b(\w+)\s+\1\b", text, re.IGNORECASE):
        issues.append({
            "type": "grammar",
            "start": m.start(),
            "end": m.end(),
            "text": m.group(),
            "suggestion": m.group(1),
            "message": f"Repeated word: '{m.group(1)}'",
        })

    # 3. lowercase "i"
    for m in re.finditer(r"\bi\b", text):
        issues.append({
            "type": "grammar",
            "start": m.start(),
            "end": m.end(),
            "text": "i",
            "suggestion": "I",
            "message": "Capitalize the pronoun 'I'",
        })

    # 4. common mistakes
    for wrong, right in COMMON_MISTAKES.items():
        for m in re.finditer(r"\b" + re.escape(wrong) + r"\b", text, re.IGNORECASE):
            issues.append({
                "type": "grammar",
                "start": m.start(),
                "end": m.end(),
                "text": m.group(),
                "suggestion": right,
                "message": f"Common mistake: use '{right}'",
            })

    # 5. sentence should start with a capital letter
    for m in re.finditer(r"(?:^|[.!?]\s+)([a-z])", text):
        issues.append({
            "type": "grammar",
            "start": m.start(1),
            "end": m.end(1),
            "text": m.group(1),
            "suggestion": m.group(1).upper(),
            "message": "Sentence should start with a capital letter",
        })

    return issues

def analyze(text):
    # Spelling words already covered by a grammar rule are skipped
    grammar = check_grammar(text)
    grammar_spans = [(g["start"], g["end"]) for g in grammar]

    spelling = [
        s for s in check_spelling(text)
        if not any(gs <= s["start"] and s["end"] <= ge for gs, ge in grammar_spans)
    ]

    # Sort by position and drop duplicates at the same spot
    seen = set()
    issues = []
    for item in sorted(spelling + grammar, key=lambda x: x["start"]):
        key = (item["start"], item["end"])
        if key in seen:
            continue
        seen.add(key)
        issues.append(item)

    n_spelling = sum(1 for i in issues if i["type"] == "spelling")
    n_grammar = sum(1 for i in issues if i["type"] == "grammar")

    return {
        "issues": issues,
        "stats": {
            "words": len(WORD_RE.findall(text)),
            "spelling": n_spelling,
            "grammar": n_grammar,
            "total": len(issues),
        },
    }