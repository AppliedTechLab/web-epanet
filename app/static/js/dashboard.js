//http://fiddle.jshell.net/F6YaR/1/

var h = 250;
var w = 250;
var servers = ['S','R','W'];
var cities = ['Ashburn', 'Atlanta', 'Chicago'];
var matrix = [{"x": 60, "y": 40}, 
               {"x": 75, "y": 40},
               {"x": 90, "y": 40},
               {"x": 120, "y": 40},
               {"x": 135, "y": 40},
               {"x": 150, "y": 40},
               {"x": 180, "y": 40},
               {"x": 195, "y": 40},
               {"x": 210, "y": 40},
               {"x": 60, "y": 60}, 
               {"x": 75, "y": 60},
               {"x": 90, "y": 60},
               {"x": 120, "y": 60},
               {"x": 135, "y": 60},
               {"x": 150, "y": 60},
               {"x": 180, "y": 60},
               {"x": 195, "y": 60},
               {"x": 210, "y": 60},
               {"x": 60, "y": 80}, 
               {"x": 75, "y": 80},
               {"x": 90, "y": 80},
               {"x": 120, "y": 80},
               {"x": 135, "y": 80},
               {"x": 150, "y": 80},
               {"x": 180, "y": 80},
               {"x": 195, "y": 80},
               {"x": 210, "y": 80},
               ];

var up = [{"x": 40, "y": 40}];
var down = [{"x": 190, "y": 80}];

var svg = d3.select("body")
             .append("svg")
             .attr("width", w)
             .attr("height", h)
             .attr('class','radSol');

var texts = svg.selectAll("text")
                .data(matrix)
                .enter();

svg.selectAll("circle")
     .data(matrix)
     .enter()
     .append("circle")
     .attr("r", 4)
     .attr("cx", function (d) {
         return d.x;
     })
     .attr("cy", function (d) {
         return d.y;
     });
 
texts.append("text")
		.text(function(d,i){
     return servers[i]
    })
   .attr('font-size', 20)
   .attr('fill', 'white')
   .attr('x', function(d,i){
     return 75+60*i
    })
   .attr('y', h/9)
   .attr('text-anchor', 'middle')

texts.append("text")
	 .text(function(d,i){
     return cities[i]
    })
   .attr('font-size', 10)
   .attr('fill', 'white')
   .attr('y', function(d,i){
     return 43+20*i
    })
   .attr('x', 6)
   .attr('text-anchor', 'left')
