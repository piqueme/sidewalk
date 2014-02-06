var current_pagenum = 1;
var allied_pagenum = 1;
var current_pages_get_url = "current";
var allied_pages_get_url = "allied";
var completion_form_url = "completion-form";

var current_quest_page_pull_count = 10;
var allied_quest_page_pull_count = 10;

var forfeit_url = "forfeit";
var quest_id = "";
var user_posted_name = "";
var tr = $();
var data_completion = "";

$(document).ready(function()
{
    $.ajaxSetup ({
        cache: false
    });
    hideAllAlerts();
    initializeDashButtons();
    callNextCurrentQuestPage(current_quest_page_pull_count);
    callNextAllyQuestPage(allied_quest_page_pull_count);
    forfeitFormListener();
    createCompletionModalListener();
});

function hideAllAlerts() {
    $(".alert").hide();
}

function initializeDashButtons()
{
    $('#start-button').onclick = function()
    {
        location.href = "../search";
    }
    $('#post-button').onclick = function()
    {
        location.href = "../post";
    }
    $('#manage-button').onclick = function()
    {
        location.href = "../view";
    }
    $('#help-button').onclick = function()
    {
        location.href = "../help";
    }
}

function callNextCurrentQuestPage( numUpdate )
{
    $("#next-current").click(function(event)
    {
        event.preventDefault();
        pagestring = ("page=" + current_pagenum);
        pagestring += ("&count=" + current_quest_page_pull_count);
        $.get(current_pages_get_url, pagestring, function(data)
        {
            /*($("#current-table tbody")).append(data);*/
            if (data.trim() === "")
            {
                
            }
            $("body").append(data);
            /*$("#removable").appendTo($("#current-table tbody")).slideDown('slow');*/
            $("#removable").insertBefore($("#current-more")).slideDown('slow');
            $("#removable").removeAttr('id');
            if (data.trim() === "")
            {
                $("#next-current").hide();    
            }

            current_pagenum += 1;
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
    }); 
}

function callNextAllyQuestPage( numUpdate )
{
    $("#next-allied").click(function(event)
    {
        event.preventDefault();
        pagestring = ("page=" + allied_pagenum);
        pagestring += ("&count=" + allied_quest_page_pull_count);
        $.get(allied_pages_get_url, pagestring, function(data)
        {
            $("body").append(data);
            /*$("#removable").appendTo($("#current-table tbody")).slideDown('slow');*/
            $("#removable").insertBefore($("#allied-more")).slideDown('slow');
            $("#removable").removeAttr('id');
            if (data.trim() === "")
            {
                $("#next-allied").hide();
            }

            allied_pagenum += 1;
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
    }); 
}

function createCompletionModalListener() {
    $('.completed-button-form').submit(function(event)
    {
        // first get rid of any completion form in the dialog from before
        $("#completion-form").remove();

        event.preventDefault();
        quest_info_str = event.target.id;
        quest_info = quest_info_str.split("-");
        quest_id = quest_info[2];
        user_posted_name = quest_info[3];
        csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        tr = $(this).closest('tr');
        csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        $.ajax({
            url: completion_form_url,
            type: "GET",
            data:"quest_id=" + quest_id + "&user_posted_name=" + user_posted_name + "&csrfmiddlewaretoken=" + csrf_token,
            success: function(data) {
                $(".modal-content").append(data);
                createCompletionFormListener();
                $('#quest-complete-dialog').modal();
            }
        });
        /*$.get("completion-form", quest_info, function(data)
        {
            $("#completion-form").load(data);
            $('#quest-complete-dialog').modal();
            createCompletionFormListener();
        }, "html");*/
    });
}

function createCompletionFormListener() {
    /*var completion_url = "complete";
    var options = {
        dataType: 'html',
        url: completion_url,
        beforeSubmit: showRequest,
        success: showResponse 
    }*/

    $('#completion-form').ajaxForm(
    {
        beforeSubmit: function()
        {
            hideAllAlerts();
        },
        uploadProgress: function()
        {
            // draw loading circle
        },
        success: function(response)
        {
            $("#completion-form").remove();
            showResponse(response);
        },
        error: function()
        {
            // handleCompletionError();
        }
    });
    //$('#completion-form').ajaxSubmit(options);
    /*$('#completion-form').ajaxForm( 
    {
        beforeSubmit: function()
        {
            removeAllAlerts();
        },
        uploadProgress: function(event, position, total, percentComplete)
        {
            // draw loading circle
        },
        success: function(response)
        {
            showResponse(response);
        },
        error: function()
        {
            handleCompletionError();
<<<<<<< Updated upstream
        }
    });*/
}

function forfeitFormListener() {
    $('.forfeit-button-form').submit(function()
    {
        event.preventDefault();
        quest_info_str = event.target.id;
        quest_info = quest_info_str.split("-");
        quest_id = quest_info[2];
        user_posted_name = quest_info[3];
        csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        tr = $(this).closest('tr');
        $.ajax({
            type:"POST",
            url:"forfeit",
            data:"quest_id=" + quest_id + "&user_posted_name=" + user_posted_name + "&csrfmiddlewaretoken=" + csrf_token,
            success: function(response) {
                handleForfeitResponse(response);
            }
        });    
    });
}

function handleForfeitResponse(response) 
{
    if (response === "success") {
        displayMessage("forfeit-success");
    }

    if (response === "already-forfeited") {
        displayMessage("forfeit-error");
    }

}

function displayMessage(responseText) 
{
    if (responseText === "forfeit-success")
    {
        tr.css("background-color","#FF3700");
        tr.fadeOut(400, function(){
            tr.remove();
        });
        $("#forfeit-success-alert").show();
    }
    else if (responseText === "forfeit-error") {
        $("#forfeit-error-alert").show();

    }
}

function showResponse(response) {
    if (response === "success")
    {
        $("#quest-complete-dialog").modal('hide');
        tr.css("background-color","#FF3700");
        tr.fadeOut(400, function(){
            tr.remove();
        });
        //$("html, body").animate({ scrollTop: 0 }, "slow");
        $("#buttons-box").append("<div class='alert alert-success'> <strong> Hooray </strong> You completed the quest! </div>");

    }
    else
    {
        $("#buttons-box").append(response);
    }
}
