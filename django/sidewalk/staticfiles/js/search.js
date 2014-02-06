var last_keyword_get = 'keywords=';
var next_search_page = 2;
var next_page_pull_count = 20;
var search_url = "../search/submit";

$(document).ready(function()
{
    $.ajaxSetup ({
        cache: false
    });

    start_autocomplete('quest');
    search_results_to_page();
    see_more_listener();
    add_model_select_listener();
    filter_change_listeners();
});

function add_model_select_listener()
{
    $("#search-model").change(function(event)
    {
        var model = $("#search-model").find(":selected").text().trim();
        if (model === "Adventurer")
        {
            start_autocomplete('user')
            $("#user-search-table").css("left", screen.width);
            $("#user-search-table").show();
            $("#search-model").blur();
            $("#search-filter").hide();
            $("#search-order").hide();
            $("#search-small-table").animate({
                left: ("-=" + screen.width)
            }, 1000, function()
            {
                $("#search-small-table").hide();
            });
            $("#user-search-table").animate({
                left: ("-=" + (screen.width))
            }, 1000, function()
            {
            });        
        }
        else if (model === "Quest")
        {
            $("#search-small-table").css("left", screen.width);
            $("#search-small-table").show();
            $("#search-model").blur();
            $("#search-filter").show();
            $("#search-order").show();
            $("#user-search-table").animate({
                left: ("-=" + screen.width)
            }, 1000, function()
            {
                $("#user-search-table").hide();
            });
            $("#search-small-table").animate({
                left: ("-=" + (screen.width))
            }, 1000, function()
            {

            });
        }    
    }); 
}

function filter_change_listeners()
{
    $("#search-filter").change(function(event)
    {
        var filter = $("#search-filter").find(":selected").text().trim();
        if (filter === "Current")
        {
            start_autocomplete('current');
        }
        else if (filter === "Completed")
        {
            start_autocomplete('completed');
        }
        else if (filter === "Allies'")
        {
            start_autocomplete('allied');
        }
        else if (filter === "All")
        {
            start_autocomplete('quest');
        }
    });
}

function start_autocomplete(model)
{
    var keywords_url = ('../search/keywords/' + model)
    $.getJSON(keywords_url, function(data) {
        $("#keywords").autocomplete({
            source: data,
            select: function(event, ui) {
                $("#keywords").val(ui.item.value);
                $("#search-form").submit();
            }
        });
    });
    if ($(".table tr").length < 21)
    {
        $("#next-results-page").hide();
    }
}

function start_user_autocomplete()
{
    $.getJSON('../search/user_keywords', function(data) {
        $("#keywords").autocomplete({
            source: data,
            select: function(event, ui) {
                $("#keywords").val(ui.item.value);
                $("#search-form").submit();
            }
        });
    });
    if ($(".table tr").length < 21)
    {
        $("#next-results-page").hide();
    }
}

function search_results_to_page()
{
    $("#search-form").submit(function(event) 
    {
        event.preventDefault();
        $("#keywords").blur();
        keyword_string = $("#keywords").val();
        keyword_split = keyword_string.split(" ");
        keyword_get = "keywords="; 
        for (var i = 0; i < (keyword_split.length - 1); i++)
        {
            keyword_get += keyword_split[i];
            keyword_get += "+";
        }
        keyword_get += keyword_split[keyword_split.length - 1];
        var filter = $("#search-filter").find(":selected").text();
        var order = $("#search-order").find(":selected").text();
        var model = $("#search-model").find(":selected").text();
        keyword_get += ("&filter=" + filter);
        keyword_get += ("&order=" + order);
        keyword_get += ("&model=" + model); 
        last_keyword_get = keyword_get;
        if (model.trim() === "Adventurer")
        {
            $("#user-search-table").load(search_url, keyword_get);
        }
        else
        {
            $("#search-small-table").load(search_url, keyword_get);
        }
        next_search_page = 2;
        $("#next-results-page").show();
        if ($(".table tr").length < 21)
        {
            $("#next-results-page").hide();
        }
    }); 
}

function see_more_listener()
{
    $("#next-results-page").click(function(event)
    {
        event.preventDefault();
        pagestring = (last_keyword_get + "&");
        pagestring += ("page=" + next_search_page);
        pagestring += ("&count=" + next_page_pull_count);
        $.get(search_url, pagestring, function(data)
        {
            $("#searchtable").append(data);
            next_search_page += 1;
            $(function(){
                $('.star').raty({
                    readOnly  : true,
                    cancel    : false,
                    half      : true,
                    size      : 25,
                    starHalf  : 'star-half.png',
                    starOff   : 'star-off.png',
                    starOn    : 'star-on.png',
                    path      : '/static/images',
                    score: function() {
                        return $(this).attr('data-score');
                    }
                });
            });
        }, "html");
        if (next_search_page == 6)
        {
            $("#next-results-page").hide();
        }
        if ($(".table tr").length < 21)
        {
            alert('here');
            $("#next-results-page").hide();
        }
    });
}

