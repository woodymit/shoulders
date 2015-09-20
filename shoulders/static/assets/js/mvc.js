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
        lines1.push({'endpoints': [paper.location[0],
                                   paper.location[1]-paper.radius,
                                   successor.location[0],
                                   successor.location[1]+successor.radius],
                      'nodes': [paper.title,successor.title]});
    }
}
for(l in papers2){
    paper = papers2[l]
    paperSuccessors = papers2[l].successors;
    for(i in paperSuccessors){
        successor = papers2[paperSuccessors[i]];
        lines2.push({'endpoints': [paper.location[0],
                                  paper.location[1]-paper.radius,
                                  successor.location[0],
                                  successor.location[1]+successor.radius],
                     'nodes': [paper.title,successor.title]});
    }
}

function getAuthorName(currentValue, i, a) {
    if (!currentValue[1]) {
        return currentValue[0]
    };

    return '<a href=' + currentValue[1] + '>' + currentValue[0] + '</a>'
};

function selectPaper(citers_page_href) {
    $("#console").empty();
    $("#console").append(citers_page_href);
};

function handleSearchResponse(response) {
    // console.log(response);
    html_to_append = '';

    var parsed_json = JSON.parse(response);

    for (i in parsed_json) {
        var p = parsed_json[i];
        var authors = p['author_list:'];

        html_to_append = html_to_append +
        '<div onclick=selectPaper(' + p['citers_page_href:'] + ') class="page-header col-lg-8 col-centered searchResult">' +
            '<h4><a href=' + p['title_href:'] + '>' + p['title:'] + '</a></h4>' +
            '<h5>' + authors.map(getAuthorName)  + '</h5>' +
            '<h6>Not a real journal. 2014 Oct 23;514(7523):455-61. doi: 10.1038/nature13808. Epub 2014 Oct 8.</h6>' +
        '</div>\n'
    }

    var searchTitle = $('<div class="col-lg-8 col-centered text-center"><h2 class="heading seachTitle">Select an Article</h2></div>');
    $("#console").append(searchTitle, html_to_append);
    $("#scroll").click();
};

var mvc = (function () {
    
    ///////////////////////////////////////
    /////
    /////        MODEL
    /////
    ///////////////////////////////////////
    /*
    Keeps the internal state of the app and updates the view accordingly
    */
    function Model() {
        var c = C(),
        exports = {},
        handler = UpdateHandler();

        /*
        Searches for relevant articles.
        */
        function searchArticles() {
            $("#console").empty();

            var search_string = $('#search-txt').val();

            $.ajax({
                type: 'POST',
                url: '/search',
                data: {'search_string': search_string},
                success: handleSearchResponse
            });
        }
        
        /*
        Calls the graph to be made
        */
        function makeGraph() {
            
        }
        
        exports.searchArticles = searchArticles;
        exports.on = handler.on;
        exports.makeGraph = makeGraph;
        
        return exports;
    }
    
    
    ///////////////////////////////////////
    /////
    /////        CONTROLLER
    /////
    ///////////////////////////////////////
    
    /*
    Connects components in the view to functions and responses
    resulting in change in the model.
    */
    function Controller(model) {
        function search() {
            model.searchArticles();
        }
        
        function makeGraph() {
            model.makeGraph();
        }
        
        return {searchArticles: search, makeGraph: makeGraph};
    }
    
    
    ///////////////////////////////////////
    /////
    /////        VIEW
    /////
    ///////////////////////////////////////
    
    /*
    Creates all components in the flowchart
    and connects them to the controller for updating
    */
    function View(div, model, controller) {
        
        //Define all visual containers
        var displayArea = $("<div class='displayArea'></div>");

        //Adds all visual containers
        div.append(displayArea);

        var searchBtn = $('<button id="search-btn" class="btn btn-info btn-lg" type="button"><i class="glyphicon glyphicon-search"></i></button>');
        $(".input-group-btn").append(searchBtn);
        searchBtn.on('click', controller.searchArticles);

        $("#search-txt").keyup(function(event){
            if(event.keyCode == 13){
                searchBtn.click();
            }
        });
    }

    /*
    Creates a model, view and controller system 
    */
    function setup(div) {
            var model = Model();
            var controller = Controller(model);
            var view = View(div, model, controller);
    }
    
    return {setup: setup};
})();

