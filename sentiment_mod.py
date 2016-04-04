import nltk
import random
#from nltk.corpus import movie_reviews
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import math
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from _overlapped import NULL
from nltk import tokenize



class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
            print(c)
            print(v)
#         votes.append('negative')
        
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        votes.append('negative')
        choice_votes = votes.count(mode(votes))
        conf = float(choice_votes / len(votes))
#         conf=float(sum(choice_votes))/math.sqrt(len(votes))
        return conf
    

    
documents_f = open("pickled_algos/documents.pickle", "rb")
documents = pickle.load(documents_f)
documents_f.close()




word_features5k_f = open("pickled_algos/word_features5k.pickle", "rb")
word_features = pickle.load(word_features5k_f)
word_features5k_f.close()

stop_words=set(stopwords.words("english"))
allowed_word_types = ["J","R","V"]
# allowed_word_types = ["J","V"]

def find_features(document):
    all_words=[]
    tokenizer_reg = RegexpTokenizer(r'\w+')
    features={}
    words=tokenizer_reg.tokenize(document)
    filtered_sentence=[]
    for w in words:
        if w not in stop_words:
            filtered_sentence.append(w)
    features = {}
    lemmatizer = WordNetLemmatizer()
    lemma_words=[]
    for w in filtered_sentence:
        lemma_words.append(lemmatizer.lemmatize(w))
    pos = nltk.pos_tag(lemma_words)
    
    for w in pos:
        if w[1][0] in allowed_word_types:
            all_words.append(w[0].lower())

    if len(all_words) is 0:
        return features;
    for w in word_features:
        features[w] = (w in  all_words)
    return features



featuresets_f = open("pickled_algos/featuresets.pickle", "rb")
featuresets = pickle.load(featuresets_f)
featuresets_f.close()

random.shuffle(featuresets)
print(len(featuresets))

testing_set = featuresets[10000:]
training_set = featuresets[:10000]



open_file = open("pickled_algos/originalnaivebayes5k.pickle", "rb")
classifier = pickle.load(open_file)
open_file.close()


open_file = open("pickled_algos/MNB_classifier5k.pickle", "rb")
MNB_classifier = pickle.load(open_file)
open_file.close()



open_file = open("pickled_algos/BernoulliNB_classifier5k.pickle", "rb")
BernoulliNB_classifier = pickle.load(open_file)
open_file.close()


open_file = open("pickled_algos/LogisticRegression_classifier5k.pickle", "rb")
LogisticRegression_classifier = pickle.load(open_file)
open_file.close()


open_file = open("pickled_algos/LinearSVC_classifier5k.pickle", "rb")
LinearSVC_classifier = pickle.load(open_file)
open_file.close()


open_file = open("pickled_algos/SGDC_classifier5k.pickle", "rb")
SGDC_classifier = pickle.load(open_file)
open_file.close()




voted_classifier = VoteClassifier(classifier,
                                  LinearSVC_classifier,
                                  SGDC_classifier,
#                                   MNB_classifier,
                                  BernoulliNB_classifier,
                                  LogisticRegression_classifier)




def sentiment(text):
    feats = find_features(text)
    return voted_classifier.classify(feats)

def sentivalue(text):
    arr_text= tokenize.sent_tokenize(text)
    for w in arr_text:
        feats = find_features(w)
        print(w)
        if not feats:
            print("naah")
        else:
            feats = find_features(text)
            print(voted_classifier.classify(feats))
        
        

def getFindFeatures(text):
    feats=find_features(text)
    return feats

def getClassify(feats):
    if not feats:
        return "neutral"
    return voted_classifier.classify(feats)

def getConfidence(feats):
    if not feats:
        return 0
    classify= voted_classifier.classify(feats)
    conf=voted_classifier.confidence(feats)
    if (classify in "negative"):
        return -1
    return 1

def value_of(sentiment):
        if sentiment == 'positive': return 1
        if sentiment == 'negative': return -1
        return 0
        

    
def sentence_score(sentence_tokens, previous_token, acum_score):    
    if not sentence_tokens:
        return acum_score
    else:
        current_token = sentence_tokens[0]
        tags = current_token[2]
        token_score = sum([value_of(tag) for tag in tags])
        if previous_token is not None:
            previous_tags = previous_token[2]
            if 'inc' in previous_tags:
                token_score *= 2.0
            elif 'dec' in previous_tags:
                token_score /= 2.0
            elif 'inv' in previous_tags:
                token_score *= -1.0
        return sentence_score(sentence_tokens[1:], current_token, acum_score + token_score)

def sentiment_score(review):
    return sum([sentence_score(sentence, None, 0.0) for sentence in review])
