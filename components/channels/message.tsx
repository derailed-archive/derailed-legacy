import React from "react";

// TODO: select author
// @ts-ignore
const Message = ({ author_name, author_id, timestamp, message_id, content }) => {
    const milliseconds_day = 86_400_000
    const milliseconds_yesterday = milliseconds_day + milliseconds_day
    const messageTimestamp = new Date(timestamp)
    var displayedTimestamp

    if (messageTimestamp.getTime() - milliseconds_day > Date.now() - milliseconds_day) {
        displayedTimestamp = `Today at ${messageTimestamp.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true })}`
    } else if (messageTimestamp.getTime() - milliseconds_yesterday > Date.now() - milliseconds_yesterday) {
        displayedTimestamp = `Yesterday at ${messageTimestamp.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true })}`
    } else {
        displayedTimestamp = `${messageTimestamp.getMonth()}/${messageTimestamp.getDay()}/${messageTimestamp.getFullYear()} ${messageTimestamp.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true })}`
    }

    return (
        <li className="bg-light-dark hover:bg-dark pb-5 pt-5 pl-4" key={message_id} style={{listStyleType: "none"}}>
            <div id="head" className="flex gap-3">
                <div className="bg-gray-700 rounded-full w-10 h-10">

                </div>
                <h3 className="text-verlp font-bold hover:underline">
                    {author_name}
                </h3>
                <h4 className="text-derailed-gray">
                    {displayedTimestamp}
                </h4>
            </div>
            <div id="content" className="max-w-lg text-white ml-14 select-text">
                {content}
            </div>
        </li>
    )
}

export default Message
