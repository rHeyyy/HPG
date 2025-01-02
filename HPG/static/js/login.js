document.addEventListener('DOMContentLoaded', function () {
    const loginModal = document.getElementById("loginModal");
    const loginBtn = document.getElementById("login-btn");
    const loginClose = document.getElementById("loginClose");
    const leftSectionTitle = document.getElementById("leftSectionTitle");
    const leftSectionText = document.getElementById("leftSectionText");
    const leftSectionButton = document.getElementById("leftSectionButton");
    const loginForm = document.getElementById("loginForm");
    const registerForm = document.getElementById("registerForm");

    // Button inside the left section (Toggle between forms)
    leftSectionButton.addEventListener("click", function () {
        // Check which form is currently visible and toggle
        if (loginForm.style.display === "block") {
            // Switch to Register
            loginForm.style.display = "none";
            registerForm.style.display = "block";

            // Update left section
            leftSectionTitle.textContent = "New Here?";
            leftSectionText.textContent = "Join us for the best pet grooming experience.";
            leftSectionButton.textContent = "Login Now";
        } else {
            // Switch to Login
            registerForm.style.display = "none";
            loginForm.style.display = "block";

            // Update left section
            leftSectionTitle.textContent = "Welcome Back!";
            leftSectionText.textContent = "Happy Paw's Grooming brings the best care for your furry friends.";
            leftSectionButton.textContent = "Register Now";
        }
    });

    // Show login modal when login button is clicked
    loginBtn.onclick = function () {
        loginModal.style.display = "flex"; // Flex to center the modal
        loginForm.style.display = "block";
        registerForm.style.display = "none";
    };

    // Close modal only when close button is clicked
    loginClose.onclick = function () {
        loginModal.style.display = "none";
    };

    // Validate register form and display error inside modal
    const registerFormElement = registerForm.querySelector("form");
    if (registerFormElement) {
        registerFormElement.addEventListener("submit", function (event) {
            const password = registerFormElement.querySelector('input[name="password1"]');
            const confirmPassword = registerFormElement.querySelector('input[name="password2"]');
            const errorContainer = document.getElementById("registerError");

            // Clear previous errors
            if (errorContainer) {
                errorContainer.textContent = "";
            }

            if (password.value !== confirmPassword.value) {
                event.preventDefault(); // Prevent form submission
                if (errorContainer) {
                    errorContainer.textContent = "Passwords do not match!";
                    errorContainer.style.color = "red"; // Optional: Style the error message
                }
                loginModal.style.display = "flex"; // Keep modal open
                loginForm.style.display = "none";
                registerForm.style.display = "block";
            }
        });
    }

    // Keep modal open on page load if errors are passed from the server
    if (loginModal.style.display === "flex") {
        if (loginForm.style.display === "block") {
            loginForm.style.display = "block";
            registerForm.style.display = "none";
        } else {
            registerForm.style.display = "block";
            loginForm.style.display = "none";
        }
    }
});
