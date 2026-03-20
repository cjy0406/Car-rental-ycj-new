import { Outlet, Link } from 'react-router-dom'

export default function Layout() {
  return (
    <div>
      <nav className="nav">
        <Link to="/cars">Cars</Link>
        <Link to="/bookings">Bookings</Link>
        <Link to="/reviews">Reviews</Link>
        <Link to="/vendor/withdraw">Vendor</Link>
        <Link to="/admin">Admin</Link>
        <Link to="/login">Login</Link>
      </nav>
      <div className="container">
        <Outlet />
      </div>
    </div>
  )
}