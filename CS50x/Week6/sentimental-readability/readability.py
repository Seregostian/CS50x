def main():

    sentence = input("Text: ")

    letters = count_letters(sentence)
    words = count_words(sentence)
    sentences = count_sentences(sentence)

    round_letters = (100 / float(words)) * float(letters)
    round_sentences = (100 / float(words)) * float(sentences)

    index = Kinclaid_index(round_letters, round_sentences)

# Before and after grader, to separate values

    if index < 1:
        print("Before Grade 1")
    elif index >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {index}")

# Count letters, words, sentences

def count_letters(text):
    cnt = 0
    for i in range(len(text)):
        if text[i].isalnum():
            cnt += 1
    return cnt


def count_words(text):
    cnt = 0
    for i in range(len(text)):
        if text[i].isspace():
            cnt += 1
    return cnt + 1


def count_sentences(text):
    cnt = 0
    for i in range(len(text)):
        if text[i] == '.' or text[i] == '!' or text[i] == '?':
            cnt += 1
    return cnt

#https://en.wikipedia.org/wiki/Flesch–Kincaid_readability_tests

def Kinclaid_index(round_letters, round_sentences):

  return round(0.0588 * round_letters - 0.296 * round_sentences - 15.8)


if __name__ == "__main__":
    main()