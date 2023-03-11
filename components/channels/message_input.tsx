import { state } from "@derailed/library/state";
import React from "react";
import { useState } from "react";
import Message from "./message";


interface Props {
    channel_id: string
}


const MessageInput = (props: Props) => {
    const [content, setContent] = useState<string | undefined>()
    const submitKey = async (event: any) => {
        if (event.keyCode === 13 && event.shiftKey) {
            return
        } else if (event.keyCode === 13) {
            event.preventDefault()
            var value = String(event.target.value)
            value = value.replace(' ', '')
            if (value !== '') {
                event.target.value = ""
                submitInput()
                setContent("")
            }
        }
    }
    const submitInput = async () => {
        // @ts-ignore
        await state.rest.send_message(content, props.channel_id)
    }

    return (
        <div className="bg-light-dark text-white fixed bottom-0 flex pl-5 pb-5">
            <form className="flex-1 max-h-10 max-w-xl mt-5 m-auto">
                <textarea
                    onChange={(event) => {
                        setContent(event.target.value)
                    }}
                    autoComplete="off"
                    spellCheck="true"
                    onKeyDown={submitKey}
                    className="form-textarea w-[50rem] px-2 py-2 rounded-lg bg-dark text-gray-300 break-words resize-none whitespace-pre-wrap outline-none"
                    placeholder="Oye lads, I went to the pub today and..."
                    maxLength={2024}
                    />
            </form>
        </div>
    )
}

export default MessageInput
