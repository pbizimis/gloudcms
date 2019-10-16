firebase.auth().onAuthStateChanged(function(user) {
  if (user) {
    // User is signed in.
    debugUI(user);
    //auth token will be send with an async request to the backend
    firebase.auth().currentUser.getIdToken(/* forceRefresh */ true).then(function(idToken) {
      $(function() {
        $.ajax({ 
          type: "POST",
          contentType: 'application/json',
          url: "/login",
          dataType: 'json',
          data: JSON.stringify(idToken)
        }).done(function(data) { 
          console.log(data);
        });
      });
    }).catch(function(error) {
      console.log(error);
    });

  } else {
    // User is signed out. Is trigger when you run firebase.auth().signout()
  }
  
}, function(error) {
  console.log(error);
});