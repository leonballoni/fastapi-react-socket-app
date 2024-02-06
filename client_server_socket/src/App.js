import './App.css';
import React, { useState } from "react"
import LoginModal from './components/LoginModal';
import { SocketConnector, SocketRooms, SocketStatusUser, SocketMessage } from './components/SocketComponents';

function App() {
  const [username, setUsername] = useState('');
  // const [activeusers, setActiveUsers] = useState([]);
  const [login, setLogin] = useState(false);
  const [room_id, setRoom] = useState(''); // id of chat that selected

  const handleLogin = (user, login) => {
    setUsername(user);
    setLogin(login);
  };

  const handleRoomClick = ( room_id ) => {
    setRoom(room_id);
    // console.log(room_id);
  }

  return (
  <>
  <div>
      <LoginModal onLogin={handleLogin}/>
  </div>
  <div  className="container">
    <div className="chats">
      <SocketRooms onRoomClick={handleRoomClick}/>
      <div className="status">
        <SocketStatusUser/>
      </div>
    </div>
      <div className='right-container'>
        <SocketMessage username={username} room_id={room_id}/>
      </div>   
    </div>
  <SocketConnector
    username={username}
    login={login}/>
    
  </>
  );
}

export default App;
