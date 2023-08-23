var slideIndex = 1;
showDivs(slideIndex);

function plusDivs(n) {
    showDivs(slideIndex += n);
}

function showDivs(n) {
    var i;
    var x = document.getElementsByClassName("slideshow_image");
    if (n > x.length) {slideIndex = 1};

    if (n < 1) {slideIndex = x.length};

    for (i = 0; i < x.length; i++) {
        var element = x[i];
        x[i].style.display = "none";
    }
    x[slideIndex-1].style.display = "block";
}

setInterval(function() {
    plusDivs(+1);
}, 3000);