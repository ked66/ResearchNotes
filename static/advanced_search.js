$(document).ready(function(){
    var project_name = '';
    var project_id = '';

    $('#project').on('change', function() {
        event.preventDefault();
        $('#subtopic').empty();

        project_name = $("#project option:selected").text();
        project_id = $("#project option:selected").val();

        $.getJSON('/_parse_data', {
            a: project_name,
            b: project_id
        }, function(data) {
            var options = $("#subtopic");
                $.each(data, function() {
                    options.append($("<option />".val($(this)[0]).text($(this)[1])))
                    // options.append($("<li><input id='subtopic'-" + $(this)[2] + "' name = 'subtopic' type='checkbox' value=" + $(this)[0] + "><label for='subtopic-" + $(this)[2] + "'>" + $(this)[1] + "</label></li>"

            });
        });
    return false;
    });
});

