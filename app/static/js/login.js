/**
 * 
 * @returns - Returns and object with methods and properties to handle login
 */
function login() {
    return {
        formHtml: null, // Login form html

        /**
         * Intializes login object.
         * Fetches login form.
         */
        init() {
            if (!this._initialized) {
                this._initialized = true;
                console.log("Login page initialized...");
                this.fetchForm();
            }
        },
        
        /**
         * Fetches login form.
         * 
         * @async
         * @throws {Error} - Throws an error if network request fails.
         */
        fetchForm() {

            fetch(`/auth/get_login_form`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        this.formHtml = data.html;
                        if (this.formHtml) {
                        }
                    }
                })
                .catch(error => {
                    Alpine.store('notifier').add(error.message || "Network error", "error");
                });
        },

        /**
         * Send user data from login form to backend.
         * 
         * @async
         * @throws {Error} - Throws an error if fails to login user or network request fails.
         */
        logUserIn() {

            // Grab the form element and create a FormData instance
            const formElement = document.querySelector('form');
            const formData = new FormData(formElement);

            fetch("/auth/log_user_in", {
                method: "POST",
                body: formData,
                credentials: "include"
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    Alpine.store('notifier').add(data.message || "You were successfully logged in; redirecting...", "success");

                    // Wait 3 seconds before redirecting
                    setTimeout(() => {
                        window.location.href = data.redirect_url || "/dashboard/dashboard_home";
                    }, 3000); // 3000 milliseconds = 3 seconds
                    
                } else {
                    Alpine.store('notifier').add(data.message || "Login was unsuccessful", "error");
                }
            })
            .catch(error => {
                Alpine.store('notifier').add(error.message || "Network error", "error");
            });
        },
    }
}
