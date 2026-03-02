# PromptLab Frontend

React frontend for the PromptLab AI Prompt Engineering Platform.

## Tech Stack

- React 18
- Vite 5
- React Router 6
- Axios
- CSS3

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

```bash
npm install
```

### Development

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### Build

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
src/
├── components/     # Reusable UI components
├── pages/          # Page components
├── services/       # API services
├── hooks/          # Custom React hooks
├── utils/          # Utility functions
├── App.jsx         # Main app component
└── main.jsx        # Entry point
```

## Environment Variables

Create a `.env` file in the root directory:

```
VITE_API_URL=http://localhost:8000
```

## Features

- ✅ Prompt list/grid view
- ✅ Create, edit, delete prompts
- ✅ Collections management
- ✅ Tag filtering
- ✅ Responsive design
- ✅ Loading states
- ✅ Error handling
