function plot_author(level1, level1_name){
  var width = 580,
      height = 350,
      padding = 1.5, // separation between same-color nodes
      clusterPadding = 6, // separation between different-color nodes
      maxRadius = 12;

  var m = 13; // number of distinct clusters

  d3.select("#author-cluster").selectAll("*").remove();
  var svg = d3.select("#author-cluster").append("svg")
      .attr("style", "outline: thin solid black;") 
      .attr("width", width)
      .attr("height", height);

  var tip = d3.tip()
      .attr('class', 'd3-tip')
      .offset([-10, 0])
      .html(function(d) {
        line1 = "<strong>Name:</strong> <span style='color:red'>" + d.name + "</span>";
        line2 = "<strong>Publications:</strong> <span style='color:red'>" + d.values + "</span>";
        line3 = "<strong>Field:</strong> <span style='color:red'>" + d.level1_name + "</span>";
        return line1 + "<br></br>"+ line2+ "<br></br>" + line3;
      });

  svg.call(tip);

  d3.json("../data/level1/authors_top.json", function(error, data) {
    // The largest node for each cluster.
    var clusters = new Array(m);

    for(i in data){
      d = data[i];
      var idx = d.index1;
      if(!clusters[idx] || (d.values > clusters[idx].values)) clusters[idx] = d;
    }

    var force = d3.layout.force()
        .nodes(data)
        .size([width, height])
        .gravity(.02)
        .charge(0)
        .on("tick", tick)
        .start();



    var node = svg.selectAll("circle")
        .data(data)
      .enter().append("circle")
        .style("fill", function(d) { return d.color; })
        .style("opacity", function(d) { if(level1==null || d.level1==level1){return 1.0; }else{return 0.3;}})
        .attr("r", function(d){ return d.values*10/clusters[d.index1].values;})
          .on("mouseover", function(d) {
            d3.select(this).attr("r", function(d){ return d.values*12/clusters[d.index1].values;});
            tip.show(d);
          })                  
          .on("mouseout", function(d) {
            d3.select(this).attr("r", function(d){ return d.values*10/clusters[d.index1].values;});
            tip.hide(d);
          })
          .on("click", function(d){
            if (d3.event.defaultPrevented) return;
            var physicist_name = d.name.split(" ").join("%20")+"%20physics";
            var url = "https://www.google.com/search?q="+physicist_name;
            var win = window.open(url, '_blank');
            win.focus();
          })
        .call(force.drag);

    for (var i = 150; i > 0; --i) force.tick();
    force.stop();

    title = svg.append("text")
        .attr("id", "title")
        .attr("x", width/2)
        .attr("y", 20)
        .attr("font-weight", "bold")
        .style("text-anchor", "middle")
        .text("Physicists With More Than 20 Publications Between 2007 and 2015");

    if(level1_name){
      svg.append("text")
        .attr("x", width/2)
        .attr("y", 40)
        .attr("font-weight", "bold")
        .style("text-anchor", "middle")
        .text("Sub-Communities: "+level1_name);
    }

    function tick(e) {
      node
          .each(cluster(10 * e.alpha * e.alpha))
          .each(collide(.5))
          .attr("cx", function(d) { d.x = Math.max(10, Math.min(width, d.x)); return d.x; })
          .attr("cy", function(d) { d.y = Math.max(10, Math.min(height-10, d.y)); return d.y; });
          // .attr("cx", function(d) { return d.x; })
          // .attr("cy", function(d) { return d.y; });
    }

    // Move d to be adjacent to the cluster node.
    function cluster(alpha) {
      return function(d) {
        var cluster = clusters[d.index1];
        if (cluster === d) return;
        var x = d.x - cluster.x,
            y = d.y - cluster.y,
            l = Math.sqrt(x * x + y * y),
            r = d.values*10/cluster.values + 10;
        if (l != r) {
          l = (l - r) / l * alpha;
          d.x -= x *= l;
          d.y -= y *= l;
          cluster.x += x;
          cluster.y += y;
        }
      };
    }

    // Resolves collisions between d and all other circles.
    function collide(alpha) {
      var quadtree = d3.geom.quadtree(data);
      return function(d) {
        var r = d.values*10/clusters[d.index1].values + maxRadius + Math.max(padding, clusterPadding),
            nx1 = d.x - r,
            nx2 = d.x + r,
            ny1 = d.y - r,
            ny2 = d.y + r;
        quadtree.visit(function(quad, x1, y1, x2, y2) {
          if (quad.point && (quad.point !== d)) {
            var x = d.x - quad.point.x,
                y = d.y - quad.point.y,
                l = Math.sqrt(x * x + y * y),
                r = d.values*10/clusters[d.index1].values + quad.point.values*10/clusters[d.index1].values + (d.cluster === quad.point.cluster ? padding : clusterPadding);
            if (l < r) {
              l = (l - r) / l * alpha;
              d.x -= x *= l;
              d.y -= y *= l;
              quad.point.x += x;
              quad.point.y += y;
            }
          }
          return x1 > nx2 || x2 < nx1 || y1 > ny2 || y2 < ny1;
        });
      };
    }
  });
  
}
plot_author(null, null);
