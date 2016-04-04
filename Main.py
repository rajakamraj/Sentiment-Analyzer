
#!/usr/bin/env python

import sys,time,os
import sentiment_mod as s
import DB_manager as db
import alchemyapi as al
import nltk
import errno
import random
from nltk.corpus import movie_reviews 
from nltk.classify.scikitlearn import SklearnClassifier
import pickle 
from pygooglechart import *
from sklearn.naive_bayes import MultinomialNB,GaussianNB,BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC,LinearSVC,NuSVC

from nltk.classify import ClassifierI
from statistics import mode
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Login_Dialog.ui'
#
# Created: Mon Nov 24 22:47:39 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from distutils.command.check import check
from _overlapped import NULL
from itertools import cycle
from DesktopApp.alchemyapi import AlchemyAPI

alchemyapi = al.AlchemyAPI()

DEFAULT_COLORS = [0x3366cc, 0xdc3912, 0xff9900, 0x109618, 0x990099,
                  0x0099c6, 0xdd4477, 0x66aa00, 0xb82e2e, 0x316395,
                  0x994499, 0x22aa99, 0xaaaa11, 0x6633cc, 0x16d620]
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

bookName=[]
reviewerName=[]
reviewerReview=[]

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.toolBar=self.addToolBar("Home")
        self.setWindowTitle("Sentiment Analyzer")
        self.central_widget = QtGui.QStackedWidget()
        self.setCentralWidget(self.central_widget)
        login_widget = Ui_Login(self)
#         login_widget.button.clicked.connect(self.login)
        self.central_widget.addWidget(login_widget)
        
    def loginSuccessful(self):
        print('Login OK')
        logged_in_widget = Ui_Form(self)
        self.parent().central_widget.addWidget(logged_in_widget)
        self.parent().central_widget.setCurrentWidget(logged_in_widget)
        
    def backToLogin(self):
        print('Login again OK')
        self.toolBar.clear()
        logged_in_widget = Ui_Form(self)

        self.central_widget.addWidget(logged_in_widget)
        self.central_widget.setCurrentWidget(logged_in_widget)   
        
    def resultWindow(self):
        print('Result OK')    
        result_widget=ResultWidget(self)
        extractAction = QtGui.QAction(QtGui.QIcon('home.png'), 'Go to Home', self)
        extractAction.triggered.connect(self.parent().backToLogin)
        self.parent().toolBar.addAction(extractAction)

        self.parent().central_widget.addWidget(result_widget)
        self.parent().central_widget.setCurrentWidget(result_widget)
        
