import { createContext } from "react"
import HTTPClient from "./http"
import Gateway from "./gateway"
import { Channel, ChannelMessage, Guild } from "./types"
import { makeAutoObservable } from "mobx"


export class State {
    public rest: HTTPClient | null
    public ws: Gateway | null
    public channel_messages: Map<string, Array<ChannelMessage>>
    public channels: Map<string, Channel>
    public guilds: Array<Guild>
    private _started: boolean

    constructor() {
        makeAutoObservable(this)
        this.rest = null
        this.ws = null
        this._started = false
        this.channel_messages = new Map()
        this.channels = new Map()
        this.guilds = []
    }

    start() {
        if (this._started === false) {
            this.ws = new Gateway()
            this.rest = new HTTPClient()
            this.ws.connect()
            this.ws.emitter.on("HELLO", () => this.ws?.identify())
            this._started = true
            this.ws.emitter.on('GUILD_CREATE', this.on_guild_create)
        }
    }

    on_guild_create(guild: Guild) {
        this.guilds.push(guild)
    }
}

export const state = createContext<State>(new State())
