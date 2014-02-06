$(document).ready(function()
{
    setupSettingsFormAjaxListener();
    changeSettingsButtonListeners();
});

function setupSettingsFormAjaxListener()
{
    $("#settings-form").ajaxForm(
    {
        beforeSubmit: function()
        {
            removeAllAlerts();
        },
        uploadProgress: function(event, position, total, percentComplete)
        {

        },
        success: function(response)
        {
            clearFormInputs();
            $("#settings-verify-dialog").modal('hide');
            handleSettingsFormResponse(response);
        },
        error: function()
        {
            handleSettingsPostError(); 
        }
    });
}

function changeSettingsButtonListeners()
{
    $(".change-button").click(function() 
    {
        event.preventDefault();
        $("#settings-verify-dialog").modal();
    });
}

function hideAllAlerts()
{
    $(".alert").hide();
}

function removeAllAlerts()
{
    $(".alert").remove();
}

function clearFormInputs()
{
    $(":input", "#settings-form")
    .not(":button, :submit, :reset, :hidden")
    .val('')
    .removeAttr('checked')
    .removeAttr('selected');
}

function handleSettingsFormResponse(response)
{
    $("#panel").before(response);
    $("html, body").animate({ scrollTop: 0 }, "slow");
}

function handleSettingsPostError()
{

}
