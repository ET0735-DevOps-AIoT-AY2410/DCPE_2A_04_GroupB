const ip = 'http://127.0.0.1:5000';

// Books list
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

let info = '';

document.addEventListener('DOMContentLoaded', () => {
    fetch(`${ip}/session`, {
        method: 'GET',
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        console.log('Session data:', data);
        if (!data.loggedIn) {
            window.location.href = '/';
        } else {
            document.getElementById('name').innerHTML = data.name;
            document.getElementById('identity').innerHTML = data.identity;
            info = data.name + "&" + data.identity;

            fetchBooks(info, 0, '#reserved-books-table tbody');
            fetchBooks(info, 1, '#borrowed-books-table tbody');
        }
    })
    .catch(error => console.error('Error fetching session data:', error));

    
    fetch(`${ip}/fines`, {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('fine').innerHTML = Math.round(data[0][info] * 100) / 100
    })
    .catch(error => console.error('Error fetching session data:', error));
});

function fetchBooks(info, selector, tableBodySelector) {
    fetch(`${ip}/reservations`)
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector(tableBodySelector);
            tableBody.innerHTML = ''; // Clear any existing rows

            if (selector == 0){
                if (data[0][info] && data[0][info].length > 0) {
                    const list = data[0][info];
                    for (let i = 0; i < list.length; i++) {
                        const book = books[parseInt(list[i][0]) - 1];
                        const row = document.createElement('tr');
                        const reservationTime = new Date(list[i][2]);
                        reservationTime.setMinutes(reservationTime.getMinutes() + 5);

                        row.innerHTML = `
                            <td>${book.bookTitle}</td>
                            <td><img src="${book.image}" width="100"></td>
                            <td>${list[i][1]}</td>
                            <td>${reservationTime.toLocaleString()}</td>
                        `;
                        tableBody.appendChild(row);
                    }
                } else {
                    const row = document.createElement('tr');
                    row.innerHTML = '<td colspan="4">No books currently reserved.</td>';
                    tableBody.appendChild(row);
                }
            } else if (selector == 1){
                if (data[1][info] && data[1][info].length > 0) {
                    const list = data[1][info];
                    for (let i = 0; i < list.length; i++) {
                        const book = books[parseInt(list[i][0]) - 1];
                        const row = document.createElement('tr');
                        const reservationTime = new Date(list[i][1]);
                        reservationTime.setMinutes(reservationTime.getMinutes() + 18);
                        row.innerHTML = `
                            <td>${book.bookTitle}</td>
                            <td><img src="${book.image}" width="100"></td>
                            <td>${reservationTime.toLocaleString()}</td>
                        `;
                        tableBody.appendChild(row);
                    }
                } else {
                    const row = document.createElement('tr');
                    row.innerHTML = '<td colspan="4">No books currently reserved.</td>';
                    tableBody.appendChild(row);
                }
            }
        })
        .catch(error => console.error(`Error fetching ${endpoint} books:`, error));
}

function openTab(evt, tabName) {
    // Declare all variables
    var i, tabcontent, tablinks;

    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementsByClassName('tablinks')[0].click();
});