#     @QtCore.pyqtSignature("on_extractAction_clicked()")
#     def goToHome(self):
#         MainWindow.loginSuccessful(self)           
class Ui_Login(QtGui.QWidget):
    def __init__(self,parent=None):
        super(Ui_Login, self).__init__(parent)
        db.tableName='masterTable'
        self.dbu = db.DatabaseUtility('UsernamePassword_DB', 'masterTable')
        self.setupUi(self)
        self.confirm = None
        
    def setupUi(self, Login_Dialog):
        Login_Dialog.setObjectName(_fromUtf8("Login_Dialog"))
        Login_Dialog.resize(285, 134)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Login_Dialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(Login_Dialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.user_lineEdit = QtGui.QLineEdit(self.groupBox)
        self.user_lineEdit.setObjectName(_fromUtf8("user_lineEdit"))
        self.horizontalLayout.addWidget(self.user_lineEdit)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.password_lineEdit = QtGui.QLineEdit(self.groupBox)
        self.password_lineEdit.setInputMask(_fromUtf8(""))
        self.password_lineEdit.setText(_fromUtf8(""))
        self.password_lineEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.password_lineEdit.setObjectName(_fromUtf8("password_lineEdit"))
        self.horizontalLayout_2.addWidget(self.password_lineEdit)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.newUser_btn = QtGui.QPushButton(self.groupBox)
        self.newUser_btn.setObjectName(_fromUtf8("newUser_btn"))
        self.horizontalLayout_4.addWidget(self.newUser_btn)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.login_btn = QtGui.QPushButton(self.groupBox)
        self.login_btn.setObjectName(_fromUtf8("login_btn"))
        self.horizontalLayout_4.addWidget(self.login_btn)
        self.cancel_btn = QtGui.QPushButton(self.groupBox)
        self.cancel_btn.setObjectName(_fromUtf8("cancel_btn"))
        self.horizontalLayout_4.addWidget(self.cancel_btn)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.verticalLayout.addWidget(self.groupBox)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Login_Dialog)
        QtCore.QMetaObject.connectSlotsByName(Login_Dialog)

    def retranslateUi(self, Login_Dialog):
        Login_Dialog.setWindowTitle(_translate("Login_Dialog", "Sentiment Analyzer User Login", None))
        self.groupBox.setTitle(_translate("Login_Dialog", "Enter your credentials", None))
        self.label.setText(_translate("Login_Dialog", "Username", None))
        self.label_2.setText(_translate("Login_Dialog", "Password", None))
        self.newUser_btn.setText(_translate("Login_Dialog", "New User", None))
        self.login_btn.setText(_translate("Login_Dialog", "Login", None))
        self.cancel_btn.setText(_translate("Login_Dialog", "Cancel", None))


    @QtCore.pyqtSignature("on_cancel_btn_clicked()")
    def Cancel_btn(self):
        sys.exit()

    @QtCore.pyqtSignature("on_login_btn_clicked()")
    def Login_btnLogin_btn(self):
        username = self.user_lineEdit.text()
        password = self.password_lineEdit.text()
        if not username:
            QtGui.QMessageBox.warning(self, 'Error', 'Username Missing!')
        elif not password:
            QtGui.QMessageBox.warning(self, 'Error', 'Password Missing!')
        else:
            self.AttemptLogin(username, password)

    def AttemptLogin(self, username, password):
        t = self.dbu.GetTable()
        print (t)
        for col in t:
            if username == col[1]:
                if password == col[2]:
                    QtGui.QMessageBox.information(self, 'Success!', 'Password verified!!')
                    MainWindow.loginSuccessful(self.parent())

                else:
                    QtGui.QMessageBox.warning(self, 'Error!', 'Password incorrect...')
                    return

    @QtCore.pyqtSignature("on_newUser_btn_clicked()")
    def NewUser_btn(self):
        self.newUser = Ui_Register(self.dbu)
        self.newUser.show()

