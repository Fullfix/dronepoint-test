import { Box, makeStyles, Table, TableBody, TableCell, TableHead, TableRow, Typography } from '@material-ui/core'
import React from 'react'

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
                    {Object.entries(data).map(([key, value]) => (
                        <TableRow key={key}>
                            <TableCell>{key}</TableCell>
                            <TableCell>{value}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </Box>
    )
}

export default DroneInfo
