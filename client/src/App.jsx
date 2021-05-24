import { createMuiTheme, makeStyles, ThemeProvider, Typography } from '@material-ui/core'
import React, { useContext } from 'react'
import { ToastContainer } from 'react-toastify';
import { YMaps } from 'react-yandex-maps';
import MainPage from './components/MainPage';
import DronepointProvider, { DronepointContext } from './contexts/DronepointProvider';

const theme = createMuiTheme({
    palette: {
      primary: {
        main: '#FF9900',
        contrastText: '#FFFFFF',
      },
      secondary: {
        main: '#1BE56E',
      },
      text: {
        primary: '#000000',
        secondary: '#4a4f52',
      },
    },
    typography: {
      fontFamily: [
        "'Roboto'",
        "'Helvetica'",
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

const Main = () => {
  const { loading, data } = useContext(DronepointContext);
  
  if (loading || !data) return (
    <Typography>Loading</Typography>
  )

  return <MainPage />
}

const App = () => {
    const classes = useStyles();
    return (
        <ThemeProvider theme={theme}>
          <DronepointProvider>
            <YMaps>
              <ToastContainer />
              <Main />
            </YMaps>
          </DronepointProvider>
        </ThemeProvider>
    )
}

export default App