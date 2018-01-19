console.log("touchscreen is", VirtualJoystick.touchScreenAvailable() ? "available" : "not available");
var joystick = new VirtualJoystick({
    container: document.getElementById("left"),
    strokeStyle: 'red',
    mouseSupport: true,
    stationaryBase: true,
    baseX: 1000,
    baseY: 150,
    limitStickTravel: true,
    stickRadius: 50
});

joystick.addEventListener('touchStartValidation', function (event) {
    var touch = event.changedTouches[0];
    return touch.pageX >= window.innerWidth / 2;

});


var joystick1 = new VirtualJoystick({
    container: document.getElementById("right"),
    strokeStyle: 'green',
    mouseSupport: true,
    stationaryBase: true,
    baseX: 150,
    baseY: 150,
    limitStickTravel: true,
    stickRadius: 50
});

joystick1.addEventListener('touchStartValidation', function (event) {
    var touch = event.changedTouches[1];
    return touch.pageX >= window.innerWidth / 4;

});
// setInterval(function () {
//     var outputEl = document.getElementById('result');
//     outputEl.innerHTML = '<b>'
//         + ' dx:' + joystick.deltaX()
//         + ' dy:' + joystick.deltaY()
//         + (joystick.right() ? ' right' : '')
//         + (joystick.up() ? ' up' : '')
//         + (joystick.left() ? ' left' : '')
//         + (joystick.down() ? ' down' : '') + '</b>'
// }, 1 / 30 * 1000);



