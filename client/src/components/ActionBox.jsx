import { Box, Button, makeStyles, Typography } from '@material-ui/core'
import React, { useContext } from 'react'
import { DronepointContext } from '../contexts/DronepointProvider';
import { getAllCells } from '../utils/cells';
import Cells from './Cells';

const useStyles = makeStyles(theme => ({
    root: {
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
}));

const ActionBox = ({ cell, allCells, onCellChange, onTest }) => {
    const classes = useStyles();
    const { data, isConnected } = useContext(DronepointContext); 
    return (
        <Box className={classes.root}>
            <Typography variant="h2">Choose a cell</Typography>
            <Cells allCells={allCells} value={cell} onChange={onCellChange}
            className={classes.cellsSelect} 
            disabled={data.state !== 'idle' || !isConnected} />
            <Button variant="contained" color="primary" size="large"
            onClick={onTest} disabled={data.executing || !isConnected}>
                <Typography variant="h3">Execute Test</Typography>
            </Button>
            <Box className={classes.stateBox}>
                <Typography variant="h2" align="center" className={classes.state}>
                    {data.state}
                </Typography>
            </Box>
        </Box>
    )
}

export default ActionBox
