import { Box, makeStyles } from '@material-ui/core'
import { Map, Placemark } from 'react-yandex-maps';
import React, { useCallback } from 'react'

const useStyles = makeStyles(theme => ({
    root: {
        flex: '60%',
    },
}));

const droneSize = 80;

const DroneMap = ({ lat, lon }) => {
    const classes = useStyles();
    const pos = [lat, lon];
    
    return (
        <Box className={classes.root}>
            <Map defaultState={{ center: pos, zoom: 15 }} width={'100%'} height={'100%'}>
                <Placemark geometry={pos} options={{
                    iconLayout: 'default#image',
                    iconImageHref: '/drone.png',
                    iconImageSize: [droneSize, droneSize],
                    iconImageOffset: [-droneSize / 2, -droneSize / 2],
                    iconShape: {
                        type: 'Circle',
                        coordinates: [0, 0],
                        radius: 20
                    },
                }}/>
            </Map>
        </Box>
    )
}

export default React.memo(DroneMap)
