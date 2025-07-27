// page.tsx
'use client'
import { useEffect } from 'react'

const page = () => {
  useEffect(() => {
    document.title = "My Client Page"
  }, [])

  return (
    <div>page</div>
  )
}

export default page