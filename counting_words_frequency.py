import string


def word_count_frequency(file_path):
    with open(file_path) as file:
        all_words= {}
        for line in file:
            for word in line.split():
                current_word = word.strip(string.punctuation).lower()
                if current_word in all_words and current_word != "":
                    all_words[current_word]+=1
                else:
                    if current_word != "":
                        all_words[current_word] = 1
    return all_words

def words_counter(all_words):
    max = 0 
    wordstring = ""
    for word in all_words:
        if(all_words[word] > max):
            max = all_words[word]
            wordstring = word
    print(f"the word {wordstring} was the most frequent word, it was written {max} times :)" )




def run_with(file_path):
    all_words = word_count_frequency(file_path)
    words_counter(all_words)

run_with("/Users/omerbanvolgyi/Documents/personal/index.html")