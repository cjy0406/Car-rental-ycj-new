import { useEffect, useState } from 'react'
import api from '../lib/api.js'

const statusColor = (status) => {
  switch (status) {
    case 'confirmed':
      return '#047857'
    case 'completed':
      return '#0f766e'
    case 'cancelled':
      return '#b91c1c'
    default:
      return '#6b7280'
  }
}

export default function BookingList() {
  const [bookings, setBookings] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')
  const [returnNotes, setReturnNotes] = useState({})
  const [submittingId, setSubmittingId] = useState('')

  const fetchBookings = async () => {
    setLoading(true)
    setError('')
    try {
      const res = await api.get('/bookings/')
      setBookings(res.data.bookings || [])
    } catch (err) {
      setError('Failed to load bookings.')
      setBookings([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchBookings()
  }, [])

  const confirmReturn = async (bookingId) => {
    setSubmittingId(bookingId)
    setMessage('')
    try {
      await api.post(`/bookings/${bookingId}/return/`, {
        return_notes: returnNotes[bookingId] || '',
      })
      setMessage('Return confirmed successfully.')
      fetchBookings()
    } catch (err) {
      setMessage('Return confirmation failed.')
    } finally {
      setSubmittingId('')
    }
  }

  const confirmPayment = async (bookingId) => {
    setSubmittingId(bookingId)
    setMessage('')
    try {
      const res = await api.post('/payments/confirm/', { booking_id: bookingId })
      setMessage(res.data.detail || 'Payment confirmed (sandbox).')
      fetchBookings()
    } catch (err) {
      setMessage('Payment confirmation failed.')
    } finally {
      setSubmittingId('')
    }
  }

  return (
    <div>
      <h2 style={{ marginBottom: 16 }}>My Bookings</h2>
      {loading && <div className="card">Loading bookings...</div>}
      {error && <div className="card" style={{ color: 'crimson' }}>{error}</div>}
      {message && <div className="card">{message}</div>}
      {!loading && !error && bookings.length === 0 && (
        <div className="card">No bookings yet.</div>
      )}

      {bookings.map((b) => (
        <div className="card" key={b.id}>
          <h3>{b.car?.name}</h3>
          <p>Dates: {b.start_date} → {b.end_date}</p>
          <p>
            Status: <strong style={{ color: statusColor(b.status) }}>{b.status}</strong>
          </p>
          <p>Admin status: {b.admin_status}</p>
          <p>Total: ${b.total_price}</p>

          {b.status === 'pending' && (
            <button
              className="btn"
              onClick={() => confirmPayment(b.id)}
              disabled={submittingId === b.id}
            >
              {submittingId === b.id ? 'Processing...' : 'Confirm payment'}
            </button>
          )}

          {b.status === 'confirmed' && (
            <div style={{ marginTop: 12 }}>
              <label>Return notes</label>
              <input
                className="input"
                value={returnNotes[b.id] || ''}
                onChange={(e) =>
                  setReturnNotes((prev) => ({ ...prev, [b.id]: e.target.value }))
                }
              />
              <button
                className="btn"
                style={{ marginTop: 8 }}
                onClick={() => confirmReturn(b.id)}
                disabled={submittingId === b.id}
              >
                {submittingId === b.id ? 'Submitting...' : 'Confirm return'}
              </button>
            </div>
          )}
        </div>
      ))}
    </div>
  )
}