import React from 'react';
import { Card, CardContent, Typography, Box } from '@mui/material';

const TelemetryCard = ({ title, value, unit, color, icon: Icon }) => {
  return (
    <Card 
      sx={{ 
        height: '100%',
        background: 'linear-gradient(135deg, rgba(15, 15, 35, 0.9) 0%, rgba(26, 26, 62, 0.8) 100%)',
        border: '1px solid rgba(0, 217, 255, 0.1)',
        transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
        position: 'relative',
        overflow: 'hidden',
        '&::before': {
          content: '""',
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          height: '2px',
          background: `linear-gradient(90deg, transparent, ${color || '#00d9ff'}, transparent)`,
          opacity: 0.5,
        },
        '&:hover': {
          transform: 'translateY(-4px)',
          borderColor: 'rgba(0, 217, 255, 0.3)',
          boxShadow: `0 12px 40px ${color ? `${color}20` : 'rgba(0, 217, 255, 0.15)'}`,
        }
      }}
    >
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
          <Typography 
            variant="caption" 
            color="text.secondary" 
            sx={{ 
              textTransform: 'uppercase',
              letterSpacing: '0.1em',
              fontWeight: 600,
            }}
          >
            {title}
          </Typography>
          {Icon && (
            <Box 
              sx={{ 
                width: 32, 
                height: 32, 
                borderRadius: '8px',
                background: `${color || '#00d9ff'}15`,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <Icon sx={{ color: color || 'primary.main', fontSize: 18 }} />
            </Box>
          )}
        </Box>
        <Typography 
          variant="h3" 
          component="div" 
          sx={{ 
            color: color || 'text.primary',
            fontWeight: 700,
            fontFamily: '"Courier New", monospace',
            lineHeight: 1.2,
          }}
        >
          {value}
        </Typography>
        {unit && (
          <Typography 
            variant="caption" 
            sx={{ 
              color: 'text.secondary',
              mt: 0.5,
              display: 'block',
              opacity: 0.7,
            }}
          >
            {unit}
          </Typography>
        )}
      </CardContent>
    </Card>
  );
};

export default TelemetryCard;

