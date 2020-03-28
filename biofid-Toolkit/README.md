# BIOfid-Toolkit User Guide

################################################################\
The BIOfid-Toolkit is has been implemented for the internship\
"Deep Learning for Textimaging".

The BIOfid-Toolkit is a console based program written in Python.\
It provides three tools for the work with XML files created by\
the Abbyy Finereader 8.0. Abbyy Finereader is an OCR application\
developed by Abbyy for the conversion of image documents into\
editable electronic formats.

How to use:

You need the Python version 3.x.

1\. install the following dependencies: numpy, sklearn, opencv,\ 
	gensim \
2\. To start the program type "python3 BIOfid-Toolkit.py"\
   in the console.\
3\. Now you can select one of the provided tools.

################################################################

Attention: The toolkit works only with the Abbyy Finereader\
       Version 8.0

The provided tools are:

1\. BlockRemover

2\. HypernymPredictor

3\. HypernymTrainingsSetCreator

################################################################

Attention:

Every provided command in the BIOfid-Toolkit looks as below:

For example: train -parameter1 -parameter2

The word "train" is the command. Every parameter is initiated\
by the character "-". In the example above you have two\
parameters.

################################################################

The BIOfid-Toolkit provides a few error messages which signal\
you if you made for example a mistake by typing some wrong path,\
or if the program not terminated correctly. You can exit the\
console program by typing "exit" in the console and press enter.

################################################################

## BlockRemover:

Scanned text pages from books always contain text like headlines,\
page numbers, table of contents and other things. These things\
don't contribute to the information content. With this tool you\
can remove such text blocks.

How to use:

1\. You need to train the algorithm. The training\
   set consists of two files, the training_set.npy\
   and the gold_standard.npy.\
2\. You use the train_from_bin function to train.\
   If your training set consists of many Abbyy XMLs,\
   than use the train function.\
3\. Now you can use the provided functions.

If you want to generate a new training set, you\
should use the AbbyyViewer. The AbbyyViewer provides\
a function "gold" to generate a gold standard.\
You should select a number of random images and the\
associated XML files.

Gold standard: A .csv file which contains the\
           information which text block\
           should be removed.

The following methods are provided:

**************************************************\
train -parameter1 -parameter2

Description: Function for training the algorithm.

parameter 1: Name of the path of the training set.\
parameter 2: Name of the path of the gold standard\
         file.

Note: Parameter 1 is a directory. Parameter 2 is\
      a .csv file. You cant use the other methods\
      before training the algorithm.\
**************************************************\
train_from_bin -parameter1 -parameter2

Description: Function for training the algorithm.

parameter 1: Name of the path of the training set.\
parameter 2: Name of the path of the gold standard\
         file.

Note: This method differs from the train method\
      in the way that the parameters are paths\
      to .npy files. You can't use the other methods\
      before training the algorithm.\
**************************************************\
export_as_xml -parameter1 -parameter2

Description: Function for saving the cleaned\
         XML files.

parameter 1: Name of the path of the XML files.\
parameter 2: Name of the path of the cleaned XML\
             files.

Note: Parameter 1 and 2 are directories.\
**************************************************\
export_as_image -parameter1 -parameter2 -parameter3

Description: Function for saving the cleaned\
         image files.

parameter 1: Name of the path of the XML files.\
parameter 2: Name of the path of the image files.\
parameter 3: Name of the path of the cleaned image\
         output files.

Note: Parameter 1, 2 and 3 are directories.\
**************************************************\
export_decisiontree -parameter1

Description: Function for saving the decision tree.\
         Can be useful for understanding the\
         decisions made by the algorithm.

parameter 1: Name of the path of the output of the\
             decision tree.

Note: Parameter 1 is a directory. The decision tree\
      is saved as a .png file.\
**************************************************\
score -parameter1 -parameter2

Description: Function for calculating a score.\
         The score is the number of matches\
         in the decisions made by the algorithm\
         and the decisions in the gold\
         standard.

parameter 1: Name of the path of the test set.\
parameter 2: Name of the path of the gold standard.

Note: Paramter 1 is a directory and parameter 2\
      is a .csv file.

################################################################

## HypernymPredictor:

An example for a hyponym and hypernym relation is "a cat is a\
animal". In that case cat is the hyponym and animal is the\
hypernym. With this tool you can import a file with an amount\
of word2vec vectors and create a table with hyponym and hypernym\
relations.

The following methods are provided:

**************************************************\
train -parameter1 -parameter2

Description: Function for training the algorithm.

parameter 1: Name of the path of the training set.\
parameter 2: Name of the path of the word2vec file.

Note: Parameter 1 is a .csv file. Parameter 2 is\
      a binary file. You cant use the other methods\
      before training the algorithm.\
**************************************************\
predict -parameter1 -parameter2

Description: Function for predicting if a word is\
         the hypernym of an other word.

parameter 1: First word.\
parameter 2: Second word.

Note: If the second word is the hypernym of the\
      first one, you will get the boolean true.\
**************************************************\
score -parameter1

Description: Function for calculating a score.\
         The score is the number of matches\
         in the decisions made by the algorithm\
         and the decisions in the test set

parameter 1: Name of the path of the test set.

Note: The paramter is a .csv file.\
**************************************************\
export_tables -parameter1 -parameter2

Description: Function for saving the cleaned\
         image files.

parameter 1: Name of the path of the output.\
parameter 2: Name of the path of the bio words.

Note: Parameter 1 is a directory and Parameter 2 is\
      a .csv file. You get two tabels, the\
      hyponymtable and the hypernymtable. In the\
      hyponymtable the key is the hyponym and the\
      value is a list of hypernyms. The hypernymtable\
      has the hypernym as a key and the number of\
      hyponyms as the values. For example a row in\
      the hypernymtable could be "cat : animal".\
      The bio words are words which occur in the\
      word2vec file.

################################################################

## HypernymTrainingsSetCreator:

This tool provides functions for creating a training set and a\
test set for the HypernymPredictor.

The following methods are provided:

**************************************************\
export_test_set -parameter1 -parameter2 -parameter3

Description:

parameter 1: Name of the path of the output.\
parameter 2: Name of the path of the word2vec file.\
parameter 3: Name of the clean set path.

Note: Parameter 1 is a directory, parameter 2 is a\
      binary file and paramater 3 is a .csv file.\
      The clean set is a number of biological taxa\
      which appear in the cleaned word2vec file.

**************************************************\
export_training_set -parameter1 -parameter2 -parameter3

Description:

parameter 1: Name of the path of the output.\
parameter 2: Name of the path of the word2vec file.\
parameter 3: Name of the clean set path.

Note: Parameter 1 is a directory, parameter 2 is a\
      binary file and paramater 3 is a .csv file.\
      The clean set is a number of biological taxa\
      which appear in the cleaned word2vec file.
