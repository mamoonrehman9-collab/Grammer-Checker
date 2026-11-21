from engine import analyze

# (text, list of words/phrases that SHOULD be flagged)
TESTS = [
    ("i have a apple", ["i", "a"]),
    ("This is teh best day", ["teh"]),
    ("the the cat sat", ["the the", "t"]),
    ("I dont know", ["dont"]),
    ("She said alot of things.", ["alot"]),
    ("We could of won.", ["could of"]),
    ("Your welcome to join.", ["Your welcome"]),
    ("Thiss is a speling mistake.", ["Thiss", "speling"]),
    ("I have an umbrella.", []),
    ("This sentence is perfectly fine.", []),
    ("He bought a book. She read it.", []),
    ("We should of gone home.", ["should of"]),
    ("There is a elephant here.", ["a"]),
    ("I cant come today.", ["cant"]),
    ("Please recieve the package.", ["recieve"]),
    ("It was a good day.", []),
    ("im happy today", ["im", "i"]),
    ("Less people came.", ["Less people"]),
    ("The cat is on the mat.", []),
    ("He is an honest man.", []),
]

tp = fp = fn = 0
for text, expected in TESTS:
    found = [i["text"] for i in analyze(text)["issues"]]
    exp = list(expected)
    for f in found:
        if f in exp:
            tp += 1
            exp.remove(f)
        else:
            fp += 1
            print(f"  FALSE POSITIVE: '{f}' in: {text}")
    for e in exp:
        fn += 1
        print(f"  MISSED: '{e}' in: {text}")

precision = tp / (tp + fp) if tp + fp else 0
recall = tp / (tp + fn) if tp + fn else 0
f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0

print("\n--- RESULTS ---")
print(f"True positives : {tp}")
print(f"False positives: {fp}")
print(f"False negatives: {fn}")
print(f"Precision: {precision:.2f}")
print(f"Recall   : {recall:.2f}")
print(f"F1 score : {f1:.2f}")   