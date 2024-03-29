import GuildSidebar from '@derailed/channels/guild_sidebar'
import { state } from '@derailed/library/state'
import { observer } from 'mobx-react-lite'
import { useParams } from 'react-router-dom'
import ChannelSidebar from '@derailed/channels/channel_sidebar'
import './arbitrary.css'
import { Navigate } from 'react-router-dom'


const Guild = observer(() => {
    if (localStorage.getItem("token") === null) {
        return <Navigate to="/login" />
    }

    let { guild_id } = useParams()

    if (guild_id === undefined) {
        return (
            <div>
                Oops...
            </div>
        )
    }

    state.start()
    state.setChannel(null)

    return (
        // @ts-ignore
        <div className="flex bg-dark select-none" style={{msOverflowStyle: 'none', scrollbarWidth: 'none'}}>
            <GuildSidebar />
            <ChannelSidebar guild_id={guild_id} />
        </div>
    )
})

export default Guild
