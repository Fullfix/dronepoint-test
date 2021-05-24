import { makeStyles } from '@material-ui/core'
import React from 'react'
import { DP_VIDEO_URL } from '../socket';

const useStyles = makeStyles(theme => ({
    root: {
        
    },
}));

const DronepointCam = () => {
    const classes = useStyles();
    return (
        <img src={DP_VIDEO_URL} />
    )
}

export default DronepointCam
