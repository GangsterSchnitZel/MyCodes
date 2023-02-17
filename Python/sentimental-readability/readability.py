from cs50 import get_string


# Ask for the text
text = get_string("Enter Text: ")
# Count the letters
letters = 0
for i in text:
    if i.isalpha():
        letters += 1
# Count the words
words = 0
words = len(text.split())
# Count the sentence
sentence = 0
for i in text:
    if i == ".":
        sentence += 1
    elif i == "!":
        sentence += 1
    elif i == "?":
        sentence += 1
# Calculate with the formula
L = (letters / words) * 100
S = (sentence / words) * 100
liam = (L * 0.0588) - (S * 0.296) - 15.8
output = round(liam)

if output < 1:
    print("Before Grade 1")
elif output > 1 and output < 16:
    print(f"Grade: {output}")
elif output >= 16:
    print("Grade 16+")