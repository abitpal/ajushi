import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Grid,
  Typography,
  AppBar,
  Toolbar,
  Paper,
  LinearProgress,
} from '@mui/material';
import SpeedIcon from '@mui/icons-material/Speed';
import SettingsIcon from '@mui/icons-material/Settings';
import LocalGasStationIcon from '@mui/icons-material/LocalGasStation';

import F1TelemetryGenerator from './services/telemetryGenerator';
import TelemetryCard from './components/TelemetryCard';
import TrackVisualization from './components/TrackVisualization';
import Leaderboard from './components/Leaderboard';
import TireStatus from './components/TireStatus';
import RaceProgress from './components/RaceProgress';
import LapPace from './components/LapPace';

function App() {
  const [telemetry, setTelemetry] = useState(null);
  const [telemetryGen] = useState(() => new F1TelemetryGenerator());

  useEffect(() => {
    const interval = setInterval(() => {
      const data = telemetryGen.generateTelemetry();
      setTelemetry(data);
    }, 100);

    return () => clearInterval(interval);
  }, [telemetryGen]);

  if (!telemetry) {
    return (
      <Box sx={{ width: '100%', mt: 4 }}>
        <LinearProgress color="primary" />
      </Box>
    );
  }

  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const secs = (seconds % 60).toFixed(3);
    return `${minutes}:${secs.padStart(6, '0')}`;
  };

  return (
    <Box sx={{ 
      minHeight: '100vh',
      background: 'radial-gradient(ellipse at top, #1a1a3e 0%, #0f0f23 50%, #000000 100%)',
      position: 'relative',
      '&::before': {
        content: '""',
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        height: '400px',
        background: 'radial-gradient(circle at 50% 0%, rgba(0, 217, 255, 0.1) 0%, transparent 70%)',
        pointerEvents: 'none',
      }
    }}>
      {/* Header */}
      <AppBar 
        position="static" 
        elevation={0}
        sx={{ 
          background: 'rgba(15, 15, 35, 0.8)',
          backdropFilter: 'blur(20px)',
          borderBottom: '1px solid rgba(0, 217, 255, 0.2)',
        }}
      >
        <Toolbar sx={{ py: 1 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Box 
              sx={{ 
                width: 8, 
                height: 8, 
                borderRadius: '50%', 
                background: '#00e676',
                boxShadow: '0 0 20px #00e676',
                animation: 'pulse 2s ease-in-out infinite',
                '@keyframes pulse': {
                  '0%, 100%': { opacity: 1 },
                  '50%': { opacity: 0.5 },
                }
              }} 
            />
            <Typography 
              variant="h5" 
              component="div" 
              sx={{ 
                fontWeight: 700,
                background: 'linear-gradient(135deg, #00d9ff 0%, #5ce1ff 100%)',
                backgroundClip: 'text',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                letterSpacing: '0.1em',
              }}
            >
              F1 TELEMETRY
            </Typography>
          </Box>
          <Box sx={{ flexGrow: 1 }} />
          <Typography variant="caption" color="text.secondary">
            LIVE
          </Typography>
        </Toolbar>
      </AppBar>

      {/* Lap Timer */}
      <Box sx={{ textAlign: 'center', py: 4, position: 'relative', zIndex: 1 }}>
        <Typography variant="caption" color="text.secondary" sx={{ mb: 1, display: 'block' }}>
          CURRENT LAP TIME
        </Typography>
        <Typography 
          variant="h1" 
          sx={{ 
            background: 'linear-gradient(135deg, #00d9ff 0%, #5ce1ff 100%)',
            backgroundClip: 'text',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            fontFamily: '"Courier New", monospace',
            fontWeight: 'bold',
            fontSize: '4rem',
            textShadow: '0 0 40px rgba(0, 217, 255, 0.3)',
          }}
        >
          {formatTime(telemetry.lapTime)}
        </Typography>
      </Box>

      <Container maxWidth="xl" sx={{ pb: 4 }}>
        <Grid container spacing={3}>
          {/* Speed & RPM */}
          <Grid item xs={12} md={6} lg={3}>
            <TelemetryCard
              title="Speed"
              value={telemetry.speed}
              unit="km/h"
              color="#00e676"
              icon={SpeedIcon}
            />
          </Grid>
          <Grid item xs={12} md={6} lg={3}>
            <TelemetryCard
              title="RPM"
              value={telemetry.rpm.toLocaleString()}
              color="#ff3d71"
              icon={SettingsIcon}
            />
          </Grid>
          <Grid item xs={12} md={6} lg={3}>
            <TelemetryCard
              title="Gear"
              value={telemetry.gear}
              color="#00d9ff"
            />
          </Grid>
          <Grid item xs={12} md={6} lg={3}>
            <TelemetryCard
              title="Sector"
              value={telemetry.sector}
            />
          </Grid>

          {/* Driver Controls */}
          <Grid item xs={12} md={6} lg={3}>
            <TelemetryCard
              title="Throttle"
              value={`${telemetry.throttle}%`}
            />
          </Grid>
          <Grid item xs={12} md={6} lg={3}>
            <TelemetryCard
              title="Brake"
              value={`${telemetry.brake}%`}
            />
          </Grid>
          <Grid item xs={12} md={6} lg={3}>
            <TelemetryCard
              title="Steering"
              value={`${(telemetry.steering * 10).toFixed(1)}°`}
            />
          </Grid>
          <Grid item xs={12} md={6} lg={3}>
            <TelemetryCard
              title="DRS"
              value={telemetry.drs ? 'ON' : 'OFF'}
              color={telemetry.drs ? '#00ff00' : '#666666'}
            />
          </Grid>

          {/* Fuel */}
          <Grid item xs={12} md={6} lg={4}>
            <Paper 
              sx={{ 
                p: 3, 
                height: '100%',
                background: 'linear-gradient(135deg, rgba(15, 15, 35, 0.9) 0%, rgba(26, 26, 62, 0.8) 100%)',
              }}
            >
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                <Box 
                  sx={{ 
                    width: 36, 
                    height: 36, 
                    borderRadius: '10px',
                    background: 'rgba(255, 193, 7, 0.15)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                  }}
                >
                  <LocalGasStationIcon sx={{ color: 'warning.main', fontSize: 20 }} />
                </Box>
                <Typography variant="h6" sx={{ color: 'text.primary' }}>
                  FUEL & SYSTEMS
                </Typography>
              </Box>
              <Typography 
                variant="h3" 
                fontWeight="bold" 
                sx={{ 
                  mb: 2,
                  background: 'linear-gradient(135deg, #ffc107 0%, #ffd54f 100%)',
                  backgroundClip: 'text',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                }}
              >
                {telemetry.fuelRemaining.toFixed(1)}%
              </Typography>
              <Box sx={{ position: 'relative' }}>
                <LinearProgress 
                  variant="determinate" 
                  value={telemetry.fuelRemaining}
                  sx={{
                    height: 12,
                    borderRadius: 6,
                    backgroundColor: 'rgba(255, 255, 255, 0.05)',
                    '& .MuiLinearProgress-bar': {
                      background: telemetry.fuelRemaining > 50 
                        ? 'linear-gradient(90deg, #00e676 0%, #66ffa6 100%)'
                        : telemetry.fuelRemaining > 20
                        ? 'linear-gradient(90deg, #ffc107 0%, #ffd54f 100%)'
                        : 'linear-gradient(90deg, #ff3d71 0%, #ff6b92 100%)',
                      borderRadius: 6,
                    }
                  }}
                />
              </Box>
              <Box sx={{ mt: 3, p: 2, background: 'rgba(0, 0, 0, 0.2)', borderRadius: 2 }}>
                <Typography variant="caption" color="text.secondary" sx={{ letterSpacing: '0.1em' }}>
                  ERS MODE
                </Typography>
                <Typography variant="h6" fontWeight="bold" sx={{ mt: 0.5 }}>
                  {telemetry.ersDeployMode}
                </Typography>
              </Box>
            </Paper>
          </Grid>

          {/* Race Progress */}
          <Grid item xs={12} md={6} lg={4}>
            <RaceProgress 
              currentLap={telemetry.currentLap}
              totalLaps={telemetry.totalLaps}
            />
          </Grid>

          {/* Lap Pace */}
          <Grid item xs={12} md={12} lg={4}>
            <LapPace
              currentLapTime={telemetry.lapTime}
              bestLapTime={telemetry.bestLapTime}
              lapTimes={telemetry.lapTimes}
              formatTime={formatTime}
            />
          </Grid>

          {/* Track Visualization */}
          <Grid item xs={12} lg={8}>
            <TrackVisualization 
              position={telemetry.position}
              angle={telemetry.angle}
            />
          </Grid>

          {/* Leaderboard */}
          <Grid item xs={12} lg={4}>
            <Leaderboard 
              drivers={telemetry.drivers}
              formatTime={formatTime}
            />
          </Grid>

          {/* Tire Temperatures */}
          <Grid item xs={12} md={6}>
            <TireStatus
              tireTemps={telemetry.tireTemps}
              tirePressures={telemetry.tirePressures}
              showPressure={false}
            />
          </Grid>

          {/* Tire Pressures */}
          <Grid item xs={12} md={6}>
            <TireStatus
              tireTemps={telemetry.tireTemps}
              tirePressures={telemetry.tirePressures}
              showPressure={true}
            />
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
}

export default App;

