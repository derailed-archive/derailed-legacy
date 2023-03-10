import React from "react";
import ChannelHeader from "./channel_header";
import MessageList from "./message_list";
import { observer } from "mobx-react-lite"
import { state } from "@derailed/library/state"


interface Props {
    channel_id: string
}


const Channel = observer((props: Props) => {
    return (
        <div>
            <ChannelHeader channel_id={props.channel_id} />
            <MessageList messages={state.channel_messages.get(String(props.channel_id)) ?? []} />
        </div>
    )
})


export default Channel
