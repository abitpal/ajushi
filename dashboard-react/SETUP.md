# Quick Setup Guide

## 🚀 Getting Started

### Prerequisites
- Node.js 16+ installed
- npm or yarn package manager

### Installation Steps

1. **Navigate to the project directory:**
```bash
cd dashboard-react
```

2. **Install dependencies:**
```bash
npm install
```

3. **Start the development server:**
```bash
npm start
```

4. **Open your browser:**
The app will automatically open at [http://localhost:3000](http://localhost:3000)

## 🎨 Design Features

### Color Palette
- **Primary (Cyan)**: `#00d9ff` - Main accent color
- **Secondary (Pink)**: `#ff3d71` - Highlights and alerts
- **Success (Green)**: `#00e676` - Positive indicators
- **Warning (Yellow)**: `#ffc107` - Caution states
- **Background**: `#0f0f23` - Deep dark blue

### Typography
- **Font Family**: Inter (Google Fonts)
- **Weights**: 400, 500, 600, 700, 800

### Effects
- **Glassmorphism**: Frosted glass effect on cards
- **Gradients**: Smooth cyan-to-blue transitions
- **Glow Effects**: Subtle shadows on interactive elements
- **Hover Animations**: Smooth lift effect on cards

## 📦 Build for Production

```bash
npm run build
```

This creates an optimized production build in the `build/` directory.

## 🔧 Customization

### Change Colors
Edit `src/theme.js` to modify the color palette:

```javascript
primary: {
  main: '#00d9ff',  // Change this
  light: '#5ce1ff',
  dark: '#00a8cc',
}
```

### Adjust Update Rate
Edit `src/App.jsx` line 22:

```javascript
setInterval(updateDashboard, 100); // Change 100 to desired ms
```

### Modify Track
Edit `src/services/telemetryGenerator.js` to change track parameters.

## 🐛 Troubleshooting

### Port Already in Use
If port 3000 is busy, you can specify a different port:
```bash
PORT=3001 npm start
```

### Dependencies Issues
Clear cache and reinstall:
```bash
rm -rf node_modules package-lock.json
npm install
```

## 📱 Mobile Testing

The dashboard is fully responsive. Test on different screen sizes:
- Mobile: < 768px
- Tablet: 768px - 1200px
- Desktop: > 1200px

## 🌐 Deployment

### Vercel (Recommended)
```bash
npm install -g vercel
vercel
```

### Netlify
```bash
npm run build
# Drag and drop the build folder to Netlify
```

### GitHub Pages
Add to `package.json`:
```json
"homepage": "https://yourusername.github.io/dashboard-react"
```

Then:
```bash
npm install --save-dev gh-pages
npm run build
npm run deploy
```

## 📚 Resources

- [React Documentation](https://react.dev/)
- [Material UI Documentation](https://mui.com/)
- [Inter Font](https://fonts.google.com/specimen/Inter)

## 🎯 Performance Tips

1. The dashboard updates every 100ms - adjust if needed for performance
2. Canvas rendering is optimized for 60fps
3. Use React DevTools to profile component renders
4. Consider memoization for expensive calculations

Enjoy your sleek F1 dashboard! 🏎️💨

