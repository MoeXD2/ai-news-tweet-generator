$(document).ready(function () {
    const toast = new bootstrap.Toast(document.getElementById("toast"));
 
    function showToast(message) {
       $("#toast .toast-body").text(message);
       toast.show();
    }
 
    $(".splash-screen").fadeOut(1000);

    function addTooltip(element) {
        new bootstrap.Tooltip(element, {
            placement: "top",
            title: "Click to see the full article",
        });
    }

    function setLoadingMessage(message) {
        $("#loading-message").text(message);
    }
 
    $("#generate-tweet-btn").on("click", function () {
        setLoadingMessage("Fetching headlines and generating a tweet...");
        $(".splash-screen").fadeIn(500);
 
        $.post("/generate_tweet", function (data) {
            $(".splash-screen").fadeOut(500);
            $("#news-list").empty();
            $("#tweet-preview").text(data.tweet);
 
            data.news.forEach(function (article) {
                let newsItem = $("<a></a>")
                    .attr("href", article.url)
                    .attr("target", "_blank")
                    .attr("data-bs-toggle", "tooltip")
                    .addClass(
                        "list-group-item list-group-item-action animate__animated animate__fadeIn"
                    )
                    .text(article.name);
                $("#news-list").append(newsItem);
                addTooltip(newsItem[0]);
            });
 
            // Animate the tweet preview
            $("#tweet-preview")
                .removeClass("animate__fadeIn")
                .addClass("animate__animated animate__fadeIn");
        });
    });
 
    $("#post-tweet-btn").on("click", function () {
     let tweetContent = $("#tweet-preview").text();
     if (tweetContent) {
        setLoadingMessage("Posting the tweet...");
        $(".splash-screen").fadeIn(500);
        $.post("/post_tweet", { tweet: tweetContent }, function (data) {
            $(".splash-screen").fadeOut(500);
            if (data.status === "success") {
                showToast("Tweet posted successfully!");
            } else {
                showToast("Failed to post the tweet.");
            }
        });
    } else {
        showToast("Please generate a tweet before posting.");
    }
    });
}); 