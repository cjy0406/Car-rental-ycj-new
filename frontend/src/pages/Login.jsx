import { useState } from 'react'
import api from '../lib/api.js'

export default function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      const { data } = await api.post('/token/', { username, password })
      localStorage.setItem('token', data.access)
      alert('Login success')
    } catch (err) {
      setError('Login failed')
    }
  }

  return (
    <div className="card">
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <label>Username</label>
        <input className="input" value={username} onChange={(e) => setUsername(e.target.value)} />
        <label style={{ marginTop: 12, display: 'block' }}>Password</label>
        <input className="input" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        {error && <p style={{ color: 'crimson', marginTop: 8 }}>{error}</p>}
        <button className="btn" style={{ marginTop: 12 }} type="submit">Login</button>
      </form>
    </div>
  )
}