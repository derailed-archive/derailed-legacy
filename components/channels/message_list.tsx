import { state } from "@derailed/library/state";
import React from "react";
import Message from "./message";
import MessageInput from "./message_input";


interface Props {
    channel_id: string
}


const MessageList = (props: Props) => {
    const fill_messages = async () => {
      const messages = await state.rest.get_messages(props.channel_id)
      console.log(messages)
      // @ts-ignore
      state.appendMessages(props.channel_id, messages)
    }
  
    if (state.channel_messages.get(props.channel_id) === undefined) {
      fill_messages()
    }
  
    return (
      <ul className="overflow-auto max-h-screen/2">
        <li id="top" key="header" className="pt-10 text-2xl pl-4 pb-5">
          <h1 className="text-white max-w-lg text-center">
            Well, seems like you've reached the top of this channel... surprise!
          </h1>
        </li>
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
    )
  }
  

export default MessageList
