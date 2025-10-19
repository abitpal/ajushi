import React from 'react';
import { Card, CardContent, Typography, Box, LinearProgress, Grid } from '@mui/material';
import FlagIcon from '@mui/icons-material/Flag';

const RaceProgress = ({ currentLap, totalLaps }) => {
  const progress = (currentLap / totalLaps) * 100;

  return (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
          <FlagIcon sx={{ color: 'primary.main' }} />
          <Typography variant="h6" sx={{ color: 'primary.main' }}>
            RACE PROGRESS
          </Typography>
        </Box>
        
        <Box sx={{ mt: 3 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
            <Typography variant="body2" color="text.secondary">
              Race Completion
            </Typography>
            <Typography variant="body2" fontWeight="bold">
              {progress.toFixed(1)}%
            </Typography>
          </Box>
          <LinearProgress 
            variant="determinate" 
            value={progress}
            sx={{
              height: 12,
              borderRadius: 6,
              backgroundColor: 'rgba(255, 255, 255, 0.05)',
              '& .MuiLinearProgress-bar': {
                background: 'linear-gradient(90deg, #00d9ff 0%, #5ce1ff 50%, #00d9ff 100%)',
                borderRadius: 6,
                boxShadow: '0 0 20px rgba(0, 217, 255, 0.4)',
              }
            }}
          />
        </Box>

        <Grid container spacing={2} sx={{ mt: 2 }}>
          <Grid item xs={6}>
            <Box sx={{ background: 'rgba(0, 0, 0, 0.3)', borderRadius: 2, p: 2, textAlign: 'center' }}>
              <Typography variant="caption" color="text.secondary">
                CURRENT LAP
              </Typography>
              <Typography variant="h4" fontWeight="bold" sx={{ mt: 1 }}>
                {currentLap}
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={6}>
            <Box sx={{ background: 'rgba(0, 0, 0, 0.3)', borderRadius: 2, p: 2, textAlign: 'center' }}>
              <Typography variant="caption" color="text.secondary">
                TOTAL LAPS
              </Typography>
              <Typography variant="h4" fontWeight="bold" sx={{ mt: 1 }}>
                {totalLaps}
              </Typography>
            </Box>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

export default RaceProgress;

