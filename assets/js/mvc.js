var console = (function () {
    
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
            $("#scroll").click();
        }
        
        /*
        Calls the graph to be made
        */
        function makeGraph(connection) {
            console.log('making graph...');
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
        
        function makeGraph(connection) {
            model.makeGraph(connection);
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
        console.setup($(this));
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
});