class Ui_Register(QtGui.QDialog):
    def __init__(self, dbu):
        QtGui.QDialog.__init__(self)
        db.tableName='masterTable'
        self.setupUi(self)
        self.dbu = dbu

    def setupUi(self, Register_Dialog):
        Register_Dialog.setObjectName(_fromUtf8("Register_Dialog"))
        Register_Dialog.resize(372, 187)
        Register_Dialog.setModal(True)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Register_Dialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(Register_Dialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.username_lineEdit = QtGui.QLineEdit(self.groupBox)
        self.username_lineEdit.setObjectName(_fromUtf8("username_lineEdit"))
        self.horizontalLayout.addWidget(self.username_lineEdit)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.password_lineEdit = QtGui.QLineEdit(self.groupBox)
        self.password_lineEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.password_lineEdit.setObjectName(_fromUtf8("password_lineEdit"))
        self.horizontalLayout_2.addWidget(self.password_lineEdit)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_4.addWidget(self.label_3)
        self.confirmPassword_lineEdit = QtGui.QLineEdit(self.groupBox)
        self.confirmPassword_lineEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.confirmPassword_lineEdit.setObjectName(_fromUtf8("confirmPassword_lineEdit"))
        self.horizontalLayout_4.addWidget(self.confirmPassword_lineEdit)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_3.addWidget(self.label_4)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.add_btn = QtGui.QPushButton(self.groupBox)
        self.add_btn.setObjectName(_fromUtf8("add_btn"))
        self.horizontalLayout_3.addWidget(self.add_btn)
        self.cancel_btn = QtGui.QPushButton(self.groupBox)
        self.cancel_btn.setObjectName(_fromUtf8("cancel_btn"))
        self.horizontalLayout_3.addWidget(self.cancel_btn)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addWidget(self.groupBox)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Register_Dialog)
        QtCore.QMetaObject.connectSlotsByName(Register_Dialog)

    def retranslateUi(self, Register_Dialog):
        Register_Dialog.setWindowTitle(_translate("Register_Dialog", "Register New User", None))
        self.groupBox.setTitle(_translate("Register_Dialog", "User Registration", None))
        self.label_2.setText(_translate("Register_Dialog", "Username", None))
        self.label.setText(_translate("Register_Dialog", "Password", None))
        self.label_3.setText(_translate("Register_Dialog", "Confirm Password", None))
        self.label_4.setText(_translate("Register_Dialog", "********************************************", None))
        self.add_btn.setText(_translate("Register_Dialog", "Add", None))
        self.cancel_btn.setText(_translate("Register_Dialog", "Cancel", None))


    @QtCore.pyqtSignature("on_cancel_btn_clicked()")
    def Cancel_btn(self):
        self.close()

    @QtCore.pyqtSignature("on_add_btn_clicked()")
    def Add_btn(self):
        username = self.username_lineEdit.text()
        password = self.password_lineEdit.text()
        cpassword = self.confirmPassword_lineEdit.text()
        if not username:
            QtGui.QMessageBox.warning(self, 'Error!', 'Username Missing')
        elif password != cpassword:
            QtGui.QMessageBox.warning(self, 'Error!', 'Passwords Do Not Match')
        else:
            t = self.dbu.GetTable()
            print (t)
            for col in t:
                if username == col[1]:
                    QtGui.QMessageBox.warning(self, 'Error!', 'Username Taken. :(')
            else:
                self.dbu.AddEntryToTable (username, password)
                QtGui.QMessageBox.information(self, 'Success!!', 'User Added SUCCESSFULLY!')
                self.close()


class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifier = classifiers
    
    def classify(self,features):
        votes=[]
        for c in self._classifier:
            v=c.classify(features)
            votes.append(v)
        votes.append("pos")    
        return mode(votes)
    
    def confidence(self,features):
        votes=[]
        for c in self._classifier:
            v=c.classify(features)
            votes.append(v)
        votes.append("pos") 
        choice_votes=votes.count(mode(votes))
        conf=choice_votes / len(votes)
        return conf
    


documents = [(list(movie_reviews.words(fileid)), category)
             for category in movie_reviews.categories()
             for fileid in movie_reviews.fileids(category)]


random.shuffle(documents)

all_words=[]
for w in movie_reviews.words():
    all_words.append(w.lower())
    
all_words=nltk.FreqDist(all_words)

word_features =list(all_words.keys())[:3000]

def find_features(document):
    words = set (document)
    features={}
    for w in word_features:
        features[w]=(w in words)
    
    return features



class Ui_Form(QtGui.QWidget):
    def __init__(self,parent=None):
        super(Ui_Form, self).__init__(parent)
        db.tableName='reviewDetails'
