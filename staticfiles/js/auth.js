document.addEventListener("DOMContentLoaded", function () {
    const toggleSignIn = document.getElementById("toggleSignIn");
    const toggleSignUp = document.getElementById("toggleSignUp");
    const signInForm = document.getElementById("signInForm");
    const signUpForm = document.getElementById("signUpForm");

    toggleSignUp.addEventListener("click", function (e) {
        e.preventDefault();
        signInForm.classList.add("hidden");
        signUpForm.classList.remove("hidden");
        toggleSignIn.classList.remove("active");
        toggleSignUp.classList.add("active");
    });

    toggleSignIn.addEventListener("click", function (e) {
        e.preventDefault();
        signUpForm.classList.add("hidden");
        signInForm.classList.remove("hidden");
        toggleSignUp.classList.remove("active");
        toggleSignIn.classList.add("active");
    });

    // Toggle password visibility
    document.getElementById("togglePassword").addEventListener("click", function () {
        let passwordField = document.getElementById("password");
        passwordField.type = passwordField.type === "password" ? "text" : "password";
    });

    document.getElementById("toggleSignUpPassword").addEventListener("click", function () {
        let passwordField = document.getElementById("signUpPassword");
        passwordField.type = passwordField.type === "password" ? "text" : "password";
    });

    document.getElementById("toggleSignUpConfirmPassword").addEventListener("click", function () {
        let passwordField = document.getElementById("confirm_password");
        passwordField.type = passwordField.type === "password" ? "text" : "password";
    });
});
