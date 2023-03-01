import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'
import { createBrowserRouter, Navigate, RouterProvider } from 'react-router-dom'


const App = React.lazy(() => import('./App'))
const Logout = React.lazy(() => import('./Logout'))
const Login = React.lazy(() => import('@derailed/accounts/login'))
const Register = React.lazy(() => import('@derailed/accounts/register'))


const router = createBrowserRouter([
  {
    path: '/',
    element: <App />
  },
  {
    path: '/login',
    element: <Login />
  },
  {
    path: '/register',
    element: <Register />
  },
  {
    path: '/logout',
    element: <Logout />
  }
])


ReactDOM.createRoot(document.getElementById('thunder') as HTMLElement).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)
