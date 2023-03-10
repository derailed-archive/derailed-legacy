import GuildSidebar from '@derailed/channels/guild_sidebar'
import { state } from '@derailed/library/state'
import { observer } from 'mobx-react-lite'
import { useParams } from 'react-router-dom'
import ChannelSidebar from '@derailed/channels/channel_sidebar'
import './arbitrary.css'
import Channel from '@derailed/channels/channel'
import { action } from 'mobx'
import { Navigate } from 'react-router-dom'


const ChannelComponent = observer(() => {
    if (localStorage.getItem("token") === null) {
        return <Navigate to="/login" />
    }

    let { guild_id, channel_id } = useParams()

    if (guild_id === undefined) {
        return (
            <div>
                Oops...
            </div>
        )
    } else if (channel_id === undefined) {
        return (
            <div>
                Oops...
            </div>
        )
    }

    state.start()

    state.setChannel(channel_id)

    return (
        // @ts-ignore
        <div className="flex bg-darker-dark" style={{msOverflowStyle: 'none', scrollbarWidth: 'none'}}>
            <nav>
                <GuildSidebar />
            </nav>
            <ChannelSidebar guild_id={guild_id} />
            <Channel channel_id={channel_id} />
        </div>
    )
})

export default ChannelComponent
