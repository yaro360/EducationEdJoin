// Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDusm8ZxlvF3y2iopCuRJWsg9ePnQd-wco",
  authDomain: "food-transparency.firebaseapp.com",
  projectId: "food-transparency",
  storageBucket: "food-transparency.firebasestorage.app",
  messagingSenderId: "728004942610",
  appId: "1:728004942610:web:a2cbb9144f7ad186de31cb",
  measurementId: "G-ME6L9YP6FF"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();
const db = firebase.firestore();
const storage = firebase.storage();

// Registration: Redirect to Company Information page after registration
document.getElementById('register-form')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const firstName = document.getElementById('register-first-name').value;
  const lastName = document.getElementById('register-last-name').value;
  const email = document.getElementById('register-email').value;
  const password = document.getElementById('register-password').value;

  try {
    const userCredential = await auth.createUserWithEmailAndPassword(email, password);
    const user = userCredential.user;

    // Store additional user info in Firestore
    await db.collection('users').doc(user.uid).set({
      firstName,
      lastName,
      email,
      createdAt: firebase.firestore.FieldValue.serverTimestamp()
    });

    // Redirect to Company Information page
    window.location.href = 'company-info.html';
  } catch (error) {
    console.error("Error registering:", error);
    alert("Error registering. Please try again.");
  }
});

// Login: Redirect based on company info status
document.getElementById('login-form')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const email = document.getElementById('login-email').value;
  const password = document.getElementById('login-password').value;

  try {
    const userCredential = await auth.signInWithEmailAndPassword(email, password);
    const user = userCredential.user;

    // Check if company info exists
    const companyDoc = await db.collection('companies').doc(user.uid).get();
    if (companyDoc.exists) {
      // Redirect to add-product.html if company data exists
      window.location.href = 'add-product.html';
    } else {
      // Redirect to company-info.html if no company data
      window.location.href = 'company-info.html';
    }
  } catch (error) {
    console.error("Error logging in:", error);
    alert("Error logging in. Please check your credentials and try again.");
  }
});

// Auth Check: Redirect based on presence of company info
auth.onAuthStateChanged(async (user) => {
  if (user) {
    const companyDoc = await db.collection('companies').doc(user.uid).get();

    if (!companyDoc.exists && window.location.pathname !== '/company-info.html') {
      // Redirect to company-info.html if no company data exists
      window.location.href = 'company-info.html';
    } else if (companyDoc.exists && window.location.pathname === '/company-info.html') {
      // Redirect to add-product.html if company info exists and user is on company-info.html
      window.location.href = 'add-product.html';
    }
  } else if (window.location.pathname !== '/index.html') {
    // Redirect to login page if not authenticated
    window.location.href = 'index.html';
  }
});

// Save Company Information after submission
document.getElementById('company-form')?.addEventListener('submit', async (e) => {
  e.preventDefault();

  const userId = auth.currentUser.uid;
  const companyData = {
    companyName: document.getElementById("company-name").value,
    repFirstName: document.getElementById("rep-first-name").value,
    repLastName: document.getElementById("rep-last-name").value,
    address: document.getElementById("address").value,
    website: document.getElementById("website").value,
    products: document.getElementById("products").value.split(","),
  };

  // Handle logo upload
  const logoFile = document.getElementById("logo").files[0];
  if (logoFile) {
    const storageRef = storage.ref(`logos/${userId}/${logoFile.name}`);
    const snapshot = await storageRef.put(logoFile);
    companyData.logoUrl = await snapshot.ref.getDownloadURL();
  }

  // Save company data to Firestore
  await db.collection('companies').doc(userId).set(companyData);

  alert("Company information saved successfully!");
  // Redirect to add-product.html after saving company data
  window.location.href = 'add-product.html';
});

// Add Product Form Submission
document.getElementById('product-form')?.addEventListener('submit', async (e) => {
  e.preventDefault();

  const userId = auth.currentUser.uid;
  const productData = {
    productName: document.getElementById("product-name").value,
    type: document.getElementById("type").value,
    shelfLife: document.getElementById("shelf-life").value,
    origin: document.getElementById("origin").value,
    transportationMethod: document.getElementById("transportation-method").value,
    companyId: userId, // Link product to the user's company
  };

  // Handle product image upload
  const productImageFile = document.getElementById("product-image").files[0];
  if (productImageFile) {
    const storageRef = storage.ref(`products/${userId}/${productImageFile.name}`);
    const snapshot = await storageRef.put(productImageFile);
    productData.imageUrl = await snapshot.ref.getDownloadURL();
  }

  // Save product data to Firestore
  await db.collection('products').add(productData);

  alert("Product information saved successfully!");
  // Redirect to home or another page as desired
  window.location.href = 'index.html';
});

// Log Out Functionality
document.getElementById('logout-button')?.addEventListener('click', async () => {
  await auth.signOut();
  window.location.href = 'index.html'; // Redirect to login page after logout
});

