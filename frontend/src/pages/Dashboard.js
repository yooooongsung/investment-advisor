import React, { useState } from 'react';
import {
  Container, Box, Typography, AppBar, Toolbar, Button, Paper, Grid,
  Tabs, Tab, IconButton, Menu, MenuItem
} from '@mui/material';
import { Logout, Person, History as HistoryIcon, MoreVert } from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import MarketOverview from '../components/MarketOverview';
import MarketChart from '../components/MarketChart';
import AIReport from '../components/AIReport';

function Dashboard() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [selectedMarket, setSelectedMarket] = useState('KOSPI');
  const [anchorEl, setAnchorEl] = useState(null);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const markets = ['KOSPI', 'KOSDAQ', 'NASDAQ', 'Bitcoin'];

  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            🤖 AI 투자 비서
          </Typography>
          <Box display="flex" alignItems="center" gap={1}>
            <Button
              color="inherit"
              startIcon={<HistoryIcon />}
              onClick={() => navigate('/history')}
            >
              리포트 히스토리
            </Button>
            <IconButton
              color="inherit"
              onClick={(e) => setAnchorEl(e.currentTarget)}
            >
              <MoreVert />
            </IconButton>
            <Menu
              anchorEl={anchorEl}
              open={Boolean(anchorEl)}
              onClose={() => setAnchorEl(null)}
            >
              <MenuItem onClick={() => { navigate('/profile'); setAnchorEl(null); }}>
                <Person sx={{ mr: 1 }} /> 내 프로필
              </MenuItem>
              <MenuItem onClick={() => { handleLogout(); setAnchorEl(null); }}>
                <Logout sx={{ mr: 1 }} /> 로그아웃
              </MenuItem>
            </Menu>
          </Box>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Paper sx={{ p: 3, mb: 3, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
          <Typography variant="h4" gutterBottom sx={{ color: 'white' }}>
            안녕하세요, {user?.name}님! 👋
          </Typography>
          <Typography variant="body1" sx={{ color: 'rgba(255,255,255,0.9)' }}>
            투자 성향: <strong>{user?.investment_style}</strong> | 
            투자 목표: <strong>{user?.investment_goal}</strong> |
            예산: <strong>{user?.budget?.toLocaleString()}만원</strong>
          </Typography>
        </Paper>

        <Box mb={4}>
          <Typography variant="h5" gutterBottom fontWeight="bold">
            📊 실시간 시장 현황
          </Typography>
          <MarketOverview />
        </Box>

        <Box mb={4}>
          <Typography variant="h5" gutterBottom fontWeight="bold">
            📈 시장 추세 분석
          </Typography>
          <Paper sx={{ p: 2 }}>
            <Tabs
              value={selectedMarket}
              onChange={(e, val) => setSelectedMarket(val)}
              variant="fullWidth"
              sx={{ mb: 2 }}
            >
              {markets.map((market) => (
                <Tab key={market} label={market} value={market} />
              ))}
            </Tabs>
            <MarketChart symbol={selectedMarket} />
          </Paper>
        </Box>

        <Box>
          <AIReport />
        </Box>
      </Container>
    </>
  );
}

export default Dashboard;
