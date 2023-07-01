<script lang="ts">
	import derailed_banner from '$lib/assets/derailed.png';
	import twm from '$lib/assets/twitter-mark.png';
	import msm from '$lib/assets/mastodon-mark.png';
	import ghm from '$lib/assets/facebook-mark.png';
	import navicon from '$lib/assets/navicon.png';
	import x_bold from '$lib/assets/x-bold.png';

	let ui_opened = false;
</script>

<header id="header">
	<div id="headerDesktop" class="sm:hidden lg:block pb-5">
		<div
			class="flex items-center justify-center gap-10"
			style="font-variation-settings: 'ital' 0, 'wdth' 125;"
		>
			<a href="/">
				<img alt="Derailed" src={derailed_banner} class="w-46 h-20 pt-4" />
			</a>
			<a href="/features" class="pt-5 text-[#e8e8ed] hover:text-white"> Features </a>
			<a href="https://blog.derailed.one" class="pt-5 text-[#e8e8ed] hover:text-white"> Blog </a>
			<a href="/terms" class="pt-5 text-[#e8e8ed] hover:text-white"> Terms </a>
			<a href="/privacy" class="pt-5 text-[#e8e8ed] hover:text-white"> Privacy Policy </a>
			<div class="pr-32" />
			<a href="https://twitter.com/derailedapp">
				<img alt="Twitter" src={twm} class="pt-5 h-11" />
			</a>
			<a href="https://mastodon.social/@derailed">
				<img alt="Mastodon" src={msm} class="pt-5 h-11" />
			</a>
			<a href="https://facebook.com/derailedapp">
				<img alt="Facebook" src={ghm} class="pt-5 h-11" />
			</a>
		</div>
	</div>

	<nav id="headerMobile" class="sm:block lg:hidden">
		<div class={ui_opened === true ? 'bg-black' : ''}>
			<div class="pb-5">
				<div class="flex justify-start items-center h-full relative">
					<div class={ui_opened === true ? 'hidden' : ''}>
						<button
							class="w-5 h-5 mt-5 ml-5 inline-block"
							on:click={() => {
								ui_opened = true;
							}}
						>
							<img alt="nav" src={navicon} />
						</button>
					</div>
					<div class={ui_opened === false ? 'hidden' : ''}>
						<button
							class="w-5 h-5 mt-5 ml-5 inline-block"
							on:click={() => {
								ui_opened = false;
							}}
						>
							<img alt="nav" src={x_bold} />
						</button>
					</div>
				</div>
				<div class={ui_opened === false ? 'hidden' : ''}>
					<ul class="list-none bg-black text-white ml-14 mt-10">
						<li class="text-[#e8e8ed] hover:text-white">
							<a href="/features"> Features </a>
						</li>
						<li class="mt-2 text-[#e8e8ed] hover:text-white">
							<a href="https://blog.derailed.one"> Blog </a>
						</li>
						<li class="mt-2 text-[#e8e8ed] hover:text-white">
							<a href="/terms"> Terms </a>
						</li>
						<li class="mt-2 text-[#e8e8ed] hover:text-white">
							<a href="/privacy"> Privacy </a>
						</li>
					</ul>
				</div>
			</div>
		</div>
	</nav>
</header>
