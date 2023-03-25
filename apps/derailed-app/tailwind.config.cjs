/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
    "../../components/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      backgroundImage: {
        'login': "url('/imgs/bg-media.jpg')"
      },
      colors: {
        'light': '#132745',
        'dark': '#0a1628',
        'verlp': '#7364FF',
        'verlp-dark': '#5d50d9',
        'derailed-gray': '#121F2F'
      }
    },
  },
  plugins: [],
}
