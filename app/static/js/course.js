/**
 * 
 * @returns - Returns and object with methods and properties to handle courses
 */
function course(role) {
    return {
        allCourses: [], // List of all courses
        role: role, // Current user
        viewOn: false, // Tab view toggle
        courseStatus: "ongoing", // Course statuse; default "ongoing"
        courses: [], // List of courses with a specific status
        formHtml: null, // Form html for creating a course
        invitationModal: false, // Invitation modal toggle
        inviteHtml: null, // form html for inviting a student
        isLoadingCreate: false, // Loading element toggle for create modal
        isLoadinginvite: false, // Loading element toggle for invite modal
        courseId: null, // Selected course ID
        _initialized: false, // Initialize status check

        /**
         * Intializes course object.
         * Fetches all courses.
         */
        init() {
            if (!this._initialized) {
                this._initialized = true;
                console.log("Page initialized for:", this.role);
                this.fetchCourses();
            }
        },

        /**
         * Fetches courses of user.
         * 
         * @async
         * @throws {Error} - Throws an error if fails to fetch or network request fails.
         */
        fetchCourses() {
            console.log("Courses fetch initiated...");
            fetch("/course/get_courses")
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        this.allCourses = data.courses;

                        if (this.allCourses) {
                                this.viewCourses("ongoing")
                        }
                    } else {
                        Alpine.store('notifier').add(data.message || "Something went wrong", "error");
                    }

                })
                .catch(error => {
                    Alpine.store('notifier').add(error.message || "Network error", "error");
                });
        },

        // Show courses based on their status (ongoing / concluded)
        viewCourses(courseStatus) {

            this.formHtml = false;
            this.viewOn = true;
            this.courseStatus = courseStatus;
            this.courses = this.allCourses.filter(course => course.status === this.courseStatus);
        },

        /**
         * Fetches course creation form - Teacher only.
         * 
         * @async
         * @throws {Error} - Throws an error if form fetch or network request fails.
         */
        fetchCourseForm() {
            this.viewOn = false;

            fetch("/course/course_form")
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        this.formHtml = data.html;
                        if (this.formHtml) {
                        }
                    }else {
                        Alpine.store('notifier').add(data.message, "error");
                    }

                })
                .catch(error => {
                    Alpine.store('notifier').add(error.message || "Network error", "error");
                });
        },

        /**
         * Send course submittion data to backend.
         * 
         * @async
         * @throws {Error} - Throws an error if form data validation or network request fails.
         */
        submitForm() {

            this.isLoadingCreate = true;

            // Find the form using 'form' tag
            const formElement = document.querySelector('form');

            // Create a FormData instance
            const formData = new FormData(formElement);
            fetch("/course/submit_form", {
                method: "POST",
                body: formData,
                credentials: "include"
            })
            .then(response => response.json())
            .then(data => {
              if (data.success) {
                Alpine.store('notifier').add(data.message, "success");

                // Reload courses
                this.fetchCourses();
              } else {
                Alpine.store('notifier').add(data.message || "Something went wrong.", "error");
              }
            })
            .catch(error => {
              Alpine.store('notifier').add(error.message || "Network error", "error");
            })
            .finally(() => {
                this.isLoadingCreate = false; // Turn loading off, success or fail
            });
        },

        /**
         * Fetches course invite form - Teacher only.
         * 
         * @async
         * @throws {Error} - Throws an error if form fetch or network request fails.
         */
        inviteForm(courseId) {

            this.courseId = courseId;
            fetch(`/course/get_invite_form?course_id=${courseId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        this.inviteHtml = data.html;
                    }else {
                        Alpine.store('notifier').add(data.message || "Something went wrong", "error");
                    }
                })
                .catch(error => {
                    Alpine.store('notifier').add(error.message || "Network error", "error");
                });
            
            // show invite modal
            this.invitationModal = true;
        },

        /**
         * Send invite information to backend.
         * 
         * @async
         * @throws {Error} - Throws an error if the network request fails.
         */
        sendInvite() {

            // If there is no course ID present for course inviation
            if (!this.courseId) {
                return;
            }

            // Show loading so that user understand the process is happening
            this.isLoadingInvite = true;

            // Find the form using 'form' tag
            const formElement = document.querySelector('form');

            // Create a FormData instance
            const formData = new FormData(formElement);

            fetch(`/course/send_invitation?course_id=${this.courseId}`, {
                method: "POST",
                body: formData,
                credentials: "include"
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        Alpine.store('notifier').add(data.message || "Invitation sent successfully", "success");
                    } else {
                        Alpine.store('notifier').add(data.message || "Something went wrong", "error");
                    }
                    this.invitationModal = false;
                })
                .catch(error => {
                    Alpine.store('notifier').add(error.message || "Network error", "error");
                })
                .finally(() => {
                    this.isLoadingInvite = false; // Turn loading off, success or fail
                });
        }
    }
}
