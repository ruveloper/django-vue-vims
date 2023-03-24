/* eslint-disable no-undef */
/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './index.html',
    './src/**/*.{vue,js,ts}',
  ],
  safelist: [
    'hidden', 'h-screen', 'h-96'
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require("daisyui"),
  ],
}
