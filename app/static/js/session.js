/**
 * 
 * @param {string} - The role of the user, either "student" or "teacher".
 * @returns - Returns and object with methods and properties to handle session
 */
function sessionPage(role) {
    return {
        role: role, // Current user
        courses: [], // List of all courses
        courseId: null, // Selected course ID
        selectedCourse: null, // Selected course
        sessions: [], // List of sessions for a selected course
        selectedSession: null, // Selected session
        isDropdownOpen: false, // For dropdown visibility
        show: false, // Show toggle
        sessionId: null, // Selected session ID
        sessionHtml: null, // Session form html
        
        /**
         * Intializes session object.
         * Fetches all courses.
         */
        init() {
            if (this._initialized) return; // Prevent multiple initializations
            this._initialized = true;
            this.fetchCourses();
        },

        /**
         * Fetches courses of user.
         * 
         * @async
         * @throws {Error} - Throws an error if network request fails.
         */
        fetchCourses() {

            fetch("/session/get_courses")
                .then((response) => response.json())
                .then((data) => {
                    if (data.success) {
                        this.courses = data.courses;
                        if (this.courses && this.courses.length > 0) {
                            if (!this.courseId) {
                                // Default to first course in courses list
                                this.courseId = this.courses[0]['id'];
                            }
                            this.fetchCourseData(this.courseId);
                        }
                    }
                })
                .catch((error) => {
                    Alpine.store('notifier').add(error.message || "Error fetching courses", "error");
                });
        },

        // Fetches selected course's data
        fetchCourseData(courseId) {
            if(this.courseId !== courseId) {
                this.courseId = courseId;
            }
            if(this.courses && this.courses.length > 0) {
                this.selectedCourse = this.courses.find((course) => course.id == this.courseId) || null;
                if (this.selectedCourse) {
                    this.fetchSessions(this.courseId);
                }
            }
        },

        /**
         * Fetches sessions of selected course.
         * 
         * @async
         * @throws {Error} - Throws an error if network request fails.
         */
        fetchSessions(courseId) {

            fetch(`/session/get_sessions?course_id=${courseId}`)
                .then((response) => response.json())
                .then((data) => {
                    if (data.success) {
                        this.sessions = data.sessions;
                    }
                })
                .catch((error) => {
                    Alpine.store('notifier').add(error.message || "Error fetching sessions", "error");
                });
        },

        /**
         * Fetches session data for selected session.
         * 
         * @async
         * @throws {Error} - Throws an error if network request fails.
         */
        fetchSessionData(sessionId) {

            if (this.sessionId !== sessionId) {
                this.sessionId = sessionId;
            }
            fetch(`/session/get_session_info?session_id=${this.sessionId}`)
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    this.sessionHtml = data.html
                    // Toggle form view on if there is a form
                    this.showForm(true);
                }
            })
            .catch((error) => {
                Alpine.store('notifier').add(error.message || "Error fetching session info", "error");
            });
        },

        // Form view toggler
        showForm(show) {
            if (this.show !== show) {
                this.show = show;
            }
        },

        /**
         * Send session update data to backend.
         * 
         * @async
         * @throws {Error} - Throws an error if network request fails.
         */
        updateSession() {
            
            // Grab form by 'form' tag and create a FormData instance
            const formElement = document.querySelector("form");
            const formData = new FormData(formElement);
            fetch("/session/update_session_info", {
                method: "POST",
                body: formData,
                credentials: "include"
            })
            .then(((response) => response.json()))
            .then((data) => {
                if(data.success) {
                    Alpine.store('notifier').add(data.message || "Successfully updated session info", "success");
                    this.fetchSessions(this.courseId);
                } else {
                    Alpine.store('notifier').add(data.message || "Session info was not updated", "error");
                }
            })
            .catch((error) => {
                Alpine.store('notifier').add(error.message || "Error updating session info", "error");
            })
            .finally(() => {

                // In any case close the form
                this.show = false;
            })
        },

        // Helper function to map status to class
        getStatusClass(status) {
            
            // Turn to lower to avoide spelling errors
            switch(status.toLowerCase()) {
                case 'pending':
                    return 'bg-yellow-600';
                case 'held':
                    return 'bg-green-600';
                case 'cancelled':
                    return 'bg-red-600';
                default:
                    return '';
            }
        },
        
    };
}
