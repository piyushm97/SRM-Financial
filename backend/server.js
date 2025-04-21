// backend/server.js
const express = require('express');
const axios = require('axios');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = 5000;

app.use(cors());

// Replace with your actual API key from Alpha Vantage or any stock API
const API_KEY = process.env.STOCK_API_KEY;
const BASE_URL = 'https://www.alphavantage.co/query';

app.get('/api/stocks', async (req, res) => {
    const { symbol = 'AAPL' } = req.query;

    try {
        const response = await axios.get(BASE_URL, {
            params: {
                function: 'TIME_SERIES_INTRADAY',
                symbol,
                interval: '5min',
                apikey: API_KEY,
            }
        });

        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: 'Error fetching stock data' });
    }
});

app.listen(PORT, () => {
    console.log(`✅ Backend server running on http://localhost:${PORT}`);
});
