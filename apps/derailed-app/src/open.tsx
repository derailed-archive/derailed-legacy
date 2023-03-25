import GuildSidebar from '@derailed/channels/guild_sidebar'
import { state } from '@derailed/library/state'
import { observer } from 'mobx-react-lite'
import './arbitrary.css'
import { Navigate } from 'react-router-dom'


const Open = observer(() => {
    if (localStorage.getItem("token") === null) {
        return <Navigate to="/login" />
    }

    state.start()
    state.setChannel(null)

    return (
        // @ts-ignore
        <div className="flex" style={{msOverflowStyle: 'none', scrollbarWidth: 'none'}}>
            <GuildSidebar />
            <div className='bg-dark w-full select-none'>
                <h1 className="text-center text-white text-4xl mt-32">
                    Welcome to back to Derailed!
                </h1>
            </div>
        </div>
    )
})

export default Open
