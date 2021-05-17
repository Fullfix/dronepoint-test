import React, { createContext, useEffect, useRef, useState } from 'react'
import { toast } from 'react-toastify';
import { login, sendGetDataEvent, sendTestEvent, subscribeConnectEvent, 
    subscribeDataEvent, subscribeErrorEvent } from '../socket';

export const DronepointContext = createContext({
    data: {},
    loading: true,
    startTest: () => {},
    authenticate: async (password) => false,
    isAuthenticated: false,
    connection: { drone: false, dronepoint: false },      
    isConnected: false,
})

const DronepointProvider = ({ children, timeout=500 }) => {
    const [data, setData] = useState(null);
    const [droneConnected, setDroneConnected] = useState(false);
    const [dronepointConnected, setDronepointConnected] = useState(false);
    const [loading, setLoading] = useState(true);
    const [authenticated, setAuthenticated] = useState(false);
    const interval = useRef();

    const getPassword = () => localStorage.getItem('password');
    const setPassword = (code) => localStorage.setItem('password', code);

    const handleConnectEvent = () => {
        console.log('Connected');
        setLoading(false);
    }

    const handleDataEvent = (data) => {
        if (!data || !data.connection) return
        setDroneConnected(data.connection.drone);
        setDronepointConnected(data.connection.dronepoint);
        delete data.connection;
        setData(data);
    }

    const handleErrorEvent = (err) => {
        console.log(err);
        setAuthenticated(false);
    }

    const authenticate = async (code) => {
        const success = await login(code);
        if (success) {
            toast.success('Logged In');
            setPassword(code);
            setAuthenticated(true);
        } else {
            toast.error('Wrong Password');
        }
        return success;
    }
    
    useEffect(() => {
        subscribeDataEvent(handleDataEvent);
        subscribeConnectEvent(handleConnectEvent);
        subscribeErrorEvent(handleErrorEvent);

        if (login(getPassword())) {
            setAuthenticated(true);
        }
    }, []);

    useEffect(() => {
        if (authenticated) {
            interval.current = setInterval(() => {
                sendGetDataEvent(getPassword());
            }, timeout); 
        } else {
            clearInterval(interval.current);
        }
    }, [authenticated])

    return (
        <DronepointContext.Provider value={{
            data: data,
            loading: loading,
            startTest: sendTestEvent,
            connection: { drone: droneConnected, dronepoint: dronepointConnected },
            isConnected: droneConnected && dronepointConnected,
            authenticate: authenticate,
            isAuthenticated: authenticated,
        }}>
            {children}
        </DronepointContext.Provider>
    )
}

export default DronepointProvider