firebase.auth().onAuthStateChanged(function(user) {
  if (user) {
    document.getElementById("dashboard-account-name").textContent = user.displayName;
    document.getElementById("dashboard-account-image").src = user.photoURL;
  } else {
    // User is signed out. Is trigger when you run firebase.auth().signout()
  }
  
}, function(error) {
  console.log(error);
});