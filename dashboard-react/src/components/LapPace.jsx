import React from 'react';
import { Card, CardContent, Typography, Box, Grid } from '@mui/material';
import TimerIcon from '@mui/icons-material/Timer';

const LapPace = ({ currentLapTime, bestLapTime, lapTimes, formatTime }) => {
  const delta = currentLapTime - bestLapTime;
  const avgLapTime = lapTimes.length > 0 
    ? lapTimes.reduce((sum, time) => sum + time, 0) / lapTimes.length 
    : 0;

  return (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
          <TimerIcon sx={{ color: 'primary.main' }} />
          <Typography variant="h6" sx={{ color: 'primary.main' }}>
            LAP PACE
          </Typography>
        </Box>

        <Grid container spacing={2} sx={{ mt: 1 }}>
          <Grid item xs={4}>
            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="caption" color="text.secondary">
                CURRENT LAP
              </Typography>
              <Typography 
                variant="h5" 
                fontWeight="bold"
                sx={{ 
                  mt: 1,
                  fontFamily: '"Courier New", monospace'
                }}
              >
                {formatTime(currentLapTime)}
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={4}>
            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="caption" color="text.secondary">
                BEST LAP
              </Typography>
              <Typography 
                variant="h5" 
                fontWeight="bold"
                sx={{ 
                  mt: 1,
                  color: 'secondary.main',
                  fontFamily: '"Courier New", monospace'
                }}
              >
                {formatTime(bestLapTime)}
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={4}>
            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="caption" color="text.secondary">
                DELTA
              </Typography>
              <Typography 
                variant="h5" 
                fontWeight="bold"
                sx={{ 
                  mt: 1,
                  color: delta >= 0 ? '#ff6b6b' : '#00ff00',
                  fontFamily: '"Courier New", monospace'
                }}
              >
                {delta >= 0 ? '+' : ''}{delta.toFixed(3)}
              </Typography>
            </Box>
          </Grid>
        </Grid>

        <Grid container spacing={2} sx={{ mt: 2 }}>
          <Grid item xs={6}>
            <Box sx={{ background: 'rgba(0, 0, 0, 0.3)', borderRadius: 2, p: 2, textAlign: 'center' }}>
              <Typography variant="caption" color="text.secondary">
                AVG LAP TIME
              </Typography>
              <Typography 
                variant="h6" 
                fontWeight="bold" 
                sx={{ 
                  mt: 1,
                  fontFamily: '"Courier New", monospace'
                }}
              >
                {avgLapTime > 0 ? formatTime(avgLapTime) : '--:--'}
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={6}>
            <Box sx={{ background: 'rgba(0, 0, 0, 0.3)', borderRadius: 2, p: 2, textAlign: 'center' }}>
              <Typography variant="caption" color="text.secondary">
                LAP COUNT
              </Typography>
              <Typography variant="h6" fontWeight="bold" sx={{ mt: 1 }}>
                {lapTimes.length}
              </Typography>
            </Box>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

export default LapPace;

