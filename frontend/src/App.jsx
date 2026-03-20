import { Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout.jsx'
import Login from './pages/Login.jsx'
import CarList from './pages/CarList.jsx'
import CarDetail from './pages/CarDetail.jsx'
import BookingList from './pages/BookingList.jsx'
import ReviewList from './pages/ReviewList.jsx'
import VendorWithdraw from './pages/VendorWithdraw.jsx'
import AdminDashboard from './pages/AdminDashboard.jsx'

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Navigate to="/cars" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/cars" element={<CarList />} />
        <Route path="/cars/:carId" element={<CarDetail />} />
        <Route path="/bookings" element={<BookingList />} />
        <Route path="/reviews" element={<ReviewList />} />
        <Route path="/vendor/withdraw" element={<VendorWithdraw />} />
        <Route path="/admin" element={<AdminDashboard />} />
      </Route>
    </Routes>
  )
}