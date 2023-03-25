import React from "react";
import ChannelHeader from "./channel_header";
import MessageList from "./message_list";
import { observer } from "mobx-react-lite"


interface Props {
    channel_id: string
}


const Channel = observer((props: Props) => {
    return (
        <div className="bg-dark select-none w-screen">
            <div>
                <ChannelHeader channel_id={props.channel_id} />
                <MessageList channel_id={props.channel_id} />
            </div>
        </div>
    )
})


export default Channel
