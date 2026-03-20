import { useEffect, useState } from 'react'
import api from '../lib/api.js'

export default function AdminDashboard() {
  const [summary, setSummary] = useState(null)

  useEffect(() => {
    api.get('/analytics/summary/').then((res) => setSummary(res.data)).catch(() => setSummary(null))
  }, [])

  if (!summary) return <div className="card">No data.</div>

  return (
    <div>
      <div className="card">
        <h2>Admin Summary</h2>
        <p>Total vendors: {summary.totals?.total_vendors}</p>
        <p>Total bookings: {summary.totals?.total_bookings}</p>
        <p>Total revenue: ${summary.totals?.total_revenue}</p>
      </div>
      <div className="card">
        <h3>Recent bookings</h3>
        {summary.recent_bookings?.map((b) => (
          <div key={b.id} style={{ marginBottom: 8 }}>
            {b.car} - {b.customer} - ${b.total_price} - {b.status}
          </div>
        ))}
      </div>
    </div>
  )
}