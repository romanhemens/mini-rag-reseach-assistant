import { useState } from 'react';
import { 
  Box, 
  Container, 
  CssBaseline, 
  ThemeProvider, 
  createTheme,
  Paper,
  Typography,
  TextField,
  Button,
  List,
  ListItem,
  ListItemText,
  CircularProgress,
  Alert
} from '@mui/material';
import { Send as SendIcon, Upload as UploadIcon } from '@mui/icons-material';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#9c27b0',
    },
  },
});

interface Message {
  text: string;
  isUser: boolean;
}

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [question, setQuestion] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isFileProcessed, setIsFileProcessed] = useState(false);

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (!selectedFile) return;

    setFile(selectedFile);
    setIsLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      if (!response.ok) throw new Error(data.message || 'Error processing file');

      setIsFileProcessed(true);
      setMessages(prev => [...prev, { text: 'PDF processed successfully! You can now ask questions.', isUser: false }]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error uploading file');
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuestionSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim() || !isFileProcessed) return;

    const userQuestion = question;
    setQuestion('');
    setMessages(prev => [...prev, { text: userQuestion, isUser: true }]);
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:5000/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: userQuestion }),
      });

      const data = await response.json();
      if (!response.ok) throw new Error(data.message || 'Error getting answer');

      setMessages(prev => [...prev, { text: data.answer, isUser: false }]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error getting answer');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="md" sx={{ height: '100vh', py: 4 }}>
        <Paper elevation={3} sx={{ height: '100%', display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
          <Box sx={{ p: 2, backgroundColor: 'primary.main', color: 'white' }}>
            <Typography variant="h5">Mini-RAG Assistant</Typography>
          </Box>

          {!isFileProcessed && (
            <Box sx={{ p: 3, textAlign: 'center' }}>
              <Button
                variant="contained"
                component="label"
                startIcon={<UploadIcon />}
                disabled={isLoading}
              >
                Upload PDF
                <input
                  type="file"
                  hidden
                  accept=".pdf"
                  onChange={handleFileUpload}
                />
              </Button>
              {file && <Typography sx={{ mt: 2 }}>Selected file: {file.name}</Typography>}
            </Box>
          )}

          {error && (
            <Alert severity="error" sx={{ m: 2 }}>
              {error}
            </Alert>
          )}

          <List sx={{ flexGrow: 1, overflow: 'auto', p: 2 }}>
            {messages.map((message, index) => (
              <ListItem
                key={index}
                sx={{
                  justifyContent: message.isUser ? 'flex-end' : 'flex-start',
                  mb: 1,
                }}
              >
                <Paper
                  sx={{
                    p: 2,
                    maxWidth: '70%',
                    backgroundColor: message.isUser ? 'primary.main' : 'grey.100',
                    color: message.isUser ? 'white' : 'text.primary',
                  }}
                >
                  <ListItemText primary={message.text} />
                </Paper>
              </ListItem>
            ))}
          </List>

          <Box
            component="form"
            onSubmit={handleQuestionSubmit}
            sx={{
              p: 2,
              borderTop: 1,
              borderColor: 'divider',
              display: 'flex',
              gap: 1,
            }}
          >
            <TextField
              fullWidth
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder={isFileProcessed ? "Ask a question about the PDF..." : "Upload a PDF first"}
              disabled={!isFileProcessed || isLoading}
              size="small"
            />
            <Button
              type="submit"
              variant="contained"
              disabled={!isFileProcessed || isLoading || !question.trim()}
              endIcon={isLoading ? <CircularProgress size={20} color="inherit" /> : <SendIcon />}
            >
              Send
            </Button>
          </Box>
        </Paper>
      </Container>
    </ThemeProvider>
  );
}

export default App;
