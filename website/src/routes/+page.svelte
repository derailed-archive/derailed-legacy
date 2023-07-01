<script lang="ts">
	import awya from '$lib/assets/availablewhereyouare.png';
	import Footer from '$lib/components/footer.svelte';
	import Header from '$lib/components/header.svelte';
</script>

<div id="main" class="bg-grayish font-main">
	<Header />

	<div class="sm:px-5">
		<h1
			class="font-black m-auto text-white pt-24 text-center text-4xl outline-none"
			style="font-variation-settings: 'ital' 0, 'wdth' 125;"
		>
			One Platform For Any Post.
		</h1>
		<h3
			class="font-light m-auto text-[#e8e8ed] text-center text-xl outline-none max-w-3xl pt-5"
			style="font-variation-settings: 'ital' 0, 'wdth' 125;"
		>
			A single platform where you and your friends can just hang out, have fun, and chat with each
			other using chat, voice, or posts. Where only your imagination is the limit to how you can
			chat...
		</h3>

		<div class="flex justify-center">
			<img alt="Available where you are" src={awya} class="pt-14" />
		</div>

		<div class="pt-72 bg-grayish">
			<Footer />
		</div>
	</div>
</div>
