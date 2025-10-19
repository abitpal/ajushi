import React from 'react';
import { Card, CardContent, Typography, Box, List, ListItem, ListItemText, Chip } from '@mui/material';
import EmojiEventsIcon from '@mui/icons-material/EmojiEvents';

const Leaderboard = ({ drivers, formatTime }) => {
  return (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
          <EmojiEventsIcon sx={{ color: 'primary.main' }} />
          <Typography variant="h6" sx={{ color: 'primary.main' }}>
            LEADERBOARD
          </Typography>
        </Box>
        <List sx={{ maxHeight: 400, overflow: 'auto' }}>
          {drivers.map((driver) => (
            <ListItem
              key={driver.id}
              sx={{
                mb: 1,
                background: driver.isCurrentDriver 
                  ? 'rgba(0, 255, 0, 0.1)' 
                  : 'rgba(0, 0, 0, 0.3)',
                borderRadius: 1,
                borderLeft: driver.isCurrentDriver 
                  ? '4px solid #00ff00' 
                  : '4px solid #e10600',
              }}
            >
              <Chip 
                label={driver.position} 
                size="small"
                sx={{ 
                  mr: 2,
                  fontWeight: 'bold',
                  background: 'primary.main',
                  color: 'white'
                }}
              />
              <ListItemText
                primary={
                  <Typography variant="body1" fontWeight="bold">
                    {driver.name}
                  </Typography>
                }
                secondary={
                  <Typography variant="caption" color="text.secondary">
                    Lap {driver.currentLap} • {formatTime(driver.lapTime)}
                  </Typography>
                }
              />
            </ListItem>
          ))}
        </List>
      </CardContent>
    </Card>
  );
};

export default Leaderboard;

