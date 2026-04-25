import React, { useEffect, useState } from 'react';
import {
  Card, CardContent, Typography, Box, Button, CircularProgress,
  Alert, Chip
} from '@mui/material';
import { Refresh, CheckCircle, Error as ErrorIcon } from '@mui/icons-material';
import { reportsAPI, multiAgentAPI } from '../services/api';

function AIReport() {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadLatestReport();
  }, []);

  const loadLatestReport = async () => {
    try {
      const response = await reportsAPI.getLatest();
      setReport(response.data);
      setError('');
    } catch (err) {
      setError('보고서를 불러올 수 없습니다.');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateReport = async () => {
    setGenerating(true);
    setError('');
    try {
      await multiAgentAPI.trigger();
      alert('AI 분석이 시작되었습니다! 약 2-3분 후 결과를 확인하세요.');
      setTimeout(loadLatestReport, 3000);
    } catch (err) {
      setError(err.response?.data?.detail || 'AI 분석 요청 실패');
    } finally {
      setGenerating(false);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" p={4}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Card>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="h5" fontWeight="bold">
            🤖 AI 투자 분석 리포트
          </Typography>
          <Button
            variant="contained"
            startIcon={generating ? <CircularProgress size={20} /> : <Refresh />}
            onClick={handleGenerateReport}
            disabled={generating}
          >
            {generating ? '분석 중...' : '새 분석 실행'}
          </Button>
        </Box>

        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

        {report ? (
          <>
            <Box mb={2}>
              <Chip
                icon={<CheckCircle />}
                label={`생성일: ${report.created_at}`}
                color="success"
                sx={{ mr: 1 }}
              />
              {report.day_of_week === 'Monday' && (
                <Chip label="📅 주간 추천" color="primary" />
              )}
            </Box>

            <Typography variant="h6" gutterBottom fontWeight="bold">
              {report.report_title || '시장 분석 보고서'}
            </Typography>

            <Box sx={{ whiteSpace: 'pre-line', lineHeight: 1.8 }}>
              {report.recommendations}
            </Box>
          </>
        ) : (
          <Alert severity="info" icon={<ErrorIcon />}>
            아직 생성된 리포트가 없습니다. 위 버튼을 클릭하여 AI 분석을 시작하세요!
          </Alert>
        )}
      </CardContent>
    </Card>
  );
}

export default AIReport;
