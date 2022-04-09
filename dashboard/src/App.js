import React from 'react';
import './App.css';

import {useAuthState} from 'react-firebase-hooks/auth';
import {useCollection} from 'react-firebase-hooks/firestore';

import { initializeApp } from "firebase/app";
//import { getAnalytics } from "firebase/analytics";
import { getAuth, signInWithRedirect, GoogleAuthProvider } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDVPUFdjO45718scYBvN23CEWNhtcimydY",
  authDomain: "pb-analytics-616.firebaseapp.com",
  projectId: "pb-analytics-616",
  storageBucket: "pb-analytics-616.appspot.com",
  messagingSenderId: "854937262435",
  appId: "1:854937262435:web:f743e807b5929294c95b56",
  measurementId: "G-6CP9FJWT2L"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
//const analytics = getAnalytics(app);
const auth = getAuth(app);
const db = getFirestore(app);
const provider = new GoogleAuthProvider();

function App() {

  const [user] = useAuthState(auth);

  return (
    <div className="App">
      <header>
        <h1>🚲 PB-Analytics 🚲</h1>
        <SignOut />
      </header>

      <section>
        {user ? <DisplayBikes /> : <SignIn />}
      </section>
    </div>
  );
}

function SignIn() {

  const signInWithGoogle = () => {
    signInWithRedirect(auth, provider);
  }

  return (
    <>
      <button className="sign-in" onClick={signInWithGoogle}>Sign in with Google</button>
    </>
  )

}

function SignOut() {
  return auth.currentUser && (
    <button className="sign-out" onClick={() => auth.signOut()}>Sign Out</button>
  )
}

// function DisplayBikes() {
//   const [snapshot] = useCollection(db.collection('trailEnduro'));
//   if (!snapshot) return null;
//   return snapshot.docs.map(doc => (
//     <div key={doc.id}>
//       <h2>{doc.data().name}</h2>
//       <p>{doc.data().description}</p>
//     </div>
//   ))
// }

function DisplayBikes() {
  return (
    <>
      <h2>Bikes</h2>
    </>
  )
}

export default App;
