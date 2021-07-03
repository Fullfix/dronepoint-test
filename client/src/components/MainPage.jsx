import { Box, Divider, makeStyles } from '@material-ui/core'
import React, { useContext, useState } from 'react'
import { toast } from 'react-toastify';
import { DronepointContext } from '../contexts/DronepointProvider';
import { DP_VIDEO_URL, DRONE_CAMERA_URL } from '../socket';
import { getAllCells } from '../utils/cells';
import ActionBox from './ActionBox';
import DroneInfo from './DroneInfo';
import DroneMap from './DroneMap';
import Logo from './Logo';
import SystemStatus from './SystemStatus';
import VideoBox from './VideoBox';

const useStyles = makeStyles(theme => ({
    root: {

    },
    main: {
        display: 'flex',
        alignItems: 'flex-start',
    },
    left: {
        flex: '33%',
    },
    middle: {
        flex: '34%',
    },
    right: {
        flex: '33%',
    },
}));

const MainPage = () => {
    const classes = useStyles();
    const { data, startTest, isConnected, video } = useContext(DronepointContext);
    const [cell, setCell] = useState(0);
    const allCells = getAllCells();

    const handleTestStart = (password) => {
        if (isConnected) {
            startTest(allCells[cell], password)
        } else {
            toast.error('Drone or Dronepoint not connected');
        }
    }

    const handleCellChange = (e) => {
        setCell(e.target.value);
    }

    return (
        <React.Fragment>
            <Box className={classes.main}>
                <Box className={classes.left}>
                    <DroneMap height={400}/>
                    <Divider />
                    <DroneInfo height={360 + 16} />
                </Box>
                <Box className={classes.middle}>
                    <SystemStatus />
                    <Divider />
                    <ActionBox
                    allCells={allCells}
                    cell={cell} 
                    onCellChange={handleCellChange} 
                    onTest={handleTestStart}
                    />
                </Box>
                <Box className={classes.right}>
                    <VideoBox
                    active={true}
                    src={video.dronepoint}
                    height={400}
                    type="dronepoint"
                    />
                    <Divider />
                    <VideoBox
                    active={true}
                    ws={true}
                    type="drone"
                    src={'/'}
                    height={400}

                    />
                </Box>
            </Box>
        </React.Fragment>
    )
}

export default MainPage
