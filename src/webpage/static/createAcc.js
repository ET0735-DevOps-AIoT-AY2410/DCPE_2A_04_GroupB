document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const identity = document.getElementById('identity').value;
    const password = document.getElementById('password').value;
    const user = document.getElementById('user').value;

    fetch(`${ip}/auth`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'fromSite': true
        },
        body: JSON.stringify({ identity: identity, password: password, user: user})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = '/';
        } else {
            alert('Sign Up failed: ' + data.message);
        }
    })
    .catch(error => console.error('Error:', error));
});