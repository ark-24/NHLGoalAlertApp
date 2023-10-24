import React, { useEffect } from 'react'

const Index = () => {
  useEffect(()=> {
    fetch('http://localhost:8080').then(response => response.json()).then(data => console.log(data))
  })
  return (
    <div>index</div>
  )
}

export default Index