# Mini RAG Research Assistant Frontend

The frontend application for the Mini RAG Research Assistant, built with modern web technologies to provide a seamless user experience for document analysis and question answering.

## Features

- Modern, responsive user interface
- Real-time PDF upload and processing
- Interactive question-answering interface
- Usage metrics display
- Error handling and user feedback

## Prerequisites

- Node.js 16.x or higher
- npm 7.x or higher

## Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

## Development

To start the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Building for Production

To create a production build:

```bash
npm run build
```

The built files will be in the `dist` directory.

## Environment Variables

Create a `.env` file in the frontend directory with the following variables:

```
VITE_API_URL=http://localhost:5000
```

## Project Structure

```
frontend/
├── src/
│   ├── components/     # React components
│   ├── services/      # API services
│   ├── styles/        # CSS styles
│   ├── utils/         # Utility functions
│   └── App.jsx        # Main application component
├── public/            # Static assets
└── index.html         # Entry HTML file
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run linter
- `npm run test` - Run tests

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
