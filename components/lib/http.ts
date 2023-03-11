// @ts-ignore
const BASE_URL = import.meta.env.VITE_API_URL

class HTTPClient {
    private _token: string | null
    private _base_url: string

    constructor() {
        this._token = localStorage.getItem("token")
        this._base_url = BASE_URL
    }

    async request(route: string, method: string, data: object | null = null): Promise<object | string | Array<object>> {
        if (this._token !== null) {
            if (data !== null) {
                const r = await fetch(this._base_url.concat(route), { method: method, headers: { 'Content-Type': 'application/json', 'Authorization': this._token }, body: JSON.stringify(data) })
                return await r.json()
            } else {
                const r = await fetch(this._base_url.concat(route), { method: method, headers: { 'Content-Type': 'application/json', 'Authorization': this._token } })
                return await r.json()
            }
        }
        else {
            if (data !== null) {
                const r = await fetch(this._base_url.concat(route), { method: method, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) })
                return await r.json()
            } else {
                const r = await fetch(this._base_url.concat(route), { method: method, headers: { 'Content-Type': 'application/json' } })
                return await r.json()
            }
        }
    }

    async register(
        username: string,
        email: string,
        password: string
    ) {
        return await this.request('/register', 'POST', { 'username': username, 'email': email, 'password': password })
    }

    async get_guild(
        guild_id: string
    ) {
        return await this.request(`/guilds/${guild_id}`, 'GET')
    }

    async create_guild(name: string) {
        return await this.request('/guilds', 'POST', { 'name': name })
    }

    async send_message(content: string, channel_id: string) {
        return await this.request(`/channels/${channel_id}/messages`, 'POST', { 'content': content })
    }

    async get_messages(channel_id: string) {
        return await this.request(`/channels/${channel_id}/messages`, 'GET')
    }
}


export default HTTPClient
