/** @type {import('tailwindcss').Config} */
module.exports = {
  purge: ['./src/**/*.{js,jsx,ts,tsx}'], // adjust this depending on your project structure
  darkMode: true,
  theme: {
    extend: {
      backgroundColor: {
        'dark': '#151515'
      }
    },
  },
  variants: {},
  plugins: [],
}
