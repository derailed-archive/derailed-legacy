import { state } from "@derailed/library/state"
import { observer } from "mobx-react-lite"
import { useState } from "react"

interface Props {
    setExit: any
}

const GuildCreateModal = observer((props: Props) => {
    const [guildName, setGuildName] = useState()

    const handleCreate = async (event: any) => {
        // this doesn't need to be cached as it is gonna be sent from the Gateway
        // @ts-ignore
        await state.rest.create_guild(guildName)
        props.setExit(false)
    }

    return (
        <div className="relative z-10 select-none" aria-labelledby="guild-create-modal" role="dialog" aria-modal="true">
            <div className="fixed inset-0 bg-darker-dark bg-opacity-60 duration-800 transition-opacity"></div>

            <div className="fixed inset-0 z-10 overflow-y-auto">
            <div className="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
            <div className="relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg">
                <div className="bg-dark px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                    <h1 className="text-center text-white text-2xl">
                        Create a Guild
                    </h1>
                    <h3 className="text-center text-white text-sm max-w-xs m-auto opacity-60">
                        Make a new shiny Guild for your friends, or a bustling community!
                    </h3>
                    <div id="input" className="mt-10 flex flex-col items-center justify-center max-w-xl">
                        <form>
                            <div className="flex gap-2">
                                <label className="font-bold text-white text-sm text-derailed-gray">GUILD NAME</label>
                                <input className="rounded-lg bg-darker-dark m-auto text-white" required minLength={1} maxLength={32} onChange={(event) => {
                                    // @ts-ignore
                                    setGuildName(event.target.value)}} />
                            </div>
                            <div className="flex gap-10 items-center justify-center mt-10">
                                <button className="text-white rounded-xl bg-verlp px-3 py-1" onSubmit={handleCreate}>Create</button>
                                <button type="submit" className="text-white" onSubmit={(event) => {event.preventDefault();props.setExit(false)}}>Exit</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
            </div>
            </div>
        </div>
    )
})

export default GuildCreateModal
