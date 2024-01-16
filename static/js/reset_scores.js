$(document).ready(function() {
    $("#reset-btn").click(function() {
        // Reset the score on the front end
        $("td").html(0);
        // Reset the score on the back end
        $.ajax({
            type: "POST",
            url: "/reset-scores",  
            data: { 
                score: 0
            },
            success: function(response) {
                // Handle the response from the server if needed
                alert("The scores have been reset successfully!");
                window.location = "/" //redirect
            },
            error: function(error) {
                // Handle the error if the request fails
                alert("Error submitting count: " + error.statusText);
            }
        });
    })
})