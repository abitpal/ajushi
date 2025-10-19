# F1 Telemetry Dashboard - React + Material UI

A sleek, modern real-time F1 telemetry dashboard built with React and Material UI. Features a stunning dark theme with cyan/blue gradients, smooth animations, and comprehensive race statistics.

![Dashboard Preview](https://img.shields.io/badge/Status-Live-00e676?style=for-the-badge)
![React](https://img.shields.io/badge/React-18-00d9ff?style=for-the-badge&logo=react)
![Material UI](https://img.shields.io/badge/MUI-v5-00d9ff?style=for-the-badge&logo=mui)

## ✨ Features

- 🏎️ **Real-time Telemetry** - Speed, RPM, Gear, Throttle, Brake, Steering with live updates
- 🗺️ **Track Visualization** - Beautiful canvas-based track with glowing car position
- 🏁 **Race Progress** - Live lap tracking with progress bars and timing
- 🔥 **Tire Monitoring** - Temperature and pressure with color-coded indicators
- ⛽ **Fuel System** - Smart fuel gauge with dynamic color changes
- 📊 **Live Leaderboard** - 20 drivers with real-time positions
- 🎨 **Stunning UI** - Sleek dark theme with cyan/blue gradients and smooth animations
- 📱 **Fully Responsive** - Adapts perfectly to mobile, tablet, and desktop
- ⚡ **High Performance** - 100ms update rate with optimized rendering
- 🎯 **Modern Design** - Glassmorphism effects, hover animations, and gradient accents

## Technologies Used

- **React 18** - Modern React with hooks
- **Material UI v5** - Component library with custom theming
- **@mui/x-charts** - Data visualization
- **@mui/x-data-grid** - Advanced data tables
- **Emotion** - CSS-in-JS styling

## Installation

1. Navigate to the project directory:
```bash
cd dashboard-react
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

4. Open your browser to [http://localhost:3000](http://localhost:3000)

## Project Structure

```
dashboard-react/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── TelemetryCard.jsx      # Reusable telemetry display card
│   │   ├── TrackVisualization.jsx # Canvas-based track renderer
│   │   ├── Leaderboard.jsx        # Driver standings
│   │   ├── TireStatus.jsx         # Tire temps & pressures
│   │   ├── RaceProgress.jsx       # Lap progress indicator
│   │   └── LapPace.jsx            # Lap time comparison
│   ├── services/
│   │   └── telemetryGenerator.js  # Simulated telemetry data
│   ├── App.jsx                    # Main dashboard component
│   ├── theme.js                   # MUI custom theme
│   └── index.js                   # App entry point
├── package.json
└── README.md
```

## Components Overview

### TelemetryCard
Displays individual telemetry metrics with customizable colors and icons.

### TrackVisualization
Canvas-based oval track with real-time car position, sector markers, and visual effects.

### Leaderboard
Shows all 20 drivers with their current lap times and positions, highlighting the current driver.

### TireStatus
Displays tire temperatures or pressures in a 2x2 grid with color-coded temperature indicators.

### RaceProgress
Linear progress bar showing race completion percentage with current/total lap counts.

### LapPace
Compares current lap time against best lap time with delta calculation and average lap time.

## Customization

### Theme
Edit `src/theme.js` to customize colors, typography, and component styles:

```javascript
const theme = createTheme({
  palette: {
    primary: { main: '#e10600' },  // F1 red
    secondary: { main: '#00ff00' }, // Green
    // ... more customization
  },
});
```

### Telemetry Data
Modify `src/services/telemetryGenerator.js` to adjust:
- Update frequency (currently 100ms)
- Track parameters (radius, sectors)
- Driver names and count
- Simulation behavior

## Building for Production

```bash
npm run build
```

This creates an optimized production build in the `build/` directory.

## Integration with Real Telemetry

To connect to real F1 telemetry data:

1. Replace the `F1TelemetryGenerator` class with your data source
2. Update the `useEffect` hook in `App.jsx` to fetch from your API
3. Ensure the data structure matches the expected format

Example:
```javascript
useEffect(() => {
  const ws = new WebSocket('ws://your-telemetry-server');
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    setTelemetry(data);
  };
  return () => ws.close();
}, []);
```

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## License

MIT

## Credits

Built with [Material UI](https://mui.com/) dashboard templates and components.

