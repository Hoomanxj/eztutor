/**
 * 
 * @param {string} role - The role of the user, either "student" or "teacher". 
 * @returns - Returns and object with methods and properties to handle dashboard
 */
function dashboard(role) {
    return {
        role: role, // Current user
        courses: [], // List of courses
        schedule: [], // List of today's schedule
        upcomingSession: [], // List of upcoming session
        upcomingCourse: [], // List of upcoming course
        selectedCourse: [], // For the custom dropdown
        isDropdownOpen: false, // Dropdown state
        courseId: null, // Selected course ID
        catScores: [], // List of category scores of a course
        students: [], // List of students for a given course
        selectedStudent: [], // Selected student
        _initialized: false, // Initilizie status check

        /**
         * Intializes dashboard object.
         * Fetches all courses, today's schedule and upcoming session info.
         */
        init() {
            if (!this._initialized) {
                this._initialized = true;
                this.fetchCourses();
                this.fetchSchedule();
                this.fetchUpcomingSession();
            }
        },
        
        /**
         * Fetches schedule of the day.
         * 
         * @async
         * @throws {Error} - Throws an error if network request fails.
         */
        fetchSchedule() {
            fetch("/dashboard/get_schedule")
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        this.schedule = data.schedule;
                    }
                })
                .catch((error) => {
                    Alpine.store('notifier').add(error.message || "Network error", "error");
                });
        },

        // Determine the background color of each event based on its type
        getTaskClass(type) {
            switch(type.toLowerCase()) {
                case 'class':
                    return 'bg-yellow-600';
                case 'custom':
                    return 'bg-green-600';
                default:
                    return 'bg-gray-600'; // Default color for unknown types
            }
        },

        /**
         * Fetches upcoming session and its course.
         * 
         * @async
         * @throws {Error} - Throws an error if session data is not found or network request fails.
         */
        fetchUpcomingSession() {
            console.log('Fetching upcoming session for user:', this.role);
            fetch("/dashboard/get_upcoming_session")
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        this.upcomingSession = data.session;
                        this.upcomingCourse = data.course;

                    } else {
                        Alpine.store('notifier').add(data.message || "Error fetching upcoming session data", "error");
                    }
                })
                .catch((error) => {
                    Alpine.store('notifier').add(error.message || "Network error", "error");
                });
        },
        
        /**
         * Fetches all courses.
         * 
         * @async
         * @throws {Error} - Throws an error if network request fails.
         */
        fetchCourses() {

            fetch("/dashboard/get_courses")
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        this.courses = data.courses;
                        if (this.courses && this.courses.length > 0) {

                            this.courseId = this.courses[0].id; // Set the first course as default
                            this.selectedCourse = this.courses[0]; // Set the first course as default
                            if (this.role === "student") {
                                this.fetchCourseScores({ courseId: this.courseId });
                            } else if (this.role === "teacher") {
                                this.fetchStudents(this.courseId);
                            }
                        }
                    }
                })
                .catch((error) => {
                    Alpine.store('notifier').add(error.message || "Network error", "error");
                });
        },

        /**
         * Fetches students of a course - Teacher only.
         * 
         * @async
         * @throws {Error} - Throws an error if no studens found or network request fails.
         */
        fetchStudents(courseId) {
        
            // Clear existing students right away so the dropdown resets.
            this.students = [];
            this.selectedStudent = null;
            
            fetch(`/dashboard/get_students?course_id=${courseId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        this.students = data.students || []; // Safely assign
                        if (this.students.length > 0) {

                            // Set default selected student
                            this.selectedStudent = this.students[0].id; 
                            // Fetch scores for that student (if you want immediate chart updates)
                            this.fetchCourseScores({ courseId: this.courseId, studentId: this.selectedStudent });
                        } else {

                            // Clear the chart:
                            this.clearChart();
                        }
                    } else {
                        Alpine.store('notifier').add(data.message || "Something went wrong", "error");
                        this.clearChart();
                    }
                })
                .catch((error) => {
                    Alpine.store('notifier').add(error.message || "Network error", "error");
                });
        },

        /**
         * Fetches category scores for each course based on student and draws the chart for it.
         * 
         * @async
         * @throws {Error} - Throws an error if network request fails.
         */
        fetchCourseScores({ courseId, studentId = null }) {
            if(this.courseId !== courseId) {
                this.clearChart();
                this.courseId = courseId;
            }
            this.courseId = courseId;
            this. selectedStudent = studentId;

            // Based on user type decide on URL params
            let url;
            if (this.role === "teacher" && studentId) {
                url = `/dashboard/get_student_scores?course_id=${courseId}&student_id=${studentId}`;

            } else {
                url = `/dashboard/get_student_scores?course_id=${courseId}`;
            }

            fetch(url)
                .then((response) => {
                    if (!response.ok) {
                        throw new Error(`Server error: ${response.status}`);
                    }
                    return response.json();
                })
                .then((data) => {
                    if (data.success){
                        this.catScores = data.scores.cat_scores;

                        if (!this.catScores || Object.keys(this.catScores).length === 0) {
                            this.clearChart();
                            return;
                        }
                    }
                    // Prepare labels and values
                    const labels = Object.keys(this.catScores);
                    const values = Object.values(this.catScores).map(Number);

                    // Define a simple color scheme for four categories
                    const backgroundColors = [
                        "rgba(54, 162, 235, 0.6)",   // Blue
                        "rgba(255, 206, 86, 0.6)",   // Yellow
                        "rgba(75, 192, 192, 0.6)",   // Teal
                        "rgba(255, 99, 132, 0.6)"    // Red
                    ];
                    const borderColors = [
                        "rgba(54, 162, 235, 1)",
                        "rgba(255, 206, 86, 1)",
                        "rgba(75, 192, 192, 1)",
                        "rgba(255, 99, 132, 1)"
                    ];

                    // Get canvas context
                    const canvas = document.getElementById("categoryScoreChart");
                    
                    // If canvas tag was not found
                    if (!canvas) {
                        return;
                    }
                    const ctx = canvas.getContext("2d");

                    // Destroy existing chart instance if it exists to prevent duplication
                    if (canvas.chartInstance) {
                        canvas.chartInstance.destroy();
                    }

                    // Create the Polar Area chart
                    canvas.chartInstance = new Chart(ctx, {
                        type: "polarArea",
                        data: {
                            labels: labels,
                            datasets: [{
                                label: "Category Scores",
                                data: values,
                                backgroundColor: backgroundColors,
                                borderColor: borderColors,
                                borderWidth: 1
                            }]
                        },
                        options: {
                            responsive: true,
                            plugins: {
                                legend: {
                                    position: "right"
                                },
                                title: {
                                    display: true,
                                    text: "Category Scores"
                                },
                                tooltip: {
                                    callbacks: {
                                        label: function(context) {
                                            let label = context.label || "";
                                            if (label) {
                                                label += ": ";
                                            }
                                            return (typeof context.raw === "number") ? label + context.raw : label + "N/A";
                                        }
                                    }
                                },
                                datalabels: {
                                    color: "#fff",
                                    formatter: (value) => value,
                                    font: {
                                        weight: "bold",
                                        size: 14
                                    }
                                }
                            },
                            scales: {
                                r: {
                                    beginAtZero: true,
                                    ticks: {
                                        backdropColor: "transparent"
                                    }
                                }
                            }
                        },
                        plugins: [ChartDataLabels]
                    });
                })
                .catch(error => {
                    Alpine.store('notifier').add(error.message || "Network error", "error");
                });
        },

        // Clear the chart and display a message if no data was passed to it
        clearChart() {
            
            // Grab canvas tag
            const canvas = document.getElementById("categoryScoreChart");
            if (canvas && canvas.chartInstance) {
                canvas.chartInstance.destroy();
                canvas.chartInstance = null;
                // Display a message on the canvas
                const ctx = canvas.getContext("2d");
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.font = "14px Arial";
                ctx.fillStyle = "#666";
                ctx.textAlign = "center";
                ctx.textBaseline = "middle";

                // Message to display in case no data was passed
                ctx.fillText("No scores to show!", canvas.width / 2, canvas.height / 2);
            }
        },
    }
}
