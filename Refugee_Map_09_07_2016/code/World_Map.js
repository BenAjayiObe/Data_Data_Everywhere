var expanded = false;
var coords;
var scale;
var projection;
var path;
var svg
var tooltip
var width = screen.width, height = screen.height;
var filePath = "https://raw.githubusercontent.com/VikingProgrammer/Data_Data_Everywhere/master/Refugee_Map_09_07_2016/data/countries.geojson"


projection = d3.geo.albers()
.center([1.0,53])
.rotate([4.4, 0])
.parallels([50, 60])
.scale(600)
.translate([width / 2, height / 2]);

path = d3.geo.path().projection(projection);

svg = d3.select("#map_area").append("svg")
.attr("width", width)
.attr("height", height);
tooltip = d3.select('body').append('div')
.attr('class', 'hidden tooltip');


d3.json(filePath, function(error, countries) {
    console.log(filePath);
    console.log(countries)
    if (error) return console.error(error);

    alert(countries.features)
    svg.selectAll("path")
    .data(countries.features)
    .enter().append("path")
    .attr("class", function(d) { return "path " + d.id; })
    .attr("d", path)
});