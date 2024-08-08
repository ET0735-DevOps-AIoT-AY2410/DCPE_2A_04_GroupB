const ip = 'http://127.0.0.1:5000'

var books = [];

const reserveBorrowList = [];
//Turn on/off overlay
function on() {
    document.getElementById("chosenBook").innerHTML = document.getElementById('reservedBook').value;
    document.getElementById("overlay").style.display = "block";
    document.getElementById("overlay-box").style.display = "block";
}

function off(event) {
    
    if (document.getElementById('location').value !== "") {
        if (confirm("Are you sure you want to stop reservation?")) {
            document.getElementById('reservationForm').reset();
            document.getElementById("overlay").style.display = "none";
            document.getElementById("overlay-box").style.display = "none";
            document.getElementById('confirmationMessage').style.display = 'none';
        }
        else {
            event.preventDefault();
        }
    }
    else{
        document.getElementById("overlay").style.display = "none";
        document.getElementById("overlay-box").style.display = "none";
        document.getElementById('confirmationMessage').style.display = 'none';
    }
}

document.onkeydown = function(evt) {
    evt = evt || window.event;
    var isEscape = false;
    if ("key" in evt) {
        isEscape = (evt.key === "Escape" || evt.key === "Esc");
    } else {
        isEscape = (evt.keyCode === 27);
    }
    if (isEscape && document.getElementById("overlay").style.display == "block") {
        document.getElementById("overlay").style.display = "none";
        document.getElementById("overlay-box").style.display = "none";
        document.getElementById('confirmationMessage').style.display = 'none';
    }
};

function checkLocation(event) {
    if (document.getElementById('location').value === "") {
        alert("Please fill out all a location.");
        event.preventDefault();
        return;
    }
}

function loadBorrowedReserved(info) {
    fetch(`${ip}/reservations`)
        .then(response => response.json())
        .then(data => {
            for (let i = 0; i < 2; i++){
                if (data[i][info] && data[i][info].length > 0) {
                    const list = data[i][info];
                    for (let j = 0; j < list.length; j++) {
                        bookId = list[j][0];

                        reserveBorrowList.push(bookId);
                    }
                }
            }
        })
        .catch(error => console.error(`Error fetching books:`, error));
    }

//Load books
document.addEventListener('DOMContentLoaded', () => {
    fetch(`${ip}/session`, {
        method: 'GET',
        credentials: 'include'
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        console.log('Session data:', data);
        if (!data.loggedIn) {
            window.location.href = '/';
        } else {
            document.getElementById('name').innerHTML = data.name;
            document.getElementById('identity').innerHTML = data.identity;
            info = data.name + "&" + data.identity;
            loadBorrowedReserved (info)
        }
    })

    fetch(`${ip}/books`, {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        books = data

        const bookContainer = document.getElementById('books');

        books.forEach(book => {
            const bookElement = document.createElement('div');
            bookElement.classList.add('book');
            bookElement.innerHTML = `
                <img src="${book.image}" alt="${book.bookTitle}">
                <h3>${book.bookTitle}</h3>
                <button class="reserve-button" data-id="${book.id}">Reserve book</button>
            `;
            bookContainer.appendChild(bookElement);
        });

        document.querySelectorAll('.reserve-button').forEach(button => {
            button.addEventListener('click', () => {
                const bookId = parseInt(button.getAttribute('data-id'));
                reserveBook(bookId);
            });
        });  
    });
});


function reserveBook(bookId) {
    const book = books.find(p => p.id === bookId);
    document.getElementById('reservedBook').value = book.bookTitle;
    document.getElementById('id').value = book.id;
    on();
}

//Pass data to back end
document.getElementById('reservationForm').addEventListener('submit', function(event) {
    event.preventDefault();

    if (reserveBorrowList.includes(document.getElementById('id').value.toString())){
        alert("Book reserved/borrowed already")
        document.getElementById("overlay").style.display = "none";
        document.getElementById("overlay-box").style.display = "none";
        document.getElementById('confirmationMessage').style.display = 'none';

    } else if (reserveBorrowList.length >= 10){
        alert("Only 10 books can be borrowed at a time")
        document.getElementById("overlay").style.display = "none";
        document.getElementById("overlay-box").style.display = "none";
        document.getElementById('confirmationMessage').style.display = 'none';

    } else {
        const formData = {
            name: document.getElementById('name').innerHTML,
            bookID: document.getElementById('id').value,
            identity: document.getElementById('identity').innerHTML,
            bookTitle: document.getElementById('reservedBook').value,
            location: document.getElementById('location').value,
            reserveTime: new Date().toISOString()
        };

        reserveBorrowList.push(document.getElementById('id').value.toString())

        //Public IP below
        fetch(`${ip}/reserve`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('confirmationMessage').style.display = 'block';
                document.getElementById('reservationForm').reset();
            } else {
                alert('There was a problem with your reservation. Please try again.');
            }
        })
        .catch(error => console.error('Error:', error));
    }  
});

function logout() {
    fetch(`${ip}/logout`, {
        method: 'POST',
    }).then(() => {
        window.location.href = "/";
    }).catch(error => console.error('Error during logout:', error));
}