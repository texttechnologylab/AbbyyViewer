import csv, random, string
from sklearn.svm import SVC
from gensim.models import KeyedVectors

# Tool for the prediction of possible hypernym and hyponym relations. 

class HypernymPredictor:

    def __init__(self):
        self.trained = 0

    # Function for converting the bio words csv file to a list of biological
    # taxa. The parameter is the path of the bio words.

    def __getBioWords(self, bioWordsPath):
        if(len(self._bioWords) > 0):
            return self._bioWords
        with open(bioWordsPath, encoding='utf-8') as bio_words_csv:
            bio_words = csv.reader(bio_words_csv, delimiter = "\t")
            for (word, url) in bio_words:
                self._bioWords.append(word)
        return self._bioWords

    # Function for the training of the support vector machine classifier. The first parameter
    # ist the path of the training set. The second parameter is the path of the word2vec file.
    # The file must be a binary file.

    def train(self, source_training_set, binary_vector_path):
        
        try:    
            self.classifier = SVC(kernel = "rbf", C = 10, gamma = 0.1)
            self.binary_vector = KeyedVectors.load_word2vec_format(binary_vector_path, binary = 1, unicode_errors = "ignore")
            self._bioWords = []
        except:
            return "Error: Wrong vector path or wrong file format"

        labels = []
        sub_vectors = []

        try:
            with open(source_training_set, encoding='utf-8') as training_set_csv:
                training_set = csv.reader(training_set_csv, delimiter = "\t")

                for word_pair in training_set:
                    try:
                        sub_vectors.append(self.binary_vector[word_pair[0]] - self.binary_vector[word_pair[1]])
                        labels.append(int(word_pair.pop()))
                    except:
                        pass

            self.classifier.fit(sub_vectors, labels)
            self.trained = 1
        except:
            return "Error: Program terminated incorrectly"
        
        return "Done"

    # Function for the prediction of a possible hypernym and hyponym relation. The
    # first parameter ist the hyponym and the second parameter is the hypernym.
    # If the function returns true, the second parameter is the hypernym of the
    # first one.

    def predict(self, hyponym, hypernym):

        if (not self.trained):
            return "Error: Support Vector Machine not trained"
        
        try:
            vector1 = self.binary_vector[hyponym]
            vector2 = self.binary_vector[hypernym]

            diff = vector1 - vector2
        except:
            return "Error: Program terminated incorrectly"
        return bool(self.classifier.predict([diff])[0])

    # Function for calculation of the score. The parameter ist the path of
    # the test set. The labels in the test set are compared with the
    # predicted labels of the support vector machine classifier and the
    # percentage share of matches is calculated.

    def score(self, source_test_set):

        if (not self.trained):
            return "Error: Support Vector Machine not trained"

        right = 0
        length = 0

        try:
            with open(source_test_set, encoding='utf-8') as test_set_csv:
                test_set = csv.reader(test_set_csv, delimiter = "\t")
                for word1, word2, label in test_set:
                    try:
                        vector1 = self.binary_vector[word1]
                        vector2 = self.binary_vector[word2]
                        a = self.classifier.predict([vector1 - vector2])[0]
                        if (a == int(label)):
                            right += 1
                        length += 1
                    except:
                        pass
        except:
            return "Error: Program terminated incorrectly"
        return "Score: " + str(right/length)


    # Function for generating the hyponym and hypernym tables. The parameter
    # is the path of the bio words.

    def __getHypoTables(self, bioWordsPath):

        hyponymTable = {}
        hypernymTable = {}

        def addToHyponymTable(hyponym, hypernym):
            if(hyponym in hyponymTable):
                hyponymTable[hyponym].append(hypernym)
            else:
                hyponymTable[hyponym] = [hypernym]

        def addToHypernymTable(hyponym, hypernym):
            if(hypernym in hypernymTable):
                hypernymTable[hypernym].append(hyponym)
            else:
                hypernymTable[hypernym] = [hyponym]

        words = self.__getBioWords(bioWordsPath)
        
        for i in range(len(words)):
            for j in range(i + 1, len(words)):
                (word_x, word_y) = (words[i], words[j])
                if(self.predict(word_x, word_y)):
                    addToHypernymTable(word_x, word_y)
                if(self.predict(word_y, word_x)):
                    addToHyponymTable(word_x, word_y)

        return (hyponymTable, hypernymTable)

    # Function for saving the tables as a file. The first parameter is the
    # table and the second parameter is the output path.

    def __exportHypoTable(self, hypoTable, path):
        with open(path, "a") as hypoFile:
            hypoFile.truncate(0)
            for key in hypoTable.keys():
                line = key + ": " + ", ".join(hypoTable[key]) + "\n"
                hypoFile.write(line)

    # Function for saving the tables. The first parameter ist the output
    # file, and the second parameter is the path of the bio words.

    def export_tables(self, path, bioWordsPath):
        
        try:
            (h1, h2) = self.__getHypoTables(bioWordsPath)
        except:
            return "Error: Wrong bio words path"
        
        try:
            self.__exportHypoTable(h1, path + "/hyponymtable.table")
            self.__exportHypoTable(h2, path + "/hypernymtable.table")
        except:
            return "Error: Program terminated incorrectly"
        return "Done"
