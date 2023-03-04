import React, { useState } from "react";
import { observer } from "mobx-react-lite";
import { Guild } from "@derailed/library/types";
import { useNavigate } from "react-router-dom"


interface Props {
    guilds: Array<Guild>
}


const GuildSidebar = observer((props: Props) => {
    const navigate = useNavigate()
    const [currentGuild, setCurrentGuild] = useState<string | null>(null)
    const enter_guild = (_: any) => {
        if (currentGuild !== null) {
            navigate(`/guilds/${currentGuild}`)
        }
    }
    const mouse_over = (event: any) => {
        setCurrentGuild(event.id)
    }
    const mouse_out = (_: any) => {
        setCurrentGuild(null)
    }

    return (
        <ul role="tree" className="flex pt-2 justify-between gap-5 h-full bg-darker-dark px-3">
            <div className="min-h-screen">
                <div className="pb-2">
                    <div aria-label="Derailed Logo" className=" px-4 bg-gray-700 text-verlp max-w-[45px] py-2 text-center ease-in-out text-xl transition duration-500 rounded-full hover:rounded-xl hover:bg-verlp hover:text-white m-auto">
                        D
                    </div>
                </div>
                <div className="pt-1 pb-2">
                    <hr className="bg-derailed-gray rounded-full h-[2px] border-none" />
                </div>
                <div aria-label="Guilds">
                    {props.guilds.map(guild => {
                        return (
                            <li className="bg-derailed-gray transition duration-300 rounded-full hover:rounded-xl" style={{listStyleType: "none"}} onClick={enter_guild} onMouseEnter={mouse_over} onMouseLeave={mouse_out}>
                                <div id={guild.id} className="bg-gray-600 rounded-full w-10 h-10" role="treeitem" aria-label={guild.name}>
                                    {guild.name.replace(/[^A-Z]+/g, "").slice(0, 3)}
                                </div>
                            </li>
                        )
                    })}
                </div>
                <div aria-label="Add Server" className="bg-gray-700 text-verlp max-w-[45px] py-2 text-center ease-in-out text-xl transition duration-500 rounded-full hover:rounded-xl hover:bg-verlp hover:text-white m-auto">
                        +
                </div>
            </div>
        </ul>
    )
})


export default GuildSidebar
