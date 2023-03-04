import { createContext } from "react"
import HTTPClient from "./http"
import Gateway from "./gateway"

export class State {
    public rest: HTTPClient | null
    public ws: Gateway | null
    private _started: boolean

    constructor() {
        this.rest = null
        this.ws = null
        this._started = false
    }

    start() {
        if (this._started === false) {
            this.ws = new Gateway()
            this.rest = new HTTPClient()
            this.ws.connect()
            this.ws.emitter.on("HELLO", () => this.ws?.identify())
            this._started = true
        }
    }
}

export const state = createContext<State>(new State())
