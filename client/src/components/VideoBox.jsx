import { Box, makeStyles, Typography } from '@material-ui/core'
import React, { useContext, useEffect, useRef, useState } from 'react'
import NotAvailable from './NotAvailable';
import JSMpeg from '@cycjimmy/jsmpeg-player';
import { DP_VIDEO_URL, sendGetVideoEvent, subscribeVideoEvent, unsubscribeVideoEvent } from '../socket';
import io from 'socket.io-client';

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

const VideoBox = ({ active, height, src, ws }) => {
    const classes = useStyles({ height });
    const imageRef = useRef();
    const [isValidSrc, setIsValidSrc] = useState(true);

    useEffect(() => {
        if (ws) {
            // const player = new JSMpeg.Player('ws://localhost:5001', {
            //     canvas: imageRef.current,
            // })
            // player.autoplay = true;
            // player.loop = true;
            const socket = io('http://localhost:5001');
            socket.on('data', data => {
                imageRef.current.src = 'data:image/jpeg;base64,' + data;
            })
            socket.on('connect', e => {
                console.log('Connect');
            })
        }
    }, []);

    const handleError = () => setIsValidSrc(false);

    if (!isValidSrc) return (
        <Box className={classes.root}>
            <NotAvailable />
        </Box>
    )
    
    return (
        <Box className={classes.root}>
            {!ws && <img className={classes.image} ref={imageRef} src={src} onError={handleError}/>}
            {/* {ws && <canvas className={classes.image} ref={imageRef} onError={handleError}/>} */}
            {ws && <img className={classes.image} ref={imageRef} src={src} />}
        </Box>
    )
}

export default VideoBox
