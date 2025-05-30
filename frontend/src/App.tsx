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
  Alert,
  Drawer,
  IconButton,
  Divider,
  ListItemIcon,
  ListItemButton,
  Toolbar,
  AppBar,
  useMediaQuery,
  useTheme
} from '@mui/material';
import { 
  Send as SendIcon, 
  Upload as UploadIcon,
  Menu as MenuIcon,
  Description as FileIcon,
  Science as ScienceIcon,
  Close as CloseIcon
} from '@mui/icons-material';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#FF7F50', // Sunset orange
      light: '#FFA07A', // Light salmon
      dark: '#E67345', // Darker orange
    },
    secondary: {
      main: '#FF6347', // Tomato
    },
    background: {
      default: '#f5f5f5',
      paper: '#ffffff',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h5: {
      fontWeight: 600,
    },
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 8,
        },
      },
    },
  },
});

interface Message {
  text: string;
  isUser: boolean;
}

interface UploadedFile {
  id: string;
  name: string;
  isSelected: boolean;
}

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [question, setQuestion] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isFileProcessed, setIsFileProcessed] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const [isDrawerOpen, setIsDrawerOpen] = useState(true);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

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

      const newFile: UploadedFile = {
        id: Date.now().toString(),
        name: selectedFile.name,
        isSelected: true,
      };

      setUploadedFiles(prev => {
        const updated = prev.map(f => ({ ...f, isSelected: false }));
        return [...updated, newFile];
      });

      setIsFileProcessed(true);
      setMessages(prev => [...prev, { text: 'Document processed successfully! You can now ask questions.', isUser: false }]);
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
        body: JSON.stringify({ 
          question: userQuestion,
          fileId: uploadedFiles.find(f => f.isSelected)?.id 
        }),
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

  const toggleFileSelection = (fileId: string) => {
    setUploadedFiles(prev => 
      prev.map(f => ({
        ...f,
        isSelected: f.id === fileId
      }))
    );
  };

  const drawerWidth = 280;

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ display: 'flex', height: '100vh' }}>
        <AppBar 
          position="fixed" 
          sx={{ 
            zIndex: (theme) => theme.zIndex.drawer + 1,
            backgroundColor: 'primary.main'
          }}
        >
          <Toolbar>
            <IconButton
              color="inherit"
              edge="start"
              onClick={() => setIsDrawerOpen(!isDrawerOpen)}
              sx={{ mr: 2 }}
            >
              <MenuIcon />
            </IconButton>
            <ScienceIcon sx={{ mr: 1 }} />
            <Typography variant="h6" noWrap component="div">
              Your Personal Research Assistant
            </Typography>
          </Toolbar>
        </AppBar>

        <Drawer
          variant={isMobile ? "temporary" : "persistent"}
          open={isDrawerOpen}
          onClose={() => setIsDrawerOpen(false)}
          sx={{
            width: drawerWidth,
            flexShrink: 0,
            '& .MuiDrawer-paper': {
              width: drawerWidth,
              boxSizing: 'border-box',
              mt: '64px',
              height: 'calc(100% - 64px)',
            },
          }}
        >
          <Box sx={{ p: 2 }}>
            <Button
              variant="contained"
              component="label"
              startIcon={<UploadIcon />}
              disabled={isLoading}
              fullWidth
            >
              Upload Document
              <input
                type="file"
                hidden
                accept=".pdf"
                onChange={handleFileUpload}
              />
            </Button>
          </Box>
          <Divider />
          <List>
            {uploadedFiles.map((file) => (
              <ListItem key={file.id} disablePadding>
                <ListItemButton
                  selected={file.isSelected}
                  onClick={() => toggleFileSelection(file.id)}
                >
                  <ListItemIcon>
                    <FileIcon color={file.isSelected ? "primary" : "inherit"} />
                  </ListItemIcon>
                  <ListItemText 
                    primary={file.name}
                    primaryTypographyProps={{
                      noWrap: true,
                      style: { fontSize: '0.9rem' }
                    }}
                  />
                </ListItemButton>
              </ListItem>
            ))}
          </List>
        </Drawer>

        <Box
          component="main"
          sx={{
            flexGrow: 1,
            p: 3,
            width: { sm: `calc(100% - ${isDrawerOpen ? drawerWidth : 0}px)` },
            mt: '64px',
            height: 'calc(100vh - 64px)',
            transition: theme.transitions.create('width', {
              easing: theme.transitions.easing.sharp,
              duration: theme.transitions.duration.leavingScreen,
            }),
          }}
        >
          <Paper 
            elevation={3} 
            sx={{ 
              height: '100%', 
              display: 'flex', 
              flexDirection: 'column',
              overflow: 'hidden',
              backgroundColor: 'background.paper'
            }}
          >
            {error && (
              <Alert 
                severity="error" 
                sx={{ m: 2 }}
                action={
                  <IconButton
                    aria-label="close"
                    color="inherit"
                    size="small"
                    onClick={() => setError(null)}
                  >
                    <CloseIcon fontSize="inherit" />
                  </IconButton>
                }
              >
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
                      borderRadius: 2,
                    }}
                  >
                    <ListItemText 
                      primary={message.text}
                      primaryTypographyProps={{
                        style: { 
                          whiteSpace: 'pre-wrap',
                          wordBreak: 'break-word'
                        }
                      }}
                    />
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
                backgroundColor: 'background.paper'
              }}
            >
              <TextField
                fullWidth
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder={isFileProcessed ? "Ask a question about your documents..." : "Upload a document first"}
                disabled={!isFileProcessed || isLoading}
                size="small"
                multiline
                maxRows={4}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    borderRadius: 2,
                  }
                }}
              />
              <Button
                type="submit"
                variant="contained"
                disabled={!isFileProcessed || isLoading || !question.trim()}
                endIcon={isLoading ? <CircularProgress size={20} color="inherit" /> : <SendIcon />}
                sx={{ borderRadius: 2 }}
              >
                Send
              </Button>
            </Box>
          </Paper>
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default App;
