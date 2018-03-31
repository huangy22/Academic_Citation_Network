function plot_theme_level1(){

  var width = 600,
    height = 400;

  d3.json('../data/level1/theme_river.json', function(data) {
      nv.addGraph(function() {
        var chart = nv.models.stackedAreaChart()
                      .style('stream')
                      .margin({right: 40})
                      .x(function(d) { return d[0]; }) //We can modify the data accessor functions...
                      .y(function(d) { return d[1]; })   //...in case your data is formatted differently.
                      .color(function(d){return d.color;})
                      .useInteractiveGuideline(true)    //Tooltips which show all data points. Very nice!
                      .rightAlignYAxis(true)      //Let's move the y-axis to the right side.
                      .showLegend(false)
                      // .Duration(500)
                      .showControls(true)       //Allow user to choose 'Stacked', 'Stream', 'Expanded' mode.
                      .clipEdge(true);

        //Format x-axis labels with custom function.
        chart.xAxis
            .tickFormat(function(d) { 
              return d3.time.format('%x')(new Date(d)) 
        });

        chart.yAxis
            .tickFormat(d3.format(',.2f'));

        d3.select("#article-theme-river-level1").selectAll("*").remove();
        var svg = d3.select("#article-theme-river-level1").append("svg")
            // .attr("style", "outline: thin solid black;") 
            .attr("width", width)
            .attr("height", height)
            .datum(data)
            .call(chart);

        nv.utils.windowResize(chart.update);

        return chart;
    },
    function(){
    	d3.selectAll(".nv-area").on('click',
        function(d){
           plot_theme_level2(d.number, d.color);
           plot_level2(d.number, d.color, d.key);
           plot_level3_text();
        });
    });
  });

}

function plot_theme_level2(level1, color){

  var width = 600,
    height = 400;

  d3.json('../data/level2/'+level1+'_theme_river.json', function(data) {
      nv.addGraph(function() {
        var chart = nv.models.stackedAreaChart()
                      .margin({right: 40})
                      .x(function(d) { return d[0]; }) //We can modify the data accessor functions...
                      .y(function(d) { return d[1]; })   //...in case your data is formatted differently.
                      .color(function(d){ return d3.rgb(color).brighter(d.key/3);})
                      .useInteractiveGuideline(true)    //Tooltips which show all data points. Very nice!

                      .rightAlignYAxis(true)      //Let's move the y-axis to the right side.
                      // .Duration(500)
                      .clipEdge(true);

        //Format x-axis labels with custom function.
        chart.xAxis
            .tickFormat(function(d) { 
              return d3.time.format('%x')(new Date(d)) 
        });

        chart.yAxis
            .tickFormat(d3.format(',.2f'));

        d3.select("#article-theme-river-level2").selectAll("*").remove();
        var svg = d3.select("#article-theme-river-level2").append("svg")
            // .attr("style", "outline: thin solid black;") 
            .attr("width", width)
            .attr("height", height)
            .datum(data)
            .call(chart);

        // d3.select("#article-theme-river-level2").selectAll("svg .nv-area")
        //   .attr("opacity", 0.5); 

        nv.utils.windowResize(chart.update);
        return chart;
    });
  });

}

plot_theme_level1();
plot_theme_level2(27601, "#3366cc");
