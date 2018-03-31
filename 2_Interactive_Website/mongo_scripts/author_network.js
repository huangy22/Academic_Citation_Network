client = new Mongo();
db = client.getDB("aps");

function find_coauthors(partial_author_coll, tot_author_coll, article_coll){
    db[partial_author_coll].aggregate({$addFields: {"coauthor": []}}, {$out: partial_author_coll});
    db[partial_author_coll].find().forEach(function(author) {
        author["articles"].forEach(function(article_id){
            article = db[article_coll].findOne({_id: article_id});	
	    for(other_author_id in article["author_list"]){
		other_author = article["author_list"][other_author_id];
		if(other_author == author["_id"]){
		     continue;
		}else if(db[tot_author_coll].findOne({_id: other_author})["publications"]<100){
		     continue;
                }else{
		    db[partial_author_coll].update({_id: author["_id"]}, {$addToSet: {"coauthor": other_author}});
		}
	    }
	});
    });
}
