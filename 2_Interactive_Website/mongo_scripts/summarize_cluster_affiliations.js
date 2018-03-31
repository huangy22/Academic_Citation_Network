
function summarize_affiliations(aff_coll, output_coll){
    pipeline_unwind_affiliations = [{ $unwind:  "$cluster_weights"},
			{ $group: { _id: {level1: "$cluster_weights.level1_cluster", level2: "$cluster_weights.level2_cluter"},
				    affiliations: {$addToSet: {id: "$_id", affiliation: "$affiliation", num_author:
				                   "$cluster_weights.num_author", weight: "$cluster_weights.weight"}}, 
	      			    level1_cluster: {$first: "$cluster_weights.level1_cluster"},
	      			    level2_cluster: {$first: "$cluster_weights.level2_cluster"}
				    }},
			{ $out: "tmp"}];

    db[aff_coll].aggregate(pipeline_unwind_affiliations, {allowDiskUse:true});

    db.tmp.find().forEach(function(doc) {
	old_id = doc._id
	doc._id = new ObjectId();
	db[aff_coll].save(doc);
	});
    db.tmp.drop();
}
