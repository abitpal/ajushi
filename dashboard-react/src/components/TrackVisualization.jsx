import React, { useEffect, useRef } from 'react';
import { Card, CardContent, Typography, Box } from '@mui/material';

const TrackVisualization = ({ position, angle }) => {
  const canvasRef = useRef(null);

  // F1-style track waypoints (inspired by circuits like Silverstone/Suzuka)
  const trackWaypoints = [
    { x: 50, y: 250 },   // Start/Finish straight
    { x: 50, y: 200 },
    { x: 50, y: 150 },
    { x: 70, y: 100 },   // Turn 1 (fast right)
    { x: 110, y: 70 },
    { x: 160, y: 60 },   // Long straight
    { x: 220, y: 60 },
    { x: 270, y: 70 },   // Hairpin entry
    { x: 300, y: 100 },
    { x: 310, y: 140 },  // Hairpin apex
    { x: 300, y: 180 },
    { x: 270, y: 210 },  // Chicane
    { x: 240, y: 220 },
    { x: 210, y: 210 },
    { x: 180, y: 190 },  // Fast sweeper
    { x: 150, y: 180 },
    { x: 120, y: 190 },
    { x: 90, y: 220 },   // Final corner
    { x: 70, y: 250 },
  ];

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;

    // Clear canvas
    ctx.clearRect(0, 0, width, height);

    // Calculate total track length
    let totalLength = 0;
    const segmentLengths = [];
    for (let i = 0; i < trackWaypoints.length; i++) {
      const p1 = trackWaypoints[i];
      const p2 = trackWaypoints[(i + 1) % trackWaypoints.length];
      const segLength = Math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2);
      segmentLengths.push(segLength);
      totalLength += segLength;
    }

    // Draw track background (wider)
    ctx.strokeStyle = 'rgba(0, 0, 0, 0.5)';
    ctx.lineWidth = 35;
    ctx.lineJoin = 'round';
    ctx.lineCap = 'round';
    ctx.beginPath();
    ctx.moveTo(trackWaypoints[0].x, trackWaypoints[0].y);
    for (let i = 1; i < trackWaypoints.length; i++) {
      ctx.lineTo(trackWaypoints[i].x, trackWaypoints[i].y);
    }
    ctx.closePath();
    ctx.stroke();

    // Draw track with gradient
    const gradient = ctx.createLinearGradient(0, 0, width, height);
    gradient.addColorStop(0, 'rgba(0, 217, 255, 0.4)');
    gradient.addColorStop(0.5, 'rgba(92, 225, 255, 0.5)');
    gradient.addColorStop(1, 'rgba(0, 217, 255, 0.4)');
    
    ctx.strokeStyle = gradient;
    ctx.lineWidth = 28;
    ctx.lineJoin = 'round';
    ctx.lineCap = 'round';
    ctx.beginPath();
    ctx.moveTo(trackWaypoints[0].x, trackWaypoints[0].y);
    for (let i = 1; i < trackWaypoints.length; i++) {
      ctx.lineTo(trackWaypoints[i].x, trackWaypoints[i].y);
    }
    ctx.closePath();
    ctx.stroke();
    
    // Draw center line
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
    ctx.lineWidth = 2;
    ctx.setLineDash([10, 10]);
    ctx.beginPath();
    ctx.moveTo(trackWaypoints[0].x, trackWaypoints[0].y);
    for (let i = 1; i < trackWaypoints.length; i++) {
      ctx.lineTo(trackWaypoints[i].x, trackWaypoints[i].y);
    }
    ctx.closePath();
    ctx.stroke();
    ctx.setLineDash([]);

    // Draw sector markers
    const sectorPositions = [0, 6, 13]; // Indices for sector markers
    sectorPositions.forEach((idx, sectorNum) => {
      const point = trackWaypoints[idx];
      
      // Marker glow
      ctx.shadowColor = '#00d9ff';
      ctx.shadowBlur = 15;
      ctx.fillStyle = '#00d9ff';
      ctx.beginPath();
      ctx.arc(point.x, point.y, 8, 0, 2 * Math.PI);
      ctx.fill();
      
      ctx.shadowBlur = 0;
      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 12px Inter, Arial';
      ctx.textAlign = 'center';
      ctx.fillText(`S${sectorNum + 1}`, point.x, point.y - 18);
    });

    // Draw start/finish line
    const startPoint = trackWaypoints[0];
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(startPoint.x - 15, startPoint.y);
    ctx.lineTo(startPoint.x + 15, startPoint.y);
    ctx.stroke();

    // Calculate car position based on angle
    const normalizedAngle = ((angle || 0) % (2 * Math.PI) + 2 * Math.PI) % (2 * Math.PI);
    const progress = normalizedAngle / (2 * Math.PI);
    const targetDistance = progress * totalLength;
    
    let accumulatedLength = 0;
    let carX = startPoint.x;
    let carY = startPoint.y;
    
    for (let i = 0; i < segmentLengths.length; i++) {
      if (accumulatedLength + segmentLengths[i] >= targetDistance) {
        const segmentProgress = (targetDistance - accumulatedLength) / segmentLengths[i];
        const p1 = trackWaypoints[i];
        const p2 = trackWaypoints[(i + 1) % trackWaypoints.length];
        carX = p1.x + (p2.x - p1.x) * segmentProgress;
        carY = p1.y + (p2.y - p1.y) * segmentProgress;
        break;
      }
      accumulatedLength += segmentLengths[i];
    }

    // Draw car position with trail
    ctx.shadowColor = '#ff3d71';
    ctx.shadowBlur = 25;
    ctx.fillStyle = '#ff3d71';
    ctx.beginPath();
    ctx.arc(carX, carY, 12, 0, 2 * Math.PI);
    ctx.fill();
    
    // Car center
    ctx.shadowBlur = 0;
    ctx.fillStyle = '#ffffff';
    ctx.beginPath();
    ctx.arc(carX, carY, 7, 0, 2 * Math.PI);
    ctx.fill();

  }, [position, angle]);

  return (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Typography variant="h6" gutterBottom sx={{ color: 'primary.main' }}>
          TRACK POSITION
        </Typography>
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', mt: 2 }}>
          <canvas 
            ref={canvasRef} 
            width={360} 
            height={280}
            style={{ 
              maxWidth: '100%',
              background: 'linear-gradient(135deg, #000000 0%, #0a0a1a 100%)',
              borderRadius: '12px',
              border: '1px solid rgba(0, 217, 255, 0.2)',
            }}
          />
        </Box>
      </CardContent>
    </Card>
  );
};

export default TrackVisualization;

