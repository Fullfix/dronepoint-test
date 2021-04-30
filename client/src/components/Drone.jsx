import { Box, Button, makeStyles, Typography } from '@material-ui/core'
import React, { useMemo } from 'react'
import { useDroneData } from '../hooks/useDroneData';
import DroneInfo from './DroneInfo';
import DroneMap from './DroneMap';

const useStyles = makeStyles(theme => ({
    root: {
        
    },
    container: {
        display: 'flex',
        justifyContent: 'stretch',
        width: '100%',
        height: 500,
    },
    actionsBox: {
        marginTop: 20,
        display: 'flex',
        justifyContent: 'center',
    },
    stateBox: {
        marginTop: 20, 
    },
    state: {
        fontSize: 32,
    },
}));

const Drone = () => {
    const classes = useStyles();
    const { loading, data, startTest } = useDroneData(100);

    if (loading || !data) {
        return (
            <div>Loading</div>
        )
    }

    const [lat, lon] = data.pos;
    const [dpLat, dpLon] = data.dronepoint_pos;

    return (
        <Box className={classes.root}>
            <Box className={classes.container}>
                <DroneInfo data={data}/>
                <DroneMap lat={lat} lon={lon} dpLat={dpLat} dpLon={dpLon} />
            </Box>
            <Box className={classes.actionsBox}>
                <Button variant="contained" color="primary" size="large"
                onClick={startTest} disabled={data.executing}>
                    <Typography variant="h3">Execute Test</Typography>
                </Button>
            </Box>
            <Box className={classes.stateBox}>
                <Typography variant="h2" align="center" className={classes.state}>
                    {data.state}
                </Typography>
            </Box>
        </Box>
    )
}

export default Drone
