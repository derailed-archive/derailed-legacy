<script lang="ts">
	import bob from '$lib/assets/bob.png';
</script>

<footer
	class="text-[#e8e8ed] pb-24 font-main"
	style="font-variation-settings: 'ital' 0, 'wdth' 125;"
>
	<div class="flex justify-center">
		<img alt="Bob" src={bob} class="w-7 mb-14 sm:block lg:hidden" />
	</div>
	<div class="flex flex-wrap justify-center items-center gap-40">
		<img alt="Bob" src={bob} class="w-7 mb-14 sm:hidden lg:block" />
		<div id="home">
			<h1 class="font-semibold mb-3.5 text-white">Home</h1>
			<a href="/">
				<h3 class="hover:text-white">Home</h3>
			</a>
			<a href="/features">
				<h3 class="hover:text-white">Features</h3>
			</a>
			<a href="https://blog.derailed.one">
				<h3 class="hover:text-white">Blog</h3>
			</a>
		</div>

		<div id="resources" class="mb-5">
			<h1 class="font-semibold mb-3.5 text-white">Resources</h1>
			<a href="/terms">
				<h3 class="hover:text-white">Terms</h3>
			</a>
			<a href="/privacy">
				<h3 class="hover:text-white">Privacy Policy</h3>
			</a>
		</div>
	</div>
</footer>
