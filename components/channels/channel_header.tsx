import React from "react";
import { observer } from "mobx-react-lite";


interface Props {
    channel_name: string
}


const ChannelHeader = observer((props: Props) => {
    return (
        <div>
            <h2 className="text-lg">
                {props.channel_name}
            </h2>
        </div>
    )
})

export default ChannelHeader
