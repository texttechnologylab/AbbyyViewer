import os, glob, cv2, csv, graphviz, sys
from xml.etree import ElementTree
from numpy import array, load
from sklearn.tree import DecisionTreeClassifier,export_graphviz
from sklearn.feature_extraction.text import CountVectorizer

# Tool for removing text blocks from Abbyy Finereader 8.0 output file format.
# The file format must be XML.

class BlockRemover:

    def __init__(self):

        self.__trained = 0
        self.__decisiontree = DecisionTreeClassifier(min_samples_split = 4, random_state = 0)

    # Function for convertion of the gold standard csv file to a dictionary with the tuple (file name, block coordinate 1,
    # block coordinate 2) as key and the label 0 or 1 as value. The label 0 means the block should be
    # removed and the label 1 means the opposite. The parameter is the path of the csv file.

    def __csv_to_dict(self, path):

        dict = {}

        with open(path, encoding='utf-8') as csv_file:
            data = csv.reader(csv_file, delimiter = ";")
            for line in data:
                dict[(line[0], int(line[1]), int(line[2]))] = line[3] == '1'
        return dict

    # Function for calculation and returning of the vector for a text block. If the text block doesn't contain
    # any character, the function returns an empty vector only with zeroes. The parameter
    # is the text block.

    def __get_point(self, block):

        text = ""

        for char in block.findall(".//*[@characterHeight]"):
            text += char.text
        if (len(text.strip()) != 0):
            vectorizer = CountVectorizer(token_pattern = r"(?u)\b\w+\b|[^\ ]").fit([text])
            token_names = vectorizer.get_feature_names()
            token_count = vectorizer.fit_transform([text]).toarray()
            wordCount = [word for word, i in zip(token_count[0], range(len(token_names))) if token_names[i].isalpha()]
            digitCount = [digit for digit, i in zip(token_count[0], range(len(token_names))) if token_names[i].isdigit()]
            punctCount = [punct for punct, i in zip(token_count[0], range(len(token_names))) if not (token_names[i].isdigit() or token_names[i].isalpha())]
            point = [len(wordCount), len(digitCount), len(punctCount), sum(wordCount), sum(digitCount), sum(punctCount)]
            return point
        return [0, 0, 0, 0, 0, 0]

    # Function for training the decision tree. The first parameter is the training set path for the csv file, and
    # the second parameter is the path for the gold standard csv file. The gold standard file is needed for
    # the supervised learning of the decision tree.

    def train(self, training_set_path, gold_standard_path):

        points = []
        sortedGoldStandardValues = []

        try:
            training_set_paths = glob.glob(training_set_path + "/**/*.xml", recursive = 1)
        except:
            return "Error: Invalid trainingset path"

        try:
            gold_standard = self.__csv_to_dict(gold_standard_path)
        except:
            return "Error: Invalid goldStandard path"

        try:
            for path in training_set_paths:
                for block in ElementTree.parse(path).getroot().findall(".//*[@blockType='Text']"):
                    key = (os.path.splitext(os.path.basename(path))[0], int(block.attrib['l']), int(block.attrib['t']))
                    if (not key in gold_standard.keys()): continue
                    goldStandardValue = gold_standard[key]
                    point = self.__get_point(block)
                    points.append(point)
                    sortedGoldStandardValues.append(goldStandardValue)

            self.__decisiontree = self.__decisiontree.fit(array(points), array(sortedGoldStandardValues))
            self.__trained = 1
            return "Done"
        except:
            return "Error: Program terminated incorrectly"

    # Same as train function above. Only difference the training set and the gold standard are
    # binary files.

    def train_from_bin(self, training_set_path, gold_standard_path):
        
        try:
            points = load(training_set_path)
        except:
            return "Error: Wrong trainingset path or wrong format"

        try:
            sortedGoldStandardValues = load(gold_standard_path)
        except:
            return "Error: Wrong goldStandard path or wrong format"
        
        try:
            self.__decisiontree = self.__decisiontree.fit(points, sortedGoldStandardValues)
            self.__trained = 1
            return "Done"
        except:
            return "Error: Program terminated incorrectly"

    # Function for exporting the new files with the removed text blocks as XMLs. The first parameter is
    # the path of the XML files and the second parameter is the output path.

    def export_as_xml(self, xml_files_path, xml_files_clean_path):

        if (self.__trained == 0):
            return "Error: Decisiontree not trained"

        try:
            xml_files_paths = glob.glob(xml_files_path + "/**/*.xml", recursive = 1)
        except:
            return "Error: Invalid xml filepath"

        ElementTree.register_namespace("", "http://www.abbyy.com/FineReader_xml/FineReader8-schema-v2.xml")

        try:
            for path in xml_files_paths:
                xmlFileName = os.path.basename(path)
                xml_tree = ElementTree.parse(path)
                xml_root = xml_tree.getroot()
                for text in xml_root.findall(".//*[@blockType='Text']"):
                    point = self.__get_point(text)
                    if (not self.__decisiontree.predict([point])[0]):
                        xml_root[0].remove(text)
                xml_tree.write(xml_files_clean_path + "/" + xmlFileName)
            return "Done"
        except:
            return "Error: Program terminated incorrectly"

    # Function for exporting the new files with the removed text blocks as images. The first parameter is
    # the path of the image files and the second parameter is the output path. An image contains a red or
    # green block. The red color means the block should be removed, and the green color means the block
    # should be kept.

    def export_as_image(self, xml_files_path, image_files_path, image_files_clean_path):


        if (self.__trained == 0):
            return "Error: Decisiontree not trained"

        points = []

        try:
            xml_files_paths = glob.glob(xml_files_path + "/**/*.xml", recursive = 1)
        except:
            return "Error: Invalid xml file path"

        try:
            image_paths = glob.glob(image_files_path + "/**/*.jpg", recursive = 1)
        except:
            return "Error: Invald image file path"

        try:
            for path in xml_files_paths:
                xmlFileName = os.path.splitext(os.path.basename(path))[0]
                image = cv2.imread([file for file in image_paths if xmlFileName == os.path.splitext(os.path.basename(file))[0]][0])
                xml_tree = ElementTree.parse(path).getroot()
                for text in xml_tree.findall(".//*[@blockType='Text']"):
                    point = self.__get_point(text)
                    points.append(point)
                    if (not self.__decisiontree.predict([point])[0]):
                        image = cv2.rectangle(image, (int(text.attrib['l']), int(text.attrib['t'])), (int(text.attrib['r']), int(text.attrib['b'])), (0, 0, 255), 2)
                    else:
                        image = cv2.rectangle(image, (int(text.attrib['l']), int(text.attrib['t'])), (int(text.attrib['r']), int(text.attrib['b'])), (0, 255, 0), 2)
                    cv2.imwrite(image_files_clean_path + "/" + os.path.splitext(os.path.basename(path))[0] + ".jpg", image)
            return "Done"
        except:
            return "Error: Program terminated incorrectly"

    # Function for exporting the decision tree. The parameter ist the output path.

    def export_decisiontree(self, path):

        if (self.__trained == 0):
            return "Error: Decisiontree not trained"

        data = export_graphviz(self.__decisiontree)
        graph = graphviz.Source(data)

        try:
            graph.render(filename = path + "/decisiontree", format = "png")
            return "Done"
        except:
            return "Error: Program terminated incorrectly"

    # Function to calculate the score. A gold standard file is needed to compare
    # the results of the predicted labels with the evaluated labels from the file.
    # The first parameter is the path of the test set and the second parameter is
    # the path of the gold standard.

    def score(self, test_set_path, gold_standard_path):

        if (self.__trained == 0):
            return "Error: Decisiontree not trained"

        number_blocks = 0
        correct_evaluation = 0
        not_entirely_wrong_evaluation = 0

        try:
            test_set_paths = glob.glob(test_set_path + "/**/*.xml", recursive = 1)
        except:
            return "Error: Invalid testset path"

        try:
            goldStandard = self.__csv_to_dict(gold_standard_path)
        except:
            return "Error: Invalid goldStandard path"

        try:
            for path in test_set_paths:
                xmlFileName = os.path.splitext(os.path.basename(path))[0]
                for text in ElementTree.parse(path).getroot().findall(".//*[@blockType='Text']"):
                    point = self.__get_point(text)
                    number_blocks += 1
                    prediction = self.__decisiontree.predict([point])[0]
                    key = (xmlFileName, int(text.attrib['l']), int(text.attrib['t']))
                    if not key in goldStandard:
                        continue
                    expectation = goldStandard[key]
                    if (prediction == expectation):
                        correct_evaluation += 1
                    if ((prediction == expectation) or ((not prediction) and expectation)):
                        not_entirely_wrong_evaluation += 1
            return "Score: " + str((correct_evaluation / number_blocks))
        except:
            return "Error: Program terminated incorrectly"
