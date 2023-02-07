import React from 'react';


export default function Header() {
    return (
        <div className="font-dino font-normal dsk:mx-40 mb:mx-2 p-1 flex items-center bg-[#202024]">
            <header>
            <a href="/">
				<img
					src="banner.png"
					className="dsk:w-30 dsk:h-24 dsk:ml-1 mb:w-24 mb:h-14 mb:object-center"
					alt="Derailed Logo Banner"
				/>
			</a>
            </header>
        </div>
    )
}
