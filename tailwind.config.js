/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./src/**/*.{html,js}"],
    theme: {
        extend: {},
    },
    plugins: [],
    theme: {
        extend: {
            colors: {
                goldyBluey: "#222930",
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

        fontFamily: {
            "YanoneKaffeesatz": ["YanoneKaffeesatz"]
        }
    }
}