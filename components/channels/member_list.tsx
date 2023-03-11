import React from "react";
import { observer } from "mobx-react-lite"


interface Props {
    guild_id: string
}


const MemberList = observer((props: Props) => {
    return (
        <div className="bg-dark select-none">
            <h1 className="text-white text-right">
                Members
            </h1>
            <ul>

            </ul>
        </div>
    )
})


export default MemberList
