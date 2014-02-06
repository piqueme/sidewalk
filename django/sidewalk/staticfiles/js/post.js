var counter = 2; 
var skill_points = 5;

function hideAllAlerts()
{
    $(".alert").hide();
}

function removeAllAlerts()
{
    $(".alert").remove();
}

function addChallengeFields(count)
{
    if (count < 11)
    {
        $("#challenges-container").append( "<div class='row challenge-row' id='challenge-row-" + count + "'>" +  
                "<div class='col-md-1'>" +
                    "<p class='challenge-id-text' id='challenge-id-" + count + "'>" + count + ":</p>" +
                "</div>" +
                "<div class='col-md-5'>" + 
                    "<input type='text' class='form-control challenge-desc' maxlength='60' name='challenge-" + count + "' id='challenge-" + count + "' placeholder='Description'> </input>" +
                "</div>" +
                "<div class='col-md-5'>" +
                    "<input type='text' class='form-control location-desc' maxlength='60' name='location-" + count + "' id='location-" + count + "' placeholder='Location'> </input>" +
                "</div>" +
                "<div class='col-xs-1' id='button-col-" + count + "'>" + 
                    "<button type='button' class='close' id='chal-close-" + count + "'> &times; </button>" +
                "</div>" + 
            "</div>"
        );

        skill_points += 5;
        $("#skill-point-counter").text(skill_points + " points to distribute"); 
        addRemoveChallengeListener(count);

        var new_loc_input = document.getElementById('location-' + count); 
        var options = {
            componentRestrictions: {country: 'us'}
        };
        newautocomplete = new google.maps.places.Autocomplete(new_loc_input, options); 
        $('input,select').keypress(function(event) {return event.keyCode != 13; });
    }
    if (count == 10) 
    {
        $("#add-challenge-row").hide();
    }
}

function addRemoveChallengeListener(count)
{
    chal_close_id = "#chal-close-" + count;
    $(chal_close_id).click(function()
    {
        chal_row_id = "#challenge-row-" + count;
        $(chal_row_id).remove();
        for (var i = (count + 1); i < counter; i++)
        {
            decrementChallenge(i);
        } 
        for (var i = count; i < (counter - 1); i++)
        {
            addRemoveChallengeListener(i);
        }
        counter -= 1;
        skill_points -= 5;
        $("#skill-point-counter").text(skill_points + " points to distribute"); 
        if (counter == 10)
        {
           $("#add-challenge-row").fadeIn; 
        }
    });
}

function decrementChallenge(count)
{
    row_id = "#challenge-row-" + count;
    new_row_id = "challenge-row-" + (count - 1);
    label_id = "#challenge-id-" + count;
    new_label_id = "challenge-id-" + (count - 1);
    desc_id = "#challenge-" + count;
    new_desc_id = "challenge-" + (count - 1);
    loc_id = "#location-" + count;
    new_loc_id = "location-" + (count - 1);
    close_id = "#button-col-" + count;
    new_close_id = "chal-close-" + (count - 1);
    $(label_id).text((count - 1) + ":");
    $(desc_id).attr("name", "challenge-" + (count - 1));
    $(loc_id).attr("name", "location-" + (count - 1));
    $(row_id).attr("id", new_row_id);
    $(label_id).attr("id", new_label_id);
    $(desc_id).attr("id", new_desc_id);
    $(loc_id).attr("id", new_loc_id);
    $(close_id).remove();
    $(("#" + new_row_id)).append("<div class='col-xs-1' id='button-col-" + (count - 1) + "'>" + 
                            "<button type='button' class='close' id='chal-close-" + (count - 1) + "'> &times; </button>" +
                           "</div>"); 
}

jQuery.fn.exists = function() {return this.length > 0}

/*
function addTooltips()
{
    var tooltips = {
        "Quest name" : "Give your quest a name",
        "Quest icon" : "Upload an icon that describes your quest",
        "Description" : "Give your quest a tagline or short description",
        "Skill Rewards Distribution" : "What skills will your quest improve?",
        "WISDOM" : "Brainpower is magic.",
        "VITALITY" : "An apple a day keeps the doctor away.",
        "EATING" : "What greater joy is there than food?",
        "SPIRITUAL" : "It is important to replenish your mana.",
        "FANCY" : "My moustache curls in circles.",
        "THRIFTY" : "Coupons never really expire.",
        "NATURE" : "I hear the sounds of birds in early morning.",
        "WORLDLY" : "Fez on my head.",
        "HIPSTER" : "So you have no knowledge of this band?",
        "Add Challenges" : "What challenges does your quest entail? (Challenges are the individual tasks in your quest and have locations, such as 'Eat a cannoli' at 'Mike's Pastries')"
    };
    
    $('.place-tooltip').each(function(){
            var labels = $(this).find('.field-label');
            var text = tooltips[$(labels[0]).html()];
            console.log(text);

            $(this).tooltip({
                placement: "top",
                trigger: "click hover focus",
                title: text
            });
    });

    $('.place-tooltip-stats').each(function(){
        var labels = $(this).find('.skill-label');
        var text = tooltips[$(labels[0]).text()];
        console.log(text);

        $(this).tooltip({
            placement: "top",
            trigger: "click hover focus",
            title: text
        });
    });
}
*/

function addPostFormAjaxListener()
{
    $("#post-form").ajaxForm(
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
            handlePostCheckResponse(response); 
        },
        error: function()
        {
            handlePostError();
        }
    });
}

function handlePostCheckResponse(response)
{
    $("#post-button").before(response);
    if ($(".alert-success").exists())
    {
        $("#instructions-panel").before($(".alert-success"));
        $("html, body").animate({ scrollTop: 0 }, "slow");
        clearFormInputs();
    }
    $('.alert').fadeIn();
}

function clearFormInputs()
{
    $(":input", "#post-form")
    .not(":button, :submit, :reset, :hidden")
    .val('')
    .removeAttr('checked')
    .removeAttr('selected');
}

function handlePostError()
{
    $("#post-ajax-error").fadeIn();
}

$(document).ready(function()
{
    $.ajaxSetup ({
        cache: false
    });
    $('#add-challenge-button').on('click', function()
    {
        addChallengeFields(counter);
        counter += 1;
    });

    var new_loc_input = document.getElementById('location-1'); 
    var options = {
        componentRestrictions: {country: 'us'}
    };
    newautocomplete = new google.maps.places.Autocomplete(new_loc_input, options); 
     
    $('.dropdown-toggle').dropdown();
   
    //addTooltips();
    hideAllAlerts();   
    addPostFormAjaxListener(); 

    // stop enter key from submitting form
    $('input,select').keypress(function(event) {return event.keyCode != 13; });
});
