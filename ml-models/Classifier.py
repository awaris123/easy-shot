# Change this later.
import numpy as np
import re
import sklearn as sk
import pickle

with open("../data/fluonlywords.pkl", 'rb') as pickle_file:
    flu_only_set = pickle.load(pickle_file)
with open("../data/flugeneralwords.pkl", 'rb') as pickle_file:
    flu_general_set = pickle.load(pickle_file)
with open("../data/generalwords.pkl", 'rb') as pickle_file:
    general_set = pickle.load(pickle_file)



class Classifier():
    """Smart classifier that takes text and returns if the person should go to 
       a vaccination place or a hospital.
       
       Args:
         text: The statement from the customer about their queries. String.
       
       Functions:
         flu_weight: Computes the weights for flu label. Double.
         general_weight: Computer the weights for general label. Double.
         classify: Compares weights and returns labels for "flu", "general", "none"
       
       Usage:
         clf = Classifier("sample text")
         label = clf.classify()
         
    """
    def __init__(self, text):
        self.text = text
        
    def flu_weight(self):
        words = parser(self.text)
        word_count = 0
        for w in words:
            if w in flu_general_set:
                word_count+=1
            elif w in flu_set:
                word_count+=1.5
        return word_count

    def general_weight(self):
        words = parser(self.text)
        word_count = 0
        for w in words:
            if w in flu_general_set:
                word_count+=1
            elif w in general_set:
                word_count+=1.5
        return word_count


    def classify(self):
        gen, flu = general_weight(self.text), flu_weight(self.text)
        if gen == 0 and flu ==0:
            return "none"
        elif flu >= gen:
            return "flu"
        else:
            return "general"