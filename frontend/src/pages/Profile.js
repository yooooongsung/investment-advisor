import React, { useState } from 'react';
import {
  Container, Box, Typography, Card, CardContent, Grid, TextField,
  Button, AppBar, Toolbar, Divider, MenuItem, Alert, CircularProgress
} from '@mui/material';
import { ArrowBack, Save, Person, TrendingUp, AccountBalance } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function Profile() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [editing, setEditing] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: user?.name || '',
    age: user?.age || '',
    investment_style: user?.investment_style || '',
    investment_goal: user?.investment_goal || '',
    budget: user?.budget || '',
    experience: user?.experience || ''
  });

  const investmentStyles = ['공격투자형', '적극투자형', '위험중립형', '안정추구형', '안정형'];
  const experiences = ['초보 (1년 미만)', '초급 (1-3년)', '중급 (3-5년)', '고급 (5년 이상)'];

  const handleSave = async () => {
    setLoading(true);
    setError('');
    try {
      const token = localStorage.getItem('token');
      await axios.put(`${API_URL}/api/auth/profile`, {
        ...formData,
        age: parseInt(formData.age),
        budget: parseInt(formData.budget)
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      setSuccess(true);
      setEditing(false);
      setTimeout(() => setSuccess(false), 3000);
    } catch (err) {
      setError(err.response?.data?.detail || '프로필 업데이트 실패');
    } finally {
      setLoading(false);
    }
  };

  const ProfileItem = ({ icon, label, value }) => (
    <Box display="flex" alignItems="center" mb={2}>
      <Box sx={{ mr: 2, color: 'primary.main' }}>{icon}</Box>
      <Box>
        <Typography variant="caption" color="text.secondary">
          {label}
        </Typography>
        <Typography variant="body1" fontWeight="bold">
          {value}
        </Typography>
      </Box>
    </Box>
  );

  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Button
            color="inherit"
            startIcon={<ArrowBack />}
            onClick={() => navigate('/dashboard')}
          >
            대시보드로
          </Button>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1, ml: 2 }}>
            👤 내 프로필
          </Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
        {success && (
          <Alert severity="success" sx={{ mb: 3 }}>
            프로필이 업데이트되었습니다!
          </Alert>
        )}
        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        <Card elevation={3}>
          <CardContent sx={{ p: 4 }}>
            <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
              <Typography variant="h5" fontWeight="bold">
                📊 투자자 프로필
              </Typography>
              <Button
                variant={editing ? 'contained' : 'outlined'}
                startIcon={editing ? (loading ? <CircularProgress size={20} /> : <Save />) : <Person />}
                onClick={editing ? handleSave : () => setEditing(true)}
                disabled={loading}
              >
                {editing ? (loading ? '저장 중...' : '저장') : '수정'}
              </Button>
            </Box>

            <Divider sx={{ mb: 3 }} />

            {!editing ? (
              <Grid container spacing={3}>
                <Grid item xs={12} sm={6}>
                  <ProfileItem
                    icon={<Person />}
                    label="이름"
                    value={user?.name}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <ProfileItem
                    icon={<Person />}
                    label="나이"
                    value={`${user?.age}세`}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <ProfileItem
                    icon={<TrendingUp />}
                    label="투자 성향"
                    value={user?.investment_style}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <ProfileItem
                    icon={<AccountBalance />}
                    label="투자 예산"
                    value={`${user?.budget?.toLocaleString()}만원`}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <ProfileItem
                    icon={<TrendingUp />}
                    label="투자 경험"
                    value={user?.experience}
                  />
                </Grid>
                <Grid item xs={12}>
                  <Box sx={{ p: 2, bgcolor: 'grey.50', borderRadius: 1 }}>
                    <Typography variant="caption" color="text.secondary">
                      투자 목표
                    </Typography>
                    <Typography variant="body1" fontWeight="bold">
                      {user?.investment_goal}
                    </Typography>
                  </Box>
                </Grid>
              </Grid>
            ) : (
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="이름"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="나이"
                    type="number"
                    value={formData.age}
                    onChange={(e) => setFormData({ ...formData, age: e.target.value })}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    select
                    label="투자 성향"
                    value={formData.investment_style}
                    onChange={(e) => setFormData({ ...formData, investment_style: e.target.value })}
                  >
                    {investmentStyles.map((style) => (
                      <MenuItem key={style} value={style}>{style}</MenuItem>
                    ))}
                  </TextField>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="투자 예산 (만원)"
                    type="number"
                    value={formData.budget}
                    onChange={(e) => setFormData({ ...formData, budget: e.target.value })}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    select
                    label="투자 경험"
                    value={formData.experience}
                    onChange={(e) => setFormData({ ...formData, experience: e.target.value })}
                  >
                    {experiences.map((exp) => (
                      <MenuItem key={exp} value={exp}>{exp}</MenuItem>
                    ))}
                  </TextField>
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="투자 목표"
                    multiline
                    rows={3}
                    value={formData.investment_goal}
                    onChange={(e) => setFormData({ ...formData, investment_goal: e.target.value })}
                  />
                </Grid>
              </Grid>
            )}
          </CardContent>
        </Card>

        <Box mt={3}>
          <Card elevation={1}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                📌 계정 정보
              </Typography>
              <Box display="flex" justifyContent="space-between" mt={2}>
                <Typography variant="body2" color="text.secondary">
                  사용자 ID
                </Typography>
                <Typography variant="body2" fontWeight="bold">
                  {user?.username}
                </Typography>
              </Box>
              <Box display="flex" justifyContent="space-between" mt={1}>
                <Typography variant="body2" color="text.secondary">
                  가입일
                </Typography>
                <Typography variant="body2" fontWeight="bold">
                  {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Box>
      </Container>
    </>
  );
}

export default Profile;
