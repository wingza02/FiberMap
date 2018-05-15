import Firebase from 'firebase'

const firebaseApp = Firebase.initializeApp({
    apiKey: "AIzaSyAU353cikWYydNQtnE3s7XVojlI1XAh9J0",
    authDomain: "senior-proj-1509371082591.firebaseapp.com",
    databaseURL: "https://senior-proj-1509371082591.firebaseio.com",
    projectId: "senior-proj-1509371082591",
    storageBucket: "senior-proj-1509371082591.appspot.com",
    messagingSenderId: "476252433199"
});

// Export the database for components to use.
// If you want to get fancy, use mixins or provide / inject to avoid redundant imports.
export const db = firebaseApp.database();