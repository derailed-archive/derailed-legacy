import { state } from "@derailed/library/state"
import { observer } from "mobx-react-lite"
import { Icon } from '@iconify/react'

interface Props {
    guild_id: string
}

const ChannelSidebar = observer((props: Props) => {
    let channels = state.guild_channels.get(props.guild_id) ?? []

    return (
        <div className="rounded-tl-3xl w-56 bg-dark text-white">
            <div className="border-b-2 border-b-darker-dark rounded-tl-3xl max-w-lg p-3">
                <div className="ml-5 py-3 pr-5 text-center max-w-lg">
                    {state.guilds_map.get(props.guild_id)?.name ?? "Guild!"}
                </div>
            </div>
            <div className="mt-2">
                <ul>
                    {channels.map((channel, _idx, _arr) => {
                        if (channel.type == "CATEGORY") {
                            return (
                                <li id={channel.id} key={channel.id} className="pb-2 pt-2 mr-32 text-sm opacity-80 text-center">
                                    {channel.name?.toUpperCase()}
                                </li>
                            )
                        }
                        return (
                            <li id={channel.id} key={channel.id} className="pt-2 pb-2 m-auto text-center flex transition duration-100 hover:bg-light-dark">
                                <div className="w-20 mt-10 hidden">
                                    <Icon icon="fluent:channel-24-regular" color="#5a5c5a" />
                                </div>
                                <h4 className="text-center m-auto">
                                    {channel.name}
                                </h4>
                            </li>
                        )
                    })}
                </ul>
            </div>
        </div>
    )
})

export default ChannelSidebar
