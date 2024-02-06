import io from 'socket.io-client'

const socket = io(process.env.REACT_APP_API_URL, {
  autoConnect: false,
  path: process.env.REACT_APP_SOCKET_PATH,
  transports: ['websocket'],
});
// console.log("Socket path: ", process.env.REACT_APP_SOCKET_PATH)
// console.log("Server url: ", process.env.REACT_APP_API_URL)

export default socket
