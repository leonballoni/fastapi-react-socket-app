
import React, { useState } from 'react';
import Modal from 'react-modal';

const LoginModal = ({ onLogin }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(true);

  const handleUsernameChange = (e) => {
    setUsername(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const handleSubmit = async () => {
    // Handle form submission, e.g., send data to the server
    try {
      const resp = await fetch(`${process.env.REACT_APP_API_URL}/auth`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(
          {
            username: username,
            password: password,
          }
        ),
      });
      if (!resp.ok) {
        throw new Error('Network response for Auth is not working')
      }
      onLogin(username, true);
      setIsModalOpen(false); // Close the modal on successful authentication
       // Call the onLogin prop with the username
    } catch (error) {
      console.error(`Error making authentication request: ${error.message}`);
      // Handle authentication error
    }
};

  const handleKeyPress = (event) => {
    if (event.key === 'Enter'){
      event.preventDefault();
      handleSubmit();
    } else if (event.key === 'Tab'){
      event.preventDefault();
      const inputs = document.getElementsByTagName('input');
      const currentIndex = Array.from(inputs).indexOf(event.target);
      const nextIndex = (currentIndex + 1) % inputs.length;
      inputs[nextIndex].focus(); // Move focus to the next input
    }
  };

  return (
    <Modal
      isOpen={isModalOpen}
      onRequestClose={() => setIsModalOpen(false)}
      contentLabel="Login Modal"
      shouldCloseOnOverlayClick={false}
      className="login-modal"
      appElement={document.getElementById('root')}
    >
      <div className='login-box'>
        <h2>Login</h2>
        <label>
          Username:
          <input type="text" value={username} onChange={handleUsernameChange} onKeyDown={handleKeyPress}/>
        </label>
        <label>
          Password:
          <input type="password" value={password} onChange={handlePasswordChange} onKeyDown={handleKeyPress}/>
        </label>
        <button onClick={handleSubmit}>Enter</button>
      </div>
    </Modal>
  );
};

export default LoginModal;
