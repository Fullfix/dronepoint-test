import { Box, makeStyles, Table, TableBody, TableCell, TableHead, TableRow, Typography } from '@material-ui/core'
import React from 'react'
import { formattedValue } from '../utils/display';

const useStyles = makeStyles(theme => ({
    root: {
        flex: '40%',
        backgroundColor: '#FAFAFA',
        padding: 20,
    },
    title: {
        fontSize: '24px',
        fontWeight: 'bold',
    },
}));

const DroneInfo = ({ data }) => {
    const classes = useStyles();
    const displayData = {
        ...data,
        pos: `[${data.pos[0]}, ${data.pos[1]}]`,
    }
    return (
        <Box className={classes.root}>
            <Table size="small">
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
                            <TableCell>{key}</TableCell>
                            <TableCell>{formattedValue(value)}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </Box>
    )
}

export default DroneInfo
