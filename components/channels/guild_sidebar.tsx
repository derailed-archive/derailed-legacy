import { state } from "@derailed/library/state";
import { observer } from "mobx-react-lite";
import { useNavigate } from "react-router-dom"


const GuildSidebar = observer(() => {
    const navigate = useNavigate()
    const enter_guild = (event: any) => {
        console.log(event)
        navigate(`/guilds/${event.target.id}`)
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
                    {state.guilds.map(guild => {
                        return (
                            <li key={guild.id} className="text-white max-w-[45px] py-2 text-center bg-derailed-gray mb-2 ease-in-out text-xl transition duration-800 rounded-full hover:rounded-xl hover:bg-verlp hover:text-white m-auto" style={{listStyleType: "none"}} onClick={enter_guild}>
                                <div id={guild.id} role="treeitem" aria-label={guild.name}>
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
