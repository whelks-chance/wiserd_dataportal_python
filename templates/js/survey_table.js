/**
 * Created by ubuntu on 29/05/15.
 */


function question_pane(id){

    var new_survey = $.parseHTML("{% include 'survey_dialog.html' %}");
    new_survey.dialog({
        modal: false,
        autoOpen: false,
        height: window.innerHeight * 0.8,
        width: window.innerWidth * 0.8,
        buttons: {
            Close: function() {
                new_survey.dialog( "close" );
            }
        },
        close: function() {}
    }).dialogExtend(
        {
            "closable" : true,
            "maximizable" : true,
            "minimizable" : true,
            "minimizeLocation" : 'left',
            "collapsable" : true,
            "dblclick" : 'minimize',
            "titlebar" : false
        }
    );

}