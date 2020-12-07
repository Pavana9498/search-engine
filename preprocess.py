# ----------------------------
# Name: Pavana Doddi
# UIN: 676352041
# ----------------------------

import json
import re
from nltk import PorterStemmer
from math import log2, sqrt, pow


web = {}
documents_dict = {}
index_table = {}
tfidf_doc = {}
document_length = {}
idf_word = {}
stopWordList = []
cos_sim = {}



pattern2 = r'[^A-za-z]'
regex2 = re.compile(pattern2)

def main():
    global web
    with open('Crawler/Spider.json', 'r') as f:
        web  = json.load(f)
        preprocess()
        build_index_table()
        build_tf_idf_doc()
        calculate_document_lengths()
        save_tf_idf_doc()
        save_index_table()

def obtain_stopwords():
    print("obtaining stop words")
    global stopWordList
    with open('stopWords.txt', 'r') as stopWordsFile:
        stopWords = stopWordsFile.readlines()
        for stopWord in stopWords:
            stopWord = stopWord.strip()
            stopWordList.append(stopWord)

def preprocess():
    print("Preprocessing")
    global documents_dict
    obtain_stopwords()
    for url, data in web.items():
        word_frequency = {}
        text = data['text']
        tokens = tokenize(text)
        word_frequency = {word:word_frequency.get(word, 0) + 1 for word in tokens}
        documents_dict[url] = word_frequency
 

def calculate_document_lengths():
    print("calulating doc lengths")
    global tfidf_doc
    for doc_id, document in tfidf_doc.items():
        length = round(sqrt(sum(pow(document[word], 2) for word, value in document.items())), 3)
        document_length[doc_id] = length


def tokenize(text):
    global stopWordList
    tokens = text.split(' ')
    tokens = [regex2.sub('', word) for word in tokens]
    tokens = [word.lower() for word in tokens]
    tokens = [word for word in tokens if word not in stopWordList]
    tokens = [PorterStemmer().stem(word) for word in tokens]
    tokens = [word for word in tokens if word not in stopWordList]
    tokens = [word for word in tokens if len(word)>2]
    tokens = [word for word in tokens if word]
    return tokens

def build_index_table():
    print("Building inverted index")
    global documents_dict
    global index_table
    for doc_id, document in documents_dict.items():
        for word in document:
            if word in index_table:
                index_table[word][doc_id] = documents_dict[doc_id][word]
            else:
                index_table[word] = {doc_id:documents_dict[doc_id][word]}
    

def build_tf_idf_doc():
    print("Building tf idf")
    global index_table
    global documents_dict
    global idf_word
    global tfidf_doc
    # print(index_table)
    for word, documents in index_table.items():
        df = len(documents)
        idf = log2(len(documents_dict)/df)
        idf_word[word] = idf
        for url, tf in documents.items():
            if url in tfidf_doc:
                tfidf_doc[url][word] = round((tf * idf), 3)
            else:
                tfidf_doc[url] = {}
                tfidf_doc[url][word] = round((tf * idf), 3)
    # print(tfidf_doc)

def tf_idf_query(query_word_frequency):
    print("computing tf idf query")
    global index_table
    tfidf_query = {}
    for word, tf_query in query_word_frequency.items():
        if word in index_table:
            df = len(index_table[word])
            idf = idf_word[word]
            tfidf_query[word] = round((tf_query * idf), 3)
        else:
            tfidf_query[word] = 0
    return tfidf_query

    
def cosine_similarity(tf_idf_query, tf_idf_doc, document_length):
    print("Calculating similarities")
    global cos_sim
    query_length = sqrt(sum(pow(value, 2) for word, value in tf_idf_query.items()))
    for key, value in tf_idf_query.items():
        print(value)
    print("query length",query_length)
    for doc_id, document in tf_idf_doc.items():
        doc_length = document_length[doc_id]
        print("doc length", doc_length)
        similarity = 0
        for word in tf_idf_query:
            similarity = similarity + (document.get(word, 0) * tf_idf_query[word])
        summation = round(similarity, 3)
        print(doc_length*query_length)
        if (doc_length*query_length>0):
            cos_sim[doc_id] = round((summation/(doc_length*query_length)), 3)
        else:
            cos_sim[doc_id] = 0

def save_tf_idf_doc():
    print("Saving tf idf")
    global tfidf_doc
    with open('tfidfdoc.json', 'w') as f:
        json.dump(tfidf_doc, f)

def save_index_table():
    print("Saving index_table")
    global index_table
    with open('inverted_index.json', 'w') as f:
        json.dump(index_table, f)
def get_index_table():
    global index_table
    return index_table
def get_tfidfdoc():
    global tfidf_doc
    return tfidf_doc


main()