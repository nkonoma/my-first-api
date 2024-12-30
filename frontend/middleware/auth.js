const jwt = require('jsonwebtoken');

function authenticateToken(req, res, next) {
    // Check if user is logged in
    const token = localStorage.getItem('token');
    if (!token) {
        return res.redirect('/login');
    }

    try {
        // Verify token
        jwt.verify(token, 'your-secret-key-here');
        next();
    } catch (err) {
        localStorage.removeItem('token');
        return res.redirect('/login');
    }
}

module.exports = authenticateToken; 
