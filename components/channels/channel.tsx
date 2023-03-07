import React from "react";
import ChannelHeader from "./channel_header";
import MessageList from "./message_list";
import { observer } from "mobx-react-lite"
import { state } from "@derailed/library/state"


interface Props {
    channel_id: string
}


const Channel = observer((props: Props) => {
    const channel = state.channels.get(props.channel_id)
    const messages = state.channel_messages.get(String(props.channel_id)) ?? []

    return (
        <div>
            <ChannelHeader channel_name={channel?.name ?? "Unknown"} />
            <MessageList messages={messages} />
        </div>
    )
})


export default Channel
