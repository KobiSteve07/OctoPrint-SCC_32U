$(function() {
    function moveArm(angle) {
        $.ajax({
            url: API_BASEURL + "plugin/SCC_32U",
            type: "POST",
            dataType: "json",
            data: JSON.stringify({
                command: "move",
                angle: angle
            }),
            contentType: "application/json; charset=UTF-8"
        }).done(function(response) {
            console.log("Move command sent successfully:", response);
        }).fail(function(jqXHR, textStatus, errorThrown) {
            console.error("Failed to send move command:", textStatus, errorThrown);
        });
    }

    // Example button click event to move the arm to 90 degrees
    $("#move-arm-button").click(function() {
        var angle = $("#angle-input").val();
        moveArm(angle);
    });
});
