import { FormEvent } from 'react'
import { Navigate } from 'react-router-dom'

const Login = () => {
    if (localStorage.getItem("token") !== null) {
        return <Navigate to="/channels/@self" />
    }

    const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
        // TODO: register to API
        event.preventDefault()
        console.log(event)
    }

    return (
        // TODO: max lengths on inputs
        <div className="bg-login min-h-screen antialiased bg-cover bg-no-repeat flex flex-col justify-center h-screen">
            <div className='border border-dark bg-dark text-white text-center rounded-2xl max-w-lg m-auto shadow-2xl px-14 py-10'>
                <main className="max-w-2xl mx-auto md:p-4">
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
                        <form className="flex flex-col" onSubmit={handleSubmit}>
                            <div className="pt-3">
                                <label className="block text-gray-500 text-left ml-1">Username</label>
                                <input type="text" id="username" className="bg-darker-dark rounded-full p-1 mt-1 px-3" />
                            </div>
                            <div className="pt-3">
                                <label className="block text-gray-500 text-left ml-1">Email</label>
                                <input type="text" id="email" className="bg-darker-dark rounded-full p-1 mt-1 px-3" />
                            </div>
                            <div className="pt-3">
                                <label className="block text-gray-500 text-left ml-1">Password</label>
                                <input type="text" id="password" className="bg-darker-dark rounded-full p-1 mt-1 px-3" />
                            </div>
                            <button className="mt-10 rounded-full bg-verlp duration-700 py-2 hover:bg-darker-dark" type="submit">Log in</button>
                        </form>
                    </section>
                </main>
            </div>
            <a href="https://unsplash.com/@marcinjozwiak">
                <h4 className="text-verlp font-mono text-xs ml-2 mb-2">
                    Made by Marcin Jozwiak on Unsplash.
                </h4>
            </a>
        </div>
    )
}

export default Login;
