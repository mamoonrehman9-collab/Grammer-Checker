import re
from spellchecker import SpellChecker

spell = SpellChecker()

CUSTOM_WORDS = {"nlp", "fastapi", "python", "github", "api", "uvicorn", "grammarlens"}
spell.word_frequency.load_words(CUSTOM_WORDS)

# words with an optional inner apostrophe: don't, it's
WORD_RE = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")

# ---------------------------------------------------------------- data

MISSPELLINGS = {
    "definately": "definitely", "seperate": "separate", "occured": "occurred",
    "recieve": "receive", "untill": "until", "wierd": "weird", "beleive": "believe",
    "accomodate": "accommodate", "tommorow": "tomorrow", "goverment": "government",
    "enviroment": "environment", "necesary": "necessary", "embarass": "embarrass",
    "begining": "beginning", "freind": "friend", "truely": "truly",
    "publically": "publicly", "adress": "address", "calender": "calendar",
    "concious": "conscious", "occurence": "occurrence", "tomorow": "tomorrow",
}

COMMON_MISTAKES = {
    "alot": "a lot",
    "could of": "could have",
    "should of": "should have",
    "would of": "would have",
    "must of": "must have",
    "might of": "might have",
    "dont": "don't",
    "cant": "can't",
    "wont": "won't",
    "didnt": "didn't",
    "doesnt": "doesn't",
    "isnt": "isn't",
    "arent": "aren't",
    "wasnt": "wasn't",
    "werent": "weren't",
    "havent": "haven't",
    "hasnt": "hasn't",
    "hadnt": "hadn't",
    "wouldnt": "wouldn't",
    "couldnt": "couldn't",
    "shouldnt": "shouldn't",
    "im": "I'm",
    "ive": "I've",
    "youre": "you're",
    "theyre": "they're",
    "thats": "that's",
    "your welcome": "you're welcome",
    "less people": "fewer people",
    "irregardless": "regardless",
    "for all intensive purposes": "for all intents and purposes",
    "could care less": "couldn't care less",
    "more better": "better",
    "more easier": "easier",
    "most easiest": "easiest",
    "a part from": "apart from",
    "suppose to": "supposed to",
    "infact": "in fact",
    "atleast": "at least",
    # wrong prepositions / redundancy
    "discuss about": "discuss",
    "discussed about": "discussed",
    "discussing about": "discussing",
    "married with": "married to",
    "depend of": "depend on",
    "depends of": "depends on",
    "return back": "return",
    "piece of mind": "peace of mind",
}

THIRD_PERSON = {
    "go": "goes", "do": "does", "have": "has", "don't": "doesn't", "dont": "doesn't",
    "want": "wants", "need": "needs", "like": "likes", "know": "knows",
    "think": "thinks", "make": "makes", "take": "takes", "come": "comes",
    "get": "gets", "say": "says", "see": "sees", "work": "works", "play": "plays",
    "live": "lives", "love": "loves", "look": "looks", "use": "uses",
    "try": "tries", "feel": "feels", "are": "is",
}

_PLURAL = {"is": "are", "was": "were", "has": "have", "does": "do", "goes": "go"}
PLURAL_FIX = {
    "i": {"is": "am", "has": "have", "does": "do", "goes": "go"},
    "we": _PLURAL, "you": _PLURAL, "they": _PLURAL,
}

INDEFINITE_FIX = {"are": "is", "were": "was", "have": "has", "do": "does"}
THESE_FIX = {"is": "are", "was": "were"}

# verb forms that are wrong after a modal / "did"
BASE_FORM = {
    "goes": "go", "does": "do", "has": "have", "comes": "come", "makes": "make",
    "takes": "take", "gets": "get", "says": "say", "sees": "see",
    "went": "go", "came": "come", "saw": "see", "took": "take", "gave": "give",
    "ate": "eat", "wrote": "write", "ran": "run",
}
BASE_RE = re.compile(
    r"\b(?:can|could|should|would|will|must|might|did|didn't|do|does)\s+(?P<w>"
    + "|".join(sorted(BASE_FORM, key=len, reverse=True)) + r")\b", re.I)
