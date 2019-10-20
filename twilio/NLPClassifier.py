# Change it on the way.
# Change this later.
import numpy as np
import re
import nltk
import pickle
from nltk.stem.snowball import SnowballStemmer

with open("../data/nlp3_fluonlywords.pkl", 'rb') as pickle_file:
    flu_only_set = pickle.load(pickle_file)
with open("../data/nlp3_mentalonlywords.pkl", 'rb') as pickle_file:
    mental_only_set = pickle.load(pickle_file)
with open("../data/nlp3_mentaldrugwords.pkl", 'rb') as pickle_file:
    mental_drug_set = pickle.load(pickle_file)
with open("../data/nlp3_fludrugwords.pkl", 'rb') as pickle_file:
    flu_drug_set = pickle.load(pickle_file)
with open("../data/nlp3_drugonlywords.pkl", 'rb') as pickle_file:
    drug_only_set = pickle.load(pickle_file)
with open("../data/nlp3_allthreewords.pkl", 'rb') as pickle_file:
    all_three_set = pickle.load(pickle_file)

snowBallStemmer = SnowballStemmer("english")

class NLPClassifier():
    """Smart classifier that takes text using NLP and returns if the person should go to 
       a vaccination place or a hospital. This model uses core stems of the words.
       
       Args:
         text: The statement from the customer about their queries. String.
       
       Functions:
         flu_weight: Computes the weights for flu label. Double.
         drug_weight: Computes the weights for drug label. Double.
         mental_weight: Computes the weights for mental label. Double.
         classify: Compares weights and returns labels for "flu", "drug", "mental", and "neighter"
       
       Usage:
         clf = NLPClassifier("sample text")
         label = clf.classify()
         
    """
    def __init__(self, text):
        self.text = text
    
    def flu_weight(self):
        text = self.text
        wordList = nltk.word_tokenize(text)
        words = [snowBallStemmer.stem(word) for word in wordList]
        word_weight = 0
        for w in words:
            if w in flu_drug_set:
                word_weight+=1.5
            elif w in flu_only_set:
                word_weight+=2
            elif w in all_three_set:
                word_weight+=1
        return word_weight

    def drug_weight(self):
        text = self.text
        wordList = nltk.word_tokenize(text)
        words = [snowBallStemmer.stem(word) for word in wordList]
        word_weight = 0
        for w in words:
            if w in flu_drug_set:
                word_weight+=1.5
            elif w in drug_only_set or w in mental_drug_set:
                word_weight+=2
            elif w in all_three_set:
                word_weight+=1
        return word_weight

    def mental_weight(self):
        text = self.text
        wordList = nltk.word_tokenize(text)
        words = [snowBallStemmer.stem(word) for word in wordList]
        word_weight = 0
        for w in words:
            print(w)
            if w in mental_only_set:
                word_weight+=2
            elif w in mental_drug_set:
                word_weight+=1.5
            elif w in all_three_set:
                word_weight+=1
        return word_weight




    def classify(self):
        flu, drug, mental = self.flu_weight(), self.drug_weight(), self.mental_weight() 
        max_weight = max(flu, drug, mental)
        if drug == 0 and flu ==0 and mental==0:
            return "neither"
        elif drug == max_weight:
            return "drug"
        elif flu == max_weight:
            return "flu"
        else:
            return "mental"