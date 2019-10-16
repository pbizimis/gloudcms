window.onload = function() {
  document.getElementById('sign-out').addEventListener('click', function() {
    firebase.auth().signOut();
    document.getElementById('user-name').style.display = 'none';
    document.getElementById('user-email').style.display = 'none';
    document.getElementById('sign-out').style.display = "none";
    ui.start("#firebaseui-auth-container", uiConfig);
  });
}
