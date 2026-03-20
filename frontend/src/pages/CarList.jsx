import { useEffect, useState } from 'react'
import api from '../lib/api.js'

export default function CarList() {
  const [cars, setCars] = useState([])

  useEffect(() => {
    api.get('/cars/').then((res) => setCars(res.data.cars || [])).catch(() => setCars([]))
  }, [])

  return (
    <div>
      <h2 style={{ marginBottom: 16 }}>Available Cars</h2>
      <div className="grid">
        {cars.map((car) => (
          <div className="card" key={car.id}>
            <h3>{car.name}</h3>
            <p>{car.description}</p>
            <p>Type: {car.car_type}</p>
            <p>${car.price_per_day} / day</p>
          </div>
        ))}
      </div>
    </div>
  )
}