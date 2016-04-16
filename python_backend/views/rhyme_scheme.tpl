<html>
<head>
<title>Analyze a poem's rhyme scheme</title>
<link rel="stylesheet" type="text/css" href="css/main.css">
<script src="js/jquery-1.9.0.js"></script>

</head>

<body>

<script>
$(document).ready(function() {

    function makePoemLineItem(line_obj) {
        return '' +
        '<li class="poem_line">' +
        line_obj.line_text +
        '<div class="scheme_letter">' + line_obj.scheme_letter + '</div>' +
        '</li>';
    }



    function processRhymeScheme(poem_text) {
        var postData = {"poem_text": poem_text};
        var requestURL = '/api/rhymescheme';
        $.ajax( {
            type: 'POST',
            url: requestURL,
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(postData),
            dataType: 'json',
            success: function(result) {
                $poemLinesList.html('');
                result.annotations.forEach(function(r) {
                    $poemLinesList.append(makePoemLineItem(r));
                });
            }
        });
    }

    var $poemTextBox = $('#poem_text_box');
    var $schemeResultsDiv = $('#scheme_results');
    var $poemLinesList = $('#lines_list');
    var $searchButton = $('#search');


    $("#submit_poem").click(function() {
        $("#lines_list").html('Processing...');
        processRhymeScheme($poemTextBox.val());
    });
});
</script>


<label for="text_of_poem">Enter poem text here:</label>
<br>
<textarea type="paragraph_text" cols="50" rows="10" id="poem_text_box" name="poem_text" required="required"></textarea>
<br>
<input type="button" value="Check rhyme scheme" id="submit_poem" />

<div class="list_container" id="scheme_results">
    <h1>Rhyme Scheme Annotations:</h1>
<div class="item_list" id="lines_list">
    <li>No poem entered yet.</li>
</div>
</div>

</body>
</html>
