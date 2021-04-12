import io from 'socket.io-client';

const socket = io('http://localhost:5000');

export const subscribeDataEvent = (cb) => {
    socket.on('data', cb);
}

export const subscribeConnectEvent = (cb) => {
    socket.on('connect', cb);
}

export const sendGetDataEvent = () => {
    socket.emit('getdata');
}

export const sendTestEvent = () => {
    socket.emit('test');
}