$(document).ready(function () {
    $('#console').each(function () {
        mvc.setup($(this));
    });

    $('a[href^="#"]').on('click',function (e) {
        e.preventDefault();

        var target = this.hash;
        var $target = $(target);

        $('html, body').stop().animate({
            'scrollTop': $target.offset().top
        }, 900, 'swing', function () {
            window.location.hash = target;
        });
    });

    // renderD3();
});


function renderD3() {
    //D3
    var svg = d3.select('svg')
        .attr('width', width)
        .attr('height', height);

    // var defs = svg.append('svg:defs');
    // var marker = defs.selectAll('marker')
    //  .data([{ id: 0, name:'arrow',path: 'M 0,0 m -5,-5 L 5,0 L -5,5 Z', viewbox: '-5 -5 10 10'}])
    //      .enter().append('svg:marker')
    //        .attr
    svg.append('svg:defs').selectAll('marker')
        .data(['end'])
      .enter().append('svg:marker')
        .attr('id', 'end')
        .attr('viewBox', '0 -5 10 10')
        .attr('refX', 10)
        .attr('refY', 0)
        .attr('markerWidth', 6)
        .attr('markerHeight', 6)
        .attr('orient','auto')
      .append('svg:path')
        .attr('d', 'M0,-5L10,0L0,5');

    var lines = svg.append('svg:g').selectAll('line')
        .data(lines1)
      .enter().append('line')
        .attr('class','line')
        .attr('x1',function(d){return d.endpoints[0];})
        .attr('y1',function(d){return d.endpoints[1];})
        .attr('x2',function(d){return d.endpoints[2];})
        .attr('y2',function(d){return d.endpoints[3];})
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
        .attr('class','node')
        .attr('transform', function(d) {
            return 'translate(' + d.location[0] + ',' + d.location[1] + ')';
        })
        .on('click',function(){alert("Present info");});
    nodes.append('circle')
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
        // update lines that stay
        var line = svg.selectAll('.line')
            .data(lines2, function(d) {return d.nodes;});
        var lineUpdate = d3.transition(line)
            .attr('d',d3.svg.line().interpolate('linear'));
        lineUpdate.attr('x1',function(d){return d.endpoints[0];})
            .attr('y1',function(d){return d.endpoints[1];})
            .attr('x2',function(d){return d.endpoints[2];})
            .attr('y2',function(d){return d.endpoints[3];});
        // get rid of old lines
        line.exit().remove();
        // make new lines
        var lineUpdate = line.enter().append('line')
            .attr('class','line')
            .attr('x1',function(d){return d.endpoints[0];})
            .attr('y1',function(d){return d.endpoints[1];})
            .attr('x2',function(d){return d.endpoints[2];})
            .attr('y2',function(d){return d.endpoints[3];})
            .attr('stroke-width',3)
            .attr('stroke','black')
            .attr('marker-end', 'url(#end)');
        

        // update nodes that stay
        var node = svg.selectAll('.node')
            .data(papers2, function(d) {return d.title;})
        var nodeUpdate = d3.transition(node)
            .attr('transform', function(d){return "translate(" + d.location[0] + ',' + d.location[1] + ")";});
        nodeUpdate.attr('r', function(d){return d.radius;})
        // get rid of old nodes
        node.exit().remove();
        // make new nodes
        var nodeEnter = node.enter().append('g')
            .attr('class','node')
            .attr('transform', function(d) {
                return 'translate(' + d.location[0] + ',' + d.location[1] + ')';
            })
            .on('click',function(){alert("Present info");});
        nodeEnter.append('circle')
            .attr('r',function(d){return d.radius})
            .attr('fill','white')
            .attr('stroke','black')
            .attr('stroke-width','3');
        nodeEnter.append('text')
            .attr('text-anchor','middle')
            .text(function(d) {
                return d.title;
            })
            .attr('class', 'hyper').on('click',function(d){window.location.href = d.title_href });
    });
};