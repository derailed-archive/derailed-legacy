import { state } from "@derailed/library/state";
import { observer } from "mobx-react-lite";
import { useState } from "react";
import { useNavigate } from "react-router-dom"
import GuildCreateModal from './guild_create_modal'


const GuildSidebar = observer(() => {
    const navigate = useNavigate()
    const enter_guild = (event: any) => {
        navigate(`/channels/${event.target.id}`)
    }
    const exit_guild = (_event: any) => {
        navigate(`/channels/@self`)
    }
    const set_guild_create = (_event: any) => {
        setGuildCreate(true)
    }

    const [guildCreate, setGuildCreate] = useState(false)

    return (
        <div>
            {guildCreate && <GuildCreateModal setExit={setGuildCreate} />}
            <ul role="tree" className="flex pt-2 justify-between gap-5 h-full bg-darker-dark px-3" >
                <div className="min-h-screen">
                    <div className="pb-2">
                        <div aria-label="Derailed Logo" className="select-none px-4 bg-gray-700 text-verlp max-w-[45px] py-2 text-center ease-in-out text-xl transition duration-500 rounded-full hover:rounded-xl hover:bg-verlp hover:text-white m-auto" onClick={exit_guild}>
                            D
                        </div>
                    </div>
                    <div className="pt-1 pb-2">
                        <hr className="bg-derailed-gray rounded-full h-[2px] border-none" />
                    </div>
                    <div aria-label="Guilds">
                        {state.guilds.map(guild => {
                            return (
                                <li key={guild.id} className="text-white select-none max-w-[45px] py-2 text-center bg-derailed-gray mb-2 ease-in-out text-xl transition duration-800 rounded-full hover:rounded-xl hover:bg-verlp hover:text-white m-auto" style={{listStyleType: "none"}} onClick={enter_guild}>
                                    <div id={guild.id} role="treeitem" aria-label={guild.name}>
                                        {guild.name.replace(/[^A-Z]+/g, "").slice(0, 3)}
                                    </div>
                                </li>
                            )
                        })}
                    </div>
                    <div aria-label="Add Server" onClick={set_guild_create} className="select-none bg-gray-700 text-verlp max-w-[45px] py-2 text-center ease-in-out text-xl transition duration-500 rounded-full hover:rounded-xl hover:bg-verlp hover:text-white m-auto">
                            +
                    </div>
                </div>
            </ul>
        </div>
    )
})


export default GuildSidebar
