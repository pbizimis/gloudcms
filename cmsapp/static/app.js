const ui = new firebaseui.auth.AuthUI(firebase.auth());

const uiConfig = {
callbacks: {
    signInSuccessWithAuthResult: function(authResult, redirectUrl) {
        //requesthandler is triggered due to the "event"
    return true;
    },
    uiShown: function() {
    // The widget is rendered.
    // Hide the loader.
    //document.getElementById('loader').style.display = 'none';
    }
},
// Will use popup for IDP Providers sign-in flow instead of the default, redirect.
signInFlow: 'redirect',
signInSuccessUrl: 'http://127.0.0.1:8080/dashboard',
signInOptions: [
{
    provider: firebase.auth.GoogleAuthProvider.PROVIDER_ID,
    scopes: ["https://www.googleapis.com/auth/documents"]
    //Need to access this provider for a "private" offline token to access their Docs over the backend
},
{
    provider: firebase.auth.EmailAuthProvider.PROVIDER_ID,
    requireDisplayName: false
}
],
// Terms of service url.
tosUrl: 'http://127.0.0.1:8080/tos',
// Privacy policy url.
privacyPolicyUrl: 'http://127.0.0.1:8080/privacy',
credentialHelper: firebaseui.auth.CredentialHelper.NONE
};

ui.start("#firebaseui-auth-container", uiConfig);