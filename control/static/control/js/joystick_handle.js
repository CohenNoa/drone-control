$(document).ready(function () {
    var joystickView = new JoystickView(150, function (callbackView) {
        $("#joystickContent").append(callbackView.render().el);
        setTimeout(function () {
            callbackView.renderSprite();
        }, 0);
    });
    joystickView.bind("verticalMove", function (y) {
        $("#yVal").html(y);
    });
    joystickView.bind("horizontalMove", function (x) {
        $("#xVal").html(x);
    });
});