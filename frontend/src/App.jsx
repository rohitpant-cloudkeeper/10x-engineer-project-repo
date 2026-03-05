import { BrowserRouter as Router, Routes, Route, NavLink, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import './App.css';
import PromptList from './pages/PromptList';
import PromptForm from './pages/PromptForm';
import PromptDetail from './pages/PromptDetail';
import Collections from './pages/Collections';
import ThemeToggle from './components/ThemeToggle';
import KeyboardShortcutsHelp from './components/KeyboardShortcutsHelp';
import { useTheme } from './hooks/useTheme';
import { useKeyboardShortcuts } from './hooks/useKeyboardShortcuts';

function AppContent() {
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();
  const [showShortcuts, setShowShortcuts] = useState(false);

  useKeyboardShortcuts([
    {
      key: 'k',
      ctrl: true,
      callback: (e) => {
        e.preventDefault();
        const searchInput = document.querySelector('.search-input');
        if (searchInput) searchInput.focus();
      }
    },
    {
      key: 'n',
      ctrl: true,
      callback: (e) => {
        e.preventDefault();
        navigate('/prompts/new');
      }
    },
    {
      key: '?',
      ctrl: false,
      callback: (e) => {
        e.preventDefault();
        setShowShortcuts(prev => !prev);
      }
    }
  ]);

  return (
    <div className="app">
      <nav className="navbar">
        <div className="nav-container">
          <NavLink to="/" className="nav-logo">
            PromptLab
          </NavLink>
          <ul className="nav-menu">
            <li className="nav-item">
              <NavLink to="/" end className="nav-link">
                Prompts
              </NavLink>
            </li>
            <li className="nav-item">
              <NavLink to="/collections" className="nav-link">
                Collections
              </NavLink>
            </li>
            <li className="nav-item">
              <ThemeToggle theme={theme} onToggle={toggleTheme} />
            </li>
          </ul>
        </div>
      </nav>

      <main className="main-content">
        <Routes>
          <Route path="/" element={<PromptList />} />
          <Route path="/prompts/new" element={<PromptForm />} />
          <Route path="/prompts/:id" element={<PromptDetail />} />
          <Route path="/prompts/:id/edit" element={<PromptForm />} />
          <Route path="/collections" element={<Collections />} />
        </Routes>
      </main>
      
      <KeyboardShortcutsHelp 
        isOpen={showShortcuts} 
        onClose={() => setShowShortcuts(false)} 
      />
    </div>
  );
}

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default App;
