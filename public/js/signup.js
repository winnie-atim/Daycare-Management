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
    const form = document.getElementById("form");

    form.addEventListener("submit", function(event) {
        event.preventDefault(); 

        if (!validate()) {
            console.log("Validation failed.");
            return; 
        }

        const formData = {
            token: document.getElementById("token").value.trim(),
            firstname: document.getElementById("firstname").value.trim(),
            lastname: document.getElementById("lastname").value.trim(),
            email: document.getElementById("email").value.trim(),
            contact: document.getElementById("contact").value.trim(),
            password: document.getElementById("password").value.trim()
        };

        fetch(form.action, {
            method: form.method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Server responded with a non-200 status: ' + response.status);
            }
            return response.json();
        })
        .then(data => {
            console.log("Success:", data);
            // alert ("Account created successfully.");
            showNotification("Account created successfully.", 'success');
            window.location.href = '../../views/html/admindashboard.html';
            // Handling success here (e.g., displaying a success message, redirecting, etc.)
        })
        .catch((error) => {
            console.error('Error:', error);
            // Handling errors here (e.g., displaying error messages)
            showNotification("Failed to login: " + (data.detail || "Unknown error"), 'error');
        });
    });

    function validate() {
        let isValid = true;

        const fields = [
            { id: 'token', errorMessage: "Token is required" },
            { id: 'firstname', errorMessage: "First name is required" },
            { id: 'lastname', errorMessage: "Last name is required" },
            { id: 'email', errorMessage: "Email is required", extraCheck: (value) => !value.includes('@'), extraMessage: "Please enter a valid email" },
            { id: 'contact', errorMessage: "Contact number is required" },
            { id: 'password', errorMessage: "Password is required", extraCheck: (value) => value.length < 8, extraMessage: "Password must be at least 8 characters" }
        ];

        fields.forEach(field => {
            const input = document.getElementById(field.id);
            const value = input.value.trim();
            if (value === "") {
                setError(input, field.errorMessage);
                isValid = false;
            } else if (field.extraCheck && field.extraCheck(value)) {
                setError(input, field.extraMessage);
                isValid = false;
            } else {
                setSuccess(input);
            }
        });

        return isValid;
    }

    function setError(element, message) {
        const inputControl = element.parentElement;
        const errorDisplay = inputControl.querySelector(".error");

        if (errorDisplay) {
            errorDisplay.innerText = message;
            inputControl.classList.add("error");
            inputControl.classList.remove("success");
        }
    }

    function setSuccess(element) {
        const inputControl = element.parentElement;
        const errorDisplay = inputControl.querySelector(".error");

        if (errorDisplay) {
            errorDisplay.innerText = "";
            inputControl.classList.add("success");
            inputControl.classList.remove("error");
        }
    }
});
