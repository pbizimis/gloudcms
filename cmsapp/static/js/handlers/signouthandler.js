window.onload = function() {
  document.getElementById('sign-out').addEventListener('click', function() {
    firebase.auth().signOut();
    ui.start("#firebaseui-auth-container", uiConfig);
  });
}

