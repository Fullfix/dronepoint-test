import { useEffect, useState } from "react"
import { sendGetDataEvent, sendTestEvent, subscribeConnectEvent, subscribeDataEvent } from "../socket";

export const useDroneData = (timeout=2000) => {
    const [data, setData] = useState(null);
    const [droneConnected, setDroneConnected] = useState(false);
    const [dronepointConnected, setDronepointConnected] = useState(false);
    const [loading, setLoading] = useState(true);

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
    
    useEffect(() => {
        subscribeDataEvent(handleDataEvent);
        subscribeConnectEvent(handleConnectEvent);
        setInterval(() => {
            sendGetDataEvent();
        }, timeout);
    }, []);

    return {
        data: data,
        loading: loading,
        startTest: sendTestEvent,
        connection: { drone: droneConnected, dronepoint: dronepointConnected },
        isConnected: droneConnected && dronepointConnected,
    }
}