# PromptLab Frontend

A modern, responsive React application for managing and organizing AI prompts with version control, collections, and advanced filtering capabilities.

## 🚀 Features

- **Prompt Management**: Full CRUD operations for AI prompts
- **Version Control**: Track, compare, and revert prompt versions
- **Collections**: Organize prompts into collections
- **Advanced Filtering**: Filter by tags, collections, and search
- **Dark/Light Theme**: Toggle between themes with persistence
- **Keyboard Shortcuts**: Power user features for quick navigation
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Toast Notifications**: Real-time feedback for all operations
- **Custom Dialogs**: Professional confirmation dialogs

## 📋 Prerequisites

- Node.js 16.x or higher
- npm 8.x or higher
- Backend API running on http://localhost:8000

## 🛠️ Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Configure environment variables**:
   Create a `.env` file in the frontend directory:
   ```env
   VITE_API_URL=http://localhost:8000
   ```

## 🏃 Running the Application

### Development Mode

Start the development server with hot reload:

```bash
npm run dev
```

The application will be available at http://localhost:5173

### Production Build

Build the application for production:

```bash
npm run build
```

Preview the production build:

```bash
npm run preview
```

### Linting

Run ESLint to check code quality:

```bash
npm run lint
```

## 📁 Project Structure

```
frontend/
├── public/
│   └── favicon.svg              # Custom PromptLab favicon
├── src/
│   ├── components/              # Reusable UI components
│   │   ├── Button.jsx           # Button with variants
│   │   ├── ConfirmDialog.jsx    # Confirmation dialogs
│   │   ├── CopyButton.jsx       # Copy to clipboard
│   │   ├── ErrorMessage.jsx     # Error display
│   │   ├── HighlightedText.jsx  # Text highlighting
│   │   ├── Icons.jsx            # Icon components
│   │   ├── KeyboardShortcutsHelp.jsx  # Shortcuts help modal
│   │   ├── LoadingSpinner.jsx   # Loading indicators
│   │   ├── Modal.jsx            # Modal dialogs
│   │   ├── PromptCard.jsx       # Prompt card display
│   │   ├── PromptPreview.jsx    # Prompt preview
│   │   ├── SearchBar.jsx        # Search input
│   │   ├── ThemeToggle.jsx      # Theme switcher
│   │   ├── Toast.jsx            # Toast notifications
│   │   └── index.js             # Component exports
│   ├── hooks/                   # Custom React hooks
│   │   ├── useClipboard.js      # Clipboard operations
│   │   ├── useKeyboardShortcuts.js  # Keyboard shortcuts
│   │   ├── useTheme.js          # Theme management
│   │   └── useToast.js          # Toast notifications
│   ├── pages/                   # Page components
│   │   ├── Collections.jsx      # Collections management
│   │   ├── PromptDetail.jsx     # Prompt detail view
│   │   ├── PromptForm.jsx       # Create/edit prompt
│   │   └── PromptList.jsx       # Prompts listing
│   ├── services/                # API services
│   │   └── api.js               # API client
│   ├── utils/                   # Utility functions
│   │   └── searchUtils.js       # Search utilities
│   ├── App.jsx                  # Main app component
│   ├── App.css                  # App styles
│   ├── main.jsx                 # Entry point
│   └── index.css                # Global styles
├── .env                         # Environment variables
├── .gitignore                   # Git ignore rules
├── eslint.config.js             # ESLint configuration
├── index.html                   # HTML template
├── package.json                 # Dependencies
├── vite.config.js               # Vite configuration
└── README.md                    # This file
```

## 🎨 Tech Stack

- **React 18**: UI library
- **React Router 6**: Client-side routing
- **Axios**: HTTP client for API calls
- **Vite**: Build tool and dev server
- **CSS Modules**: Component-scoped styling
- **ESLint**: Code quality and linting

## 🎯 Key Features

### Prompt Management
- Create, read, update, and delete prompts
- Rich text content with descriptions
- Tag-based organization
- Collection assignment
- Version history tracking

### Version Control
- Automatic version creation on updates
- View all versions of a prompt
- Compare two versions side-by-side
- Revert to previous versions
- Version metadata (date, version number)

### Collections
- Create and manage collections
- Organize prompts by collection
- View prompt counts per collection
- Quick navigation to collection prompts
- Search collections by name or description

