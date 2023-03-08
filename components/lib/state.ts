import HTTPClient from "./http"
import Gateway from "./gateway"
import { Channel, ChannelMessage, Guild } from "./types"
import { makeAutoObservable } from "mobx"


export class State {
    public rest: HTTPClient
    public ws: Gateway
    public channel_messages: Map<string, Array<ChannelMessage>>
    public channels: Map<string, Channel>
    public guilds: Array<Guild>
    public guilds_map: Map<string, Guild>
    public guild_channels: Map<string, Array<Channel>>
    private _started: boolean

    constructor() {
        makeAutoObservable(this)
        this.ws = new Gateway()
        this.rest = new HTTPClient()
        this._started = false
        /* if you're wondering
            channel_messages: ChannelID: Message
            channels: ChannelID: Channel
            guild_channels: GuildID: Channel[]
            guilds: Guild[]
        */
        this.channel_messages = new Map()
        this.channels = new Map()
        this.guild_channels = new Map()
        this.guilds = new Array()
        this.guilds_map = new Map()
    }

    start() {
        if (this._started === false) {
            this.ws.connect()
            this.ws.emitter.on("HELLO", () => this.ws?.identify())
            this._started = true
            this.ws.emitter.on('GUILD_CREATE', this.on_guild_create, this)
        }
    }

    on_guild_create(guild: Guild) {
        this.guilds_map.set(String(guild.id), guild)
        if (this.guilds.some((g, _idx, _arr) => {if (g.id === String(guild.id)) {return true}}) === false) {
            this.guilds.push(guild)
        }

        const channels = guild.channels

        // @ts-ignore
        channels?.sort((a, b) => { return a.position-b.position })

        // @ts-ignore
        this.guild_channels.set(String(guild.id), channels)
    }
}

export const state = new State()
