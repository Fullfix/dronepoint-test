// const Stream = require('node-rtsp-stream')
// const stream = new Stream({
//   name: 'name',
//   streamUrl: 'https://www.w3schools.com/html/mov_bbb.mp4',
//   wsPort: 5001,
//   ffmpegOptions: { // options ffmpeg flags
//     '-stats': '', // an option with no neccessary value uses a blank string
//     '-r': 60, // options with required values specify the value after the key
//     '-vf': 'select=concatdec_select',
//     '-af': 'aselect=concatdec_select,aresample=async=1',
//   }
// })


const rtsp = require('rtsp-ffmpeg');
const app = require('express')();
const cors = require('cors');

app.use(cors());

const server = require('http').Server(app);
const io = require('socket.io')(server, { cors: { origin: '*' }});

const stream = new rtsp.FFMpeg({ 
  input: 'https://www.w3schools.com/html/mov_bbb.mp4'
})

stream.on('error', e => {
  console.log('error');
  console.log(e);
})

stream.on('close', e => {
  console.log('close');
  console.log(e);
})

stream.on('data', e => {
  console.log('data');
  console.log(e);
})

stream.start();

io.on('connection', (socket) => {
  console.log('connection');
  const pipeStream = (data) => {
    console.log('sending');
    socket.emit('data', data.toString('base64'))
  }
  stream.on('data', pipeStream);
  socket.on('disconnect', () => {
    stream.removeListener('data', pipeStream);
  });
})

server.listen('5001', () => {
  console.log('START SERVER');
});