import { useEffect, useState } from 'react'
import api from '../lib/api.js'

export default function ReviewList() {
  const [reviews, setReviews] = useState([])

  useEffect(() => {
    api.get('/reviews/').then((res) => setReviews(res.data.reviews || [])).catch(() => setReviews([]))
  }, [])

  return (
    <div>
      <h2 style={{ marginBottom: 16 }}>Reviews</h2>
      {reviews.map((r) => (
        <div className="card" key={r.id}>
          <p>Car: {r.car?.name}</p>
          <p>Rating: {r.rating}</p>
          <p>Comment: {r.comment}</p>
          {r.reply && <p>Vendor reply: {r.reply}</p>}
        </div>
      ))}
    </div>
  )
}