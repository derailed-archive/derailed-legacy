import React from "react";
import Message from "./message";


const MessageList = ({ messages }) => {
    return (
        <ul>
            {messages.map(message => {
                <Message author_name={message.author.username} author_id={message.author.id} timestamp={message.timestamp} content={message.content} />
            })}
        </ul>
    )
}

export default MessageList
