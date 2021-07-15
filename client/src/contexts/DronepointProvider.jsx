import React, { createContext, useEffect, useRef, useState } from 'react'
import { toast } from 'react-toastify';
import { login, sendGetDataEvent, sendGetVideoEvent, sendTestEvent, subscribeConnectEvent, 
    subscribeDataEvent, subscribeErrorEvent, subscribeVideoEvent, unsubscribeVideoEvent } from '../socket';

export const DronepointContext = createContext({
    data: {},
    loading: true,
    startTest: (cell, password) => {},
    authenticate: async (password) => false,
    isAuthenticated: false,
    connection: { drone: false, dronepoint: false },
    video: { drone: null, dronepoint: null },      
    isConnected: false,
})

const DronepointProvider = ({ children, timeout=500 }) => {
    const [data, setData] = useState(null);
    const [droneConnected, setDroneConnected] = useState(false);
    const [dronepointConnected, setDronepointConnected] = useState(false);
    const [loading, setLoading] = useState(true);
    const [dpFrame, setDpFrame] = useState(null);
    const [droneFrame, setDroneFrame] = useState(null);

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
        toast.error(err);
    }
    
    useEffect(() => {
        subscribeDataEvent(handleDataEvent);
        subscribeConnectEvent(handleConnectEvent);
        subscribeErrorEvent(handleErrorEvent);

        let check = true;
        const handleVideoEvent = (data) => {
            setDpFrame(URL.createObjectURL(
                new Blob([data.dronepoint], { type: 'image/jpeg' })
            ))
            setDroneFrame(URL.createObjectURL(
                new Blob([data.drone], { type: 'image/jpeg' })
            ))
            check = true
        }

        subscribeVideoEvent(handleVideoEvent);
        
        const interval = setInterval(() => {
            if (check) {
                sendGetVideoEvent();
                check = false;
            }
        }, 20);

        const dataInterval = setInterval(() => {
            sendGetDataEvent();
        }, timeout);

        return () => {
            clearInterval(interval);
            clearInterval(dataInterval);
            unsubscribeVideoEvent();
        }
    }, []);

    return (
        <DronepointContext.Provider value={{
            data: data,
            loading: loading,
            startTest: (cell, password, testType) => sendTestEvent(cell, password, testType),
            connection: { drone: droneConnected, dronepoint: dronepointConnected },
            isConnected: dronepointConnected,
            video: { drone: droneFrame, dronepoint: dpFrame },
        }}>
            {children}
        </DronepointContext.Provider>
    )
}

export default DronepointProvider
