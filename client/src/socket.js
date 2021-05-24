import io from 'socket.io-client';
import axios from 'axios'
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const socket = io(`/`);

export const DP_VIDEO_URL = 'http://localhost:5000/api/videos/dronepoint'

export const subscribeDataEvent = (cb) => {
    socket.on('data', cb);
}

export const subscribeConnectEvent = (cb) => {
    socket.on('connect', cb);
}

export const subscribeErrorEvent = (cb) => {
    socket.on('error', cb);
}

export const sendGetDataEvent = (password) => {
    socket.emit('getdata', { password });
}

export const sendTestEvent = (cell) => {
    socket.emit('test', { cell });
}

export const login = async (password) => {
    try {
        await axios.post(`/api/login`, { password });
        return true
    } catch (err) {
        console.log(err);
        return false
    }
}