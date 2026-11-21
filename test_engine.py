from engine import analyze

LONG = ("We went to the market early in the morning because we needed fresh bread, ripe fruit, "
        "green vegetables, and some cheese for the big family dinner that our parents planned "
        "for the weekend, and then we walked home slowly while talking about school, music, "
        "travel, and the wonderful plans for next summer.")

# (text, list of texts that SHOULD be flagged)
TESTS = [
    ("i have a apple.", ["i", "a"]),
    ("This is teh best day.", ["teh"]),
    ("the the cat sat.", ["the the", "t"]),
    ("I dont know.", ["dont"]),
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
    ("im happy today.", ["im", "i"]),
    ("Less people came.", ["Less people"]),
    ("The cat is on the mat.", []),
    ("He is an honest man.", []),
    ("She waited for an hour.", []),
    ("He goes to a university.", []),
    ("It was a unique idea.", []),
    ("I saw a European tourist.", []),
    ("He go to school.", ["He go"]),
    ("They was late.", ["They was"]),
    ("She dont like it.", ["She dont"]),
    ("Everyone are happy.", ["Everyone are"]),
    ("Those is my books.", ["Those is"]),
    ("I want to go, but there car is broken.", ["there"]),
    ("Their are many options.", ["Their"]),
    ("Its a sunny day.", ["Its"]),
    ("You're welcome to take your time.", []),
    ("She is taller then me.", ["then"]),
    ("It had no affect on me.", ["affect"]),
    ("He is to tired to walk.", ["to"]),
    ("I dont know nothing.", ["dont", "nothing"]),
    ("See you on monday.", ["monday"]),
    ("This  has double spaces.", ["  "]),
    ("Hello , world.", [" ,"]),
    ("Hello,world.", [","]),
    ("Wait,, what.", [",,"]),
    ("I like tea", [""]),
    (LONG, ["while"]),
    ("Good teamwork makes hard tasks easier for everybody.", []),
    ("I seen him yesterday.", ["seen"]),
    ("He did went home.", ["went"]),
    ("She can goes there.", ["goes"]),
    ("She is more faster than me.", ["more faster"]),
    ("There are much people here.", ["much"]),
    ("We discuss about it.", ["discuss about"]),
    ("What is your name.", ["."]),
    ("However I think so.", ["However"]),
    ("Definately yes.", ["Definately"]),
    ("Do you like tea?", []),
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
            print(f"  FALSE POSITIVE: '{f}' in: {text[:60]}")
    for e in exp:
        fn += 1
        print(f"  MISSED: '{e}' in: {text[:60]}")

precision = tp / (tp + fp) if tp + fp else 0
recall = tp / (tp + fn) if tp + fn else 0
f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0

print("\n--- RESULTS ---")
print(f"Test sentences : {len(TESTS)}")
print(f"True positives : {tp}")
print(f"False positives: {fp}")
print(f"False negatives: {fn}")
print(f"Precision: {precision:.2f}")
print(f"Recall   : {recall:.2f}")
print(f"F1 score : {f1:.2f}")