# ----------------------------
# Name: Pavana Doddi
# UIN: 676352041
# ----------------------------


from PyQt5 import QtCore, QtGui, QtWidgets

import preprocess as util
import json
# from page_rank import 


class Ui_Dialog:
    def setupUi(self, Dialog):
        Dialog.setObjectName("UIC SEARCH ENGINE")
        Dialog.resize(632, 398)
        Dialog.setStyleSheet("")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(225, 20, 101, 61))
        self.label.setStyleSheet("image: url(uic.PNG);")
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(330, 130, 161, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(150, 130, 171, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setGeometry(QtCore.QRect(70, 180, 491, 192))
        self.listWidget.setStyleSheet("color: rgb(26, 26, 26);")
        self.listWidget.setObjectName("listWidget")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(Dialog)
        self.plainTextEdit.setGeometry(QtCore.QRect(70, 100, 491, 21))
        self.plainTextEdit.setStyleSheet("color: rgb(0, 0, 0);")
        self.plainTextEdit.setPlainText("")
        self.plainTextEdit.setObjectName("plainTextEdit")
        # self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        # self.pushButton_3.setGeometry(QtCore.QRect(570, 260, 51, 32))
        # self.pushButton_3.setObjectName("pushButton_3")
        # self.pushButton_4 = QtWidgets.QPushButton(Dialog)
        # self.pushButton_4.setGeometry(QtCore.QRect(10, 260, 51, 32))
        # self.pushButton_4.setObjectName("pushButton_4")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(310, 45, 81, 16))
        self.label_2.setStyleSheet("color: rgb(47, 35, 205);\n"
"font: 18pt \"Arial\";")
        self.label_2.setObjectName("label_2")
        self.pushButton.clicked.connect(self.execute_intelligent_search)
        self.pushButton_2.clicked.connect(self.execute_search)
        # self.pushButton_3.clicked.connect(self.page_next)
        # self.pushButton_4.clicked.connect(self.page_back)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.SF NS Text\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.pushButton.setText(_translate("Dialog", "Intelligent Search "))
        self.pushButton_2.setText(_translate("Dialog", "Search "))
        # self.pushButton_3.setText(_translate("Dialog", ">"))
        # self.pushButton_4.setText(_translate("Dialog", "<"))
        self.label_2.setText(_translate("Dialog", "SEARCH"))

    def execute_intelligent_search(self):
        query = self.plainTextEdit.toPlainText()
        self.search_result = self.execute_query_intelligent_v2(query)
        self.listWidget.clear()
        result = self.search_result[:10]
        for res in result:
            self.listWidget.addItem(res)
    
    def execute_query_intelligent_v2(self, query):
        frequency = {}
        query_tokens = util.tokenize(query)
        for word in query_tokens:
            if word in frequency:
                frequency[word] = frequency[word] + 1
            else:
                frequency[word] = 1
        # print("document length",len(util.document_length))
        # print("tfidf length", len(util.get_tfidfdoc))
        tfidf_query = util.tf_idf_query(frequency)
        tf_idf_doc = util.get_tfidfdoc()
        doc_length = util.document_length
        util.cosine_similarity(tfidf_query, tf_idf_doc, doc_length)
        similarity = util.cos_sim
        print(similarity)
        sorted_similarities = sorted(similarity, key = similarity.get, reverse = True)[:30]
        docs_on_page_rank = self.refine_results(sorted_similarities, similarity, query_tokens)
        return docs_on_page_rank


    def refine_results(self, sorted_similarities, similarity, query_tokens):
        ranks = {}
        prob_query = {}
        with open('querydependentrank.json', 'r') as f:
            query_page_rank = json.load(f)
        with open('pagerank.json', 'r') as f:
            pagerank = json.load(f)

        for word in query_tokens:
            prob_query[word] = 1/len(query_tokens)

        for doc in sorted_similarities:
            ranks[doc] = 5*similarity[doc]+pagerank[doc]
            # url = doc.replace("http://www.","")
            # if url in query_page_rank:
            #     ranks[doc] = ranks[doc]+(sum(prob_query[word]*query_page_rank[url][word] if word in query_page_rank[url] else 0 for word in query_tokens))

        results = sorted(ranks, key = ranks.get, reverse = True)[:20]
        for link in results:
            print(link)
        return results
        # print(sorted_similarities)

    def execute_search(self):
        query = self.plainTextEdit.toPlainText()
        self.search_result = self.execute_search_v2(query)
        self.listWidget.clear()
        result = self.search_result[:10]
        for res in result:
            self.listWidget.addItem(res)

    def execute_search_v2(self, query):
        frequency = {}
        query_tokens = util.tokenize(query)
        for word in query_tokens:
            if word in frequency:
                frequency[word] = frequency[word] + 1
            else:
                frequency[word] = 1
        # print("document length",len(util.document_length))
        # print("tfidf length", len(util.get_tfidfdoc))
        tfidf_query = util.tf_idf_query(frequency)
        tf_idf_doc = util.get_tfidfdoc()
        doc_length = util.document_length
        util.cosine_similarity(tfidf_query, tf_idf_doc, doc_length)
        similarity = util.cos_sim
        sorted_similarities = sorted(similarity, key = similarity.get, reverse = True)[:20]
        results = self.refine_results_v2(sorted_similarities, similarity)
        return results

    def refine_results_v2(self, sorted_similarities, similarity):
        ranks = {}
        with open('querydependentrank.json', 'r') as f:
            query_page_rank = json.load(f)
        with open('pagerank.json', 'r') as f:
            pagerank = json.load(f)
        for doc in sorted_similarities:
            ranks[doc] = 0.5*similarity[doc]+pagerank[doc]
        results = sorted(ranks, key = ranks.get, reverse = True)[:20]
        for link in results:
            print(link)
        return results
    
    def page_next(self):
        ll = self.search_result
        if len(self.search_result) >= (self.current_page * 10) and self.current_page < 10:
            self.current_page += 1
            self.listWidget.clear()
            result = self.search_result[(self.current_page*10)-10:self.current_page*10]
            for res in result:
                self.listWidget.addItem(res)

    def page_back(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.listWidget.clear()
            result = self.search_result[(self.current_page * 10) - 10:self.current_page * 10]
            for res in result:
                self.listWidget.addItem(res)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    Dialog.setFixedSize(630,410)
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()

    sys.exit(app.exec_())

