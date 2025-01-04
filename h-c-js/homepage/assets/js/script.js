const nameCheck = document.getElementById("fullName");
const emailCheck = document.getElementById("email");
const submitButton = document.getElementById("submit-button");
const successMessage = document.getElementById("success-message")

nameCheck.addEventListener("input", checkForm);
emailCheck.addEventListener("input", checkForm);
submitButton.addEventListener("click", pageReset);



function checkForm() {
    if (nameCheck.value !== "" && emailCheck.value !== "") {
        submitButton.disabled = false; // Enable the button
    } else {
        submitButton.disabled = true; // Keep the button disabled
    }
}

function pageReset() {
    nameCheck.value = "";
    emailCheck.value = "";
    window.scroll(0,0);
    successMessage.classList.remove("d-none");
    successMessage.textContent = "Your submition was successful. We will inform you if you are chosen."
}
