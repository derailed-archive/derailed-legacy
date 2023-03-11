import React, { Suspense } from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import Loading from './Loading'


const App = React.lazy(() => import('./App'))
const Logout = React.lazy(() => import('./Logout'))
const Open = React.lazy(() => import('./open'))
const Guild = React.lazy(() => import('./guild'))
const Channel = React.lazy(() => import('./channel'))
const Login = React.lazy(() => import('@derailed/accounts/login'))
const Register = React.lazy(() => import('@derailed/accounts/register'))


const router = createBrowserRouter([
  {
    path: '/',
    element: <Suspense fallback={<Loading />}><App /></Suspense>
  },
  {
    path: '/login',
    element: <Suspense fallback={<Loading />}><Login /></Suspense>
  },
  {
    path: '/register',
    element: <Suspense fallback={<Loading />}><Register /></Suspense>
  },
  {
    path: '/logout',
    element: <Suspense fallback={<Loading />}><Logout /></Suspense>
  },
  {
    path: '/channels/@self',
    element: <Suspense fallback={<Loading />}><Open /></Suspense>
  },
  {
    path: '/channels/:guild_id',
    element: <Suspense fallback={<Loading />}><Guild /></Suspense>
  },
  {
    path: '/channels/:guild_id/:channel_id',
    element: <Suspense fallback={<Loading />}><Channel /></Suspense>
  }
])


console.log("%cDerailed", "font-size: 48px;");
console.log("%cDO NOT COPY OR PASTE ANY PIECE OF CODE OR SCRIPTS HERE, IT MAY COMPROMISE YOUR ACCOUNT", "font-size: 16px;");


ReactDOM.createRoot(document.getElementById('thunder') as HTMLElement).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)
