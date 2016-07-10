var expanded = false;
var coords;
var scale;
var projection;
var path;
var svg
var tooltip
var width = screen.width, height = screen.height;
var filePath = "https://raw.githubusercontent.com/VikingProgrammer/Data_Data_Everywhere/master/Refugee_Map_09_07_2016/data/countries.json"


projection = d3.geo.albers()
.center([1.0,53])
.rotate([4.4, 0])
.parallels([50, 60])
.scale(600)
.translate([width / 2, height / 2]);

projection = d3.geo.mercator()
.center([0, 5 ])
.scale(900)
.rotate([-180,0]);

path = d3.geo.path().projection(projection);

svg = d3.select("body").append("svg").attr("width", width).attr("height", height);

d3.json("https://raw.githubusercontent.com/VikingProgrammer/Data_Data_Everywhere/master/Refugee_Map_09_07_2016/data/countries.json", function(error, countries) {
    console.log(countries)
    if (error) return console.error(error);

    var subunits = topojson.feature(countries, countries.objects.countries)
    console.log(subunits)
    svg.selectAll("path").data(subunits).enter().append("path").attr("d", path)
    //.attr("class", function(d) { return "path " + d.id; })
});