import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import PromptList from './pages/PromptList';
import PromptForm from './pages/PromptForm';
import Collections from './pages/Collections';

function App() {
  return (
    <Router>
      <div className="app">
        <nav className="navbar">
          <div className="nav-container">
            <Link to="/" className="nav-logo">
              PromptLab
            </Link>
            <ul className="nav-menu">
              <li className="nav-item">
                <Link to="/" className="nav-link">
                  Prompts
                </Link>
              </li>
              <li className="nav-item">
                <Link to="/collections" className="nav-link">
                  Collections
                </Link>
              </li>
              <li className="nav-item">
                <Link to="/prompts/new" className="nav-link nav-link-primary">
                  + New Prompt
                </Link>
              </li>
            </ul>
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<PromptList />} />
            <Route path="/prompts/new" element={<PromptForm />} />
            <Route path="/prompts/:id/edit" element={<PromptForm />} />
            <Route path="/collections" element={<Collections />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
