import socket from './Socket';
import React, { useState, useEffect, useCallback } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser } from '@fortawesome/free-solid-svg-icons';

export const SocketConnector = ({ username, login }) => {
  const [isConnected, setIsConnected] = useState(socket.connected);

  // Define handleDisconnect outside of the useEffect
  const handleDisconnect = useCallback(() => {
    socket.emit('status_user', { user: username, status: 'off' });
    setIsConnected(false);
    socket.disconnect();
  }, [username]);

  const handleBeforeUnload = useCallback(() => {
    socket.emit('status_user', { user: username, status: 'off' });
    socket.disconnect();
  }, [username]);

  useEffect(() => {
    if (login) {
      socket.connect();
      socket.emit('status_user', { user: username, status: 'on' });
      setIsConnected(true);
      socket.on('disconnect', handleDisconnect);
      window.addEventListener('beforeunload', handleBeforeUnload);
    }
    
    return () => {
      if (login) {
        socket.off('disconnect', handleDisconnect);
        window.removeEventListener('beforeunload', handleBeforeUnload);
      }
      // socket.emit('status_user', { user: username, status: 'off' });
      socket.disconnect();
    };
  }, [login, username]);

  const handleDisconnectClick = () => {
    // Call the disconnect handler when the button is clicked
    handleDisconnect();
    window.location.reload();
  };


  return (
    <>
      <div className={`pstatus ${isConnected ? 'on' : 'off'}`}>
        {/* status: {isConnected ? 'on' : 'off'} */}
        <button className='btn' onClick={handleDisconnectClick}>Disconnect</button>
      </div>
      
    </>
  );
};


export const SocketMessage = ({ username, room_id}) => {
  const [currentRoom, setCurrentRoom] = useState([]);
  const [sentMessage, setSentMessage] = useState('');
  // console.log(room_id);
  useEffect(() => {
    const handleJoinRoom = ({ Room }) => {
      setCurrentRoom(Room);      
      socket.emit('join_room', {"chat": Room.chat, "chat_id": Room.chat_id, "user": username})
    };
    const handleQuitRoom = () => {
      setCurrentRoom(null)
    };
    if (room_id){
      socket.emit("load_room", {"chat_id": room_id});
      socket.on('join_room', handleJoinRoom);
    }
    socket.on('left_room', handleQuitRoom);
    
    return () => {
      if (currentRoom) {
        socket.emit('left_room', {"chat": currentRoom.chat, "chat_id": currentRoom.chat_id, "user": username});
      }
      socket.off('left_room', handleQuitRoom);
      socket.off('join_room', handleJoinRoom);
    };
  }, [room_id]);

  const handleMessage = () => {
    if (sentMessage.trim() !== ''){
      socket.emit('send_message', {
        username: username,
        chat_id: currentRoom.chat_id,
        message: sentMessage
      });
    }
  }
  useEffect(() => {
    const handleReceivedMessage = ({newMessage}) => {
      // Handle the new message received from the backend
      console.log("New message: ", newMessage);
      setCurrentRoom(prevRoom => ({
        ...prevRoom,
        messages: [...prevRoom.messages, newMessage]
      }));
      setSentMessage('');
    };

    if (currentRoom) {
      // console.log(currentRoom);
      socket.on('send_message', handleReceivedMessage);
    }
    return () => {
      if (currentRoom) {
        socket.off('send_message', handleReceivedMessage);
      }
    };
  }, [currentRoom]);
  console.log("Current Room: ",currentRoom);
  return (
    <>
    <div className="chat">
    {currentRoom.length === 0 ? (
      <p> nenhuma mensagem </p>
        ):(
        <ul>
          {currentRoom.messages.map((message, index) => (
          <li key={index} className={username === message.owner ? 'owner' : 'other'}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <strong>{message.username}:</strong> {message.message} 
                </div> ({message.date})
              </div>
            </li>
          ))}
        </ul>
        )}
    </div>
    <div className="messages">
      <textarea 
        className="message-input"
        value = {sentMessage}
        onChange={(e) => setSentMessage(e.target.value)}
      ></textarea>
      <button className='button-input' onClick={handleMessage}>Send</button>
    </div>
    </>
  );
};


// Definir a recuperacão da sala clicada -> pegar msgs mais tuais qnd clicar ou qnd cehgar uma nova msg. evento load_room 
export const SocketRooms = ({ onRoomClick }) => {
  const [rooms, setRooms] = useState([]);

  useEffect(() => {
    const handleLoadRooms = (Rooms) => {
      setRooms(Rooms);
      // console.log(Rooms);
    };

    socket.on('load_rooms', handleLoadRooms)
    return () => {
      socket.off('load_rooms', handleLoadRooms);
    };
  }, [rooms]);

  return (
    <>
      <h2 align='center'>Chats</h2>
      <ul>
        {rooms.map(chat => (
          <li className='chats-list'
              key={chat.chat_id}
              onClick={() => onRoomClick( chat.chat_id )}>{chat.chat}</li>
        ))}
      </ul>
    </>
  );
{};
}

export const SocketStatusUser = ( ) => {
  const [connectedUsers, setconnectedUsers] = useState([]);
  useEffect(() => {
    const handleUsersConnected = (users) => {
      setconnectedUsers(users);
    };
    socket.on('users_connected', handleUsersConnected);
  return () => {
    socket.off('users_connected', handleUsersConnected);
    };
  }, [connectedUsers]);
  return (
    <ul className="status-list">
      {connectedUsers.map((connected_user) => (
        <li key={connected_user.sid}
            className="status-item"
            title={`${connected_user.user} is online`}>
          {connected_user.user.charAt(0).toUpperCase()} {/* Displaying the first letter of the user's name */}
          <FontAwesomeIcon icon={faUser} style={{ marginLeft: '2px'}} />
        </li>
      ))}
    </ul>
  );
};