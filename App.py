from flask import Flask, jsonify, request

app = Flask(__name__)

class TrainCoach:
    def __init__(self):
        self.rows = []
        self.total_seats = 80
        self.available_seats = 80
        self.initialize_seats()

    def initialize_seats(self):
        for i in range(11):
            self.rows.append([0] * 7)  # 7 seats in each of the first 11 rows
        self.rows.append([0] * 3)  # Last row with 3 seats

    def display_seats(self):
        return self.rows

    def book_seats(self, num_seats):
        if num_seats < 1 or num_seats > 7:
            return "You can only book between 1 and 7 seats.", False

        if self.available_seats < num_seats:
            return "Not enough seats available.", False

        # Try to book seats in one row first
        for row_index in range(len(self.rows)):
            row = self.rows[row_index]
            available_count = row.count(0)

            if available_count >= num_seats:
                booked_seats = []
                for seat_index in range(len(row)):
                    if row[seat_index] == 0:  # Seat is available
                        row[seat_index] = 1  # Mark seat as booked
                        booked_seats.append(seat_index + 1)  # Seat numbers are 1-indexed
                        if len(booked_seats) == num_seats:
                            break
                
                self.available_seats -= num_seats
                return f"Successfully booked seats: {booked_seats} in Row {row_index + 1}", True

        # If not enough seats in one row, try to book nearby seats
        booked_seats = []
        for row_index in range(len(self.rows)):
            row = self.rows[row_index]
            for seat_index in range(len(row)):
                if row[seat_index] == 0:  # Seat is available
                    row[seat_index] = 1  # Mark seat as booked
                    booked_seats.append(seat_index + 1)  # Seat numbers are 1-indexed
                    if len(booked_seats) == num_seats:
                        break
            if len(booked_seats) == num_seats:
                break

        if len(booked_seats) == num_seats:
            self.available_seats -= num_seats
            return f"Successfully booked nearby seats: {booked_seats}", True
        else:
            return "Could not find enough nearby seats.", False

coach = TrainCoach()

@app.route('/seats', methods=['GET'])
def get_seats():
    return jsonify(coach.display_seats())

@app.route('/book', methods=['POST'])
def book():
    data = request.get_json()
    num_seats = data.get('num_seats')
    message, success = coach.book_seats(num_seats)
    return jsonify({'message': message, 'success': success})

if __name__ == '__main__':
    app.run(debug=True)