#         self.dbu = db.DatabaseUtility('UsernamePassword_DB', 'masterTable')
        self.setupUi(self)
        self.confirm = None
        
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(505, 416)
        self.browseFile = QtGui.QPushButton(Form)
        self.browseFile.setGeometry(QtCore.QRect(180, 320, 101, 31))
        self.browseFile.setObjectName(_fromUtf8("browseFile"))
        self.radioNaiveBayes = QtGui.QRadioButton(Form)
        self.radioNaiveBayes.setGeometry(QtCore.QRect(160, 40, 191, 17))
        self.radioNaiveBayes.setObjectName(_fromUtf8("radioNaiveBayes"))
        self.radioMNB = QtGui.QRadioButton(Form)
        self.radioMNB.setGeometry(QtCore.QRect(160, 70, 82, 17))
        self.radioMNB.setObjectName(_fromUtf8("radioMNB"))
        self.radioBernoulliNB = QtGui.QRadioButton(Form)
        self.radioBernoulliNB.setGeometry(QtCore.QRect(160, 100, 191, 17))
        self.radioBernoulliNB.setObjectName(_fromUtf8("radioBernoulliNB"))
        self.radioLogisticRegression = QtGui.QRadioButton(Form)
        self.radioLogisticRegression.setGeometry(QtCore.QRect(160, 130, 191, 17))
        self.radioLogisticRegression.setObjectName(_fromUtf8("radioLogisticRegression"))
        self.radioSGDClassifier = QtGui.QRadioButton(Form)
        self.radioSGDClassifier.setGeometry(QtCore.QRect(160, 160, 131, 17))
        self.radioSGDClassifier.setObjectName(_fromUtf8("radioSGDClassifier"))
        self.radioSVC = QtGui.QRadioButton(Form)
        self.radioSVC.setGeometry(QtCore.QRect(160, 190, 101, 17))
        self.radioSVC.setObjectName(_fromUtf8("radioSVC"))
        self.radioLinearSVC = QtGui.QRadioButton(Form)
        self.radioLinearSVC.setGeometry(QtCore.QRect(160, 220, 141, 17))
        self.radioLinearSVC.setObjectName(_fromUtf8("radioLinearSVC"))
        self.radioAlchemyAPI = QtGui.QRadioButton(Form)
        self.radioAlchemyAPI.setGeometry(QtCore.QRect(160, 250, 141, 17))
        self.radioAlchemyAPI.setObjectName(_fromUtf8("radioAlchemyAPI"))
        self.radioVoted = QtGui.QRadioButton(Form)
        self.radioVoted.setGeometry(QtCore.QRect(160, 280, 141, 17))
        self.radioVoted.setObjectName(_fromUtf8("radioVoted"))
        self.startAnalysis = QtGui.QPushButton(Form)
        self.startAnalysis.setGeometry(QtCore.QRect(180, 320, 101, 31))
        self.startAnalysis.setObjectName(_fromUtf8("startAnalysis"))
        homelayout = QtGui.QHBoxLayout(self)
        homeGridLayout = QtGui.QGridLayout(self)
        homeGridLayout.addWidget(self.browseFile)
        homeGridLayout.addWidget(self.radioNaiveBayes)
        homeGridLayout.addWidget(self.radioMNB)
        homeGridLayout.addWidget(self.radioBernoulliNB)
        homeGridLayout.addWidget(self.radioLogisticRegression)
        homeGridLayout.addWidget(self.radioSGDClassifier)
        homeGridLayout.addWidget(self.radioSVC)
        homeGridLayout.addWidget(self.radioLinearSVC)
        homeGridLayout.addWidget(self.radioAlchemyAPI)
        homeGridLayout.addWidget(self.radioVoted)
        homeGridLayout.addWidget(self.startAnalysis)
        homelayout.addStretch(1)
        homelayout.addLayout(homeGridLayout)
        homelayout.addStretch(1)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        self.browseFile.setToolTip(_translate("Form", "Click here to open the file", None))
        self.browseFile.setText(_translate("Form", "Browse", None))
       
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.radioNaiveBayes.setToolTip(_translate("Form", "Naive bayes classifier", None))
        self.radioNaiveBayes.setText(_translate("Form", "Naive bayes classifier", None))
        self.radioMNB.setToolTip(_translate("Form", "MNB classifier", None))
        self.radioMNB.setText(_translate("Form", "MNB classifier", None))
        self.radioBernoulliNB.setToolTip(_translate("Form", "Bernoulli Naive Bayes Classifier", None))
        self.radioBernoulliNB.setText(_translate("Form", "Bernoulli Naive Bayes Classifier", None))
        self.radioLogisticRegression.setToolTip(_translate("Form", "Logistic Regression classifier", None))
        self.radioLogisticRegression.setText(_translate("Form", "Logistic Regression classifier", None))
        self.radioSGDClassifier.setToolTip(_translate("Form", "SGD Classifier", None))
        self.radioSGDClassifier.setText(_translate("Form", "SGD Classifier", None))
        self.radioSVC.setToolTip(_translate("Form", "SVC classifier", None))
        self.radioSVC.setText(_translate("Form", "SVC classifier", None))
        self.radioLinearSVC.setToolTip(_translate("Form", "Linear SVC classifier", None))
        self.radioLinearSVC.setText(_translate("Form", "Linear SVC classifier", None))
        self.radioAlchemyAPI.setToolTip(_translate("Form", "Alchemy API", None))
        self.radioAlchemyAPI.setText(_translate("Form", "Alchemy API", None))
        self.radioVoted.setToolTip(_translate("Form", "Ensemble Learning", None))
        self.radioVoted.setText(_translate("Form", "Ensemble Learning", None))
        self.startAnalysis.setToolTip(_translate("Form", "Click here to start the sentimental anaysis", None))
        self.startAnalysis.setText(_translate("Form", "Start Analysis", None))
       
