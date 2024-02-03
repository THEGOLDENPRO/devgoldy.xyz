type AnimationElements = ([HTMLElement | null, number])[];

const links = document.getElementById("links");
const image = document.getElementById("image");
const its_goldy_text = document.getElementById("its_goldy_text");
const quick_about_text = document.getElementById("quick_about_text");

const blogs_slideshow = document.getElementById("blogs-slideshow");

function doAnimationThingy(elements: AnimationElements) {

    for (let [element, timeout] of elements) {

        if (element !== null) {

            setTimeout(
                () => {
                    element.classList.remove("opacity-0");
                    element.classList.add("animate-fade-in");
                }, timeout
            );

        }

    }

}

function toggleSlideshowImage(slideshow: HTMLElement, index: number) {
    const slideshow_images = slideshow.getElementsByTagName("img");
    const slideshow_buttons = slideshow.getElementsByTagName("button");

    // hide the last slideshow image and darken it's button.
    for (let image of slideshow_images) {
        if (!image.classList.contains("hidden")) {
            image.classList.add("hidden");
        }
    }

    for (let button of slideshow_buttons) {
        if (button.classList.contains("!bg-white")) {
            button.classList.remove("!bg-white");
        }
    }

    // show the current slideshow image and brighten it's button.
    slideshow_images[index].classList.remove("hidden");
    slideshow_buttons[index].classList.add("!bg-white");
}

function startSlideshowLoopThingy(slideshow: HTMLElement) {
    const slideshow_images = slideshow.getElementsByTagName("img");

    let index: number = 0;
    const max_index: number = slideshow_images.length - 1;

    setInterval(
        () => {
            if (index > max_index) {
                index = 0;
            }

            toggleSlideshowImage(slideshow, index);

            index += 1;
        }, 6000
    );
}


const elements_to_do: AnimationElements = [
    [its_goldy_text, 250],
    [quick_about_text, 2000],
    [links, 1000],
    [image, 1400]
];

// The goofy fading in animation thingy.
doAnimationThingy(elements_to_do);

// Slideshow stuff.
if (blogs_slideshow !== null) {
    toggleSlideshowImage(blogs_slideshow, 0);
    startSlideshowLoopThingy(blogs_slideshow);
}