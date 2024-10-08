document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const identity = document.getElementById('identity').value;
    const password = document.getElementById('password').value;
    const user = document.getElementById('user').value;

    fetch(`${ip}/auth`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'fromSite': true,
        },
        body: JSON.stringify({ identity: identity, password: password, user: user})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Redirect to main.html after successful login
            window.location.href = "main";
        } else {
            alert('Login failed: ' + data.message);
        }
    })
    .catch(error => console.error('Error:', error));
});