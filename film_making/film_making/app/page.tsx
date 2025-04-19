'use client';

import { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Stepper,
  Step,
  StepLabel,
  Button,
  Paper,
  TextField,
  CircularProgress,
  Grid,
  Card,
  CardContent,
  Divider,
  Chip,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  AppBar,
  Toolbar,
  IconButton,
  Avatar,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  ThemeProvider,
  createTheme,
  CssBaseline
} from '@mui/material';

// Icons
import MenuIcon from '@mui/icons-material/Menu';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import CalendarMonthIcon from '@mui/icons-material/CalendarMonth';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';
import ShortTextIcon from '@mui/icons-material/ShortText';
import PeopleIcon from '@mui/icons-material/People';
import SyncIcon from '@mui/icons-material/Sync';
import BarChartIcon from '@mui/icons-material/BarChart';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import MovieIcon from '@mui/icons-material/Movie';
import DownloadIcon from '@mui/icons-material/Download';
import DarkModeIcon from '@mui/icons-material/DarkMode';
import LightModeIcon from '@mui/icons-material/LightMode';
import InfoIcon from '@mui/icons-material/Info';

// Create custom theme with enhanced design
const lightTheme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#4361ee', // Modern blue
      light: '#738bff',
      dark: '#2c41bb',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#f72585', // Vibrant pink
      light: '#ff5eb1',
      dark: '#c0005c',
      contrastText: '#ffffff',
    },
    background: {
      default: '#f8f9fa',
      paper: '#ffffff',
    },
    success: {
      main: '#06d6a0', // Teal
    },
    warning: {
      main: '#ffd166', // Amber
    },
    error: {
      main: '#ef476f', // Coral red
    },
    info: {
      main: '#118ab2', // Blue
    },
    text: {
      primary: '#2b2d42',
      secondary: '#575a7b',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontWeight: 800,
      letterSpacing: '-0.025em',
    },
    h2: {
      fontWeight: 700,
      letterSpacing: '-0.025em',
    },
    h3: {
      fontWeight: 700,
      letterSpacing: '-0.015em',
    },
    h4: {
      fontWeight: 700,
      letterSpacing: '-0.01em',
    },
    h5: {
      fontWeight: 600,
    },
    h6: {
      fontWeight: 600,
    },
    button: {
      fontWeight: 600,
    },
    subtitle1: {
      fontWeight: 500,
    },
    subtitle2: {
      fontWeight: 500,
    },
  },
  shape: {
    borderRadius: 12,
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          scrollbarWidth: 'thin',
          '&::-webkit-scrollbar': {
            width: '8px',
            height: '8px',
          },
          '&::-webkit-scrollbar-track': {
            background: '#f1f1f1',
          },
          '&::-webkit-scrollbar-thumb': {
            background: '#c1c1c1',
            borderRadius: '4px',
          },
          '&::-webkit-scrollbar-thumb:hover': {
            background: '#a8a8a8',
          },
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: 12,
          padding: '10px 24px',
          fontWeight: 600,
          boxShadow: 'none',
          transition: 'all 0.2s ease-in-out',
          '&:hover': {
            transform: 'translateY(-2px)',
            boxShadow: '0 6px 20px rgba(67, 97, 238, 0.15)',
          },
        },
        contained: {
          '&:hover': {
            boxShadow: '0 8px 25px rgba(67, 97, 238, 0.25)',
          },
        },
        outlined: {
          borderWidth: '2px',
          '&:hover': {
            borderWidth: '2px',
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: '0 10px 30px 0 rgba(0,0,0,0.05)',
          borderRadius: 20,
          transition: 'transform 0.3s ease, box-shadow 0.3s ease',
          overflow: 'hidden',
          '&:hover': {
            transform: 'translateY(-5px)',
            boxShadow: '0 20px 40px 0 rgba(0,0,0,0.09)',
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 16,
        },
        elevation1: {
          boxShadow: '0 2px 12px 0 rgba(0,0,0,0.05)',
        },
        elevation2: {
          boxShadow: '0 4px 16px 0 rgba(0,0,0,0.08)',
        },
        elevation3: {
          boxShadow: '0 8px 20px 0 rgba(0,0,0,0.1)',
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          boxShadow: '0 2px 15px 0 rgba(0,0,0,0.05)',
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: 12,
            transition: 'box-shadow 0.2s ease-in-out',
            '&:hover': {
              boxShadow: '0 0 0 4px rgba(67, 97, 238, 0.1)',
            },
            '&.Mui-focused': {
              boxShadow: '0 0 0 4px rgba(67, 97, 238, 0.2)',
            },
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          fontWeight: 500,
        },
      },
    },
    MuiStepLabel: {
      styleOverrides: {
        label: {
          fontWeight: 500,
        },
      },
    },
    MuiAccordion: {
      styleOverrides: {
        root: {
          borderRadius: '16px !important',
          overflow: 'hidden',
          '&:before': {
            display: 'none',
          },
          '&.Mui-expanded': {
            margin: '16px 0',
          },
        },
      },
    },
    MuiAccordionSummary: {
      styleOverrides: {
        root: {
          borderRadius: 16,
        },
      },
    },
    MuiListItem: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          transition: 'all 0.2s ease',
        },
      },
    },
    MuiDrawer: {
      styleOverrides: {
        paper: {
          borderRight: 'none',
        },
      },
    },
  },
});

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#738bff', // Lighter blue for dark mode
      light: '#a4b8ff',
      dark: '#4361ee',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#ff5eb1', // Lighter pink for dark mode
      light: '#ff90d1',
      dark: '#f72585',
      contrastText: '#ffffff',
    },
    background: {
      default: '#0a1929', // Deep blue-black
      paper: '#132f4c', // Navy blue
    },
    success: {
      main: '#06d6a0', // Teal
    },
    warning: {
      main: '#ffd166', // Amber
    },
    error: {
      main: '#ef476f', // Coral red
    },
    info: {
      main: '#118ab2', // Blue
    },
    text: {
      primary: '#e6f1ff',
      secondary: '#b0bec5',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontWeight: 800,
      letterSpacing: '-0.025em',
    },
    h2: {
      fontWeight: 700,
      letterSpacing: '-0.025em',
    },
    h3: {
      fontWeight: 700,
      letterSpacing: '-0.015em',
    },
    h4: {
      fontWeight: 700,
      letterSpacing: '-0.01em',
    },
    h5: {
      fontWeight: 600,
    },
    h6: {
      fontWeight: 600,
    },
    button: {
      fontWeight: 600,
    },
    subtitle1: {
      fontWeight: 500,
    },
    subtitle2: {
      fontWeight: 500,
    },
  },
  shape: {
    borderRadius: 12,
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          scrollbarWidth: 'thin',
          '&::-webkit-scrollbar': {
            width: '8px',
            height: '8px',
          },
          '&::-webkit-scrollbar-track': {
            background: '#132f4c',
          },
          '&::-webkit-scrollbar-thumb': {
            background: '#2c4c6e',
            borderRadius: '4px',
          },
          '&::-webkit-scrollbar-thumb:hover': {
            background: '#3a6491',
          },
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: 12,
          padding: '10px 24px',
          fontWeight: 600,
          boxShadow: 'none',
          transition: 'all 0.2s ease-in-out',
          '&:hover': {
            transform: 'translateY(-2px)',
            boxShadow: '0 6px 20px rgba(115, 139, 255, 0.25)',
          },
        },
        contained: {
          '&:hover': {
            boxShadow: '0 8px 25px rgba(115, 139, 255, 0.35)',
          },
        },
        outlined: {
          borderWidth: '2px',
          '&:hover': {
            borderWidth: '2px',
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: '0 10px 30px 0 rgba(0,0,0,0.2)',
          borderRadius: 20,
          transition: 'transform 0.3s ease, box-shadow 0.3s ease',
          overflow: 'hidden',
          '&:hover': {
            transform: 'translateY(-5px)',
            boxShadow: '0 20px 40px 0 rgba(0,0,0,0.3)',
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 16,
        },
        elevation1: {
          boxShadow: '0 2px 12px 0 rgba(0,0,0,0.2)',
        },
        elevation2: {
          boxShadow: '0 4px 16px 0 rgba(0,0,0,0.25)',
        },
        elevation3: {
          boxShadow: '0 8px 20px 0 rgba(0,0,0,0.3)',
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          boxShadow: '0 2px 15px 0 rgba(0,0,0,0.15)',
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: 12,
            transition: 'box-shadow 0.2s ease-in-out',
            '&:hover': {
              boxShadow: '0 0 0 4px rgba(115, 139, 255, 0.15)',
            },
            '&.Mui-focused': {
              boxShadow: '0 0 0 4px rgba(115, 139, 255, 0.25)',
            },
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          fontWeight: 500,
        },
      },
    },
    MuiStepLabel: {
      styleOverrides: {
        label: {
          fontWeight: 500,
        },
      },
    },
    MuiAccordion: {
      styleOverrides: {
        root: {
          borderRadius: '16px !important',
          overflow: 'hidden',
          '&:before': {
            display: 'none',
          },
          '&.Mui-expanded': {
            margin: '16px 0',
          },
        },
      },
    },
    MuiAccordionSummary: {
      styleOverrides: {
        root: {
          borderRadius: 16,
        },
      },
    },
    MuiListItem: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          transition: 'all 0.2s ease',
        },
      },
    },
    MuiDrawer: {
      styleOverrides: {
        paper: {
          borderRight: 'none',
        },
      },
    },
  },
});

