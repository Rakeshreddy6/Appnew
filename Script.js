const seatDisplay = document.getElementById('seat-display');
const numSeatsInput = document.getElementById('num-seats');
const bookSeatsButton = document.getElementById('book-seats');
const exitButton = document.getElementById('exit');
const messageDisplay = document.getElementById('message');

let seats = [];

fetch('/seats')
    .then(response => response.json())
    .then(data => {
        seats = data;
        displaySeats();
    })
    .catch(error => console.error('Error:', error));

function displaySeats() {
    seatDisplay.innerHTML = '';
    for (let i = 0; i < seats.length; i++) {
        const rowDiv = document.createElement('div');
        rowDiv.className = 'row';
        for (let j = 0; j < seats[i].length; j++) {
            const seatDiv = document.createElement('div');
            seatDiv.className = 'seat ' + (seats[i][j] === 0 ? 'available' : 'booked');
            seatDiv.textContent = (i * 7) + j + 1; // Seat numbers are 1-indexed
            rowDiv.appendChild(seatDiv);
        }
        seatDisplay.appendChild(rowDiv);
    }
}

bookSeatsButton.addEventListener('click', () => {
    const numSeats = parseInt(numSeatsInput.value);
    if (numSeats < 1 || numSeats > 7) {
        messageDisplay.textContent = "You can only book between 1 and 7 seats.";
        return;
    }

    fetch('/book', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ num_seats: numSeats })
    })
        .then(response => response.json())
        .then(data => {
            messageDisplay.textContent = data.message;
            if (data.success) {
                fetch('/seats')
                    .then(response => response.json())
                    .then(data => {
                        seats = data;
                        displaySeats();
                    })
                    .catch(error => console.error('Error:', error));
            }
        })
        .catch(error => console.error('Error:', error));
});
