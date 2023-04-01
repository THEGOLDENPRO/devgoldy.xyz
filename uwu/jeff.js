var body = document.getElementsByTagName("body")[0];
var img = document.getElementsByTagName("img")[0];
var button = document.getElementsByTagName("button")[0];
var audio = new Audio("jeff.mp3");

var elem = document.documentElement;

body.addEventListener("click", function (e) {
    button.classList.add("hidden");
    button.classList.remove("button");

    audio.play();
    img.classList.remove("hidden");

    if (elem.requestFullscreen) {
        elem.requestFullscreen();
    } else if (elem.webkitRequestFullscreen) { /* Safari */
        elem.webkitRequestFullscreen();
    } else if (elem.msRequestFullscreen) { /* IE11 */
        elem.msRequestFullscreen();
    }
})
