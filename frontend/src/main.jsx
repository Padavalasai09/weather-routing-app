import React from 'react'
import ReactDOM from 'react-dom/client'
import { CssBaseline, ThemeProvider, createTheme } from '@mui/material'
import App from './App'
import './styles.css'

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#7dd3fc',
    },
    secondary: {
      main: '#a78bfa',
    },
    background: {
      default: '#07131d',
      paper: '#102537',
    },
  },
  typography: {
    fontFamily: 'Inter, system-ui, sans-serif',
  },
})

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <App />
    </ThemeProvider>
  </React.StrictMode>,
)
