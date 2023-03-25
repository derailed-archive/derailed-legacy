import { state } from "@derailed/library/state";
import { useState } from "react";


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
        <div className="bg-transparent text-white fixed bottom-0 flex pl-5 pb-5">
            <form className="flex-1 max-h-10 max-w-xl mt-5 m-auto">
                <textarea
                    value={content}
                    onChange={(event) => {
                        setContent(event.target.value)
                    }}
                    autoComplete="off"
                    spellCheck="true"
                    onKeyDown={submitKey}
                    className="form-textarea w-[48rem] p-1 resize-none shadow-sm h-auto overflow-y-auto scroll-none rounded-md bg-derailed-gray m-auto text-gray-300 break-words whitespace-pre-wrap outline-none"
                    placeholder="Heyo! What's going on right now?"
                    maxLength={2024}
                    />
            </form>
        </div>
    )
}

export default MessageInput
