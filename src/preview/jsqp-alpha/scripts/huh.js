var huh_text = document.getElementById("huh_text")
var huh_audio = new Audio('./cdn/audio/huh.mp3');

huh_text.addEventListener("click", function(event) {
    huh_audio.play();
})