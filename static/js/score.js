$(document).ready(function() {
    // Initialize score count to zero
    let scoreCount = 0;

    // Get the title of the document
    let pageTitle = document.title;

    // Initialize variable for time remaining
    let timeRemaining;

    // Set timeRemaining based on the page title
    if (pageTitle.includes("Easy")) {
        // 3 minutes for Easy level
        timeRemaining = 1.5 * 60;
    } else if (pageTitle.includes("Intermediate")) {
        // 5 minutes for Intermediate level
        timeRemaining = 5 * 60;
    } else {
        // 7 minutes for any other level
        timeRemaining = 7 * 60;
    }

    // Function to update the timer display
    function updateTimerDisplay() {
        // Calculate minutes and seconds from timeRemaining
        const minutes = Math.floor(timeRemaining / 60);
        const seconds = timeRemaining % 60;

        // Format the timer display as 'mm:ss'
        const timerDisplay = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;

        // Update the timer display on the page
        $('#timer').text(`Time Remaining: ${timerDisplay}`);

        // Change timer text color to red when time is 1 minute or less
        if (timeRemaining <= 60) {
            $('#timer').css('color', 'red');
        }
    }

    // Function to start the countdown timer
    function startTimer() {
        // Set up an interval to decrement timeRemaining and update display every second
        const timerInterval = setInterval(function timer() {
            if (timeRemaining < 1) {
                // If time is up, clear the interval and submit scores
                clearInterval(timerInterval);
                submitScores();
            } else {
                // Decrement timeRemaining and update the timer display
                timeRemaining--;
                updateTimerDisplay();
            }
        }, 1000); // Interval set to 1000 milliseconds (1 second)
    }

    // Start the countdown timer when the page loads
    startTimer();

    // Function to handle correct button clicked
    $("input").on("click", function() {
        if ($(this).attr("id") === "correct") {
            scoreCount++;
        }
    });

    // Function to submit scores
    function submitScores(){
        // Send the scoreCount to the Flask backend
        $.ajax({
            type: "POST",
            url: "/submit-scores", 
            data: { 
                score: scoreCount,
                title: pageTitle 
            },
            success: function(response) {
                // Handle the response from the server if needed
                alert("Scores have been submitted successfully!");
                window.location = "/scores" //redirect
            },
            error: function(error) {
                // Handle the error if the request fails
                alert("Error submitting scores: " + error.statusText);
            }
        });
    }

    // Submit the scores when "Submit" button is clicked
    $("#submit-btn").click(function() {
        submitScores();
    });
});