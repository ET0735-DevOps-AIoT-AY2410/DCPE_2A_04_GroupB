function logout() {
    fetch(`${ip}/auth`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'fromSite': true
        },
    }).then(() => {
        window.location.href = "/";
    }).catch(error => console.error('Error during logout:', error));
}

document.addEventListener('DOMContentLoaded', () => {
    fetch(`${ip}/auth`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'fromSite': true
        },
        credentials: 'include'
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        console.log('Session data:', data);
        if (window.location.href != `${ip}/`){
            if (!data.loggedIn) {
                window.location.href = '/';
            } else {
                document.getElementById('name').innerHTML = data.name;
                document.getElementById('identity').innerHTML = data.identity;
                info = data.name + "&" + data.identity;
                loadBorrowedReserved(info) 
            }
        } else {
            if (data.loggedIn) {
                window.location.href = '/main';
            }
        }
    })    
});
