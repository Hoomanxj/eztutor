# count the letters, words and setences and return them
def counter(text):
    punc = [".", "?", "!"]
    letter_c = 0
    word_c = 0
    sentence_c = 0
    for c in range(len(text)):
        if text[c].isalpha():
            letter_c += 1
        elif text[c] in punc:
            sentence_c += 1
            word_c += 1
        elif text[c] == " " and text[c - 1] not in punc:
            word_c += 1
    return letter_c, word_c, sentence_c


# calculate the index
def coleman_liau(l, w, s):
    L = l / w * 100
    S = s / w * 100
    index = round(0.0588 * L - 0.296 * S - 15.8)
    return index


def main():
    text = input("Text: ")
    l, w, s = counter(text)
    i = coleman_liau(l, w, s)
    # based on the index, decide the readability level
    if i < 1:
        print("Before Grade 1")
    elif i > 16:
        print("Grade 16+")
    else:
        print(f"Grade {i}")


main()
