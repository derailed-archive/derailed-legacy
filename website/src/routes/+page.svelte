<script lang="ts">
	import awya from '$lib/assets/availablewhereyouare.png';
	import Header from '$lib/components/header.svelte';
</script>

<div id="main" class="bg-grayish h-screen font-main">
	<Header />

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

	<h6
		class="font-light m-auto text-[#e8e8ed] text-center text-xl outline-none max-w-4xl pt-10"
		style="font-variation-settings: 'ital' 0, 'wdth' 125;"
	>
		Coming soon...
	</h6>

	<div class="flex justify-center">
		<img alt="Available where you are" src={awya} class="pt-14" />
	</div>
</div>
