var width = window.innerWidth;
var height = window.innerHeight;

var foo1 = [["A0",[width*1/8,height*5/6],[7],50],
		["A1",[width*2/8,height*5/6],[7,8],50],
		["A2",[width*3/8,height*5/6],[8],50],
		["A3",[width*4/5,height*5/6],[8,9,10],50],
		["A4",[width*5/8,height*5/6],[9],50],
		["A5",[width*6/8,height*5/6],[11],50],
		["A6",[width*7/8,height*5/6],[11],50],
		["B0",[width*1/5,height*4/6],[12],50],
		["B1",[width*2/5,height*4/6],[12],50],
		["B2",[width*3/5,height*4/6],[12],50],
		["B3",[width*4/5,height*4/6],[12],50],
		["C0",[width/2,height/2],[15,16,17],50],
		["D0",[width*1/4,height*2/6],[16,17,18,19],50],
		["D1",[width*2/4,height*2/6],[19,20,22],50],
		["D2",[width*3/4,height*2/6],[20,21,22],50],
		["E0",[width*1/9,height*1/6],[],50],
		["E1",[width*2/9,height*1/6],[],50],
		["E2",[width*3/9,height*1/6],[],50],
		["E3",[width*4/9,height*1/6],[],50],
		["E4",[width*5/9,height*1/6],[],50],
		["E5",[width*6/9,height*1/6],[],50],
		["E6",[width*7/9,height*1/6],[],50],
		["E7",[width*8/9,height*1/6],[],50],
		]

var foo2 = [["B0",[width*1/5,height*5/6],[6],50],
		["B1",[width*2/5,height*5/6],[6],50],
		["B2",[width*3/5,height*5/6],[6],50],
		["B3",[width*4/5,height*5/6],[6,7],50],
		["B4",[width*4/5,height*5/6],[7],50],
		["C0",[width*1/3,height*4/6],[8],50],
		["C1",[width*2/3,height*4/6],[8],50],
		["D0",[width*1/2,height*3/6],[9,10,11,12],50],
		["E0",[width*1/5,height*2/6],[13,14,15],50],
		["E1",[width*2/5,height*2/6],[15],50],
		["E2",[width*3/5,height*2/6],[16,17],50],
		["E3",[width*4/5,height*2/6],[17],50],
		["F0",[width*1/7,height*1/6],[],50],
		["F1",[width*2/7,height*1/6],[],50],
		["F2",[width*3/7,height*1/6],[],50],
		["F3",[width*4/7,height*1/6],[],50],
		["F4",[width*5/7,height*1/6],[],50],
		["F5",[width*6/7,height*1/6],[],50]
		]

var papers1 = []
var papers2 = []
var lines1 = []
var lines2 = []

for(l in foo1) {
	papers1.push({
		'title': foo1[l][0],
		'title_href': "",
		'successors': foo1[l][2],
		'location': foo1[l][1],
		'radius': foo1[l][3]
	})
}
for(l in foo2) {
	papers2.push({
		'title': foo2[l][0],
		'title_href': "",
		'successors': foo2[l][2],
		'location': foo2[l][1],
		'radius': foo2[l][3]
	})
}
for(l in papers1){
	paper = papers1[l]
	paperSuccessors = papers1[l].successors;
	for(i in paperSuccessors){
		successor = papers1[paperSuccessors[i]];
		lines1.push([paper.location[0],paper.location[1]-paper.radius,successor.location[0],successor.location[1]+successor.radius]);
	}
}
for(l in papers2){
	paper = papers2[l]
	paperSuccessors = papers2[l].successors;
	for(i in paperSuccessors){
		successor = papers2[paperSuccessors[i]];
		lines2.push([paper.location[0],paper.location[1]-paper.radius,successor.location[0],successor.location[1]+successor.radius]);
	}
}


$(document).ready(function(){
	var svg = d3.select('svg')
	    .attr('width',width)
	    .attr('height',height);

	svg.append('svg:defs').selectAll('marker')
	    .data(['end'])
	  .enter().append('svg:marker')
	    .attr('id', 'end')
	    .attr('viewBox', '0 -5 10 10')
	    .attr('refX', 15)
	    .attr('refY',-1.5)
	    .attr('markerWidth', 6)
	    .attr('markerHeight', 6)
	    .attr('orient','auto')
	  .append('svg:path')
	    .attr('d', 'M0,-5L10,0L0,5');

	var lines = svg.append('svg:g').selectAll('line')
        .data(lines1)
      .enter().append('line')
      	.attr('class','line')
      	.attr('x1',function(d){return d[0];})
      	.attr('y1',function(d){return d[1];})
      	.attr('x2',function(d){return d[2];})
      	.attr('y2',function(d){return d[3];})
      	.attr('stroke-width',3)
      	.attr('stroke','black')
      	.attr('marker-end', 'url(#end)');

    svg.selectAll(".line")
    .attr("marker-end", "url(#end)");

	var nodes = svg.append('g')
	    .attr('class','nodes')
	 	.selectAll('circle')
        .data(papers1)
      .enter().append('g')
        .attr('transform', function(d) {
        	return 'translate(' + d.location[0] + ',' + d.location[1] + ')';
        })
        .on('click',function(){alert("Present info");});
    nodes.append('circle')
        .attr('class','node')
        .attr('r',function(d){return d.radius})
        .attr('fill','white')
        .attr('stroke','black')
        .attr('stroke-width','3');
    nodes.append('text')
        .attr('text-anchor','middle')
        .text(function(d) {
        	return d.title;
        })
        .attr('class', 'hyper').on('click',function(d){window.location.href = d.title_href });    

    $("#transitionButton").click(function() {
    	// var line = svg.selectAll('.line')
    	// 	.data(function(d) {return d.title;});
    	// var lineUpdate = d3.transition(line)
    	//     .attr('d',d3.scg.line().interpolate('linear'));
    });
});