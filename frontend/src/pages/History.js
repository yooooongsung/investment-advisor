import React, { useEffect, useState } from 'react';
import {
  Container, Box, Typography, Card, CardContent, Grid, Chip,
  AppBar, Toolbar, Button, CircularProgress, Divider
} from '@mui/material';
import { ArrowBack, CalendarToday, TrendingUp } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { reportsAPI } from '../services/api';

function History() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [days, setDays] = useState(7);
  const navigate = useNavigate();

  useEffect(() => {
    loadReports();
  }, [days]);

  const loadReports = async () => {
    setLoading(true);
    try {
      const response = await reportsAPI.getHistory(days);
      setReports(response.data);
    } catch (error) {
      console.error('리포트 기록 로드 실패:', error);
    } finally {
      setLoading(false);
    }
  };

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
            📚 AI 분석 리포트 히스토리
          </Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
          <Typography variant="h5" fontWeight="bold">
            과거 AI 분석 기록
          </Typography>
          <Box display="flex" gap={1}>
            {[7, 14, 30].map((d) => (
              <Chip
                key={d}
                label={`${d}일`}
                color={days === d ? 'primary' : 'default'}
                onClick={() => setDays(d)}
                clickable
              />
            ))}
          </Box>
        </Box>

        {loading ? (
          <Box display="flex" justifyContent="center" p={4}>
            <CircularProgress />
          </Box>
        ) : (
          <Grid container spacing={3}>
            {reports.map((report, index) => (
              <Grid item xs={12} key={index}>
                <Card elevation={3}>
                  <CardContent>
                    <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                      <Box display="flex" alignItems="center" gap={1}>
                        <CalendarToday color="action" fontSize="small" />
                        <Typography variant="h6" fontWeight="bold">
                          {report.report_title || `AI 분석 리포트 #${reports.length - index}`}
                        </Typography>
                      </Box>
                      <Box display="flex" gap={1}>
                        <Chip
                          label={report.created_at}
                          size="small"
                          color="primary"
                          variant="outlined"
                        />
                        {report.day_of_week === 'Monday' && (
                          <Chip
                            icon={<TrendingUp />}
                            label="주간 추천"
                            size="small"
                            color="success"
                          />
                        )}
                      </Box>
                    </Box>

                    <Divider sx={{ mb: 2 }} />

                    <Typography
                      variant="body1"
                      sx={{
                        whiteSpace: 'pre-line',
                        lineHeight: 1.8,
                        color: 'text.primary',
                        maxHeight: '300px',
                        overflowY: 'auto'
                      }}
                    >
                      {report.recommendations}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}

            {reports.length === 0 && (
              <Grid item xs={12}>
                <Box textAlign="center" p={4}>
                  <Typography variant="h6" color="text.secondary">
                    해당 기간에 생성된 리포트가 없습니다.
                  </Typography>
                </Box>
              </Grid>
            )}
          </Grid>
        )}
      </Container>
    </>
  );
}

export default History;
