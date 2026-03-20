import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import api from '../lib/api.js'

export default function CarDetail() {
  const { carId } = useParams()
  const [car, setCar] = useState(null)

  useEffect(() => {
    api.get(`/cars/${carId}/`).then((res) => setCar(res.data.car)).catch(() => setCar(null))
  }, [carId])

  if (!car) return <div className="card">Car not found.</div>

  return (
    <div className="card">
      <h2>{car.name}</h2>
      <p>{car.description}</p>
      <p>Price per day: ${car.price_per_day}</p>
    </div>
  )
}