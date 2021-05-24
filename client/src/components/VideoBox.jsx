import { Box, makeStyles, Typography } from '@material-ui/core'
import React from 'react'
import NotAvailable from './NotAvailable';

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

const VideoBox = ({ src, active, height }) => {
    const classes = useStyles({ height });

    if (!active) return (
        <Box className={classes.root}>
            <NotAvailable />
        </Box>
    )
    
    return (
        <Box className={classes.root}>
            <img src={src} className={classes.image} />
        </Box>
    )
}

export default VideoBox
