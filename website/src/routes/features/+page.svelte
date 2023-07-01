<script>
	import Header from '$lib/components/header.svelte';
	import derailed_phone from '$lib/assets/derailed_phone.png';
	import infinity_bold from '$lib/assets/infinity-bold.png';
	import Footer from '$lib/components/footer.svelte';
</script>

<div id="features" class="bg-white h-screen font-main">
	<div class="bg-porpol">
		<Header />
	</div>

	<h1
		class="text-center pt-40 text-3xl font-semibold m-auto text-porpol"
		style="font-variation-settings: 'ital' 0, 'wdth' 125;"
	>
		A New Type of Platform.
	</h1>

	<div class="mt-40 pt-32 pb-32 bg-[#e8e8ed] px-5">
		<div class="flex items-center justify-center">
			<div>
				<h1
					class="text-2xl font-black text-porpol"
					style="font-variation-settings: 'ital' 0, 'wdth' 125;"
				>
					Tomorrow's communication, today.
				</h1>
				<h3 class="text-lg max-w-xl pt-3 text-gray-400">
					A new, sleek, and modern-looking interface with new features to give you total control
					over your Derailed experience.
				</h3>
			</div>
			<img alt="Derailed On Phone" src={derailed_phone} class="pl-10 w-60 sm:hidden lg:inline" />
		</div>
	</div>

	<div class=" pt-32 pb-32 bg-white px-5">
		<div class="flex items-center justify-center">
			<img alt="Infinity" src={infinity_bold} class="pr-10 w-60 sm:hidden lg:inline" />
			<div>
				<h1
					class="text-2xl font-black text-porpol"
					style="font-variation-settings: 'ital' 0, 'wdth' 125;"
				>
					Reliability eternally
				</h1>
				<h3 class="text-lg max-w-xl pt-3 text-gray-400">
					Derailed's systems are made to withstand large punches, dodge DDoS attacks, and be
					fail-safe at any corner. Downtimes rare, and uptime, always.
				</h3>
			</div>
		</div>
	</div>

	<div class="pt-32 bg-porpol">
		<Footer />
	</div>
</div>
