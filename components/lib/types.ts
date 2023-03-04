export interface User {
    id: string,
    username: string,
    discriminator: string,
    email: string | undefined,
    flags: number,
    system: boolean,
    suspended: boolean
}

export interface Channel {
    id: string,
    type: number,
    name: string | null,
    last_message_id: string | null,
    parent_id: string | null,
    guild_id: string | null,
    position: number | null,
}

export interface ChannelMessage {
    id: string,
    author: User | null,
    content: string,
    channel_id: string,
    timestamp: string,
    edited_timestamp: string | null
}

export interface Guild {
    id: string,
    name: string,
    flags: number,
    owner_id: string,
    permissions: number
}
