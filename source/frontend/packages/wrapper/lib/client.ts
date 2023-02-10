export interface Options {
    gatewayURI: string,
    apiURI: string
}


export interface GatewayMessage {
    op: Number,
    d: Object,
    s: Number,
    t: String | undefined
}


export class Client extends EventTarget {
    public options?: Options
    private _token: String
    private _ws: WebSocket | null = null
    private _sequence: Number | null = null

    constructor(token: String, options?: Options) {
        super()
        this.options = options
        this._token = token
    }

    connect() {
        this._ws = new WebSocket(this.options?.gatewayURI || "gateway.derailed.one")

        this._ws.addEventListener('open', (_event) => {
            this.dispatchEvent(new Event('WS_OPEN'))
            this._ws?.addEventListener('message', (event: MessageEvent) => {
                console.debug(`GATEWAY: received message ${event.data}`)
                let message: GatewayMessage = JSON.parse(event.data)

                if (message.t !== undefined) {
                    this.dispatchEvent(new MessageEvent(message.t.toString(), {data: message.d}))
                }
                this._sequence = message.s

                if (message.op === 4) {
                    console.debug('GATEWAY: received HELLO event, sending ready')
                    this._ws?.send(JSON.stringify({
                        'op': 1,
                        'd': {
                            'token': this._token
                        }
                    }))
                }
            })
        })

        this._ws.addEventListener('close', (event: CloseEvent) => {
            if (event.code === 5004) {
                // TODO: throw error
                console.error('GATEWAY: Invalid authorization')
            }
        })
    }
}
