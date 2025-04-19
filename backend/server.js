const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();
const PORT = 5000;

app.use(cors());

// Replace with your real API key
const API_KEY = 'YOUR_ALPHA_VANTAGE_API_KEY';

app.get('/api/stock/:symbol', async (req, res) => {
  const symbol = req.params.symbol;
  try {
    const response = await axios.get(
      `https://www.alphavantage.co/query`,
      {
        params: {
          function: 'TIME_SERIES_INTRADAY',
          symbol,
          interval: '1min',
          apikey: API_KEY
        }
      }
    );

    const timeSeries = response.data['Time Series (1min)'];
    if (!timeSeries) return res.status(404).json({ error: 'Stock data not found' });

    const latestTimestamp = Object.keys(timeSeries)[0];
    const latestData = timeSeries[latestTimestamp];

    res.json({
      symbol: symbol.toUpperCase(),
      price: latestData['1. open'],
      timestamp: latestTimestamp
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Failed to fetch stock data' });
  }
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
