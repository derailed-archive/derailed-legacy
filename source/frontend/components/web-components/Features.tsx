import React from 'react';


export default function Features() {
    return (
        <div>
            <div id="stop-hassling-premium" className="pb-40 pt-40 mb:pl-5 mb:pr-5">
                <div className="text-center pt-3 text-3xl text-[#807ef2]">
                    Stop hassling with paid platforms
                </div>
                <div className="text-center pt-3 text-medium text-[#737f8d] max-w-2xl m-auto">
                    Derailed at its core is 100% free. We don't, and will <b>never</b> charge money to use Derailed's core,
                    and you can always host it yourself.
                    <br />
                    <br />
                    If you're wondering how Derailed will support itself, we will do so with community donations,
                    and Guild subscriptions. Don't get run down for your money by Discord,
                    reinvigorate yourself and save your wallet.
                </div>
            </div>
            <div id="speed" className="bg-[#ebebeb] pb-40 pt-40 mb:pl-5 mb:pr-5">
                <div className="text-center pt-3 text-3xl text-[#807ef2]">Comfortably chat while playing</div>
                <div className="text-center pt-3 text-medium text-[#737f8d] max-w-2xl m-auto">
                    Never get disturbed while planning a raid, or completing a domain. With latency in the
                    milliseconds to make your experience feel snappy.
                    <br />
                    <br />
                    Powered by the Erlang VM, Rust, and many other tools we can provide you the best experience possible.
                </div>
            </div>
            <div id="dont-get-hacked" className="pb-40 pt-40 mb:pl-5 mb:pr-5">
                <div className="text-center pt-3 text-3xl text-[#807ef2]">Don't worry about security</div>
                <div className="text-center pt-3 text-medium text-[#737f8d] max-w-2xl m-auto">
                    Derailed forces upon many security standards to make sure none of your private information
                    is ever accessed by unwanted individuals.
                    <br />
                    It'd take hundreds of years or even more to decrypt your password.
                </div>
            </div>
        </div>
    )
}
