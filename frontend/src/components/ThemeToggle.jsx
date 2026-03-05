import { MoonIcon, SunIcon } from './Icons';
import './ThemeToggle.css';

function ThemeToggle({ theme, onToggle }) {
  return (
    <button 
      className="theme-toggle" 
      onClick={onToggle}
      aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
      title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
    >
      {theme === 'light' ? <MoonIcon size={20} /> : <SunIcon size={20} />}
    </button>
  );
}

export default ThemeToggle;
