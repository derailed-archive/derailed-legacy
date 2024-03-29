/** @type {import('tailwindcss').Config} */
module.exports = {
	content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
	theme: {
		extend: {
			colors: {
				'not-black-yet': '#2B2B30',
				'almost-black-but-not': '#1e1e21',
				'almost-blue': '#807ef2',
				'almost-dark-blue': '#6664CD',
				'texty': '#23272A',
				'derailed-gray': '#6b6b6b',
			},
			fontFamily: {
				'header': ['Inter'],
				'brand': ['Vampire Wars']
			}
		},
	},
	plugins: [],
}
