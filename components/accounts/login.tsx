import { FormEvent } from 'react'
// @ts-ignore
import { Navigate, useNavigate } from 'react-router-dom'
import { useState } from 'react'

const Login = () => {
    if (localStorage.getItem("token") !== null) {
        return <Navigate to="/channels/@self" />
    }
    const navigate = useNavigate()
    const [password, setPassword] = useState<string | null>(null)
    const [email, setEmail] = useState<string | null>(null)

    const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault()
        const API_URL: string = import.meta.env.VITE_API_URL
        const resp = await fetch(API_URL.concat("/login"), { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ 'password': password, 'email': email }) })

        const value = await resp.json()

        if ('detail' in value) {
            console.error(value)
            navigate("/error?code=failed_login")
        } else {
            localStorage.setItem('token', value.token)
            navigate("/")
        }
    }

    return (
        <div className="bg-login min-h-screen antialiased bg-cover bg-no-repeat flex flex-col justify-center h-screen">
            <div className='border border-dark bg-dark text-white text-center rounded-2xl max-w-lg m-auto shadow-2xl px-14 py-10'>
                <main className="max-w-2xl mx-auto p-6">
                    <section>
                        <div>
                            <h1 className="text-2xl font-semibold">
                                Welcome back!
                            </h1>
                            <h3 className="text-lg text-gray-500">
                                Excited to return? Let's go!
                            </h3>
                        </div>
                    </section>

                    <section className="mt-10">
                        <form className="flex flex-col max-w-xl" onSubmit={handleSubmit}>
                            <div className="pt-3">
                                <label className="block text-gray-500 text-left ml-1">Email</label>
                                <input type="email" id="email" className="bg-darker-dark rounded-full p-1 mt-1 px-3" required minLength={5} maxLength={82} onChange={(event) => {setEmail(event.target.value)}} />
                            </div>
                            <div className="pt-3">
                                <label className="block text-gray-500 text-left ml-1">Password</label>
                                <input type="password" id="password" className="bg-darker-dark rounded-full p-1 mt-1 px-3" required minLength={8} maxLength={82} onChange={(event) => {setPassword(event.target.value)}} />
                            </div>
                            <div className='flex gap-3 justify-center items-center'>
                                <button className="mt-10 rounded-2xl min-w-xl max-w-xl bg-verlp duration-700 py-2 hover:bg-darker-dark px-5" type="submit">Log in</button>
                                <a href="/register" className="mt-10 rounded-2xl min-w-xl max-w-xl bg-verlp duration-700 py-2 hover:bg-darker-dark px-4">Register</a>
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
