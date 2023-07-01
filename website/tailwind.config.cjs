/** @type {import('tailwindcss').Config} */
module.exports = {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				grayish: 'hsl(234, 17%, 11%)',
				porpol: 'hsl(233, 100%, 72%)'
			},
			fontFamily: {
				main: ['Mona Sans']
			},
			screens: {
				sm: '0px',
				lg: '1050px'
			}
		}
	},
	plugins: [require('./plugins/tailwind/variableFontWorkaround.cjs')]
};
