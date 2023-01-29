module.exports = {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {},
		screens: {
			mb: { max: '847px' },
			dsk: { min: '848px' }
		},
		fontFamily: {
			dino: ['Whitney', 'Helvetica Neue', 'Helvetica', 'Arial', 'sans-serif']
		}
	},
	plugins: []
};
