import io from 'socket.io-client';
import axios from 'axios'
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const hostname = 'http://localhost'

const socket = io(`${hostname}:5000`);

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

export const sendTestEvent = (password) => {
    socket.emit('test', { password });
}

export const login = async (password) => {
    try {
        await axios.post(`${hostname}:5000/login`, { password });
        return true
    } catch (err) {
        console.log(err);
        return false
    }
}