PAST_RE = re.compile(r"\b(?:I|he|she|we|they|you)\s+(?P<w>seen|done)\b", re.I)
PAST_FIX = {"seen": "saw", "done": "did"}

MUCH_MANY = re.compile(
    r"\b(?P<w>many)\s+(?:water|money|time|information|advice|rice|milk|homework|furniture|traffic|news)\b", re.I)
MANY_MUCH = re.compile(
    r"\b(?P<w>much)\s+(?:people|friends|books|students|things|cars|children|problems|questions|ideas)\b", re.I)

COMPARATIVE = re.compile(
    r"\b(?P<more>more|most)\s+(?P<adj>faster|better|bigger|smaller|easier|harder|larger|stronger|"
    r"older|younger|taller|best|worst|worse|cheaper|higher|lower)\b", re.I)

QUESTION_RE = re.compile(
    r"(?:^|[.!?]\s+)("
    r"(?:what|why|how|where|who|which|whose|when)\s+(?:is|are|was|were|do|does|did|can|could|will|would|should|has|have)\b[^.!?\n]*"
    r"|(?:do|does|did|are|is|can|could|will|would|should)\s+(?:you|we|they|he|she|it|i|this|that|there)\b[^.!?\n]*"
    r")(?P<p>\.)", re.I)

INTRO_COMMA = re.compile(
    r"(?:^|[.!?]\s+)(?P<w>However|Moreover|Furthermore|Therefore|Meanwhile|Additionally|"
    r"Unfortunately|Nevertheless|Consequently)\s+(?=[A-Za-z])")

# (regex with a named group "w" = the wrong word, correct word)
CONFUSED = [
    (r"\b(?P<w>there)\s+(?:own|best|house|home|car|friends?|team|work|job|family|parents?|school|names?|room|books?|way|turn|money|life|children|kids|country|city|phones?|ideas?|goals?|results?)\b", "their"),
    (r"\b(?P<w>they're)\s+(?:own|best|house|car|friends?|team|family|parents?|school|names?|room|books?)\b", "their"),
    (r"\b(?P<w>their)\s+(?:is|are|was|were)\b", "there"),
    (r"\b(?P<w>their|there)\s+(?:going|coming|not|doing|ready)\b", "they're"),
    (r"\b(?P<w>its)\s+(?:a|an|the|not|been|going|very|so|too|time|my|your|our)\b", "it's"),
    (r"\b(?P<w>it's)\s+(?:own|color|colour|name|way|owner|size|shape|purpose|value)\b", "its"),
    (r"\b(?P<w>your)\s+(?:not|really|so|a|an|ready)\b", "you're"),
    (r"\b(?P<w>you're)\s+(?:own|house|car|name|friends?|team|book|family|phone|email|work|mother|father|mom|dad)\b", "your"),
    (r"\b(?:more|less|better|worse|bigger|smaller|larger|faster|slower|higher|lower|older|younger|greater|fewer|taller|easier|harder|cheaper|stronger|rather|other)\s+(?P<w>then)\b", "than"),
    (r"\b(?:an|no|any|side|positive|negative|great|big|major|little)\s+(?P<w>affect)\b", "effect"),
    (r"\b(?:will|would|can|could|may|might|not)\s+(?P<w>effect)\s+(?:the|my|your|our|his|her|their|us|them|me)\b", "affect"),
    (r"\b(?P<w>to)\s+(?:much|tired|busy|expensive|cheap|hot|cold)\b", "too"),
    (r"\b(?:to|will|would|might|could|don't|dont)\s+(?P<w>loose)\b", "lose"),
    (r"\b(?P<w>weather)\s+or\s+not\b", "whether"),
    (r"\b(?:an|some|good|bad|my|your|any|no|the|this|that)\s+(?P<w>advise)\b", "advice"),
]

NEG_WORDS = (r"(?:don't|dont|doesn't|doesnt|didn't|didnt|can't|cant|won't|wont|haven't|havent|"
             r"hadn't|hadnt|isn't|isnt|wasn't|wasnt|couldn't|couldnt|wouldn't|wouldnt|shouldn't|shouldnt)")
