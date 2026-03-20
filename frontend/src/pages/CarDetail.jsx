import { useEffect, useMemo, useState } from 'react'
import { useParams } from 'react-router-dom'
import api from '../lib/api.js'

const todayIso = () => new Date().toISOString().slice(0, 10)

export default function CarDetail() {
  const { carId } = useParams()
  const [car, setCar] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [form, setForm] = useState({
    start_date: todayIso(),
    end_date: todayIso(),
    return_notes: '',
  })
  const [submitting, setSubmitting] = useState(false)
  const [message, setMessage] = useState('')

  useEffect(() => {
    let active = true
    setLoading(true)
    api
      .get(`/cars/${carId}/`)
      .then((res) => {
        if (!active) return
        setCar(res.data.car)
        setError('')
      })
      .catch(() => {
        if (!active) return
        setCar(null)
        setError('Car not found.')
      })
      .finally(() => {
        if (active) setLoading(false)
      })

    return () => {
      active = false
    }
  }, [carId])

  const days = useMemo(() => {
    const start = new Date(form.start_date)
    const end = new Date(form.end_date)
    const diff = (end - start) / (1000 * 60 * 60 * 24)
    return Number.isFinite(diff) ? Math.max(1, Math.ceil(diff)) : 1
  }, [form.start_date, form.end_date])

  const totalPrice = useMemo(() => {
    if (!car) return 0
    return days * Number(car.price_per_day || 0)
  }, [car, days])

  const submitBooking = async (e) => {
    e.preventDefault()
    setSubmitting(true)
    setMessage('')
    try {
      const res = await api.post('/bookings/create/', {
        car: carId,
        start_date: form.start_date,
        end_date: form.end_date,
      })
      setMessage(`Booking created: ${res.data.booking?.id || ''}`)
    } catch (err) {
      setMessage('Failed to create booking. Check your dates and try again.')
    } finally {
      setSubmitting(false)
    }
  }

  const confirmPayment = async () => {
    setSubmitting(true)
    setMessage('')
    try {
      const res = await api.post('/payments/confirm/', { booking_id: carId })
      setMessage(res.data.detail || 'Payment confirmed (sandbox).')
    } catch (err) {
      setMessage('Payment confirmation failed.')
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) return <div className="card">Loading car...</div>
  if (error) return <div className="card" style={{ color: 'crimson' }}>{error}</div>
  if (!car) return <div className="card">Car not found.</div>

  return (
    <div className="grid" style={{ alignItems: 'start' }}>
      <div className="card">
        <h2>{car.name}</h2>
        <p>{car.description}</p>
        <p>Type: {car.car_type}</p>
        <p>Model year: {car.model_year}</p>
        <p>Price per day: ${car.price_per_day}</p>
      </div>
      <div className="card">
        <h3>Book this car</h3>
        <form onSubmit={submitBooking}>
          <label>Start date</label>
          <input
            className="input"
            type="date"
            value={form.start_date}
            min={todayIso()}
            onChange={(e) => setForm((prev) => ({ ...prev, start_date: e.target.value }))}
          />
          <label style={{ marginTop: 12, display: 'block' }}>End date</label>
          <input
            className="input"
            type="date"
            value={form.end_date}
            min={form.start_date}
            onChange={(e) => setForm((prev) => ({ ...prev, end_date: e.target.value }))}
          />
          <p style={{ marginTop: 12 }}>Estimated days: {days}</p>
          <p>Total: ${totalPrice.toFixed(2)}</p>
          <button className="btn" type="submit" disabled={submitting}>
            {submitting ? 'Submitting...' : 'Create booking'}
          </button>
          <button className="btn secondary" type="button" disabled={submitting} style={{ marginLeft: 8 }} onClick={confirmPayment}>
            Confirm payment (sandbox)
          </button>
        </form>
        {message && <p style={{ marginTop: 12 }}>{message}</p>}
      </div>
    </div>
  )
}