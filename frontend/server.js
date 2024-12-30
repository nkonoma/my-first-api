const express = require('express');
const app = express();
const port = 3000;

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

app.get('/dashboard', (req, res) => {
    console.log('Dashboard route hit');
    try {
        res.render('dashboard');
    } catch (error) {
        console.error('Error rendering dashboard:', error);
        res.status(500).send('Error loading dashboard');
    }
});

// Catch-all route for undefined paths
app.get('*', (req, res) => {
    res.redirect('/login');
});

// Start server
app.listen(port, () => {
    console.log(`Frontend server running at http://localhost:${port}`);
}); 
