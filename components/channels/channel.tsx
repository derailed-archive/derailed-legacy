import React, { useState } from "react";
import ChannelHeader from "./channel_header";
import MessageList from "./message_list";


const Channel = ({ channel_name, channel_id, }) => {
    const [messages, setMessages] = useState([])

    return (
        <div>
            <ChannelHeader channel_name={channel_name} />
            <MessageList messages={messages} />
        </div>
    )
}

export default Channel
