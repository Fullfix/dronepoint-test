import { Box, makeStyles, Table, TableBody, TableCell, TableHead, TableRow, Typography } from '@material-ui/core'
import React, { useContext } from 'react'
import { DronepointContext } from '../contexts/DronepointProvider';
import { formattedValue } from '../utils/display';

const useStyles = makeStyles(theme => ({
    root: {
        backgroundColor: '#F0F0F0',
        padding: 20,
        height: props => props.height,
    },
    title: {
        fontSize: '24px',
    },
    table: {
        backgroundColor: 'white',
        height: '100%',
    },
}));

const DroneInfo = ({ height }) => {
    const classes = useStyles({ height });
    const { data } = useContext(DronepointContext);
    const displayData = {
        ...data,
        pos: `[${data.pos[0]}, ${data.pos[1]}]`,
        dronepoint_pos: `[${data.dronepoint_pos[0]}, ${data.dronepoint_pos[1]}]`,
        state: data.state.toUpperCase(),
    }
    return (
        <Box className={classes.root}>
            <Table size="small" className={classes.table}>
                <TableHead>
                    <TableRow>
                        <TableCell>
                            <Typography variant="h2" className={classes.title}>Key</Typography>
                        </TableCell>
                        <TableCell>
                            <Typography variant="h2" className={classes.title}>Value</Typography>
                        </TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {Object.entries(displayData).map(([key, value]) => (
                        <TableRow key={key}>
                            <TableCell>{key.toUpperCase()}</TableCell>
                            <TableCell>{formattedValue(value)}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </Box>
    )
}

export default DroneInfo
