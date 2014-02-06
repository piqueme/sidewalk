$(document).ready(function()
{      
    $("#comments-panel").hide(); 
    var toggle = false;
    $("#comments-icon").click(function(event)
    {
        event.preventDefault();
        if (!toggle)
        {
            $("#comments-icon").css('color', "#ffffff");
            getCommentsPanelContents();
            toggle = true;
            $("#comments-panel").show();
        }
        else
        {
            $("#comments-icon").css('color', "#999999");
            toggle = false;
            $("#comments-panel").hide();
        }
    });
    timelineViewListener();
});

function timelineViewListener()
{
    $("#all-comments").click(function(event)
    {
        event.preventDefault();
        var url_split = (document.URL).split('/');
        if (url_split[url_split.length - 3] === "profile")
        {
            var profile_url = $("#comments-form").attr("action");
            $("#comments-form").attr("action", ("../" + profile_url))
        }
        else if (url_split[url_split.length - 3] === "quest")
        {
            var profile_url = $("#comments-form").attr("action");
            $("#comments-form").attr("action", ("../" + profile_url))
        }
        $("#comments-form").submit();
    });
}

function commentListeners()
{
    $(".comment-row").click(function() 
    {
        var url_split = (document.URL).split('/');
        if (url_split[url_split.length - 3] === "profile")
        {
            var profile_url = $("#comments-form").attr("action");
            $("#comments-form").attr("action", ("../" + profile_url));    
        }
        else if (url_split[url_split.length - 3] === "quest")
        {
            var profile_url = $("#comments-form").attr("action");
            $("#comments-form").attr("action", ("../" + profile_url));    
        }
        var questid = $(event.target).attr("class").split(' ')[1];
        $("#quest-id").val(questid);
        $("#comments-form").submit();
    });
}

function getCommentsPanelContents() 
{
    var comments_url = "../comments";
    var url_split = (document.URL).split('/');
    if  (url_split[url_split.length - 3] === "profile")
    {
        comments_url = "../../../../comments";
    }
    else if (url_split[url_split.length - 3] === "quest") 
    {
        comments_url = "../../../../comments";
    }
    $.get(comments_url, 'empty', function(data)
    {
        $("#comments-table").html(data);
        commentListeners();
    }, "html");
}
