const musicPlayerDiv = document.getElementById("music-player-div");
const musicPlayerButton = document.getElementById("music-player-play-button");
const musicPlayerDisplayText = document.getElementById("music-player-display-text"); 

const songIDs = [
    "vUU-Yl2Dprk", // LAMP - Kokoro no Madobe ni...
    "ELSAPf-z9VI", // LAMP - Futari no ita fukei
];

var player;

function onYouTubeIframeAPIReady() {
    const randomSongID = songIDs[Math.floor(Math.random() * songIDs.length)];

    console.debug("Picked song id '" + randomSongID + "' from list.");

    player = new YT.Player("yt-music-embed", {
        height: "0",
        width: "0",
        videoId: randomSongID,
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

var musicTitle = null;
var musicPlaying = false;

musicPlayerButton.addEventListener("click", (event) => {
    if (!ytEmbedLoaded) {
        return;
    }

    console.debug("Playing music with youtube embed API...");

    (!musicPlaying) ? player.playVideo() : player.stopVideo();

    if (musicTitle == null) {
        const videoData = player.getVideoData();

        musicTitle = videoData.title;
    }

    musicPlayerDisplayText.innerText = (!musicPlaying) ? "▶︎ PLAYING - " + musicTitle : "◼ STOPPED";

    musicPlayerButton.innerText = (!musicPlaying) ? "◼" : "▶︎";

    musicPlaying = !musicPlaying;
});