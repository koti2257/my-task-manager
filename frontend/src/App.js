import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [tasks, setTasks] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/tasks/', { withCredentials: true })
      .then(response => {
        setTasks(response.data);
      })
      .catch(error => {
        console.error('Error:', error);
        setError('Failed to fetch tasks. Please try again.');
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="App">
      <div className="container">
        <h1>Task Manager</h1>

        {loading ? (
          <p className="status">Loading...</p>
        ) : error ? (
          <p className="error">{error}</p>
        ) : tasks.length === 0 ? (
          <p className="status">No tasks found.</p>
        ) : (
          <ul className="task-list">
            {tasks.map((task) => (
              <li key={task.id} className="task-item">
                <h3>{task.title}</h3>
                <p>{task.description}</p>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default App;
