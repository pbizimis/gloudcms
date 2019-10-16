function debugUI(user) {
    let displayName = user.displayName;
    let email = user.email;
    document.getElementById('user-name').textContent = displayName;
    document.getElementById('user-email').textContent = email;
    document.getElementById('sign-out').style.display = "block";
    document.getElementById('user-name').style.display = "block";
    document.getElementById('user-email').style.display = "block";
}