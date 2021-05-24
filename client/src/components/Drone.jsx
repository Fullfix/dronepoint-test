import { Box, Button, makeStyles, Typography } from '@material-ui/core'
import React, { useContext, useMemo, useState } from 'react'
import { toast } from 'react-toastify';
import { DronepointContext } from '../contexts/DronepointProvider';
import { getAllCells } from '../utils/cells';
import Cells from './Cells';
import DroneInfo from './DroneInfo';
import DroneMap from './DroneMap';
import DronepointCam from './DronepointCam';

const useStyles = makeStyles(theme => ({
    root: {
        height: '100%',
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
        flexDirection: 'column',
        alignItems: 'center',
    },
    cellsSelect: {
        marginBottom: 10,
        width: 300,
    },
    stateBox: {
        marginTop: 20, 
    },
    state: {
        fontSize: 32,
    },
    disconnectBox: {
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
        justifyContent: 'center',
        alignItems: 'center',
    },
    bottomBox: {
        display: 'flex',
        justifyContent: 'space-between',
    },
    camBox: {
        height: '350px',
        backgroundColor: 'black',
        width: '35%',
    },
}));

const Drone = () => {
    const classes = useStyles();
    const { data, startTest, isConnected, connection } = useContext(DronepointContext);
    const allCells = getAllCells();
    const [cell, setCell] = useState(0);

    if (!data) {
        return (
            <div>Loading</div>
        )
    }

    const handleClick = () => {
        if (connection.dronepoint) {
            startTest(allCells[cell])
        } else {
            toast.error('Dronepoint not connected');
        }
    }

    const handleCellChange = (e) => {
        setCell(e.target.value);
    }

    const [lat, lon] = data.pos;
    const [dpLat, dpLon] = data.dronepoint_pos;

    if (!connection.drone) return (
        <Box className={classes.root}>
            <Box className={classes.disconnectBox}>
                <Typography variant="h2">Not connected</Typography>
                <Typography variant="h2">
                    Drone: {connection.drone ? 'Connected' : 'Disconnected'}
                </Typography>
                <Typography variant="h2">
                    Dronepoint: {connection.dronepoint ? 'Connected' : 'Disconnected'}
                </Typography>
            </Box>
        </Box>
    )

    return (
        <Box className={classes.root}>
            <Box className={classes.container}>
                <DroneInfo data={data}/>
                <DroneMap lat={lat} lon={lon} dpLat={dpLat} dpLon={dpLon} />
            </Box>
            <Box className={classes.bottomBox}>
                <Box className={classes.camBox}>
                    <DronepointCam />
                </Box>
                <Box className={classes.actionsBox}>
                    <Typography variant="h2">Выберите ячейку</Typography>
                    <Cells allCells={allCells} value={cell} onChange={handleCellChange}
                    className={classes.cellsSelect} 
                    disabled={data.state !== 'idle'} />
                    <Button variant="contained" color="primary" size="large"
                    onClick={handleClick} disabled={data.executing}>
                        <Typography variant="h3">Execute Test</Typography>
                    </Button>
                    <Box className={classes.stateBox}>
                        <Typography variant="h2" align="center" className={classes.state}>
                            {data.state}
                        </Typography>
                    </Box>
                </Box>
                <Box className={classes.camBox}>
                    <DronepointCam />
                </Box>
            </Box>
        </Box>
    )
}

export default Drone