#         self.startAnalysis.clicked.connect(self.parent().printh)
    @QtCore.pyqtSignature("on_browseFile_clicked()")  
    def browseFiles(self):
        name = QtGui.QFileDialog.getOpenFileName(self, 'Open File')
        print(name)
        if( name):
            file = open(name,'r')
            reviews=file.read()
            i=0;
            for reviewline in reviews.split('\n'):
                if(reviewline):
                    
                    print(reviewline)
                    book_details = reviewline[0:reviewline.index("\t")]
                    print(book_details)
                    book_id,bookNameValue=book_details.split('#####')
                    bookName.append(bookNameValue)
                    print(bookName)
                    review_details = reviewline[reviewline.index("\t"):].strip();
                    print(review_details)
                    reviewerNameValue = review_details[review_details.index("#####")+5:review_details.index("^^^^^")]
                    print(reviewerNameValue)
                    reviewerName.append(reviewerNameValue)
                    reviewerReviewValue = review_details[review_details.index("^^^^^")+5:].strip()  
                    print(reviewerReviewValue)   
                    reviewerReview.append(reviewerReviewValue)
#                 for splitword in reviewline.split('#####'):
#                     print(splitword)
#                     bookName[i] = splitword[1];
#                     for userreview in splitword[2].split('^^^^^'):
#                         reviewerName[i]=userreview[0];
#                         reviewerReview[i]=userreview[1];
#             for line in f1:
#                 book_details = line[0:line.index("\t")];
#                 book_id = book_details[0:line.index("#####")];
#                 book_name = book_details[line.index("#####")+5 :];
#                 review_details = line[line.index("\t"):].strip();
#                 reviewer_id = review_details[0:review_details.index("#####")]
#                 reviewer_name = review_details[review_details.index("#####")+5:review_details.index("^^^^^")]
#                 review_text = review_details[review_details.index("^^^^^")+5:].strip()       
#                     
                i=i+1  
            file.close() 
            
        
        
        
            
    @QtCore.pyqtSignature("on_startAnalysis_clicked()")   
    def printh(self):
        try:
            selectedRadio=''
            if(self.radioNaiveBayes.isChecked()):
                selectedRadio='naivebayes'
            elif(self.radioMNB.isChecked()):
                selectedRadio='mnb'
            elif(self.radioBernoulliNB.isChecked()):
                selectedRadio='bernoullinb'
            elif(self.radioLogisticRegression.isChecked()):
                selectedRadio='logisticregression'
            elif(self.radioSGDClassifier.isChecked()):
                selectedRadio='sgd'
            elif(self.radioSVC.isChecked()):
                selectedRadio='svc'
            elif(self.radioLinearSVC.isChecked()):
                selectedRadio='linearsvc'
            elif(self.radioAlchemyAPI.isChecked()):
                selectedRadio='alchemy'
            elif(self.radioVoted.isChecked()):
                selectedRadio='ensemble'
                
            if(selectedRadio is ''):
                QtGui.QMessageBox.warning(self, 'Error!', 'You have not selected any classifiers')
                return   
            
            i=0;
            print(len(bookName))
            self.dbu = db.DatabaseUtility('UsernamePassword_DB', 'reviewDetails')
            self.dbu.tableName='reviewDetails'
            for i in range(len(bookName)):
                print(bookName.__getitem__(i))
                if(selectedRadio in ('alchemy')):
                    response = alchemyapi.sentiment("text", reviewerReview.__getitem__(i))
                    review_type =response["docSentiment"]["type"]
                    if(review_type in  ('positive','negative')):
                        sentimentValue= review_type
                    else:
                        sentimentValue='positive'
                else:
                    sentimentValue=s.sentiment(reviewerReview.__getitem__(i))
                if(not sentimentValue):
                    sentimentValue='positive'
                self.dbu.AddEntryToTableReview(bookName.__getitem__(i),reviewerName.__getitem__(i),reviewerReview.__getitem__(i),sentimentValue.__str__())
                i=i+1
        except IOError as exc:
            if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
                raise  
        MainWindow.resultWindow(self.parent())
