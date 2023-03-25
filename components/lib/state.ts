import HTTPClient from "./http"
import Gateway from "./gateway"
import { Channel, ChannelMessage, Guild } from "./types"
import { makeAutoObservable } from "mobx"
import { action } from "mobx"


export class State {
    public rest: HTTPClient
    public ws: Gateway
    public channel_messages: Map<string, Array<ChannelMessage>>
    public channels: Map<string, Channel>
    public guilds: Array<Guild>
    public guilds_map: Map<string, Guild>
    public guild_channels: Map<string, Array<Channel>>
    public current_channel: string | null
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

        this.current_channel = null
    }

    setChannel(channel_id: string | null) {
        action(() => {
            this.current_channel = channel_id
        })
        if (channel_id !== null) {
            this.fill_messages(channel_id)
        }
    }

    fill_messages(channel_id: string) {
        console.log('filling up messages')
        // @ts-ignore
        this.rest.get_messages(channel_id).then(
            // @ts-ignore
            ((messages) => { this.appendMessages(channel_id, messages)}),
            ((reason) => {console.error(reason)})
        )
    }

    appendMessages(channel_id: string, messages: ChannelMessage[]) {
        var channel_messages = this.channel_messages.get(channel_id)
        messages.forEach((message, _idx, _arr) => {
            if (channel_messages !== undefined) {
                channel_messages.push(message)
            } else {
                channel_messages = new Array()
            }
        })
        const message_ids: Array<string> = []
        channel_messages = channel_messages?.filter((v, _i, _arr) => {
            if (message_ids.includes(v.id) === true) {
                return false
            } else {
                message_ids.push(v.id)
                return true
            }
        })

        if (channel_messages === undefined) {
            channel_messages = new Array()
        }

        this.channel_messages.set(channel_id, channel_messages.sort((a, b) => { return Number(BigInt(a.id) - BigInt(b.id)) }))
    }

    start() {
        if (this._started === false) {
            this.ws.connect()
            this.ws.emitter.on("HELLO", this.on_open, this)
            this._started = true
            this.ws.emitter.on('GUILD_CREATE', this.on_guild_create, this)
            this.ws.emitter.on("CLOSE", this.on_close, this)
            this.ws.emitter.on("MESSAGE_CREATE", this.on_message_create, this)
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
        channels?.forEach((v, _idx, _arr) => { this.channels.set(v.id, v) })
    }

    on_open() {
        this.ws?.identify()
        if (this.current_channel !== null) {
            this.fill_messages(this.current_channel)
        }
    }

    on_close() {
        // this follows our API principle:
        // Data shouldn't be cached after disconnection
        this.guilds = []
        this.guild_channels.clear()
        this.channels.clear()
        this.channel_messages.clear()
        this.guilds_map.clear()
    }

    on_message_create(message: ChannelMessage) {
        var channel_messages = this.channel_messages.get(message.channel_id)
        if (channel_messages !== undefined) {
            channel_messages.push(message)
        } else {
            channel_messages = new Array()
        }

        this.channel_messages.set(message.channel_id, channel_messages.sort((a, b) => { return Number(BigInt(a.id) - BigInt(b.id)) }))
    }
}

export const state = new State()
