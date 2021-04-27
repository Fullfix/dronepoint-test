import { createMuiTheme, makeStyles, ThemeProvider } from '@material-ui/core'
import React from 'react'
import { YMaps } from 'react-yandex-maps';
import Drone from './components/Drone';

const theme = createMuiTheme({
    palette: {
      primary: {
        main: '#FF9900',
        contrastText: '#FFFFFF',
      },
      text: {
        primary: '#000000',
        secondary: '#4a4f52',
      },
    },
    typography: {
      fontFamily: [
        "'Inter'",
      ].join(','),
      h2: {
        fontSize: 20,
        fontWeight: 'bold',
      },
      h3: {
        fontSize: 18,
      },
      h4: {
        fontSize: 16,
      },
      h5: {
        fontSize: 14,
      },
      h6: {
        fontSize: 12,
      }
    }
  })

const useStyles = makeStyles(theme => ({
    root: {
        
    },
}));

const App = () => {
    const classes = useStyles();
    return (
        <ThemeProvider theme={theme}>
            <YMaps>
                <Drone />
            </YMaps>
        </ThemeProvider>
    )
}

export default App