#         featuresets =[(find_features(rev), category) for (rev,category) in documents]
# 
#         training_set =featuresets[100:]
#         testing_set = featuresets[:100]
# 
#         classifier = nltk.NaiveBayesClassifier.train(training_set)
#         print("Naive bayes accuracy percent:",(nltk.classify.accuracy(classifier,testing_set))*100)
# 
#         classifier.show_most_informative_features(15)
#  
#         save_classifier =open("naivebayes.pickle","wb")
#         pickle.dump(classifier,save_classifier)
#         save_classifier.close()
#     
#         MNB_classifier = SklearnClassifier(MultinomialNB())
#         MNB_classifier.train(training_set)
#         print("MNB Accuracy accuracy percent:",(nltk.classify.accuracy(MNB_classifier,testing_set))*100)
#          
#     # GaussianNB_classifier = SklearnClassifier(GaussianNB())
#     # GaussianNB_classifier.train(training_set)
#     # print("Gaussian Accuracy accuracy percent:",(nltk.classify.accuracy(GaussianNB_classifier,testing_set))*100)
#     
#         BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
#         BernoulliNB_classifier.train(training_set)
#         print("BernoulliNB_classifier Accuracy accuracy percent:",(nltk.classify.accuracy(BernoulliNB_classifier,testing_set))*100)
#         
#         LogisticRegression_classifier =SklearnClassifier(LogisticRegression())
#         LogisticRegression_classifier.train(training_set)
#         print("LogisticRegression_classifier Accuracy accuracy percent:",(nltk.classify.accuracy(LogisticRegression_classifier,testing_set))*100)
#         
#         
#         SGDClassifier_classifier =SklearnClassifier(SGDClassifier())
#         SGDClassifier_classifier.train(training_set)
#         print("SGDClassifier_classifier Accuracy accuracy percent:",(nltk.classify.accuracy(SGDClassifier_classifier,testing_set))*100)
#         
#         SVC_classifier =SklearnClassifier(SVC())
#         SVC_classifier.train(training_set)
#         print("SVC_classifier Accuracy accuracy percent:",(nltk.classify.accuracy(SVC_classifier,testing_set))*100)
#         
#         
#         LinearSVC_classifer =SklearnClassifier(LinearSVC())
#         LinearSVC_classifer.train(training_set)
#         print("LinearSVC_classifer Accuracy accuracy percent:",(nltk.classify.accuracy(LinearSVC_classifer,testing_set))*100)
#          
#         NuSVC_classifier =SklearnClassifier(NuSVC())
#         NuSVC_classifier.train(training_set)
#         print("NuSVC_classifier Accuracy accuracy percent:",(nltk.classify.accuracy(NuSVC_classifier,testing_set))*100)
#        
#         
#         
#         
#         
#         voted_classifier= VoteClassifier(classifier,MNB_classifier,BernoulliNB_classifier,
#                                          LogisticRegression_classifier,SGDClassifier_classifier,
#                                          SVC_classifier,
#                                          LinearSVC_classifer,
#                                          NuSVC_classifier)
#         
#         print("voted classifier Accuracy accuracy percent:",(nltk.classify.accuracy(voted_classifier,testing_set))*100)
#         
#         print("Classification:", voted_classifier.classify(testing_set[0][0]),"confidence %",voted_classifier.confidence(testing_set[0][0]))
#         print("Classification:", voted_classifier.classify(testing_set[1][0]),"confidence %",voted_classifier.confidence(testing_set[1][0]))
#         print("Classification:", voted_classifier.classify(testing_set[2][0]),"confidence %",voted_classifier.confidence(testing_set[2][0]))
#         print("Classification:", voted_classifier.classify(testing_set[3][0]),"confidence %",voted_classifier.confidence(testing_set[3][0]))
#         print("Classification:", voted_classifier.classify(testing_set[4][0]),"confidence %",voted_classifier.confidence(testing_set[4][0]))
#         print("Classification:", voted_classifier.classify(testing_set[5][0]),"confidence %",voted_classifier.confidence(testing_set[5][0]))
def QChart(parent, type, **kwargs):
    class PyQtChart(type, QtGui.QWidget):
        def __init__(self, parent, **kwargs):
            QtGui.QWidget.__init__(self, parent, **kwargs)
            type.__init__(self, kwargs["size"].width(), kwargs["size"].height())
            self.pix = QtGui.QPixmap()
 
        def download(self):
            file = "./%f.png" % time.time()
            type.download(self, file)
            self.pix.load(file)
 
        def paintEvent(self, event):
            p = QtGui.QPainter(self)
            p.drawPixmap(0,0,self.pix)
            super(PyQtChart, self).paintEvent(event)
 
    return PyQtChart(parent, **kwargs)
