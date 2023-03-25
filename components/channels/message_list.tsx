import { state } from "@derailed/library/state";
import { observer } from "mobx-react-lite";
import React from "react";
import Message from "./message";
import MessageInput from "./message_input";


interface Props {
    channel_id: string
}

const MessageList = observer((props: Props) => {
  return (
    <div className="max-h-screen/2">
      <ul className="overflow-y-scroll scrollbar-thin scrollbar-thumb-gray-500 scrollbar-track-gray-300 max-h-screen/2">
        {state.channel_messages.get(props.channel_id)?.map(message => {
          return (
            <Message
              message_id={message.id}
              author_name={message.author?.username}
              author_id={message.author?.id}
              timestamp={message.timestamp}
              content={message.content}
            />
          )
        })}
        <li id="inp" key="inp" className="pt-20">
            <MessageInput channel_id={props.channel_id} />
        </li>
      </ul>
    </div>
  )
})

  

export default MessageList
