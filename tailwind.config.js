/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./web/**/*.{html,js}", "./templates/**/*.{html,js}"],
    plugins: [],
    theme: {
        extend: {
            colors: {
                exeBlack: "#090b11",
                exeGray: "#9ca3af",
                goldyPink: "#fb89ab",
                goldyDarky: {
                    DEFAULT: "#0e1114",
                    200: "#0a0b0d",
                    300: "#0b0d0f",
                    500: "#0e1114"
                },
                goldyGreyy: "#222930",
                goldyCream: "#fbc689",
                goldyOrangy: {
                    DEFAULT: "#f5671b",
                    100: "#f5671b",
                    300: "#f57d3d",
                    800: "#f5be3d"
                },
                goldyGreen: "#d0f54c"
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
            "YanoneKaffeesatz": ["YanoneKaffeesatz"],
            "hacked": ["Hacked-KerX"],
            "typewriter": ["atwriter"],
            "dosis": ["Dosis"]
        },
        animation: {
            "flicker": "flicker 0.00001s infinite ease-in",
        },
        keyframes: {
            flicker: {
                "from" : {
                    textShadow: "1px 0 0 theme(colors.goldyPink), -2px 0 0 theme(colors.goldyOrangy.300);",
                },
                "to" : {
                    textShadow: "3.6px 0.5px 2px theme(colors.goldyPink), -1px -0.5px 2px theme(colors.goldyOrangy.300);",
                },
            }
        }
    }
}