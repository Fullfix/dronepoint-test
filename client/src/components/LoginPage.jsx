import { Box, Button, makeStyles, Paper, TextField, Typography } from '@material-ui/core'
import React, { useContext, useState } from 'react'
import { DronepointContext } from '../contexts/DronepointProvider';

const useStyles = makeStyles(theme => ({
    root: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100%',  
    },
    loginBox: {
        padding: 20,
        maxWidth: 500,
        width: '100%',
        display: 'flex',
        flexDirection: 'column',
        backgroundColor: '#EFEFEF',
    },
    button: {
        marginTop: 20,
    },
    title: {
        fontSize: 36,
        marginBottom: 40,
    }
}));

const logoSrc = 'https://static.tildacdn.com/tild3363-6133-4165-b731-323763643637/_COEX_2019_.svg';

const LoginPage = () => {
    const classes = useStyles();
    const { authenticate } = useContext(DronepointContext);
    const [password, setPassword] = useState('');

    const handleSubmit = async () => {
        const success = await authenticate(password);
    }

    return (
        <Box className={classes.root}>
            <Paper className={classes.loginBox} elevation={3}>
                <Typography variant="h2" align="center" className={classes.title}>
                    Dronepoint Test
                </Typography>
                <TextField variant="outlined" placeholder="Enter Password" 
                value={password} onChange={(e) => setPassword(e.target.value)} />
                <Button variant="contained" color="primary" className={classes.button}
                onClick={handleSubmit}>Login</Button>
            </Paper>
        </Box>
    )
}

export default LoginPage