DOUBLE_NEG = re.compile(
    r"\b" + NEG_WORDS + r"\s+(?:[A-Za-z]+\s+)?(?P<w>nothing|nobody|nowhere|no\s+one)\b", re.I)
NEG_FIX = {"nothing": "anything", "nobody": "anybody", "nowhere": "anywhere", "no one": "anyone"}

_verbs = sorted(THIRD_PERSON, key=len, reverse=True)
SV_HE_SHE = re.compile(r"\b(he|she)\s+(" + "|".join(re.escape(v) for v in _verbs) + r")\b", re.I)
SV_IT = re.compile(r"\b(it)\s+(don't|dont)\b", re.I)
SV_PLURAL = re.compile(r"\b(I|we|you|they)\s+(is|was|has|does|goes)\b", re.I)
SV_INDEF = re.compile(r"\b(everyone|everybody|someone|somebody|nobody|everything)\s+(are|were|have|do)\b", re.I)
SV_THESE = re.compile(r"\b(these|those)\s+(is|was)\b", re.I)

DAYS_MONTHS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
               "january", "february", "april", "june", "july", "august",
               "september", "october", "november", "december"]
DAYS_RE = re.compile(r"\b(" + "|".join(DAYS_MONTHS) + r")\b")

COMMON_RE = [
    (re.compile(r"\b" + re.escape(w).replace(r"\ ", r"\s+") + r"\b", re.I), r)
    for w, r in COMMON_MISTAKES.items()
]

# ---- style data
FILLER_RE = re.compile(r"\b(very|really|basically|literally|actually|honestly)\b", re.I)

WORDY = {
    "in order to": "to",
    "due to the fact that": "because",
    "at this point in time": "now",
    "in the event that": "if",
    "has the ability to": "can",
    "for the purpose of": "for",
    "in spite of the fact that": "although",
}
WORDY_RE = [
    (re.compile(r"\b" + re.escape(w).replace(r"\ ", r"\s+") + r"\b", re.I), r)
    for w, r in WORDY.items()
]

CLICHES = ["at the end of the day", "think outside the box", "low hanging fruit",
           "needless to say", "last but not least"]
CLICHE_RE = re.compile(r"\b(" + "|".join(c.replace(" ", r"\s+") for c in CLICHES) + r")\b", re.I)

PASSIVE_RE = re.compile(r"\b(?:was|were|is|are|been|being)\s+\w+ed\s+by\b", re.I)

# ---------------------------------------------------------------- helpers


def issue(kind, start, end, text, suggestion, message):
    return {"type": kind, "start": start, "end": end, "text": text,
            "suggestion": suggestion, "message": message}


def match_case(src, repl):
    """Copy a leading capital letter from src to repl."""
    if src[:1].isupper():
        return repl[:1].upper() + repl[1:]
    return repl


def at_sentence_start(text, pos):
    before = text[:pos].rstrip()
    return not before or before[-1] in ".!?"


def starts_with_vowel_sound(word):
    w = word.lower()
    if w.startswith(("hour", "honest", "honor", "honour", "heir")):
        return True
    if w in ("one", "once"):
        return False
    if w.startswith("uni") and not w.startswith(("unim", "unin", "unid")):
        return False
    if w.startswith(("use", "usu", "uten", "util", "eu", "ubiq")):
        return False
    return w[0] in "aeiou"


# ---------------------------------------------------------------- spelling


def check_spelling(text):
    issues = []
    for m in WORD_RE.finditer(text):
        word = m.group()
        low = word.lower()
        if "'" in word or len(word) < 2 or low in CUSTOM_WORDS:
            continue
        if word.isupper():  # acronyms: NASA, FBI
            continue
        if low in MISSPELLINGS:  # known common misspellings
            issues.append(issue("spelling", m.start(), m.end(), word,
                                match_case(word, MISSPELLINGS[low]),
                                f"Possible spelling mistake: '{word}'"))
            continue
        if word[0].isupper() and not at_sentence_start(text, m.start()):  # names
            continue
        if low in spell.unknown([low]):
            fix = spell.correction(low)
            issues.append(issue(
                "spelling", m.start(), m.end(), word,
                match_case(word, fix) if fix and fix != low else None,
                f"Possible spelling mistake: '{word}'"))
    return issues


