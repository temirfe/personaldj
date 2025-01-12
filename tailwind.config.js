/** @type {import('tailwindcss').Config} */
const colors = require('tailwindcss/colors')
module.exports = {
    content: [
        './templates/**/*.html',
        './templates/*.html',
        './static/**/*.js',
    ],
    theme: {
        extend: {},
        colors: {
            transparent: 'transparent',
            current: 'currentColor',
            black: colors.black,
            white: colors.white,
            emerald: colors.emerald,
            indigo: colors.indigo,
            yellow: colors.yellow,
            stone: colors.stone,
            sky: colors.sky,
            neutral: colors.neutral,
            gray: colors.gray,
            slate: colors.slate,
        }
    },
    plugins: [],
}