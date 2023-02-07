/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
	"../../components/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
		extend: {},
		screens: {
			mb: { max: '847px' },
			dsk: { min: '848px' }
		},
		fontFamily: {
			dino: ['Cabin', 'Helvetica Neue', 'Helvetica', 'Arial', 'sans-serif'],
		}
  },
  plugins: [],
}