# ---------------------------------------------------------------- grammar


def check_grammar(text):
    issues = []
    sv_spans = []

    # 1. a / an (with sound exceptions)
    for m in re.finditer(r"\b(a|an)\s+([A-Za-z]+)", text, re.IGNORECASE):
        article, nxt = m.group(1), m.group(2)
        if len(nxt) > 1 and nxt.isupper():  # acronym such as "an FBI agent"
            continue
        vowel = starts_with_vowel_sound(nxt)
        if article.lower() == "a" and vowel:
            correct = "an"
        elif article.lower() == "an" and not vowel:
            correct = "a"
        else:
            continue
        correct = match_case(article, correct)
        issues.append(issue("grammar", m.start(1), m.end(1), article, correct,
                            f"Use '{correct}' before '{nxt}'"))

    # 2. repeated words
    for m in re.finditer(r"\b([A-Za-z]+)\s+\1\b", text, re.IGNORECASE):
        if m.group(1).lower() in ("had", "that"):
            continue
        issues.append(issue("grammar", m.start(), m.end(), m.group(), m.group(1),
                            f"Repeated word: '{m.group(1)}'"))

    # 3. lowercase "i"
    for m in re.finditer(r"(?<![.\w])i(?![.\w])", text):
        issues.append(issue("grammar", m.start(), m.end(), "i", "I",
                            "Capitalize the pronoun 'I'"))

    # 4. subject-verb agreement
    for rx in (SV_HE_SHE, SV_IT):
        for m in rx.finditer(text):
            subj, verb = m.group(1), m.group(2).lower()
            fixed = THIRD_PERSON[verb]
            issues.append(issue("grammar", m.start(), m.end(), m.group(),
                                f"{subj} {fixed}",
                                f"Subject-verb agreement: use '{fixed}' after '{subj}'"))
            sv_spans.append((m.start(), m.end()))

    for m in SV_PLURAL.finditer(text):
        subj, verb = m.group(1), m.group(2).lower()
        fixed = PLURAL_FIX.get(subj.lower(), {}).get(verb)
        if not fixed:
            continue
        subj_out = "I" if subj.lower() == "i" else subj
        issues.append(issue("grammar", m.start(), m.end(), m.group(),
                            f"{subj_out} {fixed}",
                            f"Subject-verb agreement: use '{fixed}' after '{subj}'"))
        sv_spans.append((m.start(), m.end()))

    for rx, table in ((SV_INDEF, INDEFINITE_FIX), (SV_THESE, THESE_FIX)):
        for m in rx.finditer(text):
            subj, verb = m.group(1), m.group(2).lower()
            fixed = table[verb]
            issues.append(issue("grammar", m.start(), m.end(), m.group(),
                                f"{subj} {fixed}",
                                f"Subject-verb agreement: use '{fixed}' after '{subj}'"))
            sv_spans.append((m.start(), m.end()))

    # 5. confused words
    for pattern, right in CONFUSED:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            wrong = m.group("w")
            sug = match_case(wrong, right)
            issues.append(issue("grammar", m.start("w"), m.end("w"), wrong, sug,
                                f"Possible confused word: use '{sug}'"))

    # 6. double negatives
    for m in DOUBLE_NEG.finditer(text):
        wrong = m.group("w")
        key = re.sub(r"\s+", " ", wrong.lower())
        issues.append(issue("grammar", m.start("w"), m.end("w"), wrong, NEG_FIX[key],
                            f"Double negative: use '{NEG_FIX[key]}'"))

    # 7. common mistakes
    for rx, right in COMMON_RE:
        for m in rx.finditer(text):
            if any(s <= m.start() and m.end() <= e for s, e in sv_spans):
                continue
            sug = match_case(m.group(), right)
            issues.append(issue("grammar", m.start(), m.end(), m.group(), sug,
                                f"Common mistake: use '{sug}'"))

    # 8. capital letters
    for m in re.finditer(r"(?:^|[.!?]\s+)([a-z])", text):
        issues.append(issue("grammar", m.start(1), m.end(1), m.group(1), m.group(1).upper(),
                            "Sentence should start with a capital letter"))
    for m in DAYS_RE.finditer(text):
        issues.append(issue("grammar", m.start(), m.end(), m.group(), m.group().capitalize(),
                            f"Capitalize '{m.group()}'"))

    # 9. spacing and punctuation
    for m in re.finditer(r"(?<=\S)[ ]{2,}(?=\S)", text):
        issues.append(issue("grammar", m.start(), m.end(), m.group(), " ",
                            "Extra spaces between words"))
    for m in re.finditer(r"(?<=\S)[ ]+([,.!?;:])", text):
        issues.append(issue("grammar", m.start(), m.end(), m.group(), m.group(1),
                            "No space before punctuation"))
    for m in re.finditer(r"(?<=[A-Za-z])([,;])(?=[A-Za-z])", text):
        issues.append(issue("grammar", m.start(), m.end(), m.group(), m.group() + " ",
                            "Add a space after punctuation"))
    for m in re.finditer(r"(?<=[a-z])(\.)(?=[A-Z][a-z])", text):
        issues.append(issue("grammar", m.start(), m.end(), m.group(), ". ",
                            "Add a space after the full stop"))
    for m in re.finditer(r"([,;:])\1+", text):
        issues.append(issue("grammar", m.start(), m.end(), m.group(), m.group(1),
                            "Repeated punctuation"))
    for m in re.finditer(r"(?<!\.)\.\.(?!\.)", text):
        issues.append(issue("grammar", m.start(), m.end(), m.group(), ".",
                            "Repeated punctuation"))

    # 10. very long sentences (marks the 40th word only)
    for m in re.finditer(r"[^.!?]+[.!?]*", text):
        words = list(WORD_RE.finditer(m.group()))
        if len(words) > 40:
            w = words[39]
            issues.append(issue("grammar", m.start() + w.start(), m.start() + w.end(),
                                w.group(), None,
                                f"Very long sentence ({len(words)} words). Consider splitting it."))

    # 11. missing end punctuation (zero-width marker at the end)
    stripped = text.rstrip()
    if stripped and stripped[-1].isalnum():
        last_sentence = re.split(r"[.!?]\s*", stripped)[-1]
        if len(WORD_RE.findall(last_sentence)) >= 3:
            n = len(stripped)
            issues.append(issue("grammar", n, n, "", ".",
                                "Sentence should end with punctuation"))

    # 12. past tense: "I seen" -> "I saw"
    for m in PAST_RE.finditer(text):
        wrong = m.group("w")
        sug = PAST_FIX[wrong.lower()]
        issues.append(issue("grammar", m.start("w"), m.end("w"), wrong, sug,
                            f"Wrong verb form: use '{sug}'"))

    # 13. modal / did + wrong verb form
    for m in BASE_RE.finditer(text):
        wrong = m.group("w")
        sug = BASE_FORM[wrong.lower()]
        issues.append(issue("grammar", m.start("w"), m.end("w"), wrong, sug,
                            f"Use the base form '{sug}' here"))

    # 14. much / many
    for rx, right in ((MUCH_MANY, "much"), (MANY_MUCH, "many")):
        for m in rx.finditer(text):
            wrong = m.group("w")
            sug = match_case(wrong, right)
            issues.append(issue("grammar", m.start("w"), m.end("w"), wrong, sug,
                                f"Use '{sug}' with this noun"))

    # 15. double comparatives (more faster)
    for m in COMPARATIVE.finditer(text):
        adj = m.group("adj")
        sug = match_case(m.group(), adj)
        issues.append(issue("grammar", m.start(), m.end(), m.group(), sug,
                            f"Double comparative: use '{sug}'"))

    # 16. missing question mark
    for m in QUESTION_RE.finditer(text):
        issues.append(issue("grammar", m.start("p"), m.end("p"), ".", "?",
                            "This looks like a question: end it with '?'"))

    # 17. comma after introductory word
    for m in INTRO_COMMA.finditer(text):
        w = m.group("w")
        issues.append(issue("grammar", m.start("w"), m.end("w"), w, w + ",",
                            f"Add a comma after '{w}'"))

    # 18. unmatched quotes and brackets
    if text.count('"') % 2:
        p = text.rfind('"')
        issues.append(issue("grammar", p, p + 1, '"', None, "Unmatched quotation mark"))
    if text.count("(") > text.count(")"):
        p = text.rfind("(")
        issues.append(issue("grammar", p, p + 1, "(", None, "Missing closing bracket ')'"))
    elif text.count(")") > text.count("("):
        p = text.rfind(")")
        issues.append(issue("grammar", p, p + 1, ")", None, "Missing opening bracket '('"))

    return issues


