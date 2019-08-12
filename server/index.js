const express = require('express');
const path = require('path');

const app = express();
const port = process.env.PORT || 8080;

app.use('/', express.static('../www'));

app.get('*', (req, res) => {
    res.status(400);
    res.sendFile(path.join(__dirname, '../www/not_found.html'));
});

app.listen(port, () => console.log(`Listening on port ${port}`));
