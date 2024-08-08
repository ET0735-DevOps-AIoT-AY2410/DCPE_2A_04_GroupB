const overdue = [];

let info = '';
let state = {};

window.onload = function () {
    var url = document.location.href
    params = url.split('?')[1]
    
    if (params == "borrowed"){
        document.getElementsByClassName('tablinks')[1].click();
    } else {
        document.getElementsByClassName('tablinks')[0].click();
    }
}

document.addEventListener('DOMContentLoaded', () => {    
    fetch(`${ip}/info`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'fromSite': true,
            'info': 'fine'
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data[0][info]){
            document.getElementById('fine').innerHTML = parseFloat(data[0][info]).toFixed(2)
        } else {
            document.getElementById('fine').innerHTML = 0
        }
        
        for (let i = 0; i < data[1].length; i++){
            if (data[1][i][2] == info) {
                overdue.push(data[1][i][0])
            }
        }
        
        fetchBooks(info, 0, '#reserved-books-table tbody');
        fetchBooks(info, 1, '#borrowed-books-table tbody');
    })
    .catch(error => console.error('Error fetching session data:', error));

    fetch(`${ip}/info`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'fromSite': true,
            'info': 'book'
        },
    })
    .then(response => response.json())
    .then(data => {
        books = data
    });
});

function preventExtend(reason){
    if (reason == 'extended'){
        alert("This book has been previously extended")
    } else if (reason == 'overdue'){
        alert("This book is already overdue")
    }
}

function fetchBooks(info, selector, tableBodySelector) {
    fetch(`${ip}/reserve`,{
        method: 'GET',        
        headers: {
            'Content-Type': 'application/json',
            'fromSite': true
        },
    })
    .then(response => response.json())
    .then(data => {
        const tableBody = document.querySelector(tableBodySelector);
        tableBody.innerHTML = '';

        if (selector == 0){
            if (data[0][info] && data[0][info].length > 0) {
                const list = data[0][info];
                for (let i = 0; i < list.length; i++) {
                    const row = document.createElement('tr');
                    const book = books[parseInt(list[i][0]) - 1];
                    const reservationTime = new Date(list[i][2].slice(0, 19));
                    reservationTime.setMinutes(reservationTime.getMinutes() + 5);

                    row.innerHTML = `
                        <td>
                        ${book.bookTitle}<br>
                        <div class="cancel">
                        <button onclick="cancelReservation(${list[i][0]})">Cancel reservation</button>
                        <div>
                        </td>
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
                    const reservationTime = new Date(list[i][1].slice(0, 19));

                    
                    reservationTime.setMinutes(reservationTime.getMinutes() + 18);
                    if (overdue.includes(list[i][0].toString())){       
                        row.style.backgroundColor = '#fc6565';                    
                        row.innerHTML = `
                            <td>${book.bookTitle}</td>
                            <td><img src="${book.image}" width="100"></td>
                            <td>${reservationTime.toLocaleString()}<br>
                            <div class="extended">
                            <button onclick="preventExtend('overdue')">Extend loan</button>
                            <div>
                            </td>                            
                        `;
                    } else if (list[i][1].slice(-1) == 'E'){
                        row.innerHTML = `
                            <td>${book.bookTitle}</td>
                            <td><img src="${book.image}" width="100"></td>
                            <td>${reservationTime.toLocaleString()}<br>
                            <div class="extended">
                            <button onclick="preventExtend('extended')">Extend loan</button>
                            <div>
                            </td>                            
                        `;
                    } else {
                        row.innerHTML = `
                            <td>${book.bookTitle}</td>
                            <td><img src="${book.image}" width="100"></td>
                            <td>${reservationTime.toLocaleString()}<br>
                            <div class="extend">
                            <button onclick="extendBorrow(${list[i][0]}, '${list[i][1]}')">Extend loan</button>
                            <div>
                            </td>                            
                        `;
                    }

                    tableBody.appendChild(row);
                }
            } else {
                const row = document.createElement('tr');
                row.innerHTML = '<td colspan="3">No books currently reserved.</td>';
                tableBody.appendChild(row);
            }
        }
    })
    .catch(error => console.error(`Error fetching ${selector} books:`, error));
}

function cancelReservation(bookId) {
    fetch(`${ip}/reserve`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'fromSite': true
        },
        body: JSON.stringify({ info: info, bookId: bookId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Reservation cancelled successfully');
            location.reload();
        } else {
            alert('Failed to cancel reservation');
        }
    })
    .catch(error => console.error('Error cancelling reservation:', error));
}

function extendBorrow(bookId, borrowDate) {
    fetch(`${ip}/extendLoan`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'fromSite': true,
        },
        body: JSON.stringify({ info: info, bookId: bookId, borrowDate: borrowDate})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Loan extended successfully');
            window.location.href = `/reserved?borrowed`;
        } else {
            alert('Failed to extend loan');
        }
    })
    .catch(error => console.error('Error cancelling reservation:', error));
}

function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    var url;

    if (tabName == 'Borrowed'){
        url = '/reserved?borrowed';
    } else if (tabName == 'Reserved') {
        url = '/reserved';
    }
    history.pushState(state, "", url);

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