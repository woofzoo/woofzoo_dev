'use client'

import { useEffect } from 'react'

const Page = () => {
  useEffect(() => {
    document.title = "My Client Page"
  }, [])

  return (
    <div className='text-amber-400'>
      <p>page</p>
    </div>
  )
}

export default Page