# ---------------------------------------------------------------- style


def check_style(text):
    out = []
    for m in FILLER_RE.finditer(text):
        out.append(issue("style", m.start(), m.end(), m.group(), None,
                         f"Filler word: '{m.group()}' can often be removed"))
    for rx, right in WORDY_RE:
        for m in rx.finditer(text):
            sug = match_case(m.group(), right)
            out.append(issue("style", m.start(), m.end(), m.group(), sug,
                             f"Wordy phrase: use '{sug}'"))
    for m in CLICHE_RE.finditer(text):
        out.append(issue("style", m.start(), m.end(), m.group(), None,
                         "Cliche: try fresher wording"))
    for m in PASSIVE_RE.finditer(text):
        out.append(issue("style", m.start(), m.end(), m.group(), None,
                         "Possible passive voice: consider active voice"))
    return out


# ---------------------------------------------------------------- readability


def count_syllables(word):
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    if len(w) <= 3:
        return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w)
    w = re.sub(r"^y", "", w)
    return max(1, len(re.findall(r"[aeiouy]{1,2}", w)))


def readability(text):
    words = WORD_RE.findall(text)
    if not words:
        return {"reading_ease": 0, "grade_level": 0, "label": "-", "sentences": 0}
    sentences = max(1, len(re.findall(r"[.!?]+", text)))
    syll = sum(count_syllables(w) for w in words)
    wps = len(words) / sentences
    spw = syll / len(words)
    ease = 206.835 - 1.015 * wps - 84.6 * spw
    grade = 0.39 * wps + 11.8 * spw - 15.59
    ease = max(0, min(100, ease))
    if ease >= 80:
        label = "Easy"
    elif ease >= 60:
        label = "Standard"
    elif ease >= 40:
        label = "Fairly difficult"
    else:
        label = "Difficult"
    return {"reading_ease": round(ease, 1), "grade_level": round(max(0, grade), 1),
            "label": label, "sentences": sentences}


# ---------------------------------------------------------------- main entry


def analyze(text):
    grammar = check_grammar(text)
    grammar_spans = [(g["start"], g["end"]) for g in grammar]

    # drop spelling issues already covered by a grammar rule
    spelling = [
        s for s in check_spelling(text)
        if not any(gs <= s["start"] and s["end"] <= ge for gs, ge in grammar_spans)
    ]
    style = check_style(text)

    seen = set()
    issues = []
    for item in sorted(spelling + grammar + style, key=lambda x: (x["start"], x["end"])):
        key = (item["start"], item["end"])
        if key in seen:
            continue
        seen.add(key)
        issues.append(item)

    n_spelling = sum(1 for i in issues if i["type"] == "spelling")
    n_grammar = sum(1 for i in issues if i["type"] == "grammar")
    n_style = sum(1 for i in issues if i["type"] == "style")

    return {
        "issues": issues,
        "stats": {
            "words": len(WORD_RE.findall(text)),
            "spelling": n_spelling,
            "grammar": n_grammar,
            "style": n_style,
            "total": len(issues),
        },
        "readability": readability(text),
    }