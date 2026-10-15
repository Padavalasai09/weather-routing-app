import { useMemo, useState } from 'react'
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  Divider,
  Grid,
  LinearProgress,
  MenuItem,
  Stack,
  TextField,
  Typography,
} from '@mui/material'
import axios from 'axios'

const cityOptions = ['Seattle', 'San Francisco', 'Denver', 'Chicago', 'Austin', 'Miami', 'New York']

const formatStatus = (status) => {
  if (status === 'Low risk') return 'success'
  if (status === 'Moderate risk') return 'warning'
  return 'error'
}

export default function App() {
  const [form, setForm] = useState({
    origin: 'Seattle',
    destination: 'Austin',
    departure_date: '2026-10-15',
    preferred_temperature_c: 22,
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [result, setResult] = useState(null)

  const metricsSummary = useMemo(() => {
    if (!result?.best_route?.score) return null
    return {
      score: result.best_route.score,
      bestName: result.best_route.name,
      summary: result.summary,
    }
  }, [result])

  const submitPlan = async () => {
    setLoading(true)
    setError('')

    try {
      const response = await axios.post('http://localhost:8000/api/routes/plan/', form)
      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.error || 'Unable to generate route recommendations right now.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto', p: { xs: 2, md: 4 } }}>
      <Stack spacing={4}>
        <Box>
          <Chip label="Weather routing assistant" color="primary" sx={{ mb: 2 }} />
          <Typography variant="h3" fontWeight={700}>Plan the cleanest route</Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mt: 1 }}>
            Rank travel options using weather comfort, rainfall risk, and wind exposure before departure.
          </Typography>
        </Box>

        <Card>
          <CardContent>
            <Grid container spacing={2} alignItems="center">
              <Grid item xs={12} md={3}>
                <TextField
                  select
                  fullWidth
                  label="Origin"
                  value={form.origin}
                  onChange={(event) => setForm((prev) => ({ ...prev, origin: event.target.value }))}
                >
                  {cityOptions.map((city) => (
                    <MenuItem key={city} value={city}>{city}</MenuItem>
                  ))}
                </TextField>
              </Grid>
              <Grid item xs={12} md={3}>
                <TextField
                  select
                  fullWidth
                  label="Destination"
                  value={form.destination}
                  onChange={(event) => setForm((prev) => ({ ...prev, destination: event.target.value }))}
                >
                  {cityOptions.map((city) => (
                    <MenuItem key={city} value={city}>{city}</MenuItem>
                  ))}
                </TextField>
              </Grid>
              <Grid item xs={12} md={3}>
                <TextField
                  fullWidth
                  label="Departure date"
                  type="date"
                  value={form.departure_date}
                  onChange={(event) => setForm((prev) => ({ ...prev, departure_date: event.target.value }))}
                  InputLabelProps={{ shrink: true }}
                />
              </Grid>
              <Grid item xs={12} md={3}>
                <TextField
                  fullWidth
                  label="Target temp °C"
                  type="number"
                  value={form.preferred_temperature_c}
                  onChange={(event) => setForm((prev) => ({ ...prev, preferred_temperature_c: Number(event.target.value) }))}
                />
              </Grid>
            </Grid>

            <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
              <Button variant="contained" size="large" onClick={submitPlan} disabled={loading}>
                {loading ? <CircularProgress size={20} /> : 'Generate route'}
              </Button>
            </Box>
          </CardContent>
        </Card>

        {error ? <Alert severity="error">{error}</Alert> : null}

        {metricsSummary ? (
          <Card>
            <CardContent>
              <Typography variant="overline" color="text.secondary">Recommended route</Typography>
              <Typography variant="h4" fontWeight={700}>{metricsSummary.bestName}</Typography>
              <Typography variant="body1" sx={{ mt: 1 }}>{metricsSummary.summary}</Typography>
              <Box sx={{ mt: 3 }}>
                <Typography variant="subtitle2" color="text.secondary">Comfort score</Typography>
                <LinearProgress
                  className="route-score"
                  variant="determinate"
                  value={metricsSummary.score}
                  sx={{ height: 12, borderRadius: 999, mt: 1, backgroundColor: 'rgba(125,211,252,0.15)' }}
                />
                <Typography variant="h5" sx={{ mt: 1, fontWeight: 700 }}>
                  {metricsSummary.score}/100
                </Typography>
              </Box>
            </CardContent>
          </Card>
        ) : null}

        {result?.route_options?.length ? (
          <Grid container spacing={2}>
            {result.route_options.map((route) => (
              <Grid item xs={12} md={4} key={route.id}>
                <Card sx={{ height: '100%' }}>
                  <CardContent>
                    <Stack spacing={2}>
                      <Box display="flex" justifyContent="space-between" alignItems="center">
                        <Typography variant="h6">{route.name}</Typography>
                        <Chip label={route.status} color={formatStatus(route.status)} size="small" />
                      </Box>

                      <Box>
                        <Typography variant="overline" color="text.secondary">Route score</Typography>
                        <Typography variant="h4" fontWeight={700}>{route.score}/100</Typography>
                      </Box>

                      <Divider />

                      <Stack spacing={1.2}>
                        {route.segments.map((segment) => (
                          <Box key={`${segment.city}-${segment.temperature_c}`}>
                            <Typography variant="subtitle2" fontWeight={700}>{segment.city}</Typography>
                            <Typography variant="caption" color="text.secondary">
                              {segment.temperature_c}°C • {segment.rain_mm} mm rain • {segment.wind_kph} km/h • {segment.condition}
                            </Typography>
                          </Box>
                        ))}
                      </Stack>
                    </Stack>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        ) : null}
      </Stack>
    </Box>
  )
}
