import { useEffect, useState } from 'react'
import api from '../lib/api.js'

export default function BookingList() {
  const [bookings, setBookings] = useState([])

  useEffect(() => {
    api.get('/bookings/').then((res) => setBookings(res.data.bookings || [])).catch(() => setBookings([]))
  }, [])

  return (
    <div>
      <h2 style={{ marginBottom: 16 }}>My Bookings</h2>
      {bookings.map((b) => (
        <div className="card" key={b.id}>
          <p>Car: {b.car?.name}</p>
          <p>Status: {b.status}</p>
          <p>Total: ${b.total_price}</p>
        </div>
      ))}
    </div>
  )
}