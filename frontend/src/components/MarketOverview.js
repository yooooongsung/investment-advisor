import React, { useEffect, useState } from 'react';
import { Grid, Card, CardContent, Typography, Chip, Box, CircularProgress } from '@mui/material';
import { TrendingUp, TrendingDown } from '@mui/icons-material';
import { marketAPI } from '../services/api';

function MarketOverview() {
  const [markets, setMarkets] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadMarketData();
  }, []);

  const loadMarketData = async () => {
    try {
      const response = await marketAPI.getSummary();
      setMarkets(response.data);
    } catch (error) {
      console.error('시장 데이터 로드 실패:', error);
    } finally {
      setLoading(false);
    }
  };

  const getRSIStatus = (rsi) => {
    if (rsi >= 70) return { label: '과매수', color: 'error' };
    if (rsi <= 30) return { label: '과매도', color: 'success' };
    return { label: '정상', color: 'default' };
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" p={4}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Grid container spacing={3}>
      {markets.map((market) => {
        const rsiStatus = getRSIStatus(market.rsi);
        const isPositive = market.daily_return >= 0;

        return (
          <Grid item xs={12} sm={6} md={3} key={market.market}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {market.market}
                </Typography>
                <Typography variant="h5" fontWeight="bold">
                  {market.close.toLocaleString()}
                </Typography>
                <Box display="flex" alignItems="center" mt={1} mb={1}>
                  {isPositive ? (
                    <TrendingUp color="success" />
                  ) : (
                    <TrendingDown color="error" />
                  )}
                  <Typography
                    variant="body2"
                    color={isPositive ? 'success.main' : 'error.main'}
                    ml={0.5}
                  >
                    {isPositive ? '+' : ''}{(market.daily_return * 100).toFixed(2)}%
                  </Typography>
                </Box>
                <Box display="flex" gap={1}>
                  <Chip
                    label={`RSI ${market.rsi.toFixed(1)}`}
                    color={rsiStatus.color}
                    size="small"
                  />
                  <Chip
                    label={market.signal}
                    size="small"
                    variant="outlined"
                  />
                </Box>
                <Typography variant="caption" color="text.secondary" mt={1} display="block">
                  {market.date}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        );
      })}
    </Grid>
  );
}

export default MarketOverview;
