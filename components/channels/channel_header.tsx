import { state } from "@derailed/library/state";
import { observer } from "mobx-react-lite";

interface Props {
    channel_id: string
}

const ChannelHeader = observer((props: Props) => {
    return (
        <div>
            <h2 className="text-lg text-white border-b-2 border-b-darker-dark">
                <div className="ml-10 mt-5 mb-5 text-xl">
                    {state.channels.get(props.channel_id)?.name ?? ""}
                </div>
            </h2>
        </div>
    )
})

export default ChannelHeader
