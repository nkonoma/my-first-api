const express = require('express');
const app = express();
const port = 3000;
const authenticateToken = require('./middleware/auth');

// Middleware to parse JSON bodies
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Set EJS as templating engine
app.set('view engine', 'ejs');

// Serve static files
app.use(express.static('public'));
app.use(express.static('views'));

// Routes
app.get('/', (req, res) => {
    res.redirect('/login');
});

app.get('/login', (req, res) => {
    res.render('login');
});

app.get('/dashboard', authenticateToken, (req, res) => {
    res.render('dashboard');
});

// Catch-all route for undefined paths
app.get('*', (req, res) => {
    res.redirect('/login');
});

// Start server
app.listen(port, () => {
    console.log(`Frontend server running at http://localhost:${port}`);
}); 