// Define steps
const steps = [
  { label: 'Upload Script', icon: <UploadFileIcon /> },
  { label: 'Script Analysis', icon: <AnalyticsIcon /> },
  { label: 'Scheduling', icon: <CalendarMonthIcon /> },
  { label: 'Budgeting', icon: <AttachMoneyIcon /> },
  { label: 'One-Liners', icon: <ShortTextIcon /> },
  { label: 'Character Breakdown', icon: <PeopleIcon /> },
  { label: 'System Overview', icon: <SyncIcon /> },
  { label: 'API Logs', icon: <BarChartIcon /> },
];

// API base URL
const API_BASE_URL = 'https://varun324242-sjuuper.hf.space/api';

// Define types for our data
interface Scene {
  scene_number: number;
  location: string;
  time_of_day: string;
  description: string;
  characters?: string[];
  title?: string;
  int_ext?: string;
  time?: string;
  metadata?: Record<string, unknown>;
  [key: string]: unknown;
}

interface ScriptAnalysis {
  title?: string;
  author?: string;
  genre?: string;
  estimated_runtime?: string;
  scenes?: Scene[];
  total_characters?: number;
  [key: string]: unknown;
}

interface ScheduleDay {
  date: string;
  location?: string;
  call_time?: string;
  wrap_time?: string;
  scenes: ScheduleScene[];
  cast_call_times: Record<string, string>;
  [key: string]: unknown;
}

interface ScheduleScene extends Scene {
  start_time?: string;
  end_time?: string;
  [key: string]: unknown;
}

interface Schedule {
  shooting_days: ScheduleDay[];
  [key: string]: unknown;
}

interface BudgetScene extends Scene {
  cost?: number;
  [key: string]: unknown;
}

interface BudgetDay {
  date: string;
  total: number;
  categories: Record<string, number>;
  scenes: BudgetScene[];
  [key: string]: unknown;
}

interface Budget {
  days: BudgetDay[];
  total: number;
  total_budget?: number;
  per_day_average?: number;
  contingency?: number;
  [key: string]: unknown;
}

interface OneLiners {
  scenes: {
    scene_number: number;
    one_liner: string;
    [key: string]: unknown;
  }[];
  [key: string]: unknown;
}

interface Character {
  name: string;
  description: string;
  scenes: number[];
  role_type?: string;
  age?: string | number;
  emotional_arc?: string;
  screen_time?: string | number;
  [key: string]: unknown;
}

interface Characters {
  characters: Character[];
  [key: string]: unknown;
}

interface SystemSync {
  sync_status: Record<string, string>;
  total_scenes?: number;
  shooting_days?: number;
  total_budget?: number;
  start_date?: string;
  end_date?: string;
  [key: string]: unknown;
}

interface ProcessedData {
  script_analysis: ScriptAnalysis | null;
  schedule: Schedule | null;
  budget: Budget | null;
  one_liners: OneLiners | null;
  characters: Characters | null;
  system_sync: SystemSync | null;
}

interface ApiStats {
  total_requests: number;
  average_response_time: number;
  success_rate: number;
  total_calls?: number;
  avg_duration?: number;
  [key: string]: unknown;
}

interface ApiLog {
  timestamp: string;
  endpoint: string;
  method: string;
  status: string | number;
  response_time: number;
  error?: string;
  provider?: string;
  model?: string;
  duration?: number;
  prompt_length?: number;
  response_length?: number;
  metadata?: Record<string, unknown>;
  [key: string]: unknown;
}

