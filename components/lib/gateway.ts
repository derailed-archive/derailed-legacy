import EventEmitter from 'eventemitter3'

// @ts-ignore
const BASE_URL = import.meta.env.VITE_GATEWAY_URL

interface GatewayMessage {
    op: number,
    s: number | null | undefined,
    t: string | undefined,
    d: object | undefined
}


class Gateway {
    private _ws: WebSocket | null
    private _sequence: number | null
    // @ts-ignore
    private _interval_pinger: number
    // TODO: resume functionality
    // @ts-ignore
    private _session_id: string
    public emitter: EventEmitter

    constructor() {
        this._ws = null
        this._sequence = null
        this.emitter = new EventEmitter()
    }

    connect() {
        console.log(">> [WS] -: CONNECTING")
        this._ws = new WebSocket(BASE_URL)

        this._ws.onopen = (_event) => {
            console.log(">> [WS] -: CONNECTED")
        }

        this._ws.onclose = (event) => {
            console.log(`>> [WS] -: CLOSED (${event.code})`)
            clearInterval(this._interval_pinger)
            this.emitter.emit("CLOSE")
            this.connect()
        }

        this._ws.onmessage = (event) => {
            const message: GatewayMessage = JSON.parse(event.data)

            if (message.s !== undefined) {
                this._sequence = message.s
            }

            if (message.op === 4) {
                console.log(">> [WS] -: GIVEN HELLO")
                // @ts-ignore
                this._interval_pinger = setInterval(() => {
                    this._ws?.send(JSON.stringify({'op': 3, 'd': {'s': this._sequence}}))
                    console.log(`>> [WS] -: HEARTBEAT SEQUENCE ${this._sequence} FINISHED`)
                // @ts-ignore
                }, message.d.heartbeat_interval)
                this.emitter.emit("HELLO")
            } else if (message.op === 1) {
                console.log(">> [WS] -: READY")
                this.emitter.emit("READY", message.d)
                // @ts-ignore
                this._session_id = message.d.session_id
            } else if (message.op === 3) {
                this._sequence = null
            }

            if (message.t !== undefined) {
                this.emitter.emit(message.t, message.d)
            }
        }
    }

    identify() {
        this._ws?.send(JSON.stringify({'op': 1, 'd': {'token': String(localStorage.getItem('token'))}}))
    }
}

export default Gateway
