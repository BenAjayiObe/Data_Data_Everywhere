var expanded = false;
var coords;
var scale;
var projection;
var path;
var svg
var tooltip
var width = screen.width, height = screen.height;


function loadMapDets(coordinates, theScale){
  projection = d3.geo.albers()
                        .center(coordinates)
                        .rotate([4.4, 0])
                        .parallels([50, 60])
                        .scale(theScale)
                        .translate([width / 2, height / 2]);

  path = d3.geo.path().projection(projection);

  svg = d3.select("#map_area").append("svg")
                                  .attr("width", width)
                                  .attr("height", height);
  tooltip = d3.select('body').append('div')
              .attr('class', 'hidden tooltip');
}

d3.json(filePath, function(error, wales_constituencies) {
    console.log(filePath);
    console.log(wales_constituencies)
    if (error) return console.error(error);

    var geofeatures = topojson.feature(wales_constituencies, wales_constituencies.objects.wpc);
    geo_var = wales_constituencies;
    //Merge the ag. data and GeoJSON
    //Loop through once for each ag. data value
    for (var i = 0; i < data_var.length; i++) {
        //Grab state name
        var dataState = data_var[i].Constituent;
        //Grab data value
        var dataValue = data_var[i].Name;

        //Find the corresponding state inside the GeoJSON
        for (var j = 0; j < geofeatures.features.length; j++) {

        var jsonState = geofeatures.features[j].properties.PCON13NM;

        if (dataState == jsonState) {

            //Copy the data value into the JSON
            geofeatures.features[j].properties.test = dataValue;

            //Stop looking through the JSON
            break;

          }
        }
      }
    svg.selectAll(".wpc")
    .data(geofeatures.features)
    .enter().append("path")
    .attr("class", function(d) { return "wpc " + d.id; })
    .attr("d", path)
    .attr("tabindex", "0")
    .attr("transform", function(d) {
      var centroid = path.centroid(d),
        x = centroid[0],
        y = centroid[1];
        return "translate(" + x + "," + y + ")" + "scale(0)" + "translate(" + -x + "," + -y + ")";
      })
    .style("stroke-width", function(d) {
      return 1;
    })
    .on('mousemove', function(d) {
                if (expanded == false){
                    var mouse = d3.mouse(svg.node()).map(function(d) {
                        return parseInt(d);
                    });
                    tooltip.classed('hidden', false)
                        .attr('style', 'left:' + (mouse[0] + 10) +
                                'px; top:' + (mouse[1] + 20) + 'px')
                        .html(d.properties.PCON13NM);
                }
                })
    .on('mouseout', function() {
                    tooltip.classed('hidden', true);
                })
    .on("click",function(d) {
      var selectedgroup = d3.select(this);
      console.log(selectedgroup);
    });
    svg.selectAll(".wpc")
    .transition()
    .duration(1000)
    .attr("transform", function(d) {
      var centroid = path.centroid(d),
        x = centroid[0],
        y = centroid[1];
        return "translate(" + x + "," + y + ")" + "scale(0.97)" + "translate(" + -x + "," + -y + ")";
      })
});