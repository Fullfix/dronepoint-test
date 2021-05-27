const Stream = require('node-rtsp-stream')
const stream = new Stream({
  name: 'name',
  streamUrl: 'rtsp://192.168.194.48:8554/video',
  wsPort: 5001,
  ffmpegOptions: { // options ffmpeg flags
    '-stats': '', // an option with no neccessary value uses a blank string
    '-r': 60, // options with required values specify the value after the key
    '-vf': 'select=concatdec_select',
    '-af': 'aselect=concatdec_select,aresample=async=1',
  }
})


// const rtsp = require('rtsp-ffmpeg');
// const app = require('express')();
// const cors = require('cors');

// app.use(cors());

// const server = require('http').Server(app);
// const io = require('socket.io')(server, { cors: { origin: '*' }});

// const stream = new rtsp.FFMpeg({ 
//   input: 'rtsp://192.168.194.48:8554/video',
//   rate: 18,
//   quality: 3,
//   arguments: [
//     '-t', '3540',
//     '-vf', 'select=concatdec_select',
//     '-af', 'aselect=concatdec_select,aresample=async=1',
//   ],
// })

// stream.on('error', e => {
//   console.log('error');
//   console.log(e);
// })

// stream.on('close', e => {
//   console.log('close');
//   console.log(e);
// })

// stream.on('data', e => {
//   console.log('data');
//   console.log(e);
// })

// stream.start();

// io.on('connection', (socket) => {
//   console.log('connection');
//   const pipeStream = (data) => {
//     console.log('sending');
//     console.log(data.toString('base64'));
//     socket.emit('data', data.toString('base64'))
//   }
//   stream.on('data', pipeStream);
//   socket.on('disconnect', () => {
//     stream.removeListener('data', pipeStream);
//   });
// })

// server.listen('5001', () => {
//   console.log('START SERVER');
// });