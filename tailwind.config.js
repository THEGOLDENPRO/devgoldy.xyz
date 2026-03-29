/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./static/**/*.{html,js}", "./templates/**/*.{html,js}", "./markdown/**/*.md"],
    plugins: [],
    theme: {
        extend: {
            animation: {
                "flicker": "flicker 0.00001s infinite ease-in",
                "fade-in": "fadeIn ease 5s",
                "fade-in-faster": "fadeIn ease 3s"
            },
            keyframes: {
                flicker: {
                    "from" : {
                        textShadow: "1px 0 0 theme(colors.goldyPink), -2px 0 0 theme(colors.goldyOrangy.300);",
                    },
                    "to" : {
                        textShadow: "3.6px 0.5px 2px theme(colors.goldyPink), -1px -0.5px 2px theme(colors.goldyOrangy.300);",
                    },
                },
                fadeIn: {
                    "from": {
                        opacity: "0",
                    },
                    "to": {
                        opacity: "1",
                    }
                }
            }
        },
        screens: {
            "mobile": {"max": "430px"},
            "tablet": {"max": "850px"},
            "small-screen": {
                "min": "430px",
                "max": "1300px"
            },
            "desktop": {"max": "1280px"}
        },
        fontFamily: {
            "yanone-kaffeesatz": ["YanoneKaffeesatz"],
            "hacked": ["Hacked-KerX"],
            "typewriter": ["atwriter"],
            "dosis": ["Dosis"]
        }
    }
}