$(document).ready(function() {
    $.ajaxSetup ({
        cache: false
    });
    hideAllAlerts();
    tabSlider();
    makeAllyFormListener();
    removeAllyFormListener();
    $('.thumbnail-viewer').carousel();
    startingTimeline();
});

function startingTimeline()
{
    var tlstartindicator = $("#timeline-start-indicator").text().trim();
    if (tlstartindicator !== "false")
    {
        $("#profile-divider").click();
    } 
    $("#timeline-start-indicator").text("false");
}

function goToTimeline(questid)
{
    $((".quest-node[data-questid='" + questid + "']")).parent().click(); 
    $("#timeline-start-questid").text("false"); 
}

function loadIScroll () {
    var myScroll = new IScroll('#timeline-wrapper');/*, {
        indicators: {
            ignoreBoundaries: true
        }
    });*/
    $("timeline-panel").css('height', (window.innerHeight - 130) + 'px');
    console.log("pop");
}

function loadTimeline() {
    var username = $("#timeline-tab").data("username");
    $("#timeline").load("../../profile/" + username + "/timeline", function() {
        timelineCreate(loadIScroll);
    }); 
}

function generateLine(time_diff, position) {
    time_diff += 17
    time_diff += "px";
    position += "px";
    var div = jQuery('<div/>', {
                class: 'timeline-stuff line',
            });
    div.css("height", time_diff);
    div.css("top", position);

    return div;
}

function generateCircle(position) {
    position += "px";
    var div = jQuery('<div/>', {
                class: 'timeline-stuff circle-node',
            });
    div.css("top", position);
    return div;
}

function timelineCreate(callback) {
    var loadedtext = $("#timeline").text();
    loadedtext = $.trim(loadedtext);
    if (loadedtext==="") {
        $("#timeline").html("<div id='empty-timeline-error'>Oops! This user has no completed quests.</div>");
    }

    var first = true;
    var line_position = 30;
    var circle_position = 15;
    var time_diff = 100;

    $(".quest-node").each(
        function() {    
            if (first) {
                var time_diff = $(this).data("timediff");
                $(this).wrap(generateCircle(circle_position));
                first = false;
            }
            else {
                time_diff = $(this).data("timediff");
                $(this).after(generateLine(time_diff, line_position));
                $(this).wrap(generateCircle(circle_position));
                line_position += 30 + time_diff;
            }
            
            circle_position += 30 + time_diff;
            
    });
    /*for (var i=0; i<10; i++) {
        $("#timeline-panel").append(generateLine(time_diff, line_position));
        line_position += 30;
        console.log("akdjfg");
    }*/
    callback();
}   


function placePopovers() {
    $('.circle-node').each(function(){
        var questname = $(this).children().first().data('questname');
        var date = $(this).children().first().data('date');
        var text = "<p>" + questname + "</p><p>" + "Date completed: " + date + "</p>";
        $(this).popover({
            placement: "right",
            trigger: "hover",
            container: "body",
            html: true,
            content: text
        });
    });
}

function challengeListeners() {
    $(".challenge-text").click(function(){
        $(".challenge-photo").hide();
        var cname = $(this).attr('id');
        console.log("text id " + cname);
        var cid = "#challenge-photo-" + cname.split('-')[2];
        console.log("selector for photo " + cid);
        if ($("#photo-filler").css('display') != "none") {
            $("#photo-filler").fadeOut();
        }
        console.log($(cid).length);
        $(cid).fadeIn();
    });
}

function nodeListeners() {
    $(".circle-node").click(function(){
        var questname = $(this).children().first().data('questname');
        var questid = $(this).children().first().data('questid');
        var questpostername = $(this).children().first().data('questpostername');
        console.log(questname);
    
        var username = $("#timeline-tab").data("username");
        var getstring = ("quest_id=" + questid);
        $("#photo-panel").load("../../profile/" + username + "/timeline/quest", getstring, function() {
            $(".challenge-photo").hide();
            challengeListeners();
            commentFormListener();
        });
    });
    var tlstartquestid = $("#timeline-start-questid").text().trim();
    if (tlstartquestid !== "false")
    {
        goToTimeline(tlstartquestid);
    }
}

function commentFormListener() {

    $('#comment-form').submit(function(event)
    {
        event.preventDefault();
        var comment = $('#comment-textarea').val();
        var questid = $(this).children().first().data('questid');
        var usernameposter = $(this).children().first().data('usernameposter');
        csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;

        $.ajax({
            type: 'POST',
            url: 'timeline/comment',
            data: {
                quest_id: questid,
                username_poster: usernameposter,
                comment: comment,
                csrfmiddlewaretoken: csrf_token
            },
            success: function(data) {
                addComment(data);
            }
        });
    });
    var tlstartquestid = $("#timeline-start-questid").text().trim();
    if (tlstartquestid !== "false")
    {
        goToTimeline(tlstartquestid);
    }
}

function addComment(data) {
    $("#comments-table").append(data);
    $("#comment-textarea").val("");
    var rowpos = $('#comments-table tr:last').position();
    //$('#photo-panel-body').scrollTop(rowpos.top);
    $('#photo-panel-body').stop().animate({
        scrollTop: rowpos.top
    }, 1500);

}

function tabSlider() {
    $("#timeline-divider").click(
        function() {
            $("#timeline-tab").slideToggle();
            $("#profile-tab").slideToggle();
        });


    $("#profile-divider").click(
        function() {
            $("#profile-tab").slideToggle();
            $("#timeline-tab").slideToggle();
            loadTimeline();
            setTimeout(function() {
                console.log($('.circle-node').length);
                placePopovers();
                nodeListeners();
            }, 800);
        });
} 




function hideAllAlerts()
{
    $(".alert").hide();
}

function makeAllyFormListener() {
    csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    var ally_url = "ally";
    $('#make-ally-form').ajaxForm(
    {
        beforeSubmit: function()
        {
            hideAllAlerts();
        },
        uploadProgress: function()
        {
            // in the case of progress
        },
        success: function(response) 
        {
            handleMakeAllyResponse(response);
        },
        data: {submit: true, csrfmiddlewaretoken: csrf_token}
    });
}

function removeAllyFormListener() {
	var de_ally_url = "de-ally";
    $('#remove-ally-form').ajaxForm(
    {
        beforeSubmit: function()
        {
            hideAllAlerts();
        },
        uploadProgress: function()
        {
            // in the case of progress
        },
        success: function(response) 
        {
            handleRemoveAllyResponse(response);
        },
        data: {submit: true}
    });
}

function handleMakeAllyResponse(response) 
{
    if (response === "success") {
        displayMessage("make-ally-success");
    }

    if (response === "already-allies") {
        displayMessage("make-ally-error");
    }
}

function handleRemoveAllyResponse(response) 
{
    if (response === "success") {
        displayMessage("remove-ally-success");
    }

    if (response === "already-not-allies") {
        displayMessage("remove-ally-error");
    }
}

function displayMessage(responseText) 
{
    if (responseText === "make-ally-success")
    {
        $("#make-ally-success-alert").slideToggle();
        $('#make-ally-button').hide();
        $('#remove-ally-button').fadeIn();
        $('#profile-divider').fadeIn();
    }

    if (responseText === "remove-ally-success")
    {
        $("#remove-ally-success-alert").slideToggle();
        $('#remove-ally-button').hide();
        $('#make-ally-button').fadeIn();
        $('#profile-divider').fadeOut();
    }
}
