import React from 'react';


export default function Footer() {
    return (
        <footer className="pt-32 pb-10 bg-[#202024] mb:pl-5 mb:pr-5">
            <div className="text-center text-4xl text-white pt-3 pb-20">
                Derailed, the free gaming platform for chat.
            </div>
            <div className="flex justify-center items-center pt-7 text-sm" style={{gap: 15}}>
                <a href="/about" className="text-center text-[#737f8d]">About</a>
                <a href="https://blog.derailed.one" className="text-center text-[#737f8d]">Blog</a>
                <a href="/terms" className="text-center text-[#737f8d]">Terms of Service</a>
                <a href="/privacy" className="text-center text-[#737f8d]">Privacy Policy</a>
            </div>
	    </footer>
    )
}

