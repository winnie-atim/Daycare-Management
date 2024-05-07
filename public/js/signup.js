const form = document.getElementById("form");
const username = document.getElementById("username");
const password = document.getElementById("password");

// Function to handle form validation
const validate = () => {
    const nameValue = username.value.trim();
    const passwordValue = password.value.trim();

    // Validate username
    if (nameValue === "") {
        setError(username, "Username is required");
    } else {
        setSuccess(username);
    }

    // Validate password
    if (passwordValue === "") {
        setError(password, "Password is required");
    } else if (passwordValue.length < 8) {
        setError(password, "Password must be at least 8 characters");
    } else {
        setSuccess(password);
    }
};

// Function to handle form submission
form.addEventListener("submit", event => {
    event.preventDefault(); 
    validate(); 
});

// Function to set error state for input element
const setError = (element, message) => {
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector(".error");

    errorDisplay.innerText = message;
    inputControl.classList.add("error");
    inputControl.classList.remove("success");
};

// Function to set success state for input element
const setSuccess = (element) => {
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector(".error");

    errorDisplay.innerText = "";
    inputControl.classList.add("success");
    inputControl.classList.remove("error");
};
