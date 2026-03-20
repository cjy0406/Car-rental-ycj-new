import { useEffect, useState } from 'react'
import api from '../lib/api.js'

const actionOptions = [
  { value: 'approve', label: 'Approve' },
  { value: 'reject', label: 'Reject' },
]

const withdrawalOptions = [
  { value: 'approve', label: 'Approve' },
  { value: 'paid', label: 'Mark Paid' },
  { value: 'reject', label: 'Reject' },
]

export default function AdminDashboard() {
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(true)
  const [message, setMessage] = useState('')
  const [bookingAction, setBookingAction] = useState({ id: '', action: 'approve' })
  const [carId, setCarId] = useState('')
  const [withdrawalAction, setWithdrawalAction] = useState({ id: '', action: 'approve', notes: '' })
  const [submitting, setSubmitting] = useState(false)

  const loadSummary = async () => {
    setLoading(true)
    try {
      const res = await api.get('/analytics/summary/')
      setSummary(res.data)
    } catch (err) {
      setSummary(null)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadSummary()
  }, [])

  const submitBookingAction = async () => {
    if (!bookingAction.id) return
    setSubmitting(true)
    setMessage('')
    try {
      await api.post(`/admin/bookings/${bookingAction.id}/approval/`, { action: bookingAction.action })
      setMessage('Booking updated.')
      setBookingAction((prev) => ({ ...prev, id: '' }))
      loadSummary()
    } catch (err) {
      setMessage('Failed to update booking.')
    } finally {
      setSubmitting(false)
    }
  }

  const submitCarApproval = async () => {
    if (!carId) return
    setSubmitting(true)
    setMessage('')
    try {
      await api.post(`/admin/cars/${carId}/approval/`)
      setMessage('Car approved.')
      setCarId('')
      loadSummary()
    } catch (err) {
      setMessage('Failed to approve car.')
    } finally {
      setSubmitting(false)
    }
  }

  const submitWithdrawalAction = async () => {
    if (!withdrawalAction.id) return
    setSubmitting(true)
    setMessage('')
    try {
      await api.post(`/admin/withdrawals/${withdrawalAction.id}/`, {
        action: withdrawalAction.action,
        notes: withdrawalAction.notes,
      })
      setMessage('Withdrawal updated.')
      setWithdrawalAction((prev) => ({ ...prev, id: '', notes: '' }))
      loadSummary()
    } catch (err) {
      setMessage('Failed to update withdrawal.')
    } finally {
      setSubmitting(false)
    }
  }

  const stats = summary?.summary

  return (
    <div>
      <div className="card" style={{ marginBottom: 20 }}>
        <h2>Admin Summary</h2>
        {loading && <p>Loading summary...</p>}
        {!loading && !stats && <p>No data.</p>}
        {stats && (
          <div>
            <p>Total cars: {stats.total_cars}</p>
            <p>Total bookings: {stats.total_bookings}</p>
            <p>Pending bookings: {stats.pending_bookings}</p>
            <p>Total revenue: ${stats.revenue}</p>
          </div>
        )}
      </div>

      <div className="card" style={{ marginBottom: 20 }}>
        <h3>Booking approval</h3>
        <label>Booking ID</label>
        <input
          className="input"
          value={bookingAction.id}
          onChange={(e) => setBookingAction((prev) => ({ ...prev, id: e.target.value }))}
        />
        <label style={{ marginTop: 12, display: 'block' }}>Action</label>
        <select
          className="input"
          value={bookingAction.action}
          onChange={(e) => setBookingAction((prev) => ({ ...prev, action: e.target.value }))}
        >
          {actionOptions.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
        <button className="btn" style={{ marginTop: 12 }} onClick={submitBookingAction} disabled={submitting}>
          {submitting ? 'Submitting...' : 'Submit'}
        </button>
      </div>

      <div className="card" style={{ marginBottom: 20 }}>
        <h3>Car approval</h3>
        <label>Car ID</label>
        <input
          className="input"
          value={carId}
          onChange={(e) => setCarId(e.target.value)}
        />
        <button className="btn" style={{ marginTop: 12 }} onClick={submitCarApproval} disabled={submitting}>
          {submitting ? 'Submitting...' : 'Approve car'}
        </button>
      </div>

      <div className="card">
        <h3>Withdrawal approval</h3>
        <label>Withdrawal ID</label>
        <input
          className="input"
          value={withdrawalAction.id}
          onChange={(e) => setWithdrawalAction((prev) => ({ ...prev, id: e.target.value }))}
        />
        <label style={{ marginTop: 12, display: 'block' }}>Action</label>
        <select
          className="input"
          value={withdrawalAction.action}
          onChange={(e) => setWithdrawalAction((prev) => ({ ...prev, action: e.target.value }))}
        >
          {withdrawalOptions.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
        <label style={{ marginTop: 12, display: 'block' }}>Notes</label>
        <input
          className="input"
          value={withdrawalAction.notes}
          onChange={(e) => setWithdrawalAction((prev) => ({ ...prev, notes: e.target.value }))}
        />
        <button className="btn" style={{ marginTop: 12 }} onClick={submitWithdrawalAction} disabled={submitting}>
          {submitting ? 'Submitting...' : 'Submit'}
        </button>
      </div>

      {message && <div className="card" style={{ marginTop: 16 }}>{message}</div>}
    </div>
  )
}