import React, { useState } from 'react';
import './App.css';

function App() {
  const [symbol, setSymbol] = useState('MSFT');
  const [stockData, setStockData] = useState(null);

  const fetchStock = async () => {
    try {
      const response = await fetch(`http://localhost:5000/api/stock/${symbol}`);
      const data = await response.json();
      setStockData(data);
    } catch (err) {
      console.error(err);
      setStockData(null);
    }
  };

  return (
    <div className="App">
      <h1>📈 Stock Rooms Viewer</h1>
      <input
        type="text"
        value={symbol}
        onChange={(e) => setSymbol(e.target.value)}
        placeholder="Enter symbol (e.g., AAPL)"
      />
      <button onClick={fetchStock}>Get Stock</button>

      {stockData ? (
        <div>
          <h2>{stockData.symbol}</h2>
          <p>💲 Price: ${stockData.price}</p>
          <p>🕒 Last Updated: {stockData.timestamp}</p>
        </div>
      ) : (
        <p>No data available. Try searching.</p>
      )}
    </div>
  );
}

export default App;

