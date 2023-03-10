import React from "react";
import Message from "./message";
import { ChannelMessage } from "@derailed/library/types";


interface Props {
    messages: ChannelMessage[]
}


const MessageList = (props: Props) => {
    return (
        <ul>
            {props.messages.map(message => {
                return <Message author_name={message.author?.username} author_id={message.author?.id} timestamp={message.timestamp} content={message.content} />
            })}
        </ul>
    )
}

export default MessageList
