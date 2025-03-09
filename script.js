document.addEventListener("DOMContentLoaded", function () {

    // Register User
    const registerForm = document.getElementById("registerForm");
    if (registerForm) {
        registerForm.addEventListener("submit", async function (event) {
            event.preventDefault();
            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;
            const fullname = document.getElementById("fullname").value;
            const city = document.getElementById("city").value;
            const email = document.getElementById("email").value;
            const phone = document.getElementById("phone").value;

            console.log(username)
            console.log(password)
            console.log(fullname)
            console.log(city)
            console.log(email)
            console.log(phone)

            const response = await fetch("http://127.0.0.1:8000/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password, fullname, city, email, phone })
            });

            const result = await response.json();
            alert(result.message);
            if (response.ok) window.location.href = "login.html";
        });
    }

    // Login User
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", async function (event) {
            event.preventDefault();
            const username = document.getElementById("loginUsername").value;
            const password = document.getElementById("loginPassword").value;

            console.log(username)
            console.log(password)

            const response = await fetch("http://127.0.0.1:8000/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password })
            });

            const result = await response.json();
            if (response.ok) {
                alert(result.message);
                localStorage.setItem("loggedIn", "true");
                window.location.href = "dashboard.html";
            }
            else
            {
                alert("Failed")
            }
        });
    }

    // Logout
    const logoutBtn = document.getElementById("logoutBtn");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", function () {
            localStorage.removeItem("loggedIn");
            window.location.href = "login.html";
        });

        // Prevent access to dashboard if not logged in
        if (!localStorage.getItem("loggedIn")) {
            alert("You must log in first!");
            window.location.href = "login.html";
        }
    }
});
