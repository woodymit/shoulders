function getAuthorName(currentValue, i, a) {
    if (!currentValue[1]) {
        return currentValue[0]
    };

    return '<a href=' + currentValue[1] + '>' + currentValue[0] + '</a>'
};


function handleGraphCreateResponse(response) {

    // var parsed_json = JSON.parse(response);
    // ## RENDER D3 HERE
    return

};


function selectPaper(title) {
    console.log('Log 4');
    $("#console").empty();
    $.ajax({
            type: 'POST',
            url: '/graph',
            data: {'title': title,
                    // 'citer_page_num': citers_page_num,
                    'height': window.innerHeight,
                    'width': window.innerWidth},
            success: handleGraphCreateResponse
        });
};

function handleSearchResponse(response) {
    // console.log(response);
    html_to_append = '';

    var parsed_json = JSON.parse(response);

    for (i in parsed_json) {
        var p = parsed_json[i];
        var authors = p['author_list:'];
        var citers = p['citers_page_href:'];
        var title = p['title:'];
        console.log('title:' + title);

        // var splits = citers.split(/cites=([\d]+)&as_sdt/);
        // citers_num = splits[1];

        html_to_append = html_to_append +
        '<div class="page-header col-lg-8 col-centered searchResult">' + 
            '<h4 ><a id="search'+i.toString()+'">' + p['title:'] + '</a></h4>' +
            '<h5><a target="_blank" href="' + p['title_href:'] + '">Go to Article</a></h5>' +
            '<h5>' + authors.map(getAuthorName)  + '</h5>' +
            '<button class="btn" onclick="selectPaper(&quot;' + title + '&quot;)">Show Lineage</button>' +
            // '<button class="btn" onclick="selectPaper(&quot;buttholesz&quot;)">Show Lineage</button>' +
        '</div>\n';
    };

    var searchTitle = $('<div class="col-lg-8 col-centered text-center"><h2 class="heading seachTitle">Select an Article</h2></div>');
    console.log('Log 1');
    $("#console").append(searchTitle, html_to_append);
    console.log('Log 2');
    $("#scroll").click();
    console.log('Log 3');
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


function renderD3(paperList) {
    duration=5000;

    //size svg
    svg = d3.select('svg')
        .attr('width',window.innerWidth)
        .attr('height',window.innerHeight);

    // create arrow
    svg.select('defs')
        .selectAll('marker')
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

    // create list of line data from paperList
    lineList = [];
    for(l in paperList){
        paper = paperList[l]
        paperSuccessors = paperList[l].successors;
        for(i in paperSuccessors){
            successor = paperList[paperSuccessors[i]];
            lineList.push(
                {'endpoints': [paper.location[0],
                               paper.location[1]-paper.radius,
                               successor.location[0],
                               successor.location[1]+successor.radius],
                 'nodes': [paper.title,successor.title]});
        }
    }


    var lines = svg.select('.lineGroup')
        .selectAll('line')
        .attr('class','line')
        .data(lineList, function(d) {return d.nodes;});
    // update lines that stay
    lines.transition()
        .duration(duration)
        .attr('d',d3.svg.line().interpolate('linear'))
        .attr('x1',function(d){return d.endpoints[0];})
        .attr('y1',function(d){return d.endpoints[1];})
        .attr('x2',function(d){return d.endpoints[2];})
        .attr('y2',function(d){return d.endpoints[3];});
    // get rid of old lines
    lines.exit()
      .attr('opacity',1)
      .transition()
        .duration(duration)
        .attr("opacity", 1e-6)
        .remove();
    // make new lines
    var lineEnter = lines.enter()
      .append('line')
        .attr('opacity',0)
        .attr('class','line')
        .attr('x1',function(d){return d.endpoints[0];})
        .attr('y1',function(d){return d.endpoints[1];})
        .attr('x2',function(d){return d.endpoints[2];})
        .attr('y2',function(d){return d.endpoints[3];})
        .attr('stroke-width',3)
        .attr('stroke','black')
        .attr('marker-end', 'url(#end)')
      .transition()
        .duration(duration)
        .attr('opacity',1);

    
    var nodes = svg.select('.lineGroup')
        .selectAll('g')
        .attr('class','node')
        .data(paperList, function(d) {return d.title;});
    // update nodes that stay
    nodes.transition()
        .duration(duration)
        .attr('transform', function(d){return "translate(" + d.location[0] + ',' + d.location[1] + ")";})
      .select('circle')
        .attr('r',function(d){return d.radius;});
    // get rid of old nodes
    nodes.exit()
      .attr('opacity',1)
      .transition()
        .duration(duration)
        .attr("opacity", 1e-6)
        .remove();
    // make new nodes
    nodeEnter = nodes.enter().append('g');
    nodeEnter.attr('class','node')
        .on('click',function(){alert("Present info");})
        .on('mouseover',function(){})
        .attr('opacity',0)
        .attr('transform', function(d) {
            return 'translate(' + d.location[0] + ',' + d.location[1] + ')';
        })
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
    nodeEnter.transition()
        .duration(duration)
        .attr('opacity',1);
};