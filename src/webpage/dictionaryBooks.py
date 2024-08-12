dictionary = [
    { 'id': 1, 'bookTitle': 'Book 1', 'image': 'https://m.media-amazon.com/images/I/81DFDGzHZqL._AC_UF1000,1000_QL80_.jpg' },
    { 'id': 2, 'bookTitle': 'Book 2', 'image': 'https://m.media-amazon.com/images/I/51gLEj8UHzL._AC_UF1000,1000_QL80_.jpg' },
    { 'id': 3, 'bookTitle': 'Book 3', 'image': 'https://m.media-amazon.com/images/I/91Yob+SFXdL._AC_UF1000,1000_QL80_.jpg' },
    { 'id': 4, 'bookTitle': 'Book 4', 'image': 'https://m.media-amazon.com/images/I/61lBRY5h+NL._AC_UF1000,1000_QL80_.jpg' },
    { 'id': 5, 'bookTitle': 'Book 5', 'image': 'https://m.media-amazon.com/images/I/915SPe6hrfL._SY342_.jpg' },
    { 'id': 6, 'bookTitle': 'Book 6', 'image': 'https://m.media-amazon.com/images/I/91NPng6lBsL._AC_UF1000,1000_QL80_.jpg' },
    { 'id': 7, 'bookTitle': 'Book 7', 'image': 'https://www.hoddereducation.sg/productCovers/9789810631307.jpg' },
    { 'id': 8, 'bookTitle': 'Book 8', 'image': 'https://www.hoddereducation.sg/productCovers/9789810631154.jpg' },
    { 'id': 9, 'bookTitle': 'Book 9', 'image': 'https://m.media-amazon.com/images/I/612ADI+BVlL._AC_UF1000,1000_QL80_.jpg' },
    { 'id': 10, 'bookTitle': 'Book 10', 'image': 'https://m.media-amazon.com/images/I/61KPPB-34FL._AC_UF1000,1000_QL80_.jpg' },
    { 'id': 11, 'bookTitle': 'Book 11', 'image': 'https://www.sp.edu.sg/images/default-source/sp70-content/sp70-forallages-book-cover.jpg?sfvrsn=1c3ec396_0' },
    { 'id': 12, 'bookTitle': 'Book 12', 'image': 'https://m.media-amazon.com/images/I/617dLkzb9-L._SY342_.jpg' },
    { 'id': 13, 'bookTitle': 'Book 13', 'image': 'https://m.media-amazon.com/images/I/71ahxYPi8KL._SY342_.jpg' },
    { 'id': 14, 'bookTitle': 'Book 14', 'image': 'https://m.media-amazon.com/images/I/612HfenZf0L._SY342_.jpg' },
    { 'id': 15, 'bookTitle': 'Book 15', 'image': 'https://m.media-amazon.com/images/I/61qSsRBSo6L._SY342_.jpg' },
];

libDict = {}
for book in dictionary:
    libDict[book['id']] = book['bookTitle']
