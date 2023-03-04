import { useContext } from "react"
import { state as state_ctx } from "@derailed/library/state"

function TestWS() {
  const state = useContext(state_ctx)

  state.start()

  return (
    <div>
        Heyo!
    </div>
  )
}

export default TestWS
