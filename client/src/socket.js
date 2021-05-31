import io from 'socket.io-client';
import axios from 'axios'
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

export const DRONE_CAMERA_URL = 'http://192.168.194.120:8080/stream?topic=/main_camera/image_raw';

const socket = io(`/`);

export const subscribeDataEvent = (cb) => {
    socket.on('data', cb);
}

export const subscribeConnectEvent = (cb) => {
    socket.on('connect', cb);
}

export const subscribeErrorEvent = (cb) => {
    socket.on('error', cb);
}

export const subscribeVideoEvent = (cb) => {
    socket.on('video', cb);
}

export const unsubscribeVideoEvent = () => {
    socket.removeAllListeners('video');
}

export const sendGetVideoEvent = () => {
    socket.emit('getvideo');
}

export const sendGetDataEvent = (password) => {
    socket.emit('getdata', { password });
}

export const sendTestEvent = (cell, password) => {
    socket.emit('test', { cell, password });
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