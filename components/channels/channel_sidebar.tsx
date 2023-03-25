import { state } from "@derailed/library/state"
import { observer } from "mobx-react-lite"
import { Icon } from '@iconify/react'
import { useNavigate, Link } from "react-router-dom"
import { Channel } from "@derailed/library/types"

interface Props {
    guild_id: string
}

interface CProps {
    channel: Channel
}

const Channel = observer((props: CProps) => {
    if (state.current_channel === props.channel.id) {
        return (
            <Link to={`/channels/${props.channel.guild_id}/${props.channel.id}`}>
                {}
                <li key={props.channel.id} className="pt-2 pb-2 px-5 m-auto text-center select-none flex transition duration-100 bg-light">
                    <div className="w-20 mt-10 hidden">
                        <Icon icon="fluent:channel-24-regular" color="#5a5c5a" />
                    </div>
                    <h4 className="text-center m-auto">
                        {props.channel.name}
                    </h4>
                </li>
            </Link>
        )
    } else {
        return (
            <Link to={`/channels/${props.channel.guild_id}/${props.channel.id}`}>
                {}
                <li key={props.channel.id} className="pt-2 pb-2 px-5 m-auto text-center select-none flex transition duration-100 bg-dark hover:bg-light">
                    <div className="w-20 mt-10 hidden">
                        <Icon icon="fluent:channel-24-regular" color="#5a5c5a" />
                    </div>
                    <h4 className="text-center m-auto">
                        {props.channel.name}
                    </h4>
                </li>
            </Link>
        )
    }
})


const ChannelSidebar = observer((props: Props) => {
    let channels = state.guild_channels.get(props.guild_id) ?? []

    return (
        <div className="rounded-tl-xl w-56 bg-dark text-white border-r border-r-derailed-gray">
            <div className="max-w-lg p-3">
                <div className="ml-5 py-3 pr-5 text-center max-w-lg">
                    {state.guilds_map.get(props.guild_id)?.name ?? ""}
                </div>
            </div>
            <div className="mt-2">
                <ul>
                    {channels.map((channel, _idx, _arr) => {
                        if (channel.type == "CATEGORY") {
                            return (
                                <li id={channel.id} key={channel.id} className="pb-2 px-5 pt-2 mr-32 text-sm opacity-80 select-none text-center">
                                    {channel.name?.toUpperCase()}
                                </li>
                            )
                        } else {
                            return <Channel channel={channel} />
                        }
                    })}
                </ul>
            </div>
        </div>
    )
})

export default ChannelSidebar
