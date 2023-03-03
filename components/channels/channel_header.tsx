import React from "react";


const ChannelHeader = ({ channel_name }) => {
    return (
        <div>
            <h2 className="text-lg">
                {channel_name}
            </h2>
        </div>
    )
}

export default ChannelHeader
