import React from 'react';
import ReactDOM from 'react-dom/client';
import CssBaseline from '@mui/material/CssBaseline';
import { ThemeProvider } from '@mui/material/styles';
import { GlobalStyles } from '@mui/material';
import App from './App';
import theme from './theme';

const globalStyles = (
  <GlobalStyles
    styles={{
      '@keyframes twinkle': {
        '0%, 100%': { opacity: 0.3 },
        '50%': { opacity: 1 },
      },
      '@keyframes pulse': {
        '0%, 100%': { opacity: 1 },
        '50%': { opacity: 0.5 },
      },
      'body': {
        margin: 0,
        padding: 0,
        overflowX: 'hidden',
      }
    }}
  />
);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {globalStyles}
      <App />
    </ThemeProvider>
  </React.StrictMode>
);

