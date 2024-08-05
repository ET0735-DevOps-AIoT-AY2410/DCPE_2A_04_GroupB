const ip = 'http://127.0.0.1:5000'
        
//Books list
const books = [
    { id: 1, bookTitle: 'Book 1', image: 'https://m.media-amazon.com/images/I/81DFDGzHZqL._AC_UF1000,1000_QL80_.jpg' },
    { id: 2, bookTitle: 'Book 2', image: 'https://m.media-amazon.com/images/I/51gLEj8UHzL._AC_UF1000,1000_QL80_.jpg' },
    { id: 3, bookTitle: 'Book 3', image: 'https://m.media-amazon.com/images/I/91Yob+SFXdL._AC_UF1000,1000_QL80_.jpg' },
    { id: 4, bookTitle: 'Book 4', image: 'https://m.media-amazon.com/images/I/61lBRY5h+NL._AC_UF1000,1000_QL80_.jpg' },
    { id: 5, bookTitle: 'Book 5', image: 'https://m.media-amazon.com/images/I/915SPe6hrfL._SY342_.jpg' },
    { id: 6, bookTitle: 'Book 6', image: 'https://m.media-amazon.com/images/I/91NPng6lBsL._AC_UF1000,1000_QL80_.jpg' },
    { id: 7, bookTitle: 'Book 7', image: 'https://www.hoddereducation.sg/productCovers/9789810631307.jpg' },
    { id: 8, bookTitle: 'Book 8', image: 'https://www.hoddereducation.sg/productCovers/9789810631154.jpg' },
    { id: 9, bookTitle: 'Book 9', image: 'https://m.media-amazon.com/images/I/612ADI+BVlL._AC_UF1000,1000_QL80_.jpg' },
    { id: 10, bookTitle: 'Book 10', image: 'https://m.media-amazon.com/images/I/61KPPB-34FL._AC_UF1000,1000_QL80_.jpg' },
];


//Turn on/off overlay
function on() {
    document.getElementById("chosenBook").innerHTML = document.getElementById('reservedBook').value;
    document.getElementById("overlay").style.display = "block";
    document.getElementById("overlay-box").style.display = "block";
}

function off() {
    
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

function checkLocation() {
    if (document.getElementById('location').value === "") {
        alert("Please fill out all a location.");
        event.preventDefault();
        return;
    }
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
        }
    })
    
    fetch(`${ip}/reservations`)
        .then(response => response.json())
        .then(data => {
            var reserveBorrowList = [];
            for (let j = 0; j < 2; j++){
                if (data[j][info] && data[j][info].length > 0) {
                    const list = data[j][info];
                    for (let i = 0; i < list.length; i++) {
                        bookId = list[i][0];

                        reserveBorrowList.push(bookId);
                    }
                }
            }

            console.log(reserveBorrowList)
        })
        .catch(error => console.error(`Error fetching ${endpoint} books:`, error));


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


function reserveBook(bookId) {
    const book = books.find(p => p.id === bookId);
    document.getElementById('reservedBook').value = book.bookTitle;
    document.getElementById('id').value = book.id;
    on();
}

//Pass data to back end
document.getElementById('reservationForm').addEventListener('submit', function(event) {
    event.preventDefault();

    
    const formData = {
        name: document.getElementById('name').innerHTML,
        bookID: document.getElementById('id').value,
        identity: document.getElementById('identity').innerHTML,
        bookTitle: document.getElementById('reservedBook').value,
        location: document.getElementById('location').value,
        reserveTime: new Date().toISOString()
    };

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
});

function logout() {
    fetch(`${ip}/logout`, {
        method: 'POST',
    }).then(() => {
        window.location.href = "/";
    }).catch(error => console.error('Error during logout:', error));
}