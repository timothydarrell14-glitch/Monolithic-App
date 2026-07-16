import { useEffect } from 'react'
import './App.css'

const BASE_URL = 'http://localhost:5000'

function App() {

  const fetchBooks = async () => {
    try {
      const response = await fetch(`${BASE_URL}/books`)

      if (!response.ok) {
        throw new Error('Network response was not ok')
      }

      const data = await response.json()
      console.log('Fetched books:', data)

    } catch (error) {
      console.error('Error fetching books:', error)
    }
  }

  useEffect(() => {
    fetchBooks()
  }, [])

  return (
    <>
      <div>Welcome to My Book APP</div>
    </>
  )
}

export default App
