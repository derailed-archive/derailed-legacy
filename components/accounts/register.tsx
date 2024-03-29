import { FormEvent, useState } from 'react'
// @ts-ignore
import { Navigate, useNavigate } from 'react-router-dom'

const Login = () => {
    if (localStorage.getItem("token") !== null) {
        return <Navigate to="/channels/@self" />
    }
    const navigate = useNavigate()
    const [username, setUsername] = useState<string | null>(null)
    const [password, setPassword] = useState<string | null>(null)
    const [email, setEmail] = useState<string | null>(null)

    const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault()
        const API_URL: string = import.meta.env.VITE_API_URL
        const resp = await fetch(API_URL.concat("/register"), { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ 'username': username, 'password': password, 'email': email }) })

        const value = await resp.json()

        if ('detail' in value) {
            console.error(value)
            navigate("/error?code=failed_register")
        } else {
            localStorage.setItem('token', value.token)
            navigate("/")
        }
    }

    return (
        <div className="bg-login min-h-screen antialiased bg-cover bg-no-repeat flex flex-col justify-center h-screen">
            <div className='border border-dark bg-dark text-white text-center rounded-2xl max-w-lg m-auto shadow-2xl px-14 py-10'>
                <main className="max-w-2xl mx-auto p-3">
                    <section>
                        <div>
                            <h1 className="text-2xl font-semibold">
                                Welcome to Derailed!
                            </h1>
                            <h3 className="text-lg max-w-xs text-gray-500">
                                First time? We hope you enjoy your stay.
                            </h3>
                        </div>
                    </section>

                    <section className="mt-5">
                        <form className="flex flex-col gap-5" onSubmit={handleSubmit}>
                            <div>
                                <label className="block text-gray-500 text-left ml-12">Username</label>
                                <input type="text" id="username" className="bg-darker-dark rounded-full p-1 mt-1 px-5" required minLength={1} maxLength={32} onChange={(event) => {setUsername(event.target.value)}} />
                            </div>
                            <div>
                                <label className="block text-gray-500 text-left ml-12">Email</label>
                                <input type="email" id="email" className="bg-darker-dark rounded-full p-1 mt-1 px-5" required minLength={5} maxLength={82} onChange={(event) => {setEmail(event.target.value)}} />
                            </div>
                            <div>
                                <label className="block text-gray-500 text-left ml-12">Password</label>
                                <input type="password" id="password" className="bg-darker-dark rounded-full p-1 mt-1 px-5" required minLength={8} maxLength={82} onChange={(event) => {setPassword(event.target.value)}} />
                            </div>
                            <div className='flex gap-3 justify-center items-center'>
                                <button className="mt-5 rounded-2xl min-w-xl max-w-xl bg-verlp duration-700 py-2 hover:bg-darker-dark px-4" type="submit">Register</button>
                                <a href="/login" className="mt-5 rounded-2xl min-w-xl max-w-xl bg-verlp duration-700 py-2 hover:bg-darker-dark px-5">Log in</a>
                            </div>
                        </form>
                    </section>
                </main>
            </div>
            <a href="https://unsplash.com/@marcinjozwiak">
                <h4 className="text-verlp font-mono text-xs ml-2 mb-2">
                    Image by Marcin Jozwiak on Unsplash.
                </h4>
            </a>
        </div>
    )
}

export default Login;
