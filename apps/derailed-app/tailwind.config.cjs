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
        'dark': '#232226',
        'darker-dark': '#1F1F22',
        'verlp': '#807ef2'
      }
    },
  },
  plugins: [],
}
