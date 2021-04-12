import { useEffect, useState } from "react"
import { sendGetDataEvent, sendTestEvent, subscribeConnectEvent, subscribeDataEvent } from "../socket";

export const useDroneData = (timeout=2000) => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    const handleConnectEvent = () => {
        console.log('Connected');
        setLoading(false);
    }

    const handleDataEvent = (data) => {
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
    }
}