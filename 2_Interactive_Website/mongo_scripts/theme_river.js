client = new Mongo();
db = client.getDB("aps");

function article_by_year(cluster_coll, article_coll){
    db[cluster_coll].find().forEach(function(doc){
	for(i in doc["articles"]){
	    year = db[article_coll].findOne({"_id": doc["articles"][i]["id"]})["date"].split("-")[0]
	    month = db[article_coll].findOne({"_id": doc["articles"][i]["id"]})["date"].split("-")[1]
	    print(year);
	    db[cluster_coll].update({_id: doc["_id"], "articles.id": doc["articles"][i]["id"]}, {$set: {"articles.$.year": year, "articles.$.month": month}})
	}
    });
}
