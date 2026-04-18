const musicPlayerDiv = document.getElementById("music-player-div");
const musicPlayerButton = document.getElementById("music-player-play-button");
const musicPlayerDisplayText = document.getElementById("music-player-display-text"); 

var player;

function onYouTubeIframeAPIReady() {
    player = new YT.Player("yt-music-embed", {
        height: "0",
        width: "0",
        videoId: "vUU-Yl2Dprk",
        host: "https://www.youtube-nocookie.com",
        playerVars: {
            "playsinline": 1,
            "origin": window.location.origin,
        },
        events: {
            "onReady": onPlayerReady,
        }
    });
}

function onPlayerReady(_event) {
    player.setVolume(30);

    musicPlayerDisplayText.innerText = "Press play again to play music.";

    ytEmbedLoaded = true;
}

var ytEmbedLoaded = false;

musicPlayerButton.addEventListener("click", (event) => {
    if (ytEmbedLoaded) {
        return;
    }

    const asyncScriptTag = document.createElement("script");
    asyncScriptTag.src = "https://www.youtube.com/iframe_api";

    const scriptTag = document.getElementById("yt-music-script");
    scriptTag.parentNode.insertBefore(asyncScriptTag, scriptTag);

    console.debug("Loading youtube embed for playing music...");
    musicPlayerDisplayText.innerText = "Loading YouTube embed...";
});

var musicPlaying = false;

musicPlayerButton.addEventListener("click", (event) => {
    if (!ytEmbedLoaded) {
        return;
    }

    console.debug("Playing music with youtube embed API...");

    const videoData = player.getVideoData();

    musicPlayerDisplayText.innerText = (!musicPlaying) ? "▶︎ PLAYING - " + videoData.title : "◼ STOPPED";

    (!musicPlaying) ? player.playVideo() : player.stopVideo();

    musicPlayerButton.innerText = (!musicPlaying) ? "◼" : "▶︎";

    musicPlaying = !musicPlaying;
});