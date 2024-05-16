$(function() {
    function sendMoveCommand(servo_id, angle) {
        $.ajax({
            url: API_BASEURL + "api/plugin/SCC_32U",
            type: "POST",
            dataType: "json",
            data: JSON.stringify({
                command: "move",
                servo_id: servo_id,
                angle: angle
            }),
            contentType: "application/json; charset=UTF-8"
        }).done(function(response) {
            console.log("Move command sent successfully", response);
        }).fail(function() {
            console.error("Failed to send move command");
        });
    }

    $("#move_arm_button").click(function() {
        var servo_id = $("#servo_id_input").val();
        var angle = $("#move_arm_input").val();
        sendMoveCommand(servo_id, angle);
    });

    // ViewModel for the settings
    function Scc32uViewModel(parameters) {
        var self = this;
        self.settings = parameters[0];
    }

    OCTOPRINT_VIEWMODELS.push({
        construct: Scc32uViewModel,
        dependencies: ["settingsViewModel"],
        elements: ["#tab_scc_32u"]
    });
});
