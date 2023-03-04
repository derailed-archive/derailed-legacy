import GuildSidebar from '@derailed/channels/guild_sidebar'
import { state as state_ctx } from '@derailed/library/state'
import { useContext } from 'react'
import { observer } from 'mobx-react-lite'
import './arbitrary.css'


const Open = observer(() => {
    const state = useContext(state_ctx)
    state.start()

    return (
        // @ts-ignore
        <div className="flex" style={{msOverflowStyle: 'none', scrollbarWidth: 'none'}}>
            <nav>
                <GuildSidebar guilds={state.guilds} />
            </nav>
            <div>
                <h1 className="text-center text-white text-xl">
                    Welcome to Derailed!
                </h1>
            </div>
        </div>
    )
})

export default Open
