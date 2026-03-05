import { SearchIcon, XIcon } from './Icons';
import './SearchBar.css';

function SearchBar({ value, onChange, placeholder = 'Search...', onClear }) {
  return (
    <div className="search-bar">
      <span className="search-icon">
        <SearchIcon size={18} />
      </span>
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="search-input"
      />
      {value && (
        <button 
          className="search-clear" 
          onClick={onClear}
          aria-label="Clear search"
        >
          <XIcon size={16} />
        </button>
      )}
    </div>
  );
}

export default SearchBar;
