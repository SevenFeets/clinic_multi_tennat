import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

/**
 * Entry Point - main.jsx
 * 
 * This is where React gets mounted to the DOM.
 * It renders the App component into the root div in index.html
 * 
 * StrictMode helps catch bugs during development
 */

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
