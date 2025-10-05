const express = require('express');
const axios = require('axios');
const app = express();

app.use(express.json());

// ⚠️ CONFIGURA TUS SECRETOS AQUÍ (o usa variables de entorno en Render)
const TELEGRAM_BOT_TOKEN = 'TU_TOKEN_AQUI'; // ← Reemplaza
const TELEGRAM_CHAT_ID = 'TU_CHAT_ID_AQUI'; // ← Reemplaza

const TELEGRAM_URL = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`;

app.post('/webhook', async (req, res) => {
    try {
        const { symbol, action, price } = req.body;
        const direction = action === 'buy' ? '🟢 COMPRA' : '🔴 VENTA';
        const message = `${direction}\nActivo: ${symbol}\nPrecio: ${parseFloat(price).toFixed(5)}\nFuente: TradingView - XTB Commodities`;
        
        await axios.post(TELEGRAM_URL, {
            chat_id: TELEGRAM_CHAT_ID,
            text: message,
            parse_mode: 'HTML'
        });
        
        console.log('Mensaje enviado a Telegram:', message);
        res.status(200).send('OK');
    } catch (error) {
        console.error('Error:', error.message);
        res.status(500).send('Error');
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0', () => {
    console.log(`Servidor escuchando en puerto ${PORT}`);
});