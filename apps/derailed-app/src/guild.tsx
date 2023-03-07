import GuildSidebar from '@derailed/channels/guild_sidebar'
import { state } from '@derailed/library/state'
import { observer } from 'mobx-react-lite'
import { useParams } from 'react-router-dom'
import ChannelSidebar from '@derailed/channels/channel_sidebar'
import './arbitrary.css'


const Guild = observer(() => {
    let { guild_id } = useParams()

    if (guild_id === undefined) {
        return (
            <div>
                Oops...
            </div>
        )
    }

    state.start()

    return (
        // @ts-ignore
        <div className="flex bg-darker-dark" style={{msOverflowStyle: 'none', scrollbarWidth: 'none'}}>
            <nav>
                <GuildSidebar />
            </nav>
            <ChannelSidebar guild_id={guild_id} />
        </div>
    )
})

export default Guild
