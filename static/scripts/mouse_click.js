const mouseClickAudio = new Audio("/audio/mouse_click.mp3");

window.addEventListener("click", (event) => {
    const target = event.target;

    const shouldClick = event.isPrimary && (
        target.closest("a") || 
        target.tagName == "BUTTON" || 
        target.hasAttribute("data-click")
    );

    if (shouldClick) {
        console.debug("Playing mouse click sound (target: " + target + ")...")

        mouseClickAudio.pause();
        mouseClickAudio.currentTime = 0;

        mouseClickAudio.play();
    }
});