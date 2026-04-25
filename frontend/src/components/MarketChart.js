import React, { useEffect, useState } from 'react';
import {
  LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import { Box, Card, CardContent, Typography, ToggleButtonGroup, ToggleButton } from '@mui/material';
import { marketAPI } from '../services/api';

function MarketChart({ symbol = 'KOSPI' }) {
  const [data, setData] = useState([]);
  const [chartType, setChartType] = useState('line');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadChartData();
  }, [symbol]);

  const loadChartData = async () => {
    try {
      const response = await marketAPI.getDetails(symbol);
      // 날짜 순서대로 정렬
      const sortedData = response.data.sort((a, b) => 
        new Date(a.date) - new Date(b.date)
      );
      setData(sortedData);
    } catch (error) {
      console.error('차트 데이터 로드 실패:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return `${date.getMonth() + 1}/${date.getDate()}`;
  };

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <Box sx={{ bgcolor: 'white', p: 1.5, border: '1px solid #ccc', borderRadius: 1 }}>
          <Typography variant="caption" display="block">
            {payload[0].payload.date}
          </Typography>
          <Typography variant="body2" color="primary" fontWeight="bold">
            종가: {payload[0].value.toLocaleString()}
          </Typography>
          {payload[0].payload.rsi && (
            <Typography variant="body2" color="text.secondary">
              RSI: {payload[0].payload.rsi.toFixed(1)}
            </Typography>
          )}
          {payload[0].payload.ma5 && (
            <Typography variant="body2" color="success.main">
              MA5: {payload[0].payload.ma5.toFixed(2)}
            </Typography>
          )}
          {payload[0].payload.ma20 && (
            <Typography variant="body2" color="warning.main">
              MA20: {payload[0].payload.ma20.toFixed(2)}
            </Typography>
          )}
        </Box>
      );
    }
    return null;
  };

  if (loading) return <Typography>차트 로딩 중...</Typography>;

  return (
    <Card>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="h6">{symbol} 추세 차트 (최근 30일)</Typography>
          <ToggleButtonGroup
            value={chartType}
            exclusive
            onChange={(e, val) => val && setChartType(val)}
            size="small"
          >
            <ToggleButton value="line">라인</ToggleButton>
            <ToggleButton value="area">영역</ToggleButton>
          </ToggleButtonGroup>
        </Box>

        <ResponsiveContainer width="100%" height={300}>
          {chartType === 'line' ? (
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" tickFormatter={formatDate} />
              <YAxis />
              <Tooltip content={<CustomTooltip />} />
              <Legend />
              <Line type="monotone" dataKey="close" stroke="#1976d2" name="종가" strokeWidth={2} />
              <Line type="monotone" dataKey="ma5" stroke="#4caf50" name="MA5" strokeWidth={1} />
              <Line type="monotone" dataKey="ma20" stroke="#ff9800" name="MA20" strokeWidth={1} />
            </LineChart>
          ) : (
            <AreaChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" tickFormatter={formatDate} />
              <YAxis />
              <Tooltip content={<CustomTooltip />} />
              <Legend />
              <Area type="monotone" dataKey="close" stroke="#1976d2" fill="#1976d2" fillOpacity={0.3} name="종가" />
            </AreaChart>
          )}
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}

export default MarketChart;
