$(document).ready(function(){
    var project_name = '';
    var project_id = '';

    $('#project').on('change', function() {
        event.preventDefault();
        $('#subtopic').empty();
        project_id = "";

        project_name = $("#project input[name='project']:checked").text();
        $("#project input[name='project']:checked").each(function(){
            project_id = project_id + $(this).val() + ",";
        });

        $.getJSON('/_parse_data', {
            a: project_name,
            b: project_id
        }, function(data) {
            var options = $("#subtopic");
                $.each(data, function() {
                    options.append($("<li><input id='subtopic-" + $(this)[2] + "' name = 'subtopic' type='checkbox' value=" + $(this)[0] + "><label for='subtopic-" + $(this)[2] + "'>" + $(this)[1] + "</label></li>"))

            });
        });
    return false;
    });
});

