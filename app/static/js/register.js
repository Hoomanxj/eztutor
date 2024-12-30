/**
 * 
 * @returns - Returns and object with methods and properties to handle registeration
 */
function register() {
    return {

        formHtml: null, // Register form Html
        userType: null, // Current user
        teacherForm: false, // Teacher form toggle
        studentForm: false, // Student form toggle
        formElement: null, // Form element in html

        /**
         * Intializes register object.
         * Fetches registeration form - Defualts teacher form.
         */
        init() {
            if(!this._initialized) {
                this._initialized = true;
                this.fetchForm("teacher");
            }
        },
        
        /**
         * Fetches registration form.
         * 
         * @async
         * @throws {Error} - Throws an error if fails to fetch or network request fails.
         */
        fetchForm(userType) {
            if (this.userType !== userType) {

                this.userType = userType;

                // Show form based on user type
                this.showForm(this.userType);

                fetch(`/auth/get_register_form?user_type=${this.userType}`)
                .then((response) => response.json())
                .then((data) => {
                    if (data.success) {
                        this.formHtml = data.html;
                        if(this.formHtml) {
                        }
                    } else {
                        Alpine.store('notifier').add(data.message || "User type could not be determined", "error");
                    }
                })
                .catch((error) => {
                    Alpine.store('notifier').add(error.message || "Network error", "error");
                });
            }
        },

        /**
         * Send user registration data to backend.
         * 
         * @async
         * @throws {Error} - Throws an error if user data does no validate or network request fails.
         */
        registerUser(userType) {
            
            // Choose the correct form based on user type
            if (userType === "teacher") {
                this.formElement = document.querySelector('#teacher-form')
            } else if (userType === "student") {
                this.formElement = document.querySelector('#student-form')
            }

            // Create a new FormData instance
            const formData = new FormData(this.formElement)

            fetch(`/auth/register_user?user_type=${userType}`, {
                method: "POST",
                body: formData,
                credentials: "include"
            })
            .then((response) => response.json())
            .then((data) => {
                if(data.success) {
                    Alpine.store('notifier').add(data.message || "Successfully registered", "success");

                    // Wait 3 seconds before redirecting
                    setTimeout(() => {
                        window.location.href = data.redirect_url || "/dashboard.dashboard_home"; // Redirect after successful login
                    }, 3000); // 3000 milliseconds = 3 seconds

                } else {
                    Alpine.store('notifier').add(data.message || "Error in registration", "error");
                }
            })
            .catch((error) => {
                Alpine.store('notifier').add(error.message || "Network error", "error");
            });
        },

        // Show the correct form based on user type
        showForm(userType) {
            if (userType === "teacher") {
                this.studentForm = false;
                this.teacherForm = true;

            } else if (userType === "student") {
                this.teacherForm = false;
                this.studentForm = true;
            }
        },
    }
}