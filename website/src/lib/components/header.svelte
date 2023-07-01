<script lang="ts">
	import derailed_banner from '$lib/assets/derailed.png';
	import twm from '$lib/assets/twitter-mark.png';
	import msm from '$lib/assets/mastodon-mark.png';
	import ghm from '$lib/assets/facebook-mark.png';
</script>

<div id="header" class="">
    <div
        id="headerDesktop"
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