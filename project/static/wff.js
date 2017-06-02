let svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height");

var format = d3.format(",d");

var color = d3.scaleOrdinal(d3.schemeCategory20);

var pack = d3.pack()
    .size([width, height])
    .padding(1.5);

d3.csv("/static/wefeelfine-feelings.csv", function (d) {
    d.count = +d.count;
    if (d.count) return d;
}, function (error, classes) {
    if (error) throw error;
    
    var root = d3.hierarchy({children: classes})
      .sum(function(d) { return d.count; })
      .each(function(d) {
        if (feeling = d.data.feeling) {
          var feeling, i = feeling.lastIndexOf(".");
          d.feeling = feeling;
          d.package = feeling.slice(0, i);
          d.class = feeling.slice(i + 1);
        }
      });

  var node = svg.selectAll(".node")
    .data(pack(root).leaves())
    .enter().append("g")
      .attr("class", "node")
      .attr("transform", d => "translate(" + d.x + "," + d.y + ")");

  node.append("circle")
      .attr("feeling", d => d.feeling)
      .attr("r", d => d.r)
      .style("fill", function(d) { return color(d.package); });

  node.append("clipPath")
      .attr("feeling", d => "clip-" + d.feeling)
    .append("use")
      .attr("xlink:href", d => "#" + d.feeling);

  node.append("text")
      .attr("clip-path", d => "url(#clip-" + d.feeling + ")")
    .selectAll("tspan")
    .data(d => d.class.split(/(?=[A-Z][^A-Z])/g))
    .enter().append("tspan")
      .attr("x", 0)
      .attr("y", (d, i, nodes) => 13 + (i - nodes.length / 2 - 0.5) * 10)
      .text(d => d);

  node.append("title")
      .text(d => d.feeling + "\n" + format(d.value));
});