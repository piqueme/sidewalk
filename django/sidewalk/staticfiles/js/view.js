$(document).ready(function()
{
    $.ajaxSetup ({
        cache: false
    });

    start_autocomplete("current");
    start_search_listener("completed");
});

function start_autocomplete(current_or_completed)
{
    var url = '';
    if (current_or_completed === "current")
    {
        url = '../view/current/keywords';
    }
    else if (current_or_completed === "completed")
    {
        url = '../view/completed/keywords';
    }
    $.getJSON(url, function(data)
    {
        $("#keywords").autocomplete(
        {
            source: data,
            select: function(event, ui) 
            {
                $("#keywords").val(ui.item.value);
                $("#search-form").submit()
            }
        });
    });
}

function start_search_listener(current_or_completed)
{
    var search_url = '';
    if (current_or_completed === "current")
    {
        url = '../view/current';
    }
    else if (current_or_completed === "completed")
    {
        url = '../view/completed';
    }
    $("#search-form").submit(function(event) 
    {
        event.preventDefault();
        keyword_string = $("#keywords").val();
        keyword_split = keyword_string.split(" ");
        keyword_get = "keywords="; 
        for (var i = 0; i < (keyword_split.length - 1); i++)
        {
            keyword_get += keyword_split[i];
            keyword_get += "+";
        }
        keyword_get += keyword_split[keyword_split.length - 1];
        $("#searchtable").load(search_url, keyword_get);
    }); 
}