class ResultWidget(QtGui.QWidget):


    def __init__(self, parent=None):
        super(ResultWidget, self).__init__(parent)
        self.initUI()

    def status(self, message):
        self.welcomeText.setText(message)

    def btStatus(self, message):
        self.btText.setText(message)

#     def gmailCheck(self, parent):
#         sender = self.sender()
#         
#         Login.obj.select()
#         Login.obj.search(None,'UnSeen')
#         unread = len(Login.obj.search(None, 'UnSeen')[1][0].split())
# 
#         if( unread > 0 ):
#             print 'Gmail Unread Count = ', str(unread), ' emails'
#             self.window().statusBar().showMessage('You got e-mail!')
#             self.status('Gmail Unread Count = ' + str(unread) + ' emails')
#             self.window().update()
#         else:
#             self.status('You have no unread e-mails')
#             self.window().statusBar().showMessage('')
#             self.window().clear()

    def buttonClicked2(self):
        sender = self.sender()
        self.window().statusBar().showMessage('')
        self.status('')
        self.window().clear()
    
    def initUI(self):

        # setup tab widget
        tab_widget = QtGui.QTabWidget()

        # define tabs
        homeTab = QtGui.QWidget()
        homelayout = QtGui.QHBoxLayout(homeTab)
        homeGridLayout = QtGui.QGridLayout(homeTab)
        # Facebook
        #facebook = QtGui.QPushButton(QtGui.QIcon('facebook.png'), 'Facebook (n/a)', self)
        #facebook.triggered.connect(self.facebookMenu)
        # Twitter
        #twitter = QtGui.QPushButton(QtGui.QIcon('twitter.png'), 'Twitter (n/a)', self)
        #twitter.triggered.connect(self.twitterMenu)

        
