import { useState } from 'react';
import './Terminal.css';

function Terminal() {
  const [command, setCommand] = useState('');
  const [prevCommands, setPrevCommands] = useState([]);

  const handleCommandChange = (event) => {
    setCommand(event.target.value);
  };

  const handleCommandSubmit = (event) => {
    event.preventDefault();
   if (command === '') {
      setPrevCommands([...prevCommands, { command, output: '' }]);
    } else if (command === 'whoami') {
      setPrevCommands([...prevCommands, { command, output: 'I am a simple chatbot, made by @notwld with <3' }]);
    } else if (command === 'clear') {
      setPrevCommands([]);
    } else  {
      const getUrl = async () => {
        await fetch('http://127.0.0.1:8000/predict', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body:String(command),
        })
          .then((res) => res.json())
          .then((data) => {
            const output = (
              <span style={{ color: 'green' }}>{data}
              </span>
            );
            setPrevCommands([...prevCommands, { command, output }]);
          })
          .catch((err) =>
            setPrevCommands([...prevCommands, { command, output: err }])
          );
      };
      
      getUrl();
    } 
    setCommand('');
  };
  

  return (
    <div className="terminal">
      <div className="terminal-header">
        <span className="terminal-header-text">$ bash</span>
        <div className="terminal-header-icons">
          <div className="terminal-header-icon close"></div>
          <div className="terminal-header-icon maximize"></div>
          <div className="terminal-header-icon minimize"></div>
        </div>
      </div>
      <div className="terminal-body">
        {/* Display previous commands and outputs */}
        {prevCommands.map(({ command, output }, index) => (
          <div key={index}>
            <span className="terminal-prompt">$ {command}</span> <br />
            <span className="terminal-promptAns">{output}</span>
          </div>
        ))}
        {/* Display current input prompt */}
        <form onSubmit={handleCommandSubmit}>
          <div className="insideForm">
            <span className="terminal-prompt">$</span>
            <input
              type="text"
              className="terminal-input"
              value={command}
              onChange={handleCommandChange}
              autoFocus
              onKeyUp={(event) => {
                if (event.key === 'ArrowUp') {
                  setCommand(prevCommands[prevCommands.length - 1].command);
                }

              }
              }
            />
          </div>
        </form>
      </div>
    </div>
  );
}

export default Terminal;
