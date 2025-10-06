// Firebase initialization
const firebaseConfig = {
    apiKey: "AIzaSyDusm8ZxlvF3y2iopCuRJWsg9ePnQd-wco",
    authDomain: "food-transparency.firebaseapp.com",
    projectId: "food-transparency",
    storageBucket: "food-transparency.appspot.com",
    messagingSenderId: "728004942610",
    appId: "1:728004942610:web:a2cbb9144f7ad186de31cb",
};

firebase.initializeApp(firebaseConfig);

const auth = firebase.auth();
const db = firebase.firestore();

// DOM elements
const productForm = document.getElementById('product-form');
const logoutButton = document.getElementById('logout-button');

// Listen for the authentication state
auth.onAuthStateChanged(user => {
    if (!user) {
        // If no user is logged in, redirect to the login page
        window.location.href = 'index.html';
    }
});

// Handle product submission
productForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const productName = document.getElementById('product-name').value;
    const productDescription = document.getElementById('product-description').value;
    const userId = auth.currentUser.uid;

    db.collection('Products').add({
        name: productName,
        description: productDescription,
        producerId: userId
    })
    .then(() => {
        alert('Product added successfully!');
        productForm.reset();
    })
    .catch(error => {
        console.error('Error adding product:', error);
        alert('Error adding product. Please try again.');
    });
});

// Logout functionality
logoutButton.addEventListener('click', () => {
    auth.signOut().then(() => {
        window.location.href = 'index.html';
    });
});

