import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../lib/api.js'

const carTypeOptions = [
  { value: '', label: 'All types' },
  { value: 'sedan', label: 'Sedan' },
  { value: 'suv', label: 'SUV' },
  { value: 'hatchback', label: 'Hatchback' },
  { value: 'convertible', label: 'Convertible' },
  { value: 'van', label: 'Van' },
  { value: 'truck', label: 'Truck' },
  { value: 'other', label: 'Other' },
]

export default function CarList() {
  const [cars, setCars] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [filters, setFilters] = useState({
    search: '',
    type: '',
    min_price: '',
    max_price: '',
  })

  const queryParams = useMemo(() => {
    const params = {}
    if (filters.search) params.search = filters.search
    if (filters.type) params.type = filters.type
    if (filters.min_price) params.min_price = filters.min_price
    if (filters.max_price) params.max_price = filters.max_price
    return params
  }, [filters])

  const fetchCars = async () => {
    setLoading(true)
    setError('')
    try {
      const res = await api.get('/cars/', { params: queryParams })
      setCars(res.data.cars || [])
    } catch (err) {
      setError('Failed to load cars. Please try again.')
      setCars([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchCars()
  }, [])

  const onSubmit = (e) => {
    e.preventDefault()
    fetchCars()
  }

  return (
    <div>
      <div className="card" style={{ marginBottom: 20 }}>
        <h2 style={{ marginBottom: 12 }}>Find a car</h2>
        <form className="grid" onSubmit={onSubmit}>
          <div>
            <label>Search</label>
            <input
              className="input"
              value={filters.search}
              onChange={(e) => setFilters((prev) => ({ ...prev, search: e.target.value }))}
              placeholder="Search by name or description"
            />
          </div>
          <div>
            <label>Type</label>
            <select
              className="input"
              value={filters.type}
              onChange={(e) => setFilters((prev) => ({ ...prev, type: e.target.value }))}
            >
              {carTypeOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label>Min price</label>
            <input
              className="input"
              type="number"
              min="0"
              value={filters.min_price}
              onChange={(e) => setFilters((prev) => ({ ...prev, min_price: e.target.value }))}
            />
          </div>
          <div>
            <label>Max price</label>
            <input
              className="input"
              type="number"
              min="0"
              value={filters.max_price}
              onChange={(e) => setFilters((prev) => ({ ...prev, max_price: e.target.value }))}
            />
          </div>
          <div style={{ display: 'flex', alignItems: 'flex-end', gap: 8 }}>
            <button className="btn" type="submit">Apply</button>
            <button
              className="btn secondary"
              type="button"
              onClick={() => {
                setFilters({ search: '', type: '', min_price: '', max_price: '' })
                setTimeout(fetchCars, 0)
              }}
            >
              Reset
            </button>
          </div>
        </form>
      </div>

      <h2 style={{ marginBottom: 16 }}>Available Cars</h2>
      {loading && <div className="card">Loading cars...</div>}
      {error && <div className="card" style={{ color: 'crimson' }}>{error}</div>}
      {!loading && !error && cars.length === 0 && (
        <div className="card">No cars found with current filters.</div>
      )}
      <div className="grid">
        {cars.map((car) => (
          <div className="card" key={car.id}>
            <h3>{car.name}</h3>
            <p>{car.description}</p>
            <p>Type: {car.car_type}</p>
            <p>${car.price_per_day} / day</p>
            <Link className="btn" to={`/cars/${car.id}`}> 
              View details
            </Link>
          </div>
        ))}
      </div>
    </div>
  )
}