### Filtering & Search
- Filter by collection
- Filter by multiple tags (AND logic)
- Full-text search across title and content
- Sort by date or title
- Active filter display with clear option

### User Experience
- Dark/light theme toggle with persistence
- Toast notifications for all operations
- Custom confirmation dialogs
- Loading states for async operations
- Error handling with retry options
- Empty states with helpful messages
- Responsive design for all screen sizes

### Keyboard Shortcuts
- `Cmd/Ctrl + K`: Focus search bar
- `Cmd/Ctrl + P`: Create new prompt
- `Cmd/Ctrl + C`: Create new collection
- `?`: Toggle shortcuts help
- `Escape`: Close modals

## 🔌 API Integration

The frontend communicates with the backend API at `http://localhost:8000`. All API calls are handled through the `services/api.js` module.

### API Endpoints Used

**Prompts:**
- `GET /prompts` - List all prompts
- `GET /prompts/{id}` - Get single prompt
- `POST /prompts` - Create prompt
- `PUT /prompts/{id}` - Update prompt
- `PATCH /prompts/{id}` - Partial update
- `DELETE /prompts/{id}` - Delete prompt

**Collections:**
- `GET /collections` - List collections
- `GET /collections/{id}` - Get collection
- `POST /collections` - Create collection
- `DELETE /collections/{id}` - Delete collection

**Tags:**
- `GET /tags` - List all tags
- `GET /tags/popular` - Get popular tags

**Versions:**
- `GET /prompts/{id}/versions` - List versions
- `GET /prompts/{id}/versions/{version}` - Get version
- `POST /prompts/{id}/versions/{version}/revert` - Revert version
- `GET /prompts/{id}/versions/compare` - Compare versions

## 🎨 Theming

The application supports dark and light themes. Theme preference is stored in localStorage and persists across sessions.

**CSS Variables:**
- `--bg-color`: Background color
- `--text-color`: Text color
- `--primary-color`: Primary brand color
- `--secondary-color`: Secondary color
- `--border-color`: Border color
- `--card-bg`: Card background
- And many more...

## 🧪 Development

### Code Style

The project uses ESLint for code quality. Run linting with:

```bash
npm run lint
```

### Component Guidelines

1. **Functional Components**: Use function components with hooks
2. **Props Validation**: Use PropTypes or TypeScript
3. **CSS Modules**: One CSS file per component
4. **Reusability**: Extract common patterns into reusable components
5. **Accessibility**: Include ARIA labels and keyboard navigation

### State Management

- Local state with `useState` for component-specific data
- Custom hooks for shared logic
- Props drilling for parent-child communication
- No global state management library (Redux, etc.)

## 📱 Responsive Design

The application is fully responsive with breakpoints:

- **Desktop**: 1024px and above
- **Tablet**: 768px - 1023px
- **Mobile**: Below 768px

## 🔒 Security

- Environment variables for API URLs
- No sensitive data in localStorage
- CORS handled by backend
- Input validation on forms
- XSS prevention through React's built-in escaping

## 🐛 Troubleshooting

### Backend Connection Issues

If you see "Failed to load data" errors:

1. Ensure backend is running on http://localhost:8000
2. Check `.env` file has correct `VITE_API_URL`
3. Verify CORS is enabled on backend
4. Check browser console for detailed errors

### Build Issues

If build fails:

1. Delete `node_modules` and `package-lock.json`
2. Run `npm install` again
3. Clear Vite cache: `rm -rf node_modules/.vite`
4. Try building again: `npm run build`

### Theme Not Persisting

If theme doesn't persist:

1. Check browser localStorage is enabled
2. Clear localStorage: `localStorage.clear()`
3. Refresh the page

## 📚 Additional Documentation

- [UI Features Guide](../docs/UI_FEATURES.md) - Detailed UI features documentation
- [API Reference](../docs/API_REFERENCE.md) - Backend API documentation
- [Project Brief](../PROJECT_BRIEF.md) - Project overview and requirements

## 🤝 Contributing

1. Follow the existing code style
2. Write meaningful commit messages
3. Test your changes thoroughly
4. Update documentation as needed
5. Run linting before committing

## 📄 License

This project is part of the PromptLab assignment.

## 🙏 Acknowledgments

- Built with React and Vite
- Icons and design inspired by modern web applications
- Blue gradient theme for professional appearance

---

**Need Help?** Check the [UI Features Guide](../docs/UI_FEATURES.md) for detailed feature documentation.
