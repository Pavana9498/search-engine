# ----------------------------
# Name: Pavana Doddi
# UIN: 676352041
# ----------------------------

import preprocess as util
import json

web = {}
page_rank_initial = {}
page_rank_final = {}
web_graph = {}
inverted_graph = {}
query_page_rank = {}


def score_node(node, p, page_rank_initial):
    alpha = 0.85
    summation = 0
    if(len(get_in_links(node))> 0 ):
        for link in get_in_links(node):
            summation = summation + (page_rank_initial[link]/len(web_graph[link]))
    score = (1-alpha)*p+alpha*(summation)
    return score
    



def page_rank():
    print("calculating page rank")
    global web
    for i in range(1, 11):
        print("iteration: ", i)
        pi = 1/ len(web)
        for node in web:
            page_rank_final[node] = score_node(node, pi, page_rank_initial)
        early_exit = True
        for i in page_rank_final:
            if early_exit and page_rank_initial[i] != page_rank_final[i]:
                early_exit = False
            page_rank_initial[i] = page_rank_final[i]
        if early_exit:
            return

def draw_web():
    print("drawing web")
    global web
    global inverted_graph
    global web_graph
    global page_rank_initial
    global page_rank_final
    with open('Crawler/Spider.json', 'r') as f:
        web = json.load(f)
    pi = 1/ len(web)
    for url, data in web.items():
        if url not in web_graph:
            web_graph[url] = {}
        for link in data['out_links']:
            if link != url:
                if link in web_graph[url]:
                    web_graph[url][link] = web_graph[url][link] + 1
                else:
                    web_graph[url][link] = 1
                if link not in inverted_graph:
                    inverted_graph[link] = []
                inverted_graph[link].append(url)
        page_rank_initial[url] = pi
        page_rank_final[url] = pi
    
def get_in_links(url):
    global inverted_graph
    try:
        if(url not in inverted_graph):
            url = url.replace("www.","")
        return inverted_graph[url]
    except:
        return []

def querydependentRank():
    print("Calculating query dependent page rank")
    alpha = 0.85
    global query_page_rank
    tfidf = util.get_tfidfdoc()
    # print(tfidf)
    for doc_id, document in tfidf.items():
        query_page_rank[doc_id] = {}
        for word, tf_idf in document.items():
            query_page_rank[doc_id][word] = 1/len(tfidf[doc_id])
    for i in range(10):
        print("iteration", i)
        for doc_id in tfidf:
            if i == 10:
                break
            for term in tfidf[doc_id]:
                s = 0
                for i in get_in_links(doc_id):
                    s += (query_page_rank[i][term] if term in query_page_rank[i] else 0) * pqi2j(term, i, doc_id, tfidf)
                summation = 0
                for i in tfidf:
                    if term in tfidf[i]:
                        summation = summation + tfidf[i][term]
                if summation>0:
                    pdash_query = tfidf[doc_id][term]/summation
                query_page_rank[doc_id][term] = (1 - alpha) * pdash_query + (alpha * s)
            # print(word, doc_id)

def pqi2j(term, inlink, doc_id, tfidf):
    global web_graph
    s = 0
    if inlink in web_graph:
        for doc in web_graph[inlink]:
            if doc in tfidf and term in tfidf[doc]:
                s = s+tfidf[doc][term]
    if s > 0:
        return(tfidf[doc_id][term] if term in tfidf[doc_id] else 0)/s
    else: 
        return 0


def get_page_rank():
    global page_rank_final
    return page_rank_final

def get_query_page_rank():
    global query_page_rank
    return query_page_rank

def get_web_graph():
    global web_graph
    return web_graph

def get_inverted_graph():
    global inverted_graph
    return inverted_graph

def save_page_rank():
    print("Saving page rank")
    global page_rank_final
    with open('pagerank.json', 'w') as f:
        json.dump(page_rank_final, f)

def save_query_page_rank():
    print("Saving query dependent page rank")
    global query_page_rank
    with open('querypagerank.json', 'w') as f:
        json.dump(query_page_rank, f)

def main():
    draw_web()
    page_rank()
    save_page_rank()
    querydependentRank()
    save_query_page_rank()

main()



