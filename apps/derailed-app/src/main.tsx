import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'


const App = React.lazy(() => import('./App'))


const router = createBrowserRouter([
  {
    path: '/',
    element: <App />
  }
])


ReactDOM.createRoot(document.getElementById('thunder') as HTMLElement).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)