export default function Home() {
  const [darkMode, setDarkMode] = useState(false);
  const theme = darkMode ? darkTheme : lightTheme;
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [activeStep, setActiveStep] = useState(0);
  const [scriptText, setScriptText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [processedData, setProcessedData] = useState<ProcessedData>({
    script_analysis: null,
    schedule: null,
    budget: null,
    one_liners: null,
    characters: null,
    system_sync: null,
  });
  const [apiStats, setApiStats] = useState<ApiStats | null>(null);
  const [apiLogs, setApiLogs] = useState<ApiLog[]>([]);

  // Handle drawer toggle
  const handleDrawerToggle = () => {
    setDrawerOpen(!drawerOpen);
  };

  // Handle theme toggle
  const toggleTheme = () => {
    setDarkMode(!darkMode);
  };

  // Handle step change
  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleStepClick = (step: number) => {
    setActiveStep(step);
    setDrawerOpen(false);
  };

  // Handle script upload
  const handleScriptUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e: ProgressEvent<FileReader>) => {
        setScriptText(e.target?.result as string);
      };
      reader.readAsText(file);
    }
  };

  // Process script
  const processScript = async () => {
    if (!scriptText) return;

    setIsLoading(true);
    try {
      // Call script analysis API
      const response = await fetch(`${API_BASE_URL}/script`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ script_text: scriptText }),
      });

      if (!response.ok) throw new Error('Failed to analyze script');

      const scriptAnalysis = await response.json();
      setProcessedData({ ...processedData, script_analysis: scriptAnalysis });

      // Move to next step
      handleNext();
    } catch (error) {
      console.error('Error processing script:', error);
      alert('Error processing script. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  // Process scheduling
  const processScheduling = async () => {
    if (!processedData.script_analysis) return;

    setIsLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/schedule`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(processedData.script_analysis),
      });

      if (!response.ok) throw new Error('Failed to create schedule');

      const scheduleData = await response.json();
      setProcessedData({ ...processedData, schedule: scheduleData });

      // Move to next step
      handleNext();
    } catch (error) {
      console.error('Error creating schedule:', error);
      alert('Error creating schedule. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  // Process budgeting
  const processBudgeting = async () => {
    if (!processedData.script_analysis || !processedData.schedule) return;

    setIsLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/budget`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          script_analysis: processedData.script_analysis,
          schedule: processedData.schedule,
        }),
      });

      if (!response.ok) throw new Error('Failed to create budget');

      const budgetData = await response.json();
      setProcessedData({ ...processedData, budget: budgetData });

      // Move to next step
      handleNext();
    } catch (error) {
      console.error('Error creating budget:', error);
      alert('Error creating budget. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  // Process one-liners
  const processOneLiners = async () => {
    if (!processedData.script_analysis) return;

    setIsLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/one-liners`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(processedData.script_analysis),
      });

      if (!response.ok) throw new Error('Failed to create one-liners');

      const oneLinersData = await response.json();
      setProcessedData({ ...processedData, one_liners: oneLinersData });

      // Move to next step
      handleNext();
    } catch (error) {
      console.error('Error creating one-liners:', error);
      alert('Error creating one-liners. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  // Process characters
  const processCharacters = async () => {
    if (!processedData.script_analysis) return;

    setIsLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/characters`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(processedData.script_analysis),
      });

      if (!response.ok) throw new Error('Failed to analyze characters');

      const charactersData = await response.json();
      setProcessedData({ ...processedData, characters: charactersData });

      // Move to next step
      handleNext();
    } catch (error) {
      console.error('Error analyzing characters:', error);
      alert('Error analyzing characters. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  // Process system sync
  const processSystemSync = async () => {
    if (!processedData.script_analysis || !processedData.schedule ||
        !processedData.budget || !processedData.one_liners ||
        !processedData.characters) return;

    setIsLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/system-sync`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(processedData),
      });

      if (!response.ok) throw new Error('Failed to sync system');

      const systemData = await response.json();
      setProcessedData({ ...processedData, system_sync: systemData });

      // Move to next step
      handleNext();
    } catch (error) {
      console.error('Error syncing system:', error);
      alert('Error syncing system. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  // Fetch API logs
  const fetchApiLogs = async () => {
    setIsLoading(true);
    try {
      // Fetch stats
      const statsResponse = await fetch(`${API_BASE_URL}/logs/stats`);
      if (!statsResponse.ok) throw new Error('Failed to fetch API stats');
      const statsData = await statsResponse.json();
      setApiStats(statsData);

      // Fetch logs
      const logsResponse = await fetch(`${API_BASE_URL}/logs`);
      if (!logsResponse.ok) throw new Error('Failed to fetch API logs');
      const logsData = await logsResponse.json();
      setApiLogs(logsData);
    } catch (error) {
      console.error('Error fetching API logs:', error);
      alert('Error fetching API logs. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  // Clear API logs
  const clearApiLogs = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/logs`, {
        method: 'DELETE',
      });

      if (!response.ok) throw new Error('Failed to clear logs');

      alert('Logs cleared successfully!');
      fetchApiLogs();
    } catch (error) {
      console.error('Error clearing logs:', error);
      alert('Error clearing logs. Please try again.');
    }
  };

  // JSON download functionality has been removed

  // Fetch API logs when reaching the logs step
  useEffect(() => {
    if (activeStep === 7) {
      fetchApiLogs();
    }
  }, [activeStep]);

  // Render step content
  const getStepContent = (step: number) => {
    switch (step) {
      case 0: // Upload Script
        return (
          <Box>
            <Box
              sx={{
                textAlign: 'center',
                mb: 5,
                animation: 'fadeIn 0.8s ease-out',
              }}
            >
              <Typography
                variant="h3"
                gutterBottom
                sx={{
                  fontWeight: 800,
                  mb: 2,
                  background: theme.palette.mode === 'dark'
                    ? 'linear-gradient(90deg, #a4b8ff, #ff90d1)'
                    : 'linear-gradient(90deg, #4361ee, #f72585)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  letterSpacing: '-0.02em',
                }}
              >
                Welcome to the Film Production AI Assistant
              </Typography>
              <Typography
                variant="h6"
                sx={{
                  maxWidth: '800px',
                  mx: 'auto',
                  mb: 4,
                  color: theme.palette.text.secondary,
                  fontWeight: 400,
                  lineHeight: 1.6,
                }}
              >
                Transform your script into a complete production plan with our AI-powered tools
              </Typography>

              <Grid container spacing={3} justifyContent="center" sx={{ mb: 4 }}>
                {[
                  { icon: <AnalyticsIcon fontSize="large" />, title: 'Scene Analysis', desc: 'Detailed breakdown of each scene' },
                  { icon: <CalendarMonthIcon fontSize="large" />, title: 'Scheduling', desc: 'Optimized shooting schedule' },
                  { icon: <AttachMoneyIcon fontSize="large" />, title: 'Budgeting', desc: 'Comprehensive budget estimates' },
                  { icon: <PeopleIcon fontSize="large" />, title: 'Characters', desc: 'Complete character breakdowns' },
                ].map((feature, index) => (
                  <Grid size={{ xs: 12, sm: 6, md: 3 }} key={index}>
                    <Card
                      sx={{
                        height: '100%',
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                        p: 3,
                        textAlign: 'center',
                        transition: 'all 0.3s ease',
                        '&:hover': {
                          transform: 'translateY(-8px)',
                        },
                      }}
                    >
                      <Box
                        sx={{
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          width: 70,
                          height: 70,
                          borderRadius: '50%',
                          mb: 2,
                          background: theme.palette.mode === 'dark'
                            ? 'linear-gradient(135deg, rgba(115, 139, 255, 0.2), rgba(255, 94, 177, 0.2))'
                            : 'linear-gradient(135deg, rgba(67, 97, 238, 0.1), rgba(247, 37, 133, 0.1))',
                          color: theme.palette.mode === 'dark' ? '#738bff' : '#4361ee',
                        }}
                      >
                        {feature.icon}
                      </Box>
                      <Typography variant="h6" fontWeight={600} gutterBottom>
                        {feature.title}
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        {feature.desc}
                      </Typography>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </Box>

            <Grid container spacing={4}>
              <Grid size={{ xs: 12, md: 6 }}>
                <Paper
                  elevation={0}
                  sx={{
                    p: 4,
                    height: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                    position: 'relative',
                    overflow: 'hidden',
                    '&::before': {
                      content: '""',
                      position: 'absolute',
                      top: 0,
                      left: 0,
                      right: 0,
                      height: '4px',
                      background: theme.palette.mode === 'dark'
                        ? 'linear-gradient(90deg, #738bff, #ff5eb1)'
                        : 'linear-gradient(90deg, #4361ee, #f72585)',
                    },
                  }}
                >
                  <Box
                    sx={{
                      display: 'flex',
                      alignItems: 'center',
                      mb: 3,
                    }}
                  >
                    <Box
                      sx={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        width: 50,
                        height: 50,
                        borderRadius: '50%',
                        mr: 2,
                        background: theme.palette.mode === 'dark'
                          ? 'linear-gradient(135deg, rgba(115, 139, 255, 0.2), rgba(255, 94, 177, 0.2))'
                          : 'linear-gradient(135deg, rgba(67, 97, 238, 0.1), rgba(247, 37, 133, 0.1))',
                        color: theme.palette.mode === 'dark' ? '#738bff' : '#4361ee',
                      }}
                    >
                      <UploadFileIcon />
                    </Box>
                    <Typography variant="h5" fontWeight={600}>
                      Upload your script file
                    </Typography>
                  </Box>

                  <Box
                    sx={{
                      border: `2px dashed ${theme.palette.mode === 'dark' ? 'rgba(255,255,255,0.2)' : 'rgba(0,0,0,0.1)'}`,
                      borderRadius: 3,
                      p: 4,
                      textAlign: 'center',
                      mb: 3,
                      transition: 'all 0.2s ease',
                      '&:hover': {
                        borderColor: theme.palette.mode === 'dark' ? '#738bff' : '#4361ee',
                        backgroundColor: theme.palette.mode === 'dark' ? 'rgba(115, 139, 255, 0.05)' : 'rgba(67, 97, 238, 0.03)',
                      },
                    }}
                  >
                    <input
                      type="file"
                      accept=".txt"
                      id="script-upload"
                      style={{ display: 'none' }}
                      onChange={handleScriptUpload}
                    />
                    <label htmlFor="script-upload">
                      <Box
                        sx={{
                          display: 'flex',
                          flexDirection: 'column',
                          alignItems: 'center',
                          cursor: 'pointer',
                        }}
                      >
                        <UploadFileIcon
                          sx={{
                            fontSize: 60,
                            mb: 2,
                            color: theme.palette.mode === 'dark' ? 'rgba(255,255,255,0.5)' : 'rgba(0,0,0,0.3)',
                          }}
                        />
                        <Typography variant="h6" gutterBottom>
                          Drag & drop your file here
                        </Typography>
                        <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
                          or click to browse files
                        </Typography>
                        <Button
                          variant="outlined"
                          component="span"
                          startIcon={<UploadFileIcon />}
                          sx={{
                            mt: 1,
                            borderWidth: 2,
                          }}
                        >
                          Choose File
                        </Button>
                      </Box>
                    </label>
                  </Box>

                  <Box sx={{ mt: 'auto' }}>
                    <Typography variant="body2" color="textSecondary" sx={{ display: 'flex', alignItems: 'center' }}>
                      <InfoIcon fontSize="small" sx={{ mr: 1, opacity: 0.7 }} />
                      Supported format: .txt (PDF and DOCX support coming soon)
                    </Typography>
                  </Box>
                </Paper>
              </Grid>

              <Grid size={{ xs: 12, md: 6 }}>
                <Paper
                  elevation={0}
                  sx={{
                    p: 4,
                    height: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                    position: 'relative',
                    overflow: 'hidden',
                    '&::before': {
                      content: '""',
                      position: 'absolute',
                      top: 0,
                      left: 0,
                      right: 0,
                      height: '4px',
                      background: theme.palette.mode === 'dark'
                        ? 'linear-gradient(90deg, #ff5eb1, #738bff)'
                        : 'linear-gradient(90deg, #f72585, #4361ee)',
                    },
                  }}
                >
                  <Box
                    sx={{
                      display: 'flex',
                      alignItems: 'center',
                      mb: 3,
                    }}
                  >
                    <Box
                      sx={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        width: 50,
                        height: 50,
                        borderRadius: '50%',
                        mr: 2,
                        background: theme.palette.mode === 'dark'
                          ? 'linear-gradient(135deg, rgba(255, 94, 177, 0.2), rgba(115, 139, 255, 0.2))'
                          : 'linear-gradient(135deg, rgba(247, 37, 133, 0.1), rgba(67, 97, 238, 0.1))',
                        color: theme.palette.mode === 'dark' ? '#ff5eb1' : '#f72585',
                      }}
                    >
                      <ShortTextIcon />
                    </Box>
                    <Typography variant="h5" fontWeight={600}>
                      Or paste your script here
                    </Typography>
                  </Box>

                  <TextField
                    fullWidth
                    multiline
                    rows={12}
                    variant="outlined"
                    value={scriptText}
                    onChange={(e) => setScriptText(e.target.value)}
                    placeholder="Paste your script text here..."
                    sx={{
                      mb: 3,
                      '& .MuiOutlinedInput-root': {
                        borderRadius: 3,
                        backgroundColor: theme.palette.mode === 'dark' ? 'rgba(19, 47, 76, 0.4)' : 'rgba(255, 255, 255, 0.8)',
                      },
                    }}
                  />

                  <Box sx={{ mt: 'auto', display: 'flex', justifyContent: 'flex-end' }}>
                    <Button
                      variant="contained"
                      size="large"
                      disabled={!scriptText || isLoading}
                      onClick={processScript}
                      startIcon={isLoading ? <CircularProgress size={20} color="inherit" /> : <AnalyticsIcon />}
                      sx={{
                        px: 4,
                        py: 1.5,
                        background: theme.palette.mode === 'dark'
                          ? 'linear-gradient(90deg, #ff5eb1, #738bff)'
                          : 'linear-gradient(90deg, #f72585, #4361ee)',
                        '&:hover': {
                          background: theme.palette.mode === 'dark'
                            ? 'linear-gradient(90deg, #cc4a8e, #5a6ecc)'
                            : 'linear-gradient(90deg, #c51e6a, #354db8)',
                        },
                        '&.Mui-disabled': {
                          opacity: 0.5,
                          background: theme.palette.mode === 'dark'
                            ? 'linear-gradient(90deg, #ff5eb1, #738bff)'
                            : 'linear-gradient(90deg, #f72585, #4361ee)',
                          color: 'white',
                        },
                      }}
                    >
                      {isLoading ? 'Processing...' : 'Process Script'}
                    </Button>
                  </Box>
                </Paper>
              </Grid>
            </Grid>
          </Box>
        );

      case 1: // Script Analysis
        if (!processedData.script_analysis) {
          return (
            <Box sx={{ textAlign: 'center', py: 8 }}>
              <Box
                sx={{
                  width: 120,
                  height: 120,
                  borderRadius: '50%',
                  background: theme.palette.mode === 'dark'
                    ? 'linear-gradient(135deg, rgba(115, 139, 255, 0.1), rgba(255, 94, 177, 0.1))'
                    : 'linear-gradient(135deg, rgba(67, 97, 238, 0.05), rgba(247, 37, 133, 0.05))',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  mx: 'auto',
                  mb: 4,
                }}
              >
                <AnalyticsIcon
                  sx={{
                    fontSize: 60,
                    color: theme.palette.mode === 'dark' ? 'rgba(255,255,255,0.3)' : 'rgba(0,0,0,0.2)',
                  }}
                />
              </Box>
              <Typography
                variant="h4"
                sx={{
                  fontWeight: 700,
                  mb: 2,
                  color: theme.palette.text.primary,
                }}
              >
                No Script Analysis Available
              </Typography>
              <Typography
                variant="body1"
                color="textSecondary"
                sx={{
                  maxWidth: 500,
                  mx: 'auto',
                  mb: 4,
                  fontSize: '1.1rem',
                }}
              >
                Please upload and process a script first to view the analysis results.
              </Typography>
              <Button
                variant="contained"
                size="large"
                onClick={() => setActiveStep(0)}
                startIcon={<UploadFileIcon />}
                sx={{
                  px: 4,
                  py: 1.5,
                  background: theme.palette.mode === 'dark'
                    ? 'linear-gradient(90deg, #738bff, #ff5eb1)'
                    : 'linear-gradient(90deg, #4361ee, #f72585)',
                  '&:hover': {
                    background: theme.palette.mode === 'dark'
                      ? 'linear-gradient(90deg, #5a6ecc, #cc4a8e)'
                      : 'linear-gradient(90deg, #354db8, #c51e6a)',
                  },
                }}
              >
                Go to Script Upload
              </Button>
            </Box>
          );
        }

        return (
          <Box>
            <Box sx={{ mb: 4 }}>
              <Typography
                variant="h4"
                sx={{
                  fontWeight: 700,
                  mb: 1,
                  background: theme.palette.mode === 'dark'
                    ? 'linear-gradient(90deg, #a4b8ff, #ff90d1)'
                    : 'linear-gradient(90deg, #4361ee, #f72585)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                }}
              >
                {processedData.script_analysis.title || 'Script Analysis'}
              </Typography>
              <Typography
                variant="subtitle1"
                color="textSecondary"
                sx={{ mb: 3 }}
              >
                by {processedData.script_analysis.author || 'Unknown Author'}
              </Typography>

              <Box
                sx={{
                  display: 'flex',
                  flexWrap: 'wrap',
                  gap: 1,
                  mb: 4,
                }}
              >
                <Chip
                  label={`Genre: ${processedData.script_analysis.genre || 'Drama'}`}
                  color="primary"
                  variant="outlined"
                  sx={{ fontWeight: 500 }}
                />
                <Chip
                  label={`Runtime: ${processedData.script_analysis.estimated_runtime || '90'} min`}
                  color="secondary"
                  variant="outlined"
                  sx={{ fontWeight: 500 }}
                />
                <Chip
                  label={`${processedData.script_analysis.scenes?.length || '0'} Scenes`}
                  color="info"
                  variant="outlined"
                  sx={{ fontWeight: 500 }}
                />
                <Chip
                  label={`${processedData.script_analysis.total_characters || '0'} Characters`}
                  color="success"
                  variant="outlined"
                  sx={{ fontWeight: 500 }}
                />
              </Box>
            </Box>

            <Typography
              variant="h5"
              sx={{
                fontWeight: 600,
                mb: 3,
                display: 'flex',
                alignItems: 'center',
              }}
            >
              <Box
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  width: 40,
                  height: 40,
                  borderRadius: '50%',
                  mr: 2,
                  background: theme.palette.mode === 'dark'
                    ? 'linear-gradient(135deg, rgba(115, 139, 255, 0.2), rgba(255, 94, 177, 0.2))'
                    : 'linear-gradient(135deg, rgba(67, 97, 238, 0.1), rgba(247, 37, 133, 0.1))',
                  color: theme.palette.mode === 'dark' ? '#738bff' : '#4361ee',
                }}
              >
                <MovieIcon />
              </Box>
              Scene Breakdown
            </Typography>

            {processedData.script_analysis.scenes?.map((scene, index) => (
              <Accordion
                key={index}
                sx={{
                  mb: 2,
                  borderRadius: '16px !important',
                  overflow: 'hidden',
                  '&:before': {
                    display: 'none',
                  },
                  boxShadow: theme.palette.mode === 'dark'
                    ? '0 4px 20px 0 rgba(0,0,0,0.1)'
                    : '0 4px 20px 0 rgba(0,0,0,0.03)',
                  border: `1px solid ${theme.palette.mode === 'dark' ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.05)'}`,
                  transition: 'all 0.3s ease',
                  '&:hover': {
                    boxShadow: theme.palette.mode === 'dark'
                      ? '0 8px 25px 0 rgba(0,0,0,0.15)'
                      : '0 8px 25px 0 rgba(0,0,0,0.06)',
                  },
                }}
              >
                <AccordionSummary
                  expandIcon={
                    <ExpandMoreIcon sx={{
                      transition: 'transform 0.3s ease',
                      color: theme.palette.mode === 'dark' ? '#738bff' : '#4361ee',
                    }} />
                  }
                  sx={{
                    borderBottom: `1px solid ${theme.palette.mode === 'dark' ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.03)'}`,
                    '&.Mui-expanded': {
                      borderBottom: `1px solid ${theme.palette.mode === 'dark' ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.05)'}`,
                    },
                  }}
                >
                  <Box sx={{ display: 'flex', alignItems: 'center', width: '100%' }}>
                    <Chip
                      label={`Scene ${scene.scene_number}`}
                      color="primary"
                      size="small"
                      sx={{
                        mr: 2,
                        fontWeight: 600,
                        minWidth: 80,
                        textAlign: 'center',
                      }}
                    />
                    <Typography
                      variant="subtitle1"
                      sx={{
                        fontWeight: 600,
                        flexGrow: 1,
                      }}
                    >
                      {scene.title || scene.location || `Scene ${scene.scene_number}`}
                    </Typography>
                    <Box
                      sx={{
                        display: { xs: 'none', md: 'flex' },
                        alignItems: 'center',
                        gap: 1,
                      }}
                    >
                      <Chip
                        label={scene.int_ext || 'INT'}
                        size="small"
                        color={scene.int_ext?.toLowerCase().includes('int') ? 'primary' : 'secondary'}
                        variant="outlined"
                        sx={{ fontWeight: 500 }}
                      />
                      <Chip
                        label={scene.time_of_day || scene.time || 'DAY'}
                        size="small"
                        color="default"
                        variant="outlined"
                        sx={{ fontWeight: 500 }}
                      />
                    </Box>
                  </Box>
                </AccordionSummary>
                <AccordionDetails sx={{ p: 3 }}>
                  <Grid container spacing={3}>
                    <Grid size={{ xs: 12, md: 6 }}>
                      <Box
                        sx={{
                          p: 2,
                          borderRadius: 2,
                          backgroundColor: theme.palette.mode === 'dark' ? 'rgba(19, 47, 76, 0.4)' : 'rgba(248, 249, 250, 0.8)',
                          height: '100%',
                        }}
                      >
                        <Typography
                          variant="subtitle2"
                          color="textSecondary"
                          gutterBottom
                          sx={{
                            display: 'flex',
                            alignItems: 'center',
                            mb: 2,
                          }}
                        >
                          <Box
                            component="span"
                            sx={{
                              width: 8,
                              height: 8,
                              borderRadius: '50%',
                              bgcolor: theme.palette.primary.main,
                              display: 'inline-block',
                              mr: 1,
                            }}
                          />
                          SCENE DETAILS
                        </Typography>

                        <Box sx={{ mb: 2 }}>
                          <Typography variant="body2" color="textSecondary" gutterBottom>
                            Location
                          </Typography>
                          <Typography variant="body1" fontWeight={500}>
                            {scene.location || 'Unknown location'}
                          </Typography>
                        </Box>

                        <Box sx={{ mb: 2 }}>
                          <Typography variant="body2" color="textSecondary" gutterBottom>
                            Setting
                          </Typography>
                          <Box sx={{ display: 'flex', gap: 1 }}>
                            <Chip
                              label={scene.int_ext || 'INT'}
                              size="small"
                              color={scene.int_ext?.toLowerCase().includes('int') ? 'primary' : 'secondary'}
                              sx={{ fontWeight: 500 }}
                            />
                            <Chip
                              label={scene.time_of_day || scene.time || 'DAY'}
                              size="small"
                              sx={{ fontWeight: 500 }}
                            />
                          </Box>
                        </Box>

                        <Box>
                          <Typography variant="body2" color="textSecondary" gutterBottom>
                            Characters
                          </Typography>
                          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                            {(scene.characters || []).map((char: string, i: number) => (
                              <Chip
                                key={i}
                                label={char}
                                size="small"
                                sx={{
                                  fontWeight: 500,
                                  backgroundColor: theme.palette.mode === 'dark'
                                    ? 'rgba(115, 139, 255, 0.1)'
                                    : 'rgba(67, 97, 238, 0.05)',
                                }}
                              />
                            ))}
                            {!scene.characters?.length && (
                              <Typography variant="body2" color="textSecondary">
                                No characters specified
                              </Typography>
                            )}
                          </Box>
                        </Box>
                      </Box>
                    </Grid>

                    <Grid size={{ xs: 12, md: 6 }}>
                      <Box
                        sx={{
                          p: 2,
                          borderRadius: 2,
                          backgroundColor: theme.palette.mode === 'dark' ? 'rgba(19, 47, 76, 0.4)' : 'rgba(248, 249, 250, 0.8)',
                          height: '100%',
                        }}
                      >
                        <Typography
                          variant="subtitle2"
                          color="textSecondary"
                          gutterBottom
                          sx={{
                            display: 'flex',
                            alignItems: 'center',
                            mb: 2,
                          }}
                        >
                          <Box
                            component="span"
                            sx={{
                              width: 8,
                              height: 8,
                              borderRadius: '50%',
                              bgcolor: theme.palette.secondary.main,
                              display: 'inline-block',
                              mr: 1,
                            }}
                          />
                          DESCRIPTION
                        </Typography>

                        <Typography
                          variant="body1"
                          sx={{
                            lineHeight: 1.6,
                            fontStyle: 'italic',
                            color: theme.palette.text.primary,
                          }}
                        >
                          {scene.description || 'No description available'}
                        </Typography>
                      </Box>
                    </Grid>

                    {scene.metadata && (
                      <Grid size={{ xs: 12 }}>
                        <Box
                          sx={{
                            p: 2,
                            borderRadius: 2,
                            backgroundColor: theme.palette.mode === 'dark' ? 'rgba(19, 47, 76, 0.4)' : 'rgba(248, 249, 250, 0.8)',
                          }}
                        >
                          <Typography
                            variant="subtitle2"
                            color="textSecondary"
                            gutterBottom
                            sx={{
                              display: 'flex',
                              alignItems: 'center',
                              mb: 2,
                            }}
                          >
                            <Box
                              component="span"
                              sx={{
                                width: 8,
                                height: 8,
                                borderRadius: '50%',
                                bgcolor: theme.palette.info.main,
                                display: 'inline-block',
                                mr: 1,
                              }}
                            />
                            METADATA
                          </Typography>

                          <Paper
                            variant="outlined"
                            sx={{
                              p: 2,
                              bgcolor: theme.palette.mode === 'dark' ? 'rgba(10, 25, 41, 0.7)' : 'rgba(255, 255, 255, 0.7)',
                              borderRadius: 2,
                              border: `1px solid ${theme.palette.mode === 'dark' ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.05)'}`,
                            }}
                          >
                            <pre style={{
                              margin: 0,
                              overflow: 'auto',
                              fontFamily: '"Roboto Mono", monospace',
                              fontSize: '0.875rem',
                              color: theme.palette.text.secondary,
                            }}>
                              {JSON.stringify(scene.metadata, null, 2)}
                            </pre>
                          </Paper>
                        </Box>
                      </Grid>
                    )}
                  </Grid>
                </AccordionDetails>
              </Accordion>
            ))}

            <Box
              sx={{
                mt: 4,
                display: 'flex',
                justifyContent: 'space-between',
                flexWrap: 'wrap',
                gap: 2,
              }}
            >

              <Button
                variant="contained"
                onClick={processScheduling}
                disabled={isLoading}
                startIcon={isLoading ? <CircularProgress size={20} color="inherit" /> : <CalendarMonthIcon />}
                sx={{
                  px: 3,
                  background: theme.palette.mode === 'dark'
                    ? 'linear-gradient(90deg, #738bff, #ff5eb1)'
                    : 'linear-gradient(90deg, #4361ee, #f72585)',
                  '&:hover': {
                    background: theme.palette.mode === 'dark'
                      ? 'linear-gradient(90deg, #5a6ecc, #cc4a8e)'
                      : 'linear-gradient(90deg, #354db8, #c51e6a)',
                  },
                  '&.Mui-disabled': {
                    opacity: 0.5,
                    background: theme.palette.mode === 'dark'
                      ? 'linear-gradient(90deg, #738bff, #ff5eb1)'
                      : 'linear-gradient(90deg, #4361ee, #f72585)',
                    color: 'white',
                  },
                }}
              >
                {isLoading ? 'Processing...' : 'Generate Schedule'}
              </Button>
            </Box>
          </Box>
        );

      case 2: // Scheduling
        if (!processedData.schedule) {
          return (
            <Box sx={{ mt: 4, textAlign: 'center' }}>
              <Typography variant="h5" color="textSecondary" gutterBottom>
                No scheduling data available.
              </Typography>
              <Button
                variant="contained"
                onClick={() => processScheduling()}
                disabled={!processedData.script_analysis || isLoading}
                startIcon={isLoading ? <CircularProgress size={20} /> : null}
              >
                {isLoading ? 'Processing...' : 'Generate Schedule'}
              </Button>
            </Box>
          );
        }

        return (
          <Box sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>
              Scheduling & Resource Allocation
            </Typography>
            <Typography variant="body1" sx={{ mb: 2 }}>
              Optimized shooting schedule based on your script analysis.
            </Typography>

            <Typography variant="h5" gutterBottom sx={{ mt: 3 }}>
              Shooting Schedule
            </Typography>

            {processedData.schedule.shooting_days.map((day, index: number) => (
              <Accordion key={index} sx={{ mb: 2 }}>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography variant="subtitle1">
                    <strong>Day {index + 1}:</strong> {day.date} - {day.location}
                  </Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Grid container spacing={3}>
                    <Grid size={{ xs: 12, md: 6 }}>
                      <Typography variant="body1">
                        <strong>Call Time:</strong> {day.call_time}
                      </Typography>
                      <Typography variant="body1">
                        <strong>Wrap Time:</strong> {day.wrap_time}
                      </Typography>
                    </Grid>
                    <Grid size={{ xs: 12, md: 6 }}>
                      <Typography variant="body1">
                        <strong>Cast Call Times:</strong>
                      </Typography>
                      <Box component="ul" sx={{ pl: 2 }}>
                        {Object.entries(day.cast_call_times).map(([actor, time], i: number) => (
                          <li key={i}>
                            <Typography variant="body2">
                              <strong>{actor}:</strong> {String(time)}
                            </Typography>
                          </li>
                        ))}
                      </Box>
                    </Grid>
                    <Grid size={{ xs: 12 }}>
                      <Divider sx={{ my: 2 }} />
                      <Typography variant="body1" sx={{ mb: 1 }}>
                        <strong>Scenes:</strong>
                      </Typography>
                      <Grid container spacing={2}>
                        {day.scenes.map((scene, i: number) => (
                          <Grid size={{ xs: 12, sm: 6, md: 4 }} key={i}>
                            <Card variant="outlined">
                              <CardContent>
                                <Typography variant="subtitle2">
                                  Scene {scene.scene_number}: {scene.title}
                                </Typography>
                                <Typography variant="body2" color="textSecondary">
                                  {scene.start_time} - {scene.end_time}
                                </Typography>
                              </CardContent>
                            </Card>
                          </Grid>
                        ))}
                      </Grid>
                    </Grid>
                  </Grid>
                </AccordionDetails>
              </Accordion>
            ))}

            <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
              <Button
                variant="contained"
                color="primary"
                onClick={processBudgeting}
                disabled={isLoading}
                startIcon={isLoading ? <CircularProgress size={20} /> : null}
              >
                {isLoading ? 'Processing...' : 'Generate Budget'}
              </Button>
            </Box>
          </Box>
        );

      case 3: // Budgeting
        if (!processedData.budget) {
          return (
            <Box sx={{ mt: 4, textAlign: 'center' }}>
              <Typography variant="h5" color="textSecondary" gutterBottom>
                No budget data available.
              </Typography>
              <Button
                variant="contained"
                onClick={() => processBudgeting()}
                disabled={!processedData.script_analysis || !processedData.schedule || isLoading}
                startIcon={isLoading ? <CircularProgress size={20} /> : null}
              >
                {isLoading ? 'Processing...' : 'Generate Budget'}
              </Button>
            </Box>
          );
        }

        return (
          <Box sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>
              Budgeting Module
            </Typography>
            <Typography variant="body1" sx={{ mb: 2 }}>
              Detailed budget estimates based on your script and schedule.
            </Typography>

            <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
              <Typography variant="h5" gutterBottom>
                Budget Summary
              </Typography>
              <Grid container spacing={3}>
                <Grid size={{ xs: 12, md: 4 }}>
                  <Card sx={{ height: '100%' }}>
                    <CardContent sx={{ textAlign: 'center' }}>
                      <Typography variant="h6" color="textSecondary" gutterBottom>
                        Total Budget
                      </Typography>
                      <Typography variant="h3" color="primary">
                        ${processedData.budget.total_budget?.toLocaleString('en-US', { minimumFractionDigits: 2 }) ?? '0.00'}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid size={{ xs: 12, md: 4 }}>
                  <Card sx={{ height: '100%' }}>
                    <CardContent sx={{ textAlign: 'center' }}>
                      <Typography variant="h6" color="textSecondary" gutterBottom>
                        Per Day Average
                      </Typography>
                      <Typography variant="h3" color="primary">
                        ${processedData.budget.per_day_average?.toLocaleString('en-US', { minimumFractionDigits: 2 }) ?? '0.00'}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid size={{ xs: 12, md: 4 }}>
                  <Card sx={{ height: '100%' }}>
                    <CardContent sx={{ textAlign: 'center' }}>
                      <Typography variant="h6" color="textSecondary" gutterBottom>
                        Contingency
                      </Typography>
                      <Typography variant="h3" color="primary">
                        ${processedData.budget.contingency?.toLocaleString('en-US', { minimumFractionDigits: 2 }) ?? '0.00'}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>
            </Paper>

            <Typography variant="h5" gutterBottom>
              Day-wise Budget Breakdown
            </Typography>

            {processedData.budget.days.map((day, index: number) => (
              <Accordion key={index} sx={{ mb: 2 }}>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography variant="subtitle1">
                    <strong>Day {index + 1}:</strong> ${day.total.toLocaleString('en-US', { minimumFractionDigits: 2 })}
                  </Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Grid container spacing={3}>
                    <Grid size={{ xs: 12, md: 6 }}>
                      <Typography variant="body1" sx={{ mb: 1 }}>
                        <strong>Category Breakdown:</strong>
                      </Typography>
                      <Box component="ul" sx={{ pl: 2 }}>
                        {Object.entries(day.categories).map(([category, amount], i: number) => (
                          <li key={i}>
                            <Typography variant="body2">
                              <strong>{category}:</strong> ${typeof amount === 'number' ? amount.toLocaleString('en-US', { minimumFractionDigits: 2 }) : String(amount)}
                            </Typography>
                          </li>
                        ))}
                      </Box>
                    </Grid>
                    <Grid size={{ xs: 12, md: 6 }}>
                      <Typography variant="body1" sx={{ mb: 1 }}>
                        <strong>Scene Costs:</strong>
                      </Typography>
                      <Box component="ul" sx={{ pl: 2 }}>
                        {day.scenes.map((scene, i: number) => (
                          <li key={i}>
                            <Typography variant="body2">
                              <strong>Scene {scene.scene_number}:</strong> ${scene.cost?.toLocaleString('en-US', { minimumFractionDigits: 2 }) ?? '0.00'}
                            </Typography>
                          </li>
                        ))}
                      </Box>
                    </Grid>
                  </Grid>
                </AccordionDetails>
              </Accordion>
            ))}

            <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
              <Button
                variant="contained"
                color="primary"
                onClick={processOneLiners}
                disabled={isLoading}
                startIcon={isLoading ? <CircularProgress size={20} /> : null}
              >
                {isLoading ? 'Processing...' : 'Generate One-Liners'}
              </Button>
            </Box>
          </Box>
        );

      case 4: // One-Liners
        if (!processedData.one_liners) {
          return (
            <Box sx={{ mt: 4, textAlign: 'center' }}>
              <Typography variant="h5" color="textSecondary" gutterBottom>
                No one-liner data available.
              </Typography>
              <Button
                variant="contained"
                onClick={() => processOneLiners()}
                disabled={!processedData.script_analysis || isLoading}
                startIcon={isLoading ? <CircularProgress size={20} /> : null}
              >
                {isLoading ? 'Processing...' : 'Generate One-Liners'}
              </Button>
            </Box>
          );
        }

        return (
          <Box sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>
              One-Liner Creation Module
            </Typography>
            <Typography variant="body1" sx={{ mb: 2 }}>
              Concise one-line summaries for each scene in your script.
            </Typography>

            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h5" gutterBottom>
                Scene One-Liners
              </Typography>
              <Grid container spacing={2}>
                {processedData.one_liners.scenes.map((scene, index: number) => (
                  <Grid size={{ xs: 12 }} key={index}>
                    <Card variant="outlined" sx={{ mb: 1 }}>
                      <CardContent>
                        <Typography variant="subtitle1" gutterBottom>
                          <strong>Scene {scene.scene_number}</strong>
                        </Typography>
                        <Typography variant="body1">
                          {scene.one_liner}
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </Paper>

            <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
              <Button
                variant="contained"
                color="primary"
                onClick={processCharacters}
                disabled={isLoading}
                startIcon={isLoading ? <CircularProgress size={20} /> : null}
              >
                {isLoading ? 'Processing...' : 'Analyze Characters'}
              </Button>
            </Box>
          </Box>
        );

      case 5: // Character Breakdown
        if (!processedData.characters) {
          return (
            <Box sx={{ mt: 4, textAlign: 'center' }}>
              <Typography variant="h5" color="textSecondary" gutterBottom>
                No character data available.
              </Typography>
              <Button
                variant="contained"
                onClick={() => processCharacters()}
                disabled={!processedData.script_analysis || isLoading}
                startIcon={isLoading ? <CircularProgress size={20} /> : null}
              >
                {isLoading ? 'Processing...' : 'Analyze Characters'}
              </Button>
            </Box>
          );
        }

        return (
          <Box sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>
              Character Breakdown Module
            </Typography>
            <Typography variant="body1" sx={{ mb: 2 }}>
              Detailed analysis of characters in your script.
            </Typography>

            <Typography variant="h5" gutterBottom sx={{ mt: 3 }}>
              Character Profiles
            </Typography>

            <Grid container spacing={3}>
              {processedData.characters.characters.map((character, index: number) => (
                <Grid size={{ xs: 12, md: 6, lg: 4 }} key={index}>
                  <Card sx={{ height: '100%' }}>
                    <CardContent>
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                        <Avatar sx={{ bgcolor: theme.palette.primary.main, mr: 2 }}>
                          {character.name.charAt(0)}
                        </Avatar>
                        <Box>
                          <Typography variant="h6">
                            {character.name}
                          </Typography>
                          <Chip
                            label={character.role_type}
                            size="small"
                            color={
                              character.role_type === 'Lead' ? 'primary' :
                              character.role_type === 'Supporting' ? 'secondary' : 'default'
                            }
                          />
                        </Box>
                      </Box>

                      <Typography variant="body2" sx={{ mb: 1 }}>
                        <strong>Age:</strong> {character.age}
                      </Typography>

                      <Typography variant="body2" sx={{ mb: 1 }}>
                        <strong>Description:</strong> {character.description}
                      </Typography>

                      <Typography variant="body2" sx={{ mb: 1 }}>
                        <strong>Emotional Arc:</strong> {character.emotional_arc}
                      </Typography>

                      <Typography variant="body2" sx={{ mb: 1 }}>
                        <strong>Screen Time:</strong> {character.screen_time}%
                      </Typography>

                      <Divider sx={{ my: 2 }} />

                      <Typography variant="body2" sx={{ mb: 1 }}>
                        <strong>Appears in Scenes:</strong>
                      </Typography>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                        {character.scenes.map((scene: number, i: number) => (
                          <Chip key={i} label={`Scene ${scene}`} size="small" variant="outlined" />
                        ))}
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>

            <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
              <Button
                variant="contained"
                color="primary"
                onClick={processSystemSync}
                disabled={isLoading}
                startIcon={isLoading ? <CircularProgress size={20} /> : null}
              >
                {isLoading ? 'Processing...' : 'Generate System Overview'}
              </Button>
            </Box>
          </Box>
        );

      case 6: // System Overview
        if (!processedData.system_sync) {
          return (
            <Box sx={{ mt: 4, textAlign: 'center' }}>
              <Typography variant="h5" color="textSecondary" gutterBottom>
                No system overview data available.
              </Typography>
              <Button
                variant="contained"
                onClick={() => processSystemSync()}
                disabled={
                  !processedData.script_analysis ||
                  !processedData.schedule ||
                  !processedData.budget ||
                  !processedData.one_liners ||
                  !processedData.characters ||
                  isLoading
                }
                startIcon={isLoading ? <CircularProgress size={20} /> : null}
              >
                {isLoading ? 'Processing...' : 'Generate System Overview'}
              </Button>
            </Box>
          );
        }

        return (
          <Box sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>
              System Synchronization and Overview
            </Typography>
            <Typography variant="body1" sx={{ mb: 2 }}>
              Comprehensive overview of your entire production.
            </Typography>

            <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
              <Typography variant="h5" gutterBottom>
                Production Overview
              </Typography>
              <Grid container spacing={3}>
                <Grid size={{ xs: 12, md: 4 }}>
                  <Card sx={{ height: '100%' }}>
                    <CardContent sx={{ textAlign: 'center' }}>
                      <Typography variant="h6" color="textSecondary" gutterBottom>
                        Total Scenes
                      </Typography>
                      <Typography variant="h3" color="primary">
                        {processedData.system_sync.total_scenes}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid size={{ xs: 12, md: 4 }}>
                  <Card sx={{ height: '100%' }}>
                    <CardContent sx={{ textAlign: 'center' }}>
                      <Typography variant="h6" color="textSecondary" gutterBottom>
                        Shooting Days
                      </Typography>
                      <Typography variant="h3" color="primary">
                        {processedData.system_sync.shooting_days}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid size={{ xs: 12, md: 4 }}>
                  <Card sx={{ height: '100%' }}>
                    <CardContent sx={{ textAlign: 'center' }}>
                      <Typography variant="h6" color="textSecondary" gutterBottom>
                        Total Budget
                      </Typography>
                      <Typography variant="h3" color="primary">
                        ${processedData.system_sync.total_budget?.toLocaleString('en-US', { minimumFractionDigits: 2 }) ?? '0.00'}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>
            </Paper>

            <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
              <Typography variant="h5" gutterBottom>
                Production Timeline
              </Typography>
              <Grid container spacing={2}>
                <Grid size={{ xs: 12, md: 6 }}>
                  <Typography variant="body1">
                    <strong>Start Date:</strong> {processedData.system_sync.start_date}
                  </Typography>
                </Grid>
                <Grid size={{ xs: 12, md: 6 }}>
                  <Typography variant="body1">
                    <strong>End Date:</strong> {processedData.system_sync.end_date}
                  </Typography>
                </Grid>
              </Grid>
            </Paper>

            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h5" gutterBottom>
                Data Synchronization Status
              </Typography>
              <Grid container spacing={2}>
                {Object.entries(processedData.system_sync.sync_status).map(([module, status], index: number) => (
                  <Grid size={{ xs: 12, sm: 6, md: 4 }} key={index}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography variant="subtitle1">
                          {module}
                        </Typography>
                        <Chip
                          label={String(status)}
                          color={String(status) === 'Synchronized' ? 'success' : 'warning'}
                          sx={{ mt: 1 }}
                        />
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </Paper>

            <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
              <Button
                variant="contained"
                color="primary"
                onClick={() => setActiveStep(7)}
              >
                View API Logs
              </Button>
            </Box>
          </Box>
        );

      case 7: // API Logs
        return (
          <Box sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>
              API Logs and Analytics
            </Typography>
            <Typography variant="body1" sx={{ mb: 2 }}>
              Detailed logs of API calls made during the production process.
            </Typography>

            {isLoading ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
                <CircularProgress />
              </Box>
            ) : (
              <>
                {apiStats && (
                  <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
                    <Typography variant="h5" gutterBottom>
                      API Usage Summary
                    </Typography>
                    <Grid container spacing={3}>
                      <Grid size={{ xs: 12, md: 4 }}>
                        <Card sx={{ height: '100%' }}>
                          <CardContent sx={{ textAlign: 'center' }}>
                            <Typography variant="h6" color="textSecondary" gutterBottom>
                              Total API Calls
                            </Typography>
                            <Typography variant="h3" color="primary">
                              {apiStats.total_calls}
                            </Typography>
                          </CardContent>
                        </Card>
                      </Grid>
                      <Grid size={{ xs: 12, md: 4 }}>
                        <Card sx={{ height: '100%' }}>
                          <CardContent sx={{ textAlign: 'center' }}>
                            <Typography variant="h6" color="textSecondary" gutterBottom>
                              Success Rate
                            </Typography>
                            <Typography variant="h3" color="primary">
                              {apiStats.success_rate.toFixed(1)}%
                            </Typography>
                          </CardContent>
                        </Card>
                      </Grid>
                      <Grid size={{ xs: 12, md: 4 }}>
                        <Card sx={{ height: '100%' }}>
                          <CardContent sx={{ textAlign: 'center' }}>
                            <Typography variant="h6" color="textSecondary" gutterBottom>
                              Avg. Response Time
                            </Typography>
                            <Typography variant="h3" color="primary">
                              {apiStats.avg_duration?.toFixed(2) ?? '0.00'}s
                            </Typography>
                          </CardContent>
                        </Card>
                      </Grid>
                    </Grid>
                  </Paper>
                )}

                {apiLogs && apiLogs.length > 0 ? (
                  <>
                    <Typography variant="h5" gutterBottom>
                      Detailed API Logs
                    </Typography>

                    {apiLogs.map((log, index) => (
                      <Accordion key={index} sx={{ mb: 2 }}>
                        <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                          <Typography variant="subtitle1">
                            {String(log.status) === 'success' ? '🟢' : '🔴'} {log.provider?.toUpperCase()} - {log.model} - {log.timestamp}
                          </Typography>
                        </AccordionSummary>
                        <AccordionDetails>
                          <Grid container spacing={2}>
                            <Grid size={{ xs: 12, md: 6 }}>
                              <Typography variant="body2">
                                <strong>Duration:</strong> {log.duration?.toFixed(2) ?? '0.00'}s
                              </Typography>
                              <Typography variant="body2">
                                <strong>Prompt Length:</strong> {log.prompt_length} chars
                              </Typography>
                              <Typography variant="body2">
                                <strong>Response Length:</strong> {log.response_length} chars
                              </Typography>
                            </Grid>
                            <Grid size={{ xs: 12, md: 6 }}>
                              {log.error && (
                                <Typography variant="body2" color="error">
                                  <strong>Error:</strong> {log.error}
                                </Typography>
                              )}
                            </Grid>
                            {log.metadata && (
                              <Grid size={{ xs: 12 }}>
                                <Typography variant="body2">
                                  <strong>Metadata:</strong>
                                </Typography>
                                <Paper variant="outlined" sx={{ p: 2, bgcolor: theme.palette.mode === 'dark' ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.03)' }}>
                                  <pre style={{ margin: 0, overflow: 'auto' }}>
                                    {JSON.stringify(log.metadata, null, 2)}
                                  </pre>
                                </Paper>
                              </Grid>
                            )}
                          </Grid>
                        </AccordionDetails>
                      </Accordion>
                    ))}

                    <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
                      <Button
                        variant="contained"
                        color="secondary"
                        onClick={clearApiLogs}
                      >
                        Clear Logs
                      </Button>
                    </Box>
                  </>
                ) : (
                  <Box sx={{ textAlign: 'center', py: 4 }}>
                    <Typography variant="h6" color="textSecondary">
                      No API logs available. Start using the application to generate logs.
                    </Typography>
                  </Box>
                )}
              </>
            )}
          </Box>
        );

      default:
        return (
          <Box sx={{ mt: 4, textAlign: 'center' }}>
            <Typography variant="h5" color="error">
              Unknown step
            </Typography>
          </Box>
        );
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ display: 'flex' }}>
        {/* App Bar */}
        <AppBar
          position="fixed"
          elevation={0}
          sx={{
            zIndex: (theme) => theme.zIndex.drawer + 1,
            backdropFilter: 'blur(8px)',
            backgroundColor: theme.palette.mode === 'dark'
              ? 'rgba(19, 47, 76, 0.9)'
              : 'rgba(255, 255, 255, 0.9)',
            borderBottom: `1px solid ${theme.palette.mode === 'dark' ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.05)'}`,
          }}
        >
          <Toolbar sx={{ px: { xs: 2, sm: 4 } }}>
            <IconButton
              color="inherit"
              aria-label="open drawer"
              edge="start"
              onClick={handleDrawerToggle}
              sx={{
                mr: 2,
                transition: 'transform 0.2s',
                '&:hover': {
                  transform: 'scale(1.1)',
                  backgroundColor: theme.palette.mode === 'dark'
                    ? 'rgba(255,255,255,0.1)'
                    : 'rgba(0,0,0,0.05)',
                }
              }}
            >
              <MenuIcon />
            </IconButton>
            <Box
              sx={{
                display: 'flex',
                alignItems: 'center',
                background: theme.palette.mode === 'dark'
                  ? 'linear-gradient(90deg, #738bff, #ff5eb1)'
                  : 'linear-gradient(90deg, #4361ee, #f72585)',
                borderRadius: '50%',
                p: 1,
                mr: 2,
                boxShadow: theme.palette.mode === 'dark'
                  ? '0 0 15px rgba(115, 139, 255, 0.5)'
                  : '0 0 15px rgba(67, 97, 238, 0.5)',
              }}
            >
              <MovieIcon sx={{ color: '#fff' }} />
            </Box>
            <Typography
              variant="h6"
              noWrap
              component="div"
              sx={{
                flexGrow: 1,
                fontWeight: 700,
                background: theme.palette.mode === 'dark'
                  ? 'linear-gradient(90deg, #a4b8ff, #ff90d1)'
                  : 'linear-gradient(90deg, #4361ee, #f72585)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                letterSpacing: '-0.01em',
              }}
            >
              Film Production AI Assistant
            </Typography>
            <IconButton
              color="inherit"
              onClick={toggleTheme}
              sx={{
                ml: 1,
                transition: 'all 0.3s ease',
                transform: darkMode ? 'rotate(180deg)' : 'rotate(0deg)',
                '&:hover': {
                  backgroundColor: theme.palette.mode === 'dark'
                    ? 'rgba(255,255,255,0.1)'
                    : 'rgba(0,0,0,0.05)',
                }
              }}
            >
              {darkMode ? <LightModeIcon /> : <DarkModeIcon />}
            </IconButton>
          </Toolbar>
        </AppBar>

        {/* Drawer */}
        <Drawer
          variant="temporary"
          open={drawerOpen}
          onClose={handleDrawerToggle}
          sx={{
            width: 280,
            flexShrink: 0,
            '& .MuiDrawer-paper': {
              width: 280,
              boxSizing: 'border-box',
              borderRight: 'none',
              boxShadow: theme.palette.mode === 'dark'
                ? '5px 0 20px rgba(0,0,0,0.5)'
                : '5px 0 20px rgba(0,0,0,0.1)',
              background: theme.palette.mode === 'dark'
                ? 'linear-gradient(180deg, #132f4c 0%, #0a1929 100%)'
                : 'linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%)',
            },
          }}
        >
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              p: 2,
              pt: 3,
              pb: 2,
              borderBottom: `1px solid ${theme.palette.mode === 'dark' ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.05)'}`,
            }}
          >
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <Box
                sx={{
                  background: theme.palette.mode === 'dark'
                    ? 'linear-gradient(90deg, #738bff, #ff5eb1)'
                    : 'linear-gradient(90deg, #4361ee, #f72585)',
                  borderRadius: '50%',
                  p: 1,
                  mr: 2,
                  boxShadow: theme.palette.mode === 'dark'
                    ? '0 0 15px rgba(115, 139, 255, 0.5)'
                    : '0 0 15px rgba(67, 97, 238, 0.5)',
                }}
              >
                <MovieIcon sx={{ color: '#fff' }} />
              </Box>
              <Typography variant="h6" fontWeight="bold">Navigation</Typography>
            </Box>
            <IconButton onClick={handleDrawerToggle}>
              <ChevronLeftIcon />
            </IconButton>
          </Box>
          <Box sx={{ overflow: 'auto', p: 2 }}>
            <List>
              {steps.map((step, index) => (
                <ListItem
                  key={index}
                  onClick={() => handleStepClick(index)}
                  sx={{
                    backgroundColor: activeStep === index ?
                      (theme.palette.mode === 'dark' ? 'rgba(115, 139, 255, 0.15)' : 'rgba(67, 97, 238, 0.08)') :
                      'transparent',
                    borderRadius: 2,
                    mb: 1,
                    py: 1.5,
                    transition: 'all 0.2s ease',
                    position: 'relative',
                    overflow: 'hidden',
                    cursor: 'pointer',
                    '&::before': activeStep === index ? {
                      content: '""',
                      position: 'absolute',
                      left: 0,
                      top: 0,
                      bottom: 0,
                      width: '4px',
                      background: theme.palette.mode === 'dark'
                        ? 'linear-gradient(180deg, #738bff, #ff5eb1)'
                        : 'linear-gradient(180deg, #4361ee, #f72585)',
                      borderRadius: '0 4px 4px 0',
                    } : {},
                    bgcolor: activeStep === index ?
                      (theme.palette.mode === 'dark' ? 'rgba(115, 139, 255, 0.15)' : 'rgba(67, 97, 238, 0.08)') :
                      'transparent',
                    '&:hover': {
                      bgcolor: theme.palette.mode === 'dark' ? 'rgba(115, 139, 255, 0.1)' : 'rgba(67, 97, 238, 0.05)',
                      transform: 'translateX(5px)',
                    }
                  }}
                >
                  <ListItemIcon sx={{
                    color: activeStep === index ?
                      (theme.palette.mode === 'dark' ? '#738bff' : '#4361ee') :
                      'inherit',
                    minWidth: 45,
                  }}>
                    {step.icon}
                  </ListItemIcon>
                  <ListItemText
                    primary={step.label}
                    sx={{
                      '& .MuiTypography-root': {
                        fontWeight: activeStep === index ? 600 : 400,
                        color: activeStep === index ?
                          (theme.palette.mode === 'dark' ? '#738bff' : '#4361ee') :
                          'inherit',
                      }
                    }}
                  />
                  {activeStep === index && (
                    <ChevronRightIcon sx={{
                      color: theme.palette.mode === 'dark' ? '#738bff' : '#4361ee',
                      opacity: 0.7,
                    }} />
                  )}
                </ListItem>
              ))}
            </List>
          </Box>
        </Drawer>

        {/* Main content */}
        <Box
          component="main"
          sx={{
            flexGrow: 1,
            p: { xs: 2, sm: 3, md: 4 },
            transition: 'all 0.3s ease',
            background: theme.palette.mode === 'dark'
              ? 'linear-gradient(135deg, #0a1929 0%, #132f4c 100%)'
              : 'linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%)',
            minHeight: '100vh',
            display: 'flex',
            flexDirection: 'column',
          }}
        >
          <Toolbar />

          {/* Progress indicator */}
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              mb: 2,
              px: { xs: 0, sm: 2 },
            }}
          >
            <Typography
              variant="h5"
              sx={{
                fontWeight: 700,
                background: theme.palette.mode === 'dark'
                  ? 'linear-gradient(90deg, #a4b8ff, #ff90d1)'
                  : 'linear-gradient(90deg, #4361ee, #f72585)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                letterSpacing: '-0.01em',
              }}
            >
              {steps[activeStep].label}
            </Typography>
            <Chip
              label={`Step ${activeStep + 1} of ${steps.length}`}
              color="primary"
              variant="outlined"
              sx={{
                fontWeight: 600,
                borderWidth: 2,
                px: 1,
              }}
            />
          </Box>

          {/* Stepper */}
          <Paper
            elevation={0}
            sx={{
              p: { xs: 2, sm: 3 },
              mb: 4,
              borderRadius: 3,
              border: `1px solid ${theme.palette.mode === 'dark' ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.05)'}`,
              background: theme.palette.mode === 'dark' ? 'rgba(19, 47, 76, 0.5)' : 'rgba(255, 255, 255, 0.8)',
              backdropFilter: 'blur(10px)',
            }}
          >
            <Stepper
              activeStep={activeStep}
              alternativeLabel
              sx={{
                '& .MuiStepConnector-line': {
                  minHeight: 3,
                  borderTopWidth: 3,
                  borderRadius: 3,
                  borderColor: theme.palette.mode === 'dark' ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.08)',
                },
                '& .MuiStepConnector-active': {
                  '& .MuiStepConnector-line': {
                    borderColor: theme.palette.mode === 'dark' ? '#738bff' : '#4361ee',
                  },
                },
                '& .MuiStepConnector-completed': {
                  '& .MuiStepConnector-line': {
                    borderColor: theme.palette.mode === 'dark' ? '#738bff' : '#4361ee',
                  },
                },
              }}
            >
              {steps.map((step, index) => (
                <Step
                  key={index}
                  completed={activeStep > index}
                  sx={{
                    '& .MuiStepLabel-iconContainer': {
                      transition: 'transform 0.3s ease',
                      '&:hover': {
                        transform: 'scale(1.2)',
                      },
                    },
                  }}
                >
                  <StepLabel
                    sx={{
                      cursor: 'pointer',
                      '& .MuiStepIcon-root': {
                        fontSize: '1.5rem',
                        ...(activeStep === index && {
                          color: theme.palette.mode === 'dark' ? '#738bff' : '#4361ee',
                          boxShadow: theme.palette.mode === 'dark'
                            ? '0 0 15px rgba(115, 139, 255, 0.5)'
                            : '0 0 15px rgba(67, 97, 238, 0.5)',
                          borderRadius: '50%',
                          zIndex: 1,
                        }),
                      },
                      '& .MuiStepLabel-label': {
                        mt: 1,
                        fontWeight: activeStep === index ? 600 : 400,
                        color: activeStep === index
                          ? (theme.palette.mode === 'dark' ? '#738bff' : '#4361ee')
                          : 'inherit',
                      },
                    }}
                    onClick={() => handleStepClick(index)}
                  >
                    {step.label}
                  </StepLabel>
                </Step>
              ))}
            </Stepper>
          </Paper>

          {/* Step content */}
          <Paper
            elevation={0}
            sx={{
              p: { xs: 2, sm: 3, md: 4 },
              mb: 4,
              borderRadius: 3,
              flexGrow: 1,
              border: `1px solid ${theme.palette.mode === 'dark' ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.05)'}`,
              background: theme.palette.mode === 'dark' ? 'rgba(19, 47, 76, 0.5)' : 'rgba(255, 255, 255, 0.8)',
              backdropFilter: 'blur(10px)',
              transition: 'all 0.3s ease',
              animation: 'fadeIn 0.5s ease-out',
              '@keyframes fadeIn': {
                '0%': {
                  opacity: 0,
                  transform: 'translateY(10px)',
                },
                '100%': {
                  opacity: 1,
                  transform: 'translateY(0)',
                },
              },
            }}
          >
            {getStepContent(activeStep)}
          </Paper>

          {/* Navigation buttons */}
          <Box
            sx={{
              display: 'flex',
              justifyContent: 'space-between',
              mb: 4,
              px: { xs: 0, sm: 2 },
            }}
          >
            <Button
              variant="outlined"
              disabled={activeStep === 0}
              onClick={handleBack}
              startIcon={<ChevronLeftIcon />}
              sx={{
                borderWidth: 2,
                px: 3,
                '&.Mui-disabled': {
                  opacity: 0.5,
                },
              }}
            >
              Back
            </Button>
            <Button
              variant="contained"
              disabled={
                activeStep === steps.length - 1 ||
                (activeStep === 0 && !scriptText) ||
                isLoading
              }
              onClick={activeStep === 0 && scriptText ? processScript : handleNext}
              endIcon={<ChevronRightIcon />}
              sx={{
                px: 3,
                background: theme.palette.mode === 'dark'
                  ? 'linear-gradient(90deg, #738bff, #ff5eb1)'
                  : 'linear-gradient(90deg, #4361ee, #f72585)',
                '&:hover': {
                  background: theme.palette.mode === 'dark'
                    ? 'linear-gradient(90deg, #5a6ecc, #cc4a8e)'
                    : 'linear-gradient(90deg, #354db8, #c51e6a)',
                },
                '&.Mui-disabled': {
                  opacity: 0.5,
                  background: theme.palette.mode === 'dark'
                    ? 'linear-gradient(90deg, #738bff, #ff5eb1)'
                    : 'linear-gradient(90deg, #4361ee, #f72585)',
                  color: 'white',
                },
              }}
            >
              {activeStep === 0 && scriptText ? 'Process Script' : 'Next'}
            </Button>
          </Box>

          {/* Footer */}
          <Box
            sx={{
              mt: 'auto',
              pt: 4,
              pb: 2,
              textAlign: 'center',
              opacity: 0.8,
              transition: 'opacity 0.3s ease',
              '&:hover': {
                opacity: 1,
              },
            }}
          >
            <Divider sx={{ mb: 2 }} />
            <Box
              sx={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: 1,
              }}
            >
              <MovieIcon fontSize="small" color="primary" />
              <Typography
                variant="body2"
                color="textSecondary"
                sx={{
                  fontWeight: 500,
                  letterSpacing: '0.02em',
                }}
              >
                Film Production AI Assistant | Powered by OpenAI GPT-4.1 Mini
              </Typography>
            </Box>
          </Box>
        </Box>
      </Box>
    </ThemeProvider>
  );
}