import { Box, Button, makeStyles, Typography, useMediaQuery } from '@material-ui/core'
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
        [theme.breakpoints.down('sm')]: {
            paddingBottom: 10,
        }
    },
    cellsSelect: {
        marginBottom: 10,
        width: 300,
    },
    stateBox: {
        marginTop: 20, 
        [theme.breakpoints.down('sm')]: {
            marginTop: 10,
        }
    },
    state: {
        fontSize: 32,
        [theme.breakpoints.down('sm')]: {
            fontSize: 28,
        }
    },
    buttonBox: {
        padding: 20,
        paddingBottom: 0,
        paddingTop: 0,
        display: 'flex',
        flexDirection: 'column',
        [theme.breakpoints.down('sm')]: {
            padding: 0,
        },
    },
    button: {
        width: 400,
        marginBottom: 10,
        [theme.breakpoints.down('sm')]: {
            width: 300,
        },
    },
}));

const ActionBox = ({ cell, allCells, onCellChange, onTest }) => {
    const classes = useStyles();
    const { data, isConnected, connection } = useContext(DronepointContext); 
    const [open, setOpen] = useState(false);
    const [testType, setTestType] = useState(null);
    const isMobile = useMediaQuery(theme => theme.breakpoints.down('sm'));

    const handleSubmit = (password) => {
        onTest(password, testType);
        setTestType(null);
        setOpen(false);
    }

    const handleOpen = (newTestType) => () => {
        setOpen(true);
        setTestType(newTestType);
    };
    const handleClose = () => {
        setOpen(false);
        setTestType(null);
    };

    const droneDisabled = data.executing || !connection.drone;
    const dronepointDisabled = data.executing || !connection.dronepoint;
    const fullDisabled = data.executing || !isConnected;


    return (
        <Box className={classes.root}>
            <LoginDialog 
            open={open}
            onClose={handleClose} onSubmit={handleSubmit} />
            <Typography variant="h2">Choose a cell</Typography>
            <Cells 
            allCells={allCells} 
            value={cell} 
            onChange={onCellChange}
            className={classes.cellsSelect} 
            disabled={dronepointDisabled} 
            />
            <Box className={classes.buttonBox}>
                <Button 
                className={classes.button}
                variant="contained" 
                color="primary" 
                size={isMobile ? 'small' : 'large'}
                onClick={handleOpen('drone')}
                disabled={droneDisabled}
                >
                    <Typography variant={isMobile ? 'h5' : 'h4'}>Execute Test (Drone)</Typography>
                </Button>
                <Button 
                className={classes.button}
                variant="contained" 
                
                color="primary" 
                size={isMobile ? 'small' : 'large'}
                onClick={handleOpen('dronepoint')}
                disabled={dronepointDisabled}
                >
                    <Typography variant={isMobile ? 'h5' : 'h4'}>Execute Test (Dronepoint)</Typography>
                </Button>
                <Button 
                className={classes.button}
                variant="contained" 
                color="primary" 
                size={isMobile ? 'small' : 'large'}
                onClick={handleOpen('full')}
                disabled={fullDisabled}
                >
                    <Typography variant={isMobile ? 'h5' : 'h4'}>Execute Test (Full Iteration)</Typography>
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

export default ActionBox
