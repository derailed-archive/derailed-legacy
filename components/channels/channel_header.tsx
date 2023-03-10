import { state } from "@derailed/library/state";
import { observer } from "mobx-react-lite";

interface Props {
    channel_id: string
}

const ChannelHeader = observer((props: Props) => {
    return (
        <div>
            <h2 className="text-lg text-white">
                {state.channels.get(props.channel_id)?.name ?? ""}
            </h2>
        </div>
    )
})

export default ChannelHeader
