class HTTPClient {
    private _token: string | null
    private _base_url: string

    constructor(base_url: string) {
        this._token = localStorage.getItem("token")
        this._base_url = base_url
    }

    async request(route: string, method: string, data: object | null = null): Promise<object | string> {
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
}

