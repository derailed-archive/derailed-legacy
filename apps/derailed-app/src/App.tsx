import { Navigate } from "react-router-dom"


function App() {
  let token = localStorage.getItem('token')

  if (token === null) {
    return <Navigate to="/login" />
  } else {
    return <Navigate to="/channels/@self" />
  }
}

export default App

