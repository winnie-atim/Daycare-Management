function showNotification(message, type) {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.style.backgroundColor = type === 'success' ? '#4CAF50' : '#f44336';
    notification.classList.add('show');
    
    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');

    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();

        // if (!validate()) {
        //     console.log("Validation failed.");
        //     return; 
        // }

        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value.trim();

        // // Validate inputs here if needed
        // function validate() {
        //     let isValid = true;
    
        //     const fields = [

        //         { id: 'email', errorMessage: "Email is required", extraCheck: (value) => !value.includes('@'), extraMessage: "Please enter a valid email" },
        //         { id: 'password', errorMessage: "Password is required", extraCheck: (value) => value.length < 8, extraMessage: "Password must be at least 8 characters" }
        //     ];
    
        //     fields.forEach(field => {
        //         const input = document.getElementById(field.id);
        //         const value = input.value.trim();
        //         if (value === "") {
        //             setError(input, field.errorMessage);
        //             isValid = false;
        //         } else if (field.extraCheck && field.extraCheck(value)) {
        //             setError(input, field.extraMessage);
        //             isValid = false;
        //         } else {
        //             setSuccess(input);
        //         }
        //     });
    
        //     return isValid;
        // }

        fetch('http://127.0.0.1:8014/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email: email, password: password })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            if (data.message === "Admin logged in successfully") {
                showNotification("Login successful", 'success');
                window.location.href = '../../views/html/admindashboard.html'; 
            } else {
                showNotification("Failed to login ", 'error');
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            showNotification("Failed to login: ", 'error');
        });
    });
});
