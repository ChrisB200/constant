import SignUp from "./pages/SignUpPage"
import Login from "./pages/LoginPage"
import Home from "./pages/HomePage"
import ProtectedRoutes from "./utils/protectedRoutes"
import { Routes, Route } from 'react-router-dom'

function App() {
  return (
    <Routes>
      <Route path="/signup" element={<SignUp/>} />
      <Route path="/login" element={<Login/>} />

      <Route element={<ProtectedRoutes/>}>
        <Route path="/" element={<Home />}/>
      </Route>
    </Routes>
  )
}

export default App
