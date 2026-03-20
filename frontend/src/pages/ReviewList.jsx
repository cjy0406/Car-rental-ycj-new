import { useEffect, useMemo, useState } from 'react'
import api from '../lib/api.js'

export default function ReviewList() {
  const [reviews, setReviews] = useState([])
  const [bookings, setBookings] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')
  const [reviewForm, setReviewForm] = useState({
    booking: '',
    rating: 5,
    comment: '',
  })
  const [replyInputs, setReplyInputs] = useState({})
  const [submittingId, setSubmittingId] = useState('')

  const loadData = async () => {
    setLoading(true)
    setError('')
    try {
      const [reviewsRes, bookingsRes] = await Promise.all([
        api.get('/reviews/'),
        api.get('/bookings/'),
      ])
      setReviews(reviewsRes.data.reviews || [])
      setBookings(bookingsRes.data.bookings || [])
    } catch (err) {
      setError('Failed to load reviews.')
      setReviews([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadData()
  }, [])

  const completedBookings = useMemo(
    () => bookings.filter((b) => b.status === 'completed'),
    [bookings]
  )

  const submitReview = async (e) => {
    e.preventDefault()
    setSubmittingId('create')
    setMessage('')
    try {
      await api.post('/reviews/create/', {
        booking: reviewForm.booking,
        rating: Number(reviewForm.rating),
        comment: reviewForm.comment,
      })
      setMessage('Review submitted.')
      setReviewForm({ booking: '', rating: 5, comment: '' })
      loadData()
    } catch (err) {
      setMessage('Failed to submit review. Ensure booking is completed.')
    } finally {
      setSubmittingId('')
    }
  }

  const submitReply = async (reviewId) => {
    setSubmittingId(reviewId)
    setMessage('')
    try {
      await api.post(`/reviews/${reviewId}/reply/`, {
        reply: replyInputs[reviewId] || '',
      })
      setMessage('Reply submitted.')
      loadData()
    } catch (err) {
      setMessage('Failed to submit reply.')
    } finally {
      setSubmittingId('')
    }
  }

  return (
    <div>
      <h2 style={{ marginBottom: 16 }}>Reviews</h2>

      <div className="card" style={{ marginBottom: 20 }}>
        <h3>Submit a review</h3>
        <form onSubmit={submitReview}>
          <label>Booking</label>
          <select
            className="input"
            value={reviewForm.booking}
            onChange={(e) => setReviewForm((prev) => ({ ...prev, booking: e.target.value }))}
          >
            <option value="">Select a completed booking</option>
            {completedBookings.map((booking) => (
              <option key={booking.id} value={booking.id}>
                {booking.car?.name} ({booking.start_date} → {booking.end_date})
              </option>
            ))}
          </select>
          <label style={{ marginTop: 12, display: 'block' }}>Rating</label>
          <input
            className="input"
            type="number"
            min="1"
            max="5"
            value={reviewForm.rating}
            onChange={(e) => setReviewForm((prev) => ({ ...prev, rating: e.target.value }))}
          />
          <label style={{ marginTop: 12, display: 'block' }}>Comment</label>
          <textarea
            className="input"
            rows="3"
            value={reviewForm.comment}
            onChange={(e) => setReviewForm((prev) => ({ ...prev, comment: e.target.value }))}
          />
          <button className="btn" type="submit" disabled={submittingId === 'create'}>
            {submittingId === 'create' ? 'Submitting...' : 'Submit review'}
          </button>
        </form>
      </div>

      {loading && <div className="card">Loading reviews...</div>}
      {error && <div className="card" style={{ color: 'crimson' }}>{error}</div>}
      {message && <div className="card">{message}</div>}
      {!loading && !error && reviews.length === 0 && (
        <div className="card">No reviews yet.</div>
      )}

      {reviews.map((r) => (
        <div className="card" key={r.id}>
          <p>Car: {r.car?.name}</p>
          <p>Rating: {r.rating}</p>
          <p>Comment: {r.comment}</p>
          {r.reply ? (
            <p>Vendor reply: {r.reply}</p>
          ) : (
            <div style={{ marginTop: 10 }}>
              <label>Reply (vendor only)</label>
              <input
                className="input"
                value={replyInputs[r.id] || ''}
                onChange={(e) =>
                  setReplyInputs((prev) => ({ ...prev, [r.id]: e.target.value }))
                }
              />
              <button
                className="btn"
                style={{ marginTop: 8 }}
                onClick={() => submitReply(r.id)}
                disabled={submittingId === r.id}
              >
                {submittingId === r.id ? 'Submitting...' : 'Submit reply'}
              </button>
            </div>
          )}
        </div>
      ))}
    </div>
  )
}