function plot_level3(level1, level2, color){

  var width = 280,
      height = 280,
      radius = 4,
      padding = 0.5;

  var force = d3.layout.force()
      .gravity(.08)
      .charge(-10)
      .linkDistance(30)
      .size([width, height]);

  d3.select("#article-network-level3").selectAll("*").remove();
  var svg = d3.select("#article-network-level3").append("svg")
      .attr("style", "outline: thin solid black;") 
      .attr("width", width)
      .attr("height", height);

  var tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([-10, 0])
    .html(function(d) {
      return "<strong>Doi:</strong> <span style='color:red'>" + d.name + "</span>";
    });

  // var fisheye = d3.fisheye
  //   .circular()
  //   .radius(20)
  //   .distortion(2);

  svg.call(tip);

  d3.json("../data/level3/"+level1+"_"+level2+"_citation_network.json", function(error, graph) {
    if (error) throw error;

    var link = svg.selectAll("line")
        .data(graph.links)
      .enter().append("line")
        .attr("stroke", "black")
        .attr("stroke-width", function(d){return d.value;});

    var node = svg.selectAll("circle")
        .data(graph.nodes)
      .enter().append("circle")
        .attr("r", function(d){return radius;})
        .style("fill", color)
        .style("stroke", function(d) { return d3.rgb(color).darker(); })
        .on("mouseover", function(d) {
          d3.select(this).attr("r", function(d){ return radius*2;});
          tip.show(d);
        })                  
        .on("mouseout", function(d) {
          d3.select(this).attr("r", function(d){ return radius;});
          tip.hide(d);
        })
        .on("click", function(d){
          if (d3.event.defaultPrevented) return;
          var array = d.name.split("/");
          var journal = array[1].split(".")[0];
          if(journal=="PhysRevLett"){
            journal = "prl";
          }else if(journal=="PhysRevX"){
            journal = "prx";
          }else{
            journal = "rmp";
          }
          var url = "https://journals.aps.org/"+journal+"/abstract/"+array[0]+"/"+array[1];
          var win = window.open(url, '_blank');
          win.focus();
          // $(location).attr('href', url);
          // window.location.assign(url, "_blank");
        })
        .call(force.drag);

    var title = svg.append("text")
      .attr("x", 10)
      .attr("y", 20)
      .attr("font-weight", "bold")
      .text("Articles with High Citations");

    force
        .nodes(graph.nodes)
        .links(graph.links)
        .on("tick", tick)
        .start();

    // svg.on("mousemove", function() {
    //   fisheye.center(d3.mouse(this));

    //   node.each(function(d) { d.fisheye = fisheye(d); })
    //       .attr("cx", function(d) { return d.fisheye.x; })
    //       .attr("cy", function(d) { return d.fisheye.y; })
    //       .attr("r", function(d) { return d.fisheye.z * 4.5; });

    //   link.attr("x1", function(d) { return d.source.fisheye.x; })
    //       .attr("y1", function(d) { return d.source.fisheye.y; })
    //       .attr("x2", function(d) { return d.target.fisheye.x; })
    //       .attr("y2", function(d) { return d.target.fisheye.y; });
    // });

    function tick() {

      node
          .each(collide(.5))
          .attr("cx", function(d) { return d.x = Math.max(radius, Math.min(width - radius, d.x)); })
          .attr("cy", function(d) { return d.y = Math.max(radius+20, Math.min(height - radius, d.y)); });

      link.attr("x1", function(d) { return d.source.x; })
          .attr("y1", function(d) { return d.source.y; })
          .attr("x2", function(d) { return d.target.x; })
          .attr("y2", function(d) { return d.target.y; });
    }

    // Resolves collisions between d and all other circles.
    function collide(alpha) {
      var quadtree = d3.geom.quadtree(graph.nodes);
      return function(d) {
        var r = radius + Math.max(padding),
            nx1 = d.x - r,
            nx2 = d.x + r,
            ny1 = d.y - r,
            ny2 = d.y + r;
        quadtree.visit(function(quad, x1, y1, x2, y2) {
          if (quad.point && (quad.point !== d)) {
            var x = d.x - quad.point.x,
                y = d.y - quad.point.y,
                l = Math.sqrt(x * x + y * y),
                r = radius + radius + padding;
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

function plot_level3_text(){

  var width = 280,
      height = 280,
      radius = 4,
      padding = 0.5;


  d3.select("#article-network-level3").selectAll("*").remove();
  var svg = d3.select("#article-network-level3").append("svg")
      .attr("style", "outline: thin solid black;") 
      .attr("width", width)
      .attr("height", height);

  var title = svg.append("text")
    .attr("x", 10)
    .attr("y", 20)
    .attr("font-weight", "bold")
    .text("Articles with High Citations");

  var text = svg.append("text")
        .attr("x", width/2)
        .attr("y", height/2)
        .attr("text-anchor", "middle")
        .attr("font-weight", "bold")
        .style("fill", "grey")
        .attr("font-family", "Monospace")
        .text("Click on a sub-community");
  var text2 = svg.append("text")
        .attr("x", width/2)
        .attr("y", height/2+20)
        .attr("text-anchor", "middle")
        .attr("font-weight", "bold")
        .style("fill", "grey")
        .attr("font-family", "Monospace")
        .text("to see the articles!");

} 

plot_level3("27601", "1500", "#3366cc");