type AnimationElements = ([HTMLElement | null, number])[];

function do_animation_thingy(elements: AnimationElements) {

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

const its_goldy_text = document.getElementById("its_goldy_text");
const quick_about_text = document.getElementById("quick_about_text");
const links = document.getElementById("links");
const image = document.getElementById("image");

const elements_to_do: AnimationElements = [
    [its_goldy_text, 250],
    [quick_about_text, 2000],
    [links, 1000],
    [image, 1400]
];

do_animation_thingy(elements_to_do);