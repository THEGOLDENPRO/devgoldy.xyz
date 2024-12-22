/*
I don't use the typescript script any more, as of v1.3.8 I dropped nodejs as a dependency,
*/

type AnimationElements = ([HTMLElement | null, number])[];

const links = document.getElementById("links");
const image = document.getElementById("image");
const its_goldy_text = document.getElementById("its_goldy_text");
const quick_about_text = document.getElementById("quick_about_text");
const toggle_effects_button = document.getElementById("toggle-effects-button");
const static_bg_div = document.getElementById("static-bg-div");
const about_me_div = document.getElementById("about-me-div");

const blogs_slideshow = document.getElementById("blogs-slideshow");

var blogs_slideshow_id: number;

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
    blogs_slideshow_id = startSlideshowLoopThingy(blogs_slideshow, 1);
}

toggle_effects_button?.addEventListener("mousedown", (e) => {
    static_bg_div?.classList.toggle("hidden");
    about_me_div?.classList.toggle("animated-crt-lines");
});

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
    const slideshow_titles = slideshow.getElementsByTagName("h3");

    // hide the last slideshow image and darken it's button.
    for (let image of slideshow_images) {
        if (!image.classList.contains("hidden")) {
            image.classList.add("hidden");
        }
    }

    for (let button of slideshow_buttons) {
        if (button.classList.contains("!bg-goldyCream-200")) {
            button.classList.remove("!bg-goldyCream-200");
        }
    }

    for (let title of slideshow_titles) {
        if (!title.classList.contains("hidden")) {
            title.classList.add("hidden");
        }
    }

    // show the current slideshow image and brighten it's button.
    slideshow_images[index].classList.remove("hidden");
    slideshow_buttons[index].classList.add("!bg-goldyCream-200");
    slideshow_titles[index].classList.remove("hidden");

    // show title on hover.
    let hover_callback = (e: MouseEvent) => {
        if (e.type == "mouseover") {
            slideshow_images[index].classList.add("blur-sm");
            //slideshow_images[index].classList.add("saturate-50");
            slideshow_images[index].classList.add("brightness-50");
            slideshow_images[index].classList.add("sepia");

            slideshow_titles[index].classList.add("opacity-100");
        } else {
            slideshow_images[index].classList.remove("blur-sm");
            //slideshow_images[index].classList.remove("saturate-50");
            slideshow_images[index].classList.remove("brightness-50");
            slideshow_images[index].classList.remove("sepia");

            slideshow_titles[index].classList.remove("opacity-100");
        }
    };

    slideshow_titles[index].addEventListener("mouseover", hover_callback);
    slideshow_images[index].addEventListener("mouseover", hover_callback);

    slideshow_titles[index].addEventListener("mouseleave", hover_callback);
    slideshow_images[index].addEventListener("mouseleave", hover_callback);
}

function startSlideshowLoopThingy(slideshow: HTMLElement, start_from: number = 0) {
    console.log(`Slideshow with id '${slideshow.id}' is being started...`);

    const slideshow_images = slideshow.getElementsByTagName("img");

    let index: number = start_from;
    const max_index: number = slideshow_images.length - 1;

    return setInterval(
        () => {
            if (index > max_index) {
                index = 0;
            }

            toggleSlideshowImage(slideshow, index);

            index += 1;
        }, 6000
    );
}

function stopSlideshowLoopThingy(id: number) {
    console.log(`Slideshow with id '${id}' is being stopped...`);
    clearInterval(id);
}