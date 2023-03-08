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
        'light-dark': '#323036',
        'dark': '#232226',
        'darker-dark': '#1F1F22',
        'derailed-gray': '#5a5c5a',
        'verlp': '#807ef2',
        'verlp-dark': '#6664CD'
      }
    },
  },
  plugins: [],
}
