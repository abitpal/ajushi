import React, { useEffect, useRef } from 'react';
import { Box } from '@mui/material';

const StarField = () => {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const width = window.innerWidth;
    const height = window.innerHeight;
    
    canvas.width = width;
    canvas.height = height;

    // Generate stars with varying sizes and brightness
    const stars = [];
    const starCount = 200;
    
    for (let i = 0; i < starCount; i++) {
      stars.push({
        x: Math.random() * width,
        y: Math.random() * height,
        radius: Math.random() * 1.5 + 0.5,
        opacity: Math.random() * 0.5 + 0.3,
        twinkleSpeed: Math.random() * 0.02 + 0.01,
        twinklePhase: Math.random() * Math.PI * 2,
      });
    }

    // Distant galaxies
    const galaxies = [
      {
        x: 0.25,
        y: 0.35,
        size: 40,
        rotation: 0,
        color: 'rgba(147, 112, 219, 0.3)', // Purple
        type: 'spiral',
      },
      {
        x: 0.70,
        y: 0.75,
        size: 30,
        rotation: Math.PI / 4,
        color: 'rgba(0, 191, 255, 0.25)', // Deep sky blue
        type: 'spiral',
      },
      {
        x: 0.85,
        y: 0.30,
        size: 25,
        rotation: -Math.PI / 3,
        color: 'rgba(255, 182, 193, 0.2)', // Light pink
        type: 'elliptical',
      },
    ];

    // Famous constellation patterns (simplified)
    const constellations = [
      // Big Dipper (Ursa Major)
      {
        name: 'Ursa Major',
        stars: [
          { x: 0.15, y: 0.25 },
          { x: 0.18, y: 0.28 },
          { x: 0.20, y: 0.26 },
          { x: 0.23, y: 0.25 },
          { x: 0.24, y: 0.22 },
          { x: 0.22, y: 0.20 },
          { x: 0.19, y: 0.21 },
        ],
        color: 'rgba(0, 217, 255, 0.6)',
      },
      // Orion's Belt
      {
        name: 'Orion',
        stars: [
          { x: 0.75, y: 0.45 },
          { x: 0.78, y: 0.46 },
          { x: 0.81, y: 0.47 },
          { x: 0.78, y: 0.40 },
          { x: 0.78, y: 0.52 },
        ],
        color: 'rgba(255, 255, 255, 0.7)',
      },
      // Cassiopeia (W shape)
      {
        name: 'Cassiopeia',
        stars: [
          { x: 0.80, y: 0.15 },
          { x: 0.83, y: 0.18 },
          { x: 0.85, y: 0.14 },
          { x: 0.88, y: 0.17 },
          { x: 0.91, y: 0.15 },
        ],
        color: 'rgba(255, 193, 7, 0.6)',
      },
      // Leo
      {
        name: 'Leo',
        stars: [
          { x: 0.40, y: 0.60 },
          { x: 0.43, y: 0.58 },
          { x: 0.45, y: 0.62 },
          { x: 0.48, y: 0.60 },
          { x: 0.46, y: 0.66 },
        ],
        color: 'rgba(255, 61, 113, 0.5)',
      },
    ];

    let animationFrame;
    let time = 0;

    // Function to draw a spiral galaxy
    const drawSpiralGalaxy = (x, y, size, rotation, color, time) => {
      ctx.save();
      ctx.translate(x, y);
      ctx.rotate(rotation + time * 0.05);

      // Galaxy core
      const coreGradient = ctx.createRadialGradient(0, 0, 0, 0, 0, size * 0.3);
      coreGradient.addColorStop(0, color.replace(/[\d.]+\)$/g, '0.6)'));
      coreGradient.addColorStop(0.5, color.replace(/[\d.]+\)$/g, '0.3)'));
      coreGradient.addColorStop(1, 'transparent');
      
      ctx.beginPath();
      ctx.arc(0, 0, size * 0.3, 0, Math.PI * 2);
      ctx.fillStyle = coreGradient;
      ctx.fill();

      // Spiral arms
      for (let arm = 0; arm < 2; arm++) {
        ctx.beginPath();
        const armRotation = (arm * Math.PI);
        
        for (let i = 0; i < 100; i++) {
          const t = i / 100;
          const angle = armRotation + t * Math.PI * 3;
          const radius = t * size;
          const x = Math.cos(angle) * radius;
          const y = Math.sin(angle) * radius * 0.4; // Flattened
          
          if (i === 0) {
            ctx.moveTo(x, y);
          } else {
            ctx.lineTo(x, y);
          }
        }
        
        ctx.strokeStyle = color;
        ctx.lineWidth = size * 0.08;
        ctx.stroke();
        
        // Add blur effect
        ctx.strokeStyle = color.replace(/[\d.]+\)$/g, '0.15)');
        ctx.lineWidth = size * 0.15;
        ctx.stroke();
      }

      // Add some random star clusters in the galaxy
      for (let i = 0; i < 15; i++) {
        const angle = Math.random() * Math.PI * 2;
        const radius = Math.random() * size * 0.8;
        const px = Math.cos(angle) * radius;
        const py = Math.sin(angle) * radius * 0.4;
        
        ctx.beginPath();
        ctx.arc(px, py, Math.random() * 1.5 + 0.5, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
        ctx.fill();
      }

      ctx.restore();
    };

    // Function to draw an elliptical galaxy
    const drawEllipticalGalaxy = (x, y, size, rotation, color) => {
      ctx.save();
      ctx.translate(x, y);
      ctx.rotate(rotation);

      // Create gradient
      const gradient = ctx.createRadialGradient(0, 0, 0, 0, 0, size);
      gradient.addColorStop(0, color.replace(/[\d.]+\)$/g, '0.5)'));
      gradient.addColorStop(0.3, color.replace(/[\d.]+\)$/g, '0.3)'));
      gradient.addColorStop(0.6, color.replace(/[\d.]+\)$/g, '0.1)'));
      gradient.addColorStop(1, 'transparent');

      ctx.beginPath();
      ctx.ellipse(0, 0, size, size * 0.6, 0, 0, Math.PI * 2);
      ctx.fillStyle = gradient;
      ctx.fill();

      // Add some bright spots
      for (let i = 0; i < 20; i++) {
        const angle = Math.random() * Math.PI * 2;
        const radius = Math.random() * size * 0.6;
        const px = Math.cos(angle) * radius;
        const py = Math.sin(angle) * radius * 0.6;
        
        ctx.beginPath();
        ctx.arc(px, py, Math.random() * 1 + 0.5, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
        ctx.fill();
      }

      ctx.restore();
    };

    const animate = () => {
      ctx.clearRect(0, 0, width, height);
      time += 0.01;

      // Draw galaxies first (in background)
      galaxies.forEach(galaxy => {
        const gx = galaxy.x * width;
        const gy = galaxy.y * height;
        
        if (galaxy.type === 'spiral') {
          drawSpiralGalaxy(gx, gy, galaxy.size, galaxy.rotation, galaxy.color, time);
        } else {
          drawEllipticalGalaxy(gx, gy, galaxy.size, galaxy.rotation, galaxy.color);
        }
      });

      // Draw random stars with twinkling
      stars.forEach(star => {
        const twinkle = Math.sin(time * star.twinkleSpeed + star.twinklePhase);
        const currentOpacity = star.opacity + twinkle * 0.3;
        
        ctx.beginPath();
        ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255, 255, 255, ${Math.max(0, currentOpacity)})`;
        ctx.fill();

        // Add glow for brighter stars
        if (star.radius > 1.2) {
          ctx.beginPath();
          ctx.arc(star.x, star.y, star.radius * 2, 0, Math.PI * 2);
          ctx.fillStyle = `rgba(255, 255, 255, ${Math.max(0, currentOpacity * 0.2)})`;
          ctx.fill();
        }
      });

      // Draw constellations
      constellations.forEach(constellation => {
        const points = constellation.stars.map(star => ({
          x: star.x * width,
          y: star.y * height,
        }));

        // Draw connecting lines
        ctx.strokeStyle = constellation.color;
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(points[0].x, points[0].y);
        for (let i = 1; i < points.length; i++) {
          ctx.lineTo(points[i].x, points[i].y);
        }
        ctx.stroke();

        // Draw constellation stars
        points.forEach(point => {
          const pulse = Math.sin(time * 2) * 0.2 + 0.8;
          ctx.beginPath();
          ctx.arc(point.x, point.y, 2.5 * pulse, 0, Math.PI * 2);
          ctx.fillStyle = constellation.color;
          ctx.fill();

          // Glow effect
          ctx.beginPath();
          ctx.arc(point.x, point.y, 6 * pulse, 0, Math.PI * 2);
          ctx.fillStyle = constellation.color.replace(/[\d.]+\)$/g, '0.2)');
          ctx.fill();
        });
      });

      animationFrame = requestAnimationFrame(animate);
    };

    animate();

    // Handle window resize
    const handleResize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };

    window.addEventListener('resize', handleResize);

    return () => {
      cancelAnimationFrame(animationFrame);
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return (
    <Box
      sx={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        zIndex: 0,
        pointerEvents: 'none',
      }}
    >
      <canvas
        ref={canvasRef}
        style={{
          width: '100%',
          height: '100%',
          display: 'block',
        }}
      />
    </Box>
  );
};

export default StarField;

