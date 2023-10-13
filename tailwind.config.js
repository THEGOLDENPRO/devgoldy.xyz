/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./src/**/*.{html,js}", "./templates/**/*.{html,js}"],
    plugins: [],
    theme: {
        extend: {
            colors: {
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
            "YanoneKaffeesatz": ["YanoneKaffeesatz"]
        }
    }
}