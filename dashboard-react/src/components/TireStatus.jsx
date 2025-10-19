import React from 'react';
import { Card, CardContent, Typography, Box, Grid } from '@mui/material';

const TireStatus = ({ tireTemps, tirePressures, showPressure = false }) => {
  const getTempColor = (temp) => {
    if (temp > 100) return '#ff4444';
    if (temp > 80) return '#ffaa44';
    return '#44ff44';
  };

  const tirePositions = [
    { key: 'fl', label: 'FL', name: 'Front Left' },
    { key: 'fr', label: 'FR', name: 'Front Right' },
    { key: 'rl', label: 'RL', name: 'Rear Left' },
    { key: 'rr', label: 'RR', name: 'Rear Right' },
  ];

  return (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Typography variant="h6" gutterBottom sx={{ color: 'primary.main' }}>
          {showPressure ? 'TIRE PRESSURES' : 'TIRE TEMPERATURES'}
        </Typography>
        <Grid container spacing={2} sx={{ mt: 1 }}>
          {tirePositions.map((tire) => (
            <Grid item xs={6} key={tire.key}>
              <Box
                sx={{
                  background: 'rgba(0, 0, 0, 0.3)',
                  borderRadius: 2,
                  p: 2,
                  textAlign: 'center',
                }}
              >
                <Typography variant="caption" color="text.secondary">
                  {tire.label}
                </Typography>
                <Typography
                  variant="h4"
                  sx={{
                    color: showPressure ? 'text.primary' : getTempColor(tireTemps[tire.key]),
                    fontWeight: 'bold',
                    fontFamily: '"Courier New", monospace',
                    my: 1,
                  }}
                >
                  {showPressure 
                    ? tirePressures[tire.key].toFixed(1)
                    : Math.round(tireTemps[tire.key])
                  }
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  {showPressure ? 'PSI' : '°C'}
                </Typography>
              </Box>
            </Grid>
          ))}
        </Grid>
      </CardContent>
    </Card>
  );
};

export default TireStatus;

