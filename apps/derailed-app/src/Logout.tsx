import { Navigate } from "react-router-dom"


function Logout() {
  	localStorage.removeItem('token')

	return <Navigate to="/login" />
}

export default Logout

