import React, { Suspense } from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import Loading from './Loading'


const App = React.lazy(() => import('./App'))
const Logout = React.lazy(() => import('./Logout'))
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
  }
])


ReactDOM.createRoot(document.getElementById('thunder') as HTMLElement).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)
