client = new Mongo();
db = client.getDB("aps");

function articles_to_authors(input_coll, output_coll){
    pipeline_unwind_authors = [{ $unwind:  "$authors"},
			{ $unwind:  "$authors.affiliationIds"},
			{ $unwind:  "$affiliations"},
			{ $addFields: {  is_same: {$eq: ["$affiliations.id", "$authors.affiliationIds"]}}},
			{ $match:{ is_same: true, "authors.type": "Person" }},
			{ $group: { _id: {article: "$_id", author: "$authors"},
				    articleId: {$first: "$_id"},
				    author: {$first: "$authors"},
				    affiliations: {$addToSet: "$affiliations.name"},
				    }},
			{ $unwind: "$affiliations"},
			{ $out: "tmp"}];
    db[input_coll].aggregate(pipeline_unwind_authors, {allowDiskUse:true});

    pipeline_group_authors = [{ $group: { _id: { author: "$author.name"},
					  author: {$first: "$author"}, 
					  affiliations: {$addToSet: "$affiliations"},
					  articles: {$addToSet: "$articleId"},
					}},
			      { $addFields: {publications: {$size: "$articles"}}},
			      { $sort: {publications: -1}},
			      { $out: "tmp"}];
    db.tmp.aggregate(pipeline_group_authors, {allowDiskUse:true});

    db.tmp.find().forEach(function(doc) {
	old_id = doc._id
	doc._id = new ObjectId();
	db[output_coll].save(doc);
	});
    db.tmp.drop();
}

function authors_to_affiliations(input_coll, output_coll){
    pipeline_unwind_affiliations = [{ $unwind:  "$affiliations"},
			{ $group: { _id: "$affiliations",
				    authors: {$addToSet: {id: "$_id"}}, 
	      			    affiliation: {$first: "$affiliations"}
				    }},
			{ $addFields: {authornum: {$size: "$authors"}}},
			{ $sort: {authornum: -1}},
			{ $out: "tmp"}];

    db[input_coll].aggregate(pipeline_unwind_affiliations, {allowDiskUse:true});

    db.tmp.find().forEach(function(doc) {
	old_id = doc._id
	doc._id = new ObjectId();
	db[output_coll].save(doc);
	});
    db.tmp.drop();
}

function articles_affiliations_to_id(input_coll, aff_coll){
    db[input_coll].find().forEach(function(doc){
	affiliation_list = [];
	if(doc["affiliations"]){
	    doc["affiliations"].forEach(function(affiliation){
		aff =  db[aff_coll].findOne({ affiliation: affiliation["name"]});
		if(aff){
		    affiliation_list.push(aff["_id"]);
		}
	    });
	    db[input_coll].update( { _id: doc["_id"] },{ $set: { "affiliation_list": affiliation_list } });
	}
    });
    print("change affiliations to ids done!")
}

function authors_affiliations_to_id(input_coll, aff_coll){
    db[aff_coll].find().forEach(function(doc){
	id = doc["_id"];
	if(doc["authors"]){
	    doc["authors"].forEach(function(author){
		db[input_coll].update( { _id: author["id"] },{ $push: { affiliation_list: id } });
	    });
	}
    });
    print("change affiliations to ids done!")
}

function articles_authors_to_id(input_coll, author_coll){
    db[input_coll].find({}, noTimeout=true).forEach(function(doc){
	author_list = [];
	if(doc["authors"]){
	    doc["authors"].forEach(function(author){
		author =  db[author_coll].findOne({ "author.name": author["name"]});
		if(author){
		    author_list.push(author["_id"]);
		}
	    });
	    db[input_coll].update( { _id: doc["_id"] },{ $set: { "author_list": author_list } });
	}
    });
    print("change author to ids done!")
}


function generate_test_collections(){
    db["test_authors"].drop();
    db["test_affiliations"].drop();

    print("articles to authors:");
    articles_to_authors("test_articles", "test_authors");
    print("authors to affiliations:");
    authors_to_affiliations("test_authors", "test_affiliations");
    print("update affiliations list in articles:");
    articles_affiliations_to_id("test_articles", "test_affiliations");
    print("update affiliations list in authors:");
    authors_affiliations_to_id("test_authors", "test_affiliations");
    print("update author list in articles:");
    authors_to_id("test_articles", "test_articles_new", "test_authors");
}

function generate_collections(){

    db["tot_authors"].drop();
    db["tot_affiliations"].drop();
    db["tot_articles_new"].drop();

    print("articles to authors:");
    articles_to_authors("tot_articles", "tot_authors");
    print("authors to affiliations:");
    authors_to_affiliations("tot_authors", "tot_affiliations");
    print("update affiliations list in articles:");
    articles_affiliations_to_id("tot_articles", "tot_affiliations");
    print("update affiliations list in authors:");
    authors_affiliations_to_id("tot_authors", "tot_affiliations");

    print("update author list in articles:");
    articles_authors_to_id("tot_articles", "tot_authors");
}

function filter_network(articles_coll, network_coll, output_coll){
    print("Filtering network data:");
    db[articles_coll].createIndex( { "articleId": "hashed" } );
    print("Hash done!");
    var i = 0;
    db[network_coll].find().forEach(function(doc){
        i = i+1;
	if(db[articles_coll].findOne({"articleId": doc["cited_doi"]}) && db[articles_coll].findOne({"articleId": doc["citing_doi"]})){ 
	    print(i);
	    db[output_coll].save(doc);
        }
    });
}
