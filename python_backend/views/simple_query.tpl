<html>
<head>
<title>Make a query</title>
<link rel="stylesheet" type="text/css" href="css/main.css">
<script src="js/jquery-1.9.0.js"></script>

</head>

<body>

<script>
$(document).ready(function() {
    function makeResultItem(result) {
        itemCode = '' +
        '<li>' +
        result.transcription + '<br>' + 
        result.stress + '<br>' + 
        '</li>';
        return itemCode;
    }


    function processSearch(term) {
        var requestURL = '/api/spelling/' + term;
        $.ajax( {
            type: 'GET',
            url: requestURL,
            success: function(result) {
                $resultsBox.html('');
                result.results.forEach(function(r) {
                    $resultsBox.append(makeResultItem(r));
                });
            }
        });
    }

    var $searchBox = $('#search_term');
    var $resultsBox = $('#results_list');
    var $searchButton = $('#search');

    // hitting enter in search box calls a click on search button
    $searchBox.keypress(function (e) {
        var key = e.which;
        if (key == 13) {
            $searchButton.click();
        }
    });

    $("#search").click(function() {
        processSearch($searchBox.val());
    });
});
</script>


<label for="search_term">Search term:</label>
<input type="text" id="search_term" name="search_term" required="required" />
<input type="button" value="Search" id="search" />

<div class="list_container" id="search_results">
    <h1>Search results:</h1>
<div class="item_list" id="results_list">
    <li>No search preformed yet.</li>
</div>
</div>

</body>
</html>
