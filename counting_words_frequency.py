import string
import sys


#counting all the words form a file,
# and returns a dictionary of each word and how many times it was written
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


#returns the word that was repited most times
def words_counter(all_words):
    max = 0 
    wordstring = ""
    for word in all_words:
        if(all_words[word] > max):
            max = all_words[word]
            wordstring = word
    print(f"the word {wordstring} was the most frequent word, it was written {max} times :)\n{all_words}" )


#returning a sorted dict of the N most repeated words
def N_most_frequent_words(N, all_words):
    sorted_dict = sorted(all_words.items(), key= lambda item: item[1], reverse= True)
    return sorted_dict[:N]

def run_with(file_path):
    all_words = word_count_frequency(file_path)
    words_counter(all_words)

file_path = "/Users/omerbanvolgyi/Documents/personal/index.html"
run_with(file_path)
print(N_most_frequent_words(int(sys.argv[1]), word_count_frequency(file_path)))