#         gmailBtn.setIcon(QtGui.QIcon('gmail.png'))
#         gmailBtn.clicked.connect(self.gmailCheck)
#         #btn1.move(30, 100)
#         clearBtn = QtGui.QPushButton("Clear Notifications", self)
#         clearBtn.clicked.connect(self.buttonClicked2)

        #facebook.move(50,130)
        #twitter.move(50,160)
        self.tablewidget = QtGui.QTableWidget(self)
        self.dbu = db.DatabaseUtility('UsernamePassword_DB', 'none')
        self.dbu.tableName='reviewDetails'
        t = self.dbu.GetTableReview()
        self.tablewidget.setRowCount(100) ##set number of rows
        self.tablewidget.setColumnCount(5) ##this is fixed for myTableWidget, ensure that both of your tables, sql and qtablewidged have the same number of columns
        self.tablewidget.setMaximumWidth(1000)
        self.tablewidget.setColumnWidth(0,100)
        self.tablewidget.setColumnWidth(1,100)
        self.tablewidget.setColumnWidth(2,100)
        self.tablewidget.setColumnWidth(3,600)
        self.tablewidget.setColumnWidth(4,100)
        print (t)
        self.tablewidget.setHorizontalHeaderLabels(_fromUtf8("S.no;Book Name;Reviewer Name;Review;Sentiment").split(";"))
        row=0
        for col in t:
            for i in range(0,5):
                print(i)
                print(col[i])
                if(i is 0):
                    print("cmg")
                    self.tablewidget.setItem(row,i,QtGui.QTableWidgetItem(row.__str__()))
                else:
                    self.tablewidget.setItem(row,i,QtGui.QTableWidgetItem(col[i]))
            
            row += 1
        
        tCount=self.dbu.GetTableReviewCount()
        sentimentCount=[]
        counter=0
        negativeCount=0
        positiveCount=0
        for col in tCount:
            if(counter is 0):
                negativeCount=col[1]
            elif(counter is 1):
                positiveCount=col[1]
            counter += 1
#             if username == col[1]:
#                 if password == col[2]:
#                     QtGui.QMessageBox.information(self, 'Success!', 'Password verified!!')
#                     MainWindow.loginSuccessful(self.parent())
# 
#                 else:
#                     QtGui.QMessageBox.warning(self, 'Error!', 'Password incorrect...')

        self.btText = QtGui.QLabel('Pie chart in next tab', self)

        # stretch(1) centers the widgets
        homeGridLayout.addWidget(self.tablewidget, 1, 0)
        homeGridLayout.addWidget(self.btText, 2, 0)
        
#         homeGridLayout.setRowStretch(1,0)
# #         homeGridLayout.setColumnStretch()
#         homelayout.
        
        homelayout.addLayout(homeGridLayout)
    
       
        self.overallChart = QtGui.QLabel('Overall Sentiment Analysis', self)
        chartTab = QtGui.QWidget()
        fbTab = QtGui.QWidget()
        t = QChart(self, PieChart3D, size=QtCore.QSize(400,200))
#         row=0
#         positive=
#         for col in t:
#             for i in range(0,5):
#                 print(i)
#                 print(col[i])
#                 if(i is 4):
#                     print("cmg")
#                     self.tablewidget.setItem(row,i,QtGui.QTableWidgetItem(col[i]))
#             
#             row += 1
       
        t.add_data([negativeCount,positiveCount])
        t.set_pie_labels(['Negative', 'Positive'])
        t.download()
        # setup automatic updates
       
        # place a grid layout inside a horizontal box layout
        glayout = QtGui.QHBoxLayout(chartTab)
        gGridlayout = QtGui.QGridLayout(chartTab)
        gGridlayout.addWidget(self.overallChart, 1, 0)
        gGridlayout.addWidget(t, 2, 0)
#         gGridlayout.setc
#         gGridlayout.addWidget(gAuto5, 2, 0)
#         gGridlayout.addWidget(gAuto10, 3, 0)
#         gGridlayout.addWidget(gAuto30, 4, 0)
#         gGridlayout.addWidget(gmailBtn, 5, 0)
        
        # center the grid layout
#         glayout.addStretch(1)
        glayout.addLayout(gGridlayout)
#         glayout.addStretch(1)

        # add tabs
        tab_widget.addTab(homeTab, "Results")
        tab_widget.addTab(chartTab, "Pie Chart")
        
        #special debug tab
        # 1. declare tab
       
        
#         redLEDBtn.clicked.connect(self.window().updateLEDR)
#         greenLEDBtn.clicked.connect(self.window().updateLEDG)
#         blueLEDBtn.clicked.connect(self.window().updateLEDB)
        #
      

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(tab_widget)

        self.setLayout(mainLayout)   
        
        



        
         
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
