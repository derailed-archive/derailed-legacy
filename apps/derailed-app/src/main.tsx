// @ts-nocheck
import React, { Suspense } from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import Loading from './loading'


const App = React.lazy(() => import('./app'))
const Logout = React.lazy(() => import('./logout'))
const Open = React.lazy(() => import('./open'))
const Login = React.lazy(() => import('@derailed/accounts/login'))
const Register = React.lazy(() => import('@derailed/accounts/register'))
import Message from '@derailed/channels/message'
import TestWS from './test_ws'


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
    path: '/message',
    element: <Message author_name="VincentRPS" author_id="1234567890" timestamp="2023-03-03T11:21:38.492Z" content="Derailed is awesome!" />
  },
  {
    path: '/test-ws',
    element: <TestWS />
  },
  {
    path: '/channels/@self',
    element: <Suspense fallback={<Loading />}><Open /></Suspense>
  }
])


console.log("%cDerailed", "font-size: 48px;");
console.log("%cDO NOT COPY OR PASTE ANY PIECE OF CODE OR SCRIPTS HERE, IT MAY COMPROMISE YOUR ACCOUNT", "font-size: 16px;");


ReactDOM.createRoot(document.getElementById('thunder') as HTMLElement).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)
