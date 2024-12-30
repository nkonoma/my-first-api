document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    try {
        const response = await fetch('http://localhost:8000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: document.getElementById('username').value,
                password: document.getElementById('password').value
            })
        });

        const data = await response.json();
        
        if (response.ok) {
            alert('Login successful!');
            window.location.href = '/dashboard';
        } else {
            alert('Login failed: ' + data.detail);
        }
    } catch (error) {
        alert('Error during login: ' + error);
    }
}); 
