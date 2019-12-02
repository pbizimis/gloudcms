from pymongo import MongoClient
import os

if os.environ["MONGO_IP"] == "testing":
    import mongomock
    db = mongomock.MongoClient().db
else:
    DATABASE_URI = 'mongodb://' + os.environ["MONGO_IP"] + ':27017/'
    client = MongoClient(DATABASE_URI)
    db = client.gloudcms


def query_articles_date(apiid, order):
    articles = list(db.articles.find({"apiid": apiid}, {"_id": 0}).sort("date", int(order)))
    return articles

def query_articles_modified(apiid, order):
    articles = list(db.articles.find({"apiid": apiid}, {"_id": 0}).sort("lastModified", int(order)))
    return articles

def query_article(apiid, article_url):
    article = db.articles.find_one({"apiid": apiid, "url": article_url}, {"_id": 0})
    return article

def query_author(apiid, author, order):
    articles = list(db.articles.find({"apiid": apiid, "author": author}, {"_id": 0}).sort("date", int(order)))
    return articles

def query_keyword(apiid, keyword):
    articles = list(db.articles.find({"apiid": apiid, "$text":{ "$search": keyword}}, {"_id": 0}))
    return articles

def query_tags(apiid, tags, intersect):
    if intersect == "n":
        articles = list(db.articles.find({"apiid": apiid, "tags":{ "$in": tags }}, {"_id": 0}))
    elif intersect == "i":
        articles = list(db.articles.find({"apiid": apiid, "tags":{ "$all": tags }}, {"_id": 0}))
    else:
        articles = {"error": "Please use /<apiid>/tags/<tags>/<i/n>"}
    return articles

def query_article_titles(apiid):
    pipeline = [
        {"$match": {"apiid": apiid}},
        {"$group": {"_id": None, "articles": { "$push": "$title"}}},
        {"$project": {"_id": 0}}
    ]
    try:
        articles = list(db.articles.aggregate(pipeline))[0]
    except IndexError:
        articles = {"error": "You don't have any articles!"}
    return articles

def query_articles_by_author(apiid):
    pipeline = [
        {"$match": {"apiid": apiid}},
        {"$group": {"_id": "$author", "articles": { "$push": "$title"}}},
        {"$project": {"_id": 0, "author": "$_id", "articles": 1}}
    ]
    articles = list(db.articles.aggregate(pipeline))
    return articles

def query_articles_length(apiid, order):
    pipeline = [
        {"$match": {"apiid": apiid}},
        {"$project": {"_id": "$title", "length": {"$strLenCP": {"$reduce": {
                    "input": {"$map": {"input": "$content", "as": "p", "in": "$$p.para"}},
                    "initialValue": "",
                    "in": { "$concat" : ["$$value", "$$this"] }}}}}},
        {"$sort": {"length": int(order)}}
    ]
    article_length = list(db.articles.aggregate(pipeline))
    return article_length

def query_account(apiid):
    account_info = db.user.find_one({"apiid": apiid}, {"_id": 0, "credentials": 0, "gid": 0})
    return account_info

def query_stats(apiid):
    name = list(db.user.aggregate([{"$match": {"apiid": apiid}}, {"$project": {"_id": 0, "name": {"$concat": ["$given_name", " ", "$family_name"]}}}]))[0]["name"]

    pipeline = [
        {"$facet": {
         "stats": [
            {"$match": {"apiid": apiid}},
            {"$sort": {"date": 1}},
            {"$group": {"_id": None, "articles": {"$sum": 1}, "authors": {"$addToSet": "$author"},"from": {"$first": "$date"}, "to": {"$last": "$date"}}},
            {"$project": {"_id": 0, "name": name, "articles": 1, "authors": {"$size": "$authors"}, "period": {"from": "$from", "to": "$to"}}}],
        "topFiveTags": [
            {"$match": {"apiid": apiid}},
            {"$unwind": "$tags"},
            {"$group": {"_id": "$tags", "times": {"$sum": 1}}},
            {"$project": {"_id": 0, "tag": "$_id", "times": 1}},
            {"$sort": {"times": -1}},
            {"$limit": 5}]
        }},
        {"$unwind": "$stats"},
        {"$project": {"stats": "$stats", "tags": {"topFiveTags": "$topFiveTags"}}},
        {"$replaceRoot": {"newRoot":  {"$mergeObjects": ["$stats", "$tags"]}}}
    ]
    try:
        account_stats = list(db.articles.aggregate(pipeline))[0]
    except IndexError:
        account_stats = {"error": "You don't have any articles!"}
    return account_stats
