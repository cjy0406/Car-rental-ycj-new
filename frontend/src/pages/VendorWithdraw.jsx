import { useState } from 'react'
import api from '../lib/api.js'

const statusColor = (status) => {
  switch (status) {
    case 'approved':
      return '#047857'
    case 'paid':
      return '#0f766e'
    case 'rejected':
      return '#b91c1c'
    default:
      return '#6b7280'
  }
}

export default function VendorWithdraw() {
  const [amount, setAmount] = useState('')
  const [message, setMessage] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [history, setHistory] = useState([])

  const submit = async (e) => {
    e.preventDefault()
    setSubmitting(true)
    setMessage('')
    try {
      const res = await api.post('/withdrawals/', { amount })
      const withdrawal = res.data.withdrawal || { amount, status: 'pending', requested_at: new Date().toISOString() }
      setHistory((prev) => [withdrawal, ...prev])
      setAmount('')
      setMessage('Withdrawal request submitted')
    } catch (err) {
      setMessage('Failed to submit')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div>
      <div className="card" style={{ marginBottom: 20 }}>
        <h2>Vendor Withdrawal</h2>
        <form onSubmit={submit}>
          <label>Amount</label>
          <input
            className="input"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            type="number"
            min="0"
            step="0.01"
          />
          <button className="btn" style={{ marginTop: 12 }} type="submit" disabled={submitting}>
            {submitting ? 'Submitting...' : 'Submit'}
          </button>
        </form>
        {message && <p style={{ marginTop: 10 }}>{message}</p>}
      </div>

      <div className="card">
        <h3>Recent withdrawal requests</h3>
        {history.length === 0 && <p>No local history yet. Submit a request to see it here.</p>}
        {history.map((item, index) => (
          <div key={item.id || index} style={{ marginBottom: 12 }}>
            <p>Amount: ${item.amount}</p>
            <p>
              Status: <strong style={{ color: statusColor(item.status) }}>{item.status}</strong>
            </p>
            {item.requested_at && <p>Requested at: {new Date(item.requested_at).toLocaleString()}</p>}
          </div>
        ))}
      </div>
    </div>
  )
}