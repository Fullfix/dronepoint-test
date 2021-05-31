import { Box, makeStyles, Typography } from '@material-ui/core'
import React, { useContext, useEffect, useRef, useState } from 'react'
import NotAvailable from './NotAvailable';
import JSMpeg from '@cycjimmy/jsmpeg-player';
import { DP_VIDEO_URL, sendGetVideoEvent, subscribeVideoEvent, unsubscribeVideoEvent } from '../socket';
import { io } from 'socket.io-client';
import { encode } from '../utils/display';
import { DronepointContext } from '../contexts/DronepointProvider';

const useStyles = makeStyles(theme => ({
    root: {
        height: props => props.height,
        backgroundColor: '#F0F0F0',
    },
    image: {
        height: '100%',
        width: '100%',
    }
}));

const VideoBox = ({ active, height, src }) => {
    const classes = useStyles({ height });
    const imageRef = useRef();
    const [isValidSrc, setIsValidSrc] = useState(true);

    const handleError = () => setIsValidSrc(false);

    if (!isValidSrc) return (
        <Box className={classes.root}>
            <NotAvailable />
        </Box>
    )
    
    return (
        <Box className={classes.root}>
            <img className={classes.image} ref={imageRef} src={src} onError={handleError}/>
        </Box>
    )
}

export default VideoBox
