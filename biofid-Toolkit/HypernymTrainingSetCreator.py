import csv, random, string
from gensim.models import KeyedVectors

# Tool for creating a training set or test set for the training of the support vector
# machine classifier for hypernym recognition. 

class HypernymTrainingSetCreator:

    def __init__(self):
        pass

    # Function to load the word2vec binary file and choose only words without any punctuation.
    # The first parameter is the word2vec binary file path and the second parameter is the path
    # of the bio words which occur in the cleaned word2vec file.
    
    def __init(self, binary_vector_path, cleanSetPath):
        binary_vector = KeyedVectors.load_word2vec_format(binary_vector_path, binary = 1, unicode_errors = "ignore")
        self.cleanSetPath = cleanSetPath
        self.vectorKeys = []
        pnktu = string.punctuation + "¬"
        for word in binary_vector.vocab:
            punct_count = len([i for i in word if i in pnktu])
            if(word[0].isupper() and (punct_count == 0)):
                self.vectorKeys.append(word)

        self.set = self.__getSet()
    
    # Function to get the training set. The first parameter is the word2vec binary file path
    # and the second parameter is the path of the bio words which occur in the cleaned word2vec file.

    def __getTrainingsSet(self, binary_vector_path, cleanSetPath):
        self.__init(binary_vector_path, cleanSetPath)
        return self.set[len(self.set)//5:]

    # Function to get the test set. Same as the function above.

    def __getTestSet(self, binary_vector_path, cleanSetPath):
        self.__init(binary_vector_path, cleanSetPath)
        return self.set[:len(self.set)//5]

    # Function to select random word pairs from the amount of words which
    # don't have any punctuation. The parameter ist the number of pairs.

    def __getRandomWordPairs(self, numberOfPairs):

        words = random.sample(self.vectorKeys, numberOfPairs*2)

        word_pairs = []
        for i in range(numberOfPairs):
            word_pairs.append([words[2*i], words[2*i+1], 0])

        return word_pairs

    # Function to concate each word from the list of word pairs with random
    # words. The first parameter is the list of word pairs and the second
    # parameter is the number of random words.

    def __getWord2RandomizedWordpairs(self, word_pairs, numberOfRandoms):

        newWordPairs = []

        for  (word1, word2, _) in word_pairs:
            for i in range(numberOfRandoms):
                randomWord1 = random.choice(self.vectorKeys)
                randomWord2 = random.choice(self.vectorKeys)
                newWordPairs.append([word1, randomWord1, 0])
                newWordPairs.append([randomWord2, word2, 0])

        return newWordPairs
    
    # Function to generate a set from random words. First it generates a set of
    # random words, and then it generates random words pairs. 

    def __getSet(self):

        training_set = []

        with open(self.cleanSetPath, encoding = "utf-8") as training_set_csv:
            training_set_reader = csv.reader(training_set_csv, delimiter = "\t")

            for word_pair in training_set_reader:
                if(word_pair[0] != word_pair[1]):
                    training_set.append(word_pair)
            random.shuffle(training_set)

        part_one = training_set
        part_two = []

        part_three = self.__getRandomWordPairs(len(training_set))

        part_four = self.__getWord2RandomizedWordpairs(part_one, 5)

        all_set = part_one + part_two + part_three
        random.shuffle(all_set)

        return all_set

    # Function for exporting the test set. The first parameter is the output path,
    # the second parameter is the word2vec binary file and the third parameter
    # is the path of the bio words which occur in the cleaned word2vec file.

    def export_test_set(self, path, binary_vector_path, cleanSetPath):
        
        try:
            test_set = self.__getTestSet(binary_vector_path, cleanSetPath)
        except:
            return "Error: Wrong path or wrong file format"
        
        with open(path + "/test_set.csv", "a") as t_set:
            t_set.truncate(0)
            for word1, word2, label in test_set:
                t_set.write(word1 + "\t" + word2 + "\t" + str(label) + "\n")
        return "Done"

    # Function for exporting the training set. Same as the function above.

    def export_training_set(self, path, binary_vector_path, cleanSetPath):
        
        try:
            training_set = self.__getTrainingsSet(binary_vector_path, cleanSetPath)
        except:
            return "Error: Wrong path or wrong file format"
        
        with open(path + "/training_set.csv", "a") as t_set:
            t_set.truncate(0)
            for word1, word2, label in training_set:
                t_set.write(word1 + "\t" + word2 + "\t" + str(label) + "\n")
        return "Done"

