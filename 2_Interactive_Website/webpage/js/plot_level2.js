function plot_level2(level1, color, community_name){

  var width = 280,
    height = 280,
    padding = 1.5;


  var force = d3.layout.force()
      .gravity(.08)
      .charge(-10)
      .linkDistance(130)
      .size([width, height]);

  d3.select("#article-network-level2").selectAll("*").remove();
  var svg = d3.select("#article-network-level2").append("svg")
      .attr("style", "outline: thin solid black;") 
      .attr("width", width)
      .attr("height", height);

  var circle_tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([-10, 0])
    .html(function(d) {
      return "<strong>Number of Articles:</strong> <span style='color:red'>" + d.size + "</span>";
    });

  var link_tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([-10, 0])
    .html(function(d) {
      return "<strong>Number of Citations:</strong> <span style='color:red'>" + d.value + "</span>";
    });

  svg.call(circle_tip);
  svg.call(link_tip);

  d3.json("../data/level2/"+level1+"_citation_network.json", function(error, graph) {
    if (error) throw error;
    
    maxsize = 0;
    for(node in graph.nodes){
      if(+graph.nodes[node]["size"] > maxsize)
        maxsize = graph.nodes[node]['size'];
    }

    maxlink = 0;
    for(link in graph.links){
      if(+graph.links[link]["value"] > maxlink)
        maxlink = graph.links[link]['value'];
    }

    var link = svg.selectAll("line")
        .data(graph.links)
      .enter().append("line")
      .attr("stroke", "black")
      .attr("stroke-width", function(d){return d.value*6/maxlink;})
      .on("mouseover", function(d) {
        d3.select(this).attr("stroke-width", function(d){ return 8;});
        link_tip.show(d);
      })                  
      .on("mouseout", function(d) {
        d3.select(this).attr("stroke-width", function(d){ return d.value*6/maxlink;});
        link_tip.hide(d);
      })

    var node = svg.selectAll("circle")
        .data(graph.nodes)
      .enter().append("circle")
        .attr("r", function(d){ return d.size/maxsize*30;})
        .style("fill", function(d) { return color; })
        .style("stroke", function(d) { return d3.rgb(color).darker(); })
        .on("mouseover", function(d) {
          d3.select(this).attr("r", function(d){ return d.size/maxsize*40;});
          circle_tip.show(d);
        })                  
        .on("mouseout", function(d) {
          d3.select(this).attr("r", function(d){ return d.size/maxsize*30;});
          circle_tip.hide(d);
        })
        .on('click', function(d){ 
          if (d3.event.defaultPrevented) return;
          svg.selectAll("circle").style("opacity", 0.3);
          d3.select(this).style("opacity", 1.0);
          plot_level3(level1, d.name, color);
        })
        .call(force.drag);

    var title = svg.append("text")
      .attr("x", 10)
      .attr("y", 20)
      .attr("font-weight", "bold")
      .text("Sub-Communities:");

    svg
      .append("text")
      .attr("x", 10)
      .attr("y", 40)
      .attr("font-weight", "bold")
      .text(community_name);

    var footnote = svg.append("text")
        .attr("x", width-20)
        .attr("y", height-5)
        .style("text-anchor", "end")
        .text("+ smaller sub-communities");

    force
        .nodes(graph.nodes)
        .links(graph.links)
        .on("tick", tick)
        .start();
    for (var i = 100; i > 0; --i) force.tick();
    force.stop();

    function tick(e) {
      node.each(collide(.5))
          .attr("cx", function(d) { return d.x; })
          // .attr("cy", function(d) { return d.y; });
          // .attr("cx", function(d) { return d.x = Math.max(30, Math.min(width - 30, d.x)); })
          .attr("cy", function(d) { return d.y = Math.max(40, Math.min(height-20, d.y)); });

      link.attr("x1", function(d) { return d.source.x; })
          .attr("y1", function(d) { return d.source.y; })
          .attr("x2", function(d) { return d.target.x; })
          .attr("y2", function(d) { return d.target.y; });
    }

    // Resolves collisions between d and all other circles.
    function collide(alpha) {
      var quadtree = d3.geom.quadtree(graph.nodes);
      return function(d) {
        var r = d.size*30/maxsize + 50 + Math.max(padding),
            nx1 = d.x - r,
            nx2 = d.x + r,
            ny1 = d.y - r,
            ny2 = d.y + r;
        quadtree.visit(function(quad, x1, y1, x2, y2) {
          if (quad.point && (quad.point !== d)) {
            var x = d.x - quad.point.x,
                y = d.y - quad.point.y,
                l = Math.sqrt(x * x + y * y),
                r = d.size*30/maxsize + quad.point.size*30/maxsize + padding;
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

plot_level2("27601", "#3366cc", "Condensed Matter Theory");