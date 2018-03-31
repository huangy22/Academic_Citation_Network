function plot_cluster(){

  var width = 580,
    height = 350,
    padding = 1.5;


  var force = d3.layout.force()
      .gravity(.08)
      .charge(-10)
      .linkDistance(150)
      .size([width, height]);

  d3.select("#article-cluster").selectAll("*").remove();
  var svg = d3.select("#article-cluster").append("svg")
      .attr("style", "outline: thin solid black;") 
      .attr("width", width)
      .attr("height", height);

  var tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([-10, 0])
    .html(function(d) {
      line1 = "<strong>Size:</strong> <span style='color:red'>" + d.size + "</span>";
      line2 = "<strong>Field:</strong> <span style='color:red'>" + d.title + "</span>";
      return line1 + "<br></br>"+ line2;
    });

  svg.call(tip);

  d3.json("../data/level1/citation_network.json", function(error, graph) {
    if (error) throw error;

    var link = svg.selectAll("line")
        .data(graph.links)
      .enter().append("line")
      .attr("stroke", "black")
      .attr("stroke-width", function(d){return d.value/200;});

    var node = svg.selectAll("g.node")
      .data(graph.nodes)
      .enter().append("svg:g")
        .attr("class", "node")
        .call(force.drag);
      
    circles = node.append("circle")
        .attr("r", function(d){ return d.size/180;})
        .style("fill", function(d) { return d.color; })
        .style("stroke", function(d) { return d3.rgb(d.color).darker(); })
        .on("mouseover", function(d) {
          d3.select(this).attr("r", function(d){ return d.size/150;});
          svg.selectAll("rect").style("opacity", 0.5);
          svg.select("#rect_"+d.title.split(" ").join("_").split(",").join("_")).style("opacity", 1.0);

          svg.selectAll("text").style("opacity", 0.5);
          svg.select("#text_"+d.title.split(" ").join("_").split(",").join("_")).style("opacity", 1.0);
          svg.select("#title").style("opacity", 1.0);
          svg.select("#footnote").style("opacity", 1.0);
          tip.show(d);
        })                  
        .on("mouseout", function(d) {
          d3.select(this).attr("r", function(d){ return d.size/180;});
          tip.hide(d);

          svg.selectAll("rect").style("opacity", 1.0);
          svg.selectAll("text").style("opacity", 1.0);
        })
        .on("click", function(d) {
          plot_author(d.name, d.title);
        });

    title = svg.append("text")
        .attr("id", "title")
        .attr("x", 300)
        .attr("y", 20)
        .attr("font-weight", "bold")
        .style("text-anchor", "middle")
        .text("Physical Review Articles, 27695 vertices");

    footnote = svg.append("text")
        .attr("id", "footnote")
        .attr("x", width-20)
        .attr("y", height-5)
        .style("text-anchor", "end")
        .text("+ 487 smaller communities");

    var legend = svg.selectAll(".legend")
    .data(graph.nodes)
    .enter().append("g")
    .attr("class", "legend")
    .attr("transform", function(d, i) { return "translate(0," + (+i * 18+110) + ")"; });

    legend.append("rect")
      .attr("id", function(d){return "rect_"+d.title.split(" ").join("_").split(",").join("_");})
      .attr("x", 5)
      .attr("width", 12)
      .attr("height", 12)
      .style("fill", function(d){return d.color;});

    legend.append("text")
      .attr("id", function(d){return "text_"+d.title.split(" ").join("_").split(",").join("_");})
      .attr("font-size", "8pt")
      .attr("x", 24)
      .attr("y", 8)
      .attr("dy", ".25em")
      .style("text-anchor", "front")
      .text(function(d) { return d.title; });

    force
        .nodes(graph.nodes)
        .links(graph.links)
        .on("tick", tick)
        .start();

    for (var i = 300; i > 0; --i) force.tick();
    force.stop();

    function tick(e) {
      circles
          .each(collide(.5))
          .attr("cx", function(d) { d.x = Math.max(220, Math.min(width, d.x)); return d.x; })
          .attr("cy", function(d) { d.y = Math.max(10, Math.min(height-10, d.y)); return d.y; });
          // .attr("cx", function(d) {  return d.x; })
          // .attr("cy", function(d) {  return d.y; });

      link.attr("x1", function(d) { return d.source.x; })
          .attr("y1", function(d) { return d.source.y; })
          .attr("x2", function(d) { return d.target.x; })
          .attr("y2", function(d) { return d.target.y; });
    }

    // Resolves collisions between d and all other circles.
    function collide(alpha) {
      var quadtree = d3.geom.quadtree(graph.nodes);
      return function(d) {
        var r = d.size/180 + 30 + Math.max(padding),
            nx1 = d.x - r,
            nx2 = d.x + r,
            ny1 = d.y - r,
            ny2 = d.y + r;
        quadtree.visit(function(quad, x1, y1, x2, y2) {
          if (quad.point && (quad.point !== d)) {
            var x = d.x - quad.point.x,
                y = d.y - quad.point.y,
                l = Math.sqrt(x * x + y * y),
                r = d.size/180 + quad.point.size/180 + padding;
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
plot_cluster();
