import { useState } from 'react'
import './App.css'

function App() {
  const [filePath, setFilePath] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    // console.log("HandleSubmit triggered!")
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const formData = new FormData()
      formData.append('file_path', filePath)
      const res = await fetch('http://localhost:8000/submit-file-path/', {
        method: 'POST',
        body: formData,
      })
      // console.log('Raw response:', res)
      // if (!res.ok) throw new Error('Request failed')
      const text = await res.text()
      // console.log('Response text:', text)
      let data
      try {
        data = JSON.parse(text)
      } catch (jsonErr) {
        setError('Response is not valid JSON: ' + text)
        return
      }
      if (!res.ok) {
        setError(data.detail || JSON.stringify(data))
        return
      }
      setResult(data)
    } catch (err) {
      setError('Failed to process file. Please check the backend and file path.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h1>AutoFix-AI</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter Python file path"
          value={filePath}
          onChange={e => setFilePath(e.target.value)}
          style={{ width: '350px' }}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Processing...' : 'Submit'}
        </button>
      </form>
      {error && <div style={{ color: 'red', marginTop: '1em' }}>{error}</div>}
      {result && (
        <div style={{ textAlign: 'left', marginTop: '2em', background: '#222', color: '#fff', padding: '1em', borderRadius: '8px' }}>
          <h2>Result</h2>
          <pre style={{ whiteSpace: 'pre-wrap' }}>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  )
}

export default App