import { Box, Button, makeStyles, Typography } from '@material-ui/core'
import React, { useContext, useState } from 'react'
import { DronepointContext } from '../contexts/DronepointProvider';
import { getAllCells } from '../utils/cells';
import Cells from './Cells';
import LoginDialog from './LoginDialog';

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
    const [open, setOpen] = useState(false);

    const handleSubmit = (password) => {
        onTest(password);
    }

    const handleOpen = () => setOpen(true);
    const handleClose = () => setOpen(false);

    const buttonDisabled = data.executing || !isConnected


    return (
        <Box className={classes.root}>
            <LoginDialog 
            open={open && !buttonDisabled}
            onClose={handleClose} onSubmit={handleSubmit} />
            <Typography variant="h2">Choose a cell</Typography>
            <Cells allCells={allCells} value={cell} onChange={onCellChange}
            className={classes.cellsSelect} 
            disabled={buttonDisabled} />
            <Button variant="contained" color="primary" size="large"
            onClick={handleOpen}
            disabled={buttonDisabled}
            >
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
