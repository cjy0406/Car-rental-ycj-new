import { useState } from 'react'
import api from '../lib/api.js'

export default function VendorWithdraw() {
  const [amount, setAmount] = useState('')
  const [message, setMessage] = useState('')

  const submit = async (e) => {
    e.preventDefault()
    try {
      await api.post('/withdrawals/', { amount })
      setMessage('Withdrawal request submitted')
    } catch (err) {
      setMessage('Failed to submit')
    }
  }

  return (
    <div className="card">
      <h2>Vendor Withdrawal</h2>
      <form onSubmit={submit}>
        <label>Amount</label>
        <input className="input" value={amount} onChange={(e) => setAmount(e.target.value)} />
        <button className="btn" style={{ marginTop: 12 }} type="submit">Submit</button>
      </form>
      {message && <p style={{ marginTop: 10 }}>{message}</p>}
    </div>
  )
}