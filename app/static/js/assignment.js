/**
 * 
 * @param {string} role - The role of the user, either "student" or "teacher". 
 * @returns - Returns and object with methods and properties to handle assignments
 */
function assignmentPage(role) {
    return {
        role: role,
        courseId: null, // Selected course's ID
        courses: [], // List of courses
        students: [], // List of students
        studentId: null, // Selected student's ID
        selectedCourse: null, // Currently selected course
        assignments: [], // List of assignments
        selectedStatus: null, // Status of currently selected course
        assignmentId: null, // Selected assignment's ID
        selectedAssignments: [], // Selected assignments list
        activeTab: "pending", // Active tab - default to "pending"
        isModalOpen: false, // Modal status
        formType: null, // Form type
        choices: {}, // Array of choices
        category: null, // Assignment category
        formHtml: null, // Form html
        isLoading: false, // loading status

        /**
         * Intializes the assignments object.
         * Fetches course and sets the intial state.
         */
        init() {
            if (this._initialized) return;
            this._initialized = true;
            this.fetchCourses();            
        },

        /**
         * Fetches the list of courses for the user.
         * 
         * @async
         * @throws {Error} - Throws an error if the network request fails.
         */
        fetchCourses() {
            this.courses = []; // Clear previous course's data
            fetch("/assignment/get_courses")
                .then((response) => response.json())
                .then((data) => {
                    if(data.success) {
                        this.courses = data.courses;
                        if(!this.courseId && this.courses.length > 0) {
                            this.courseId = this.courses[0].id;
                            this.fetchCourseData(this.courseId);
                        }
                    }
                })
                .catch((error) => {
                    Alpine.store('notifier').add(error.message || "Network error:", error);
                });
        },
        /**
         * Fetches the course data for the selected course.
         * 
         */        
        fetchCourseData(courseId) {
            this.selectedCourse = null; 
            this.students = [];       // Clear old students
            this.assignments = [];    // Clear old assignments
            this.selectedAssignments = [];

          
            // Update the selected course
            this.courseId = courseId;  
            this.selectedCourse = this.courses.find((course) => course.id == courseId);
            
            if (this.selectedCourse) {
          
              // If teacher => fetchStudents(); if student => fetchAssignments()
              if (this.role === "teacher") {
                this.fetchStudents(this.courseId);
              } else if (this.role === "student") {
                this.fetchAssignments({ courseId: this.courseId });
              }
            }
        },

        /**
         * Fetches the list of students for the selected course.
         * 
         * @async
         * @throws {info} - Throws info if the list is empty
         * @throws {Error} - Throws an error if the network request fails.
         */
        fetchStudents(courseId) {
            // Always clear old data first 
            this.students = [];
            this.assignments = [];
            this.selectedAssignments = [];
            this.studentId = null;
          
            fetch(`/assignment/get_students?course_id=${courseId}`)
              .then(response => response.json())
              .then(data => {
                if (data.success && data.students.length > 0) {

                  // We have students
                  this.students = data.students;

                  // Pick the first student by default
                  this.studentId = this.students[0].id;

                  // Fetch the assignments for that student
                  this.fetchAssignments({ courseId: courseId, studentId: this.studentId });
                } else {

                  // No students => keep arrays empty
                  Alpine.store('notifier').add(
                    data.message || "No students found for this course",
                    "info"
                  );

                  // The user will see empty lists and “no assignments / no students” messages
                }
              })
              .catch(error => {
                Alpine.store('notifier').add(error.message || "Network error", "error");
              });
        },
         
        /**
         * Fetches the list of assignments for the selected user.
         * 
         * @async
         * @throws {info} - Throws info if the there are no assignments
         * @throws {Error} - Throws an error if the network request fails.
         */
        fetchAssignments({ courseId, studentId = null }) {
            // Clear old data
            this.assignments = [];
            this.selectedAssignments = [];

            // Select the URL based on user type
            let url;
            if (this.role === "teacher") {
              url = `/assignment/get_assignments?course_id=${courseId}&student_id=${studentId}`;
            } else {
              url = `/assignment/get_assignments?course_id=${courseId}`;
            }
          
            fetch(url)
              .then((response) => response.json())
              .then((data) => {
                if (data.success) {
                  this.assignments = data.assignments;
          
                  // Show the pending tab by default
                  this.showAssignments("pending");
          
                  // If no assignments at all, you can also notify the user here:
                  if (this.assignments.length === 0) {
                    Alpine.store('notifier').add("No assignments found for the selected course", "info");
                  }
                } else {

                  // The server responded with success=false or something
                  Alpine.store('notifier').add(
                    data.message || "No assignments found for this course",
                    "info"
                  );
                  // assignments remain empty => user sees no old data
                }
              })
              .catch((error) => {
                Alpine.store('notifier').add(error.message || "Network error while fetching assignments", "error");
              });
        },
          
        // Show assignments
        showAssignments(status) {
            this.activeTab = status;
            this.selectedStatus = status;
            // Filter the current assignment list
            this.selectedAssignments = this.assignments.filter(
              (assignment) => assignment.status === status
            );
        },
        
        /**
         * Fetches the correct form type based on arguments provided.
         * 
         * @async
         * @throws {Error} - Throws an error if form fetch or network request fails.
         */
        openModal({ courseId = null, formType = null, category = null, assignmentId = null, studentId=null } = {}) {
            
            // Pass any arguments given
            this.courseId = courseId;
            this.formType = formType || null;
            this.category = category || null;
            this.assignmentId = assignmentId || null;
            this.studentId = studentId;

            const params = new URLSearchParams();

            // Append arguments to URL
            if (courseId !== null) params.append('course_id', courseId);
            if (formType !== null) params.append('form_type', formType);
            if (category !== null) params.append('category', category);
            if (assignmentId !== null) params.append('assignment_id', assignmentId);
            if (studentId !== null) params.append('student_id', studentId);

            const fetchUrl = `/assignment/get_form?${params.toString()}`;

            fetch(fetchUrl)
                .then((response) => response.json())
                .then((data) => {
                    if (data.success) {
                        this.formHtml = data.html || '';
                        this.isModalOpen = true;
                    } else {
                        this.closeModal();
                        Alpine.store('notifier').add(data.message || "Something went wrong", "error");
                    }

                })
                .catch((error) => {
                    this.closeModal();
                    Alpine.store('notifier').add(error.message || "Network error", "error");
                });
        },

        // Close modal
        closeModal() {
            this.isModalOpen = false;
            this.formHtml = '';
            this.choices = {};
        },

        /**
         * Send user data provided in forms to backend.
         * 
         * @async
         * @throws {Error} - Throws an error if form data is not valid or netwrok request fails.
         */
        submitForm() {
            this.isLoading = true; // Turn loading on
        
            const formElement = this.$refs.assignmentForm;
            const formData = new FormData(formElement);
            const formType = formData.get('form_type'); // read the hidden input
            
            let url;
            // Decide the backend route based on form_type
            if (formType === 'create') {
                url = "/assignment/create_assignment";
                formData.append('course_id', this.courseId);

            } else if (formType === 'submit') {
                url = "/assignment/submit_assignment";
                formData.append('assignment_id', this.assignmentId);

            } else if (formType === 'score') {
                url = "/assignment/score_assignment";
                formData.append('assignment_id', this.assignmentId);
                formData.append('student_id', this.studentId);
                
            } else {
                return;
            }
        
            fetch(url, {
                method: "POST",
                body: formData,
                credentials: 'include'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    Alpine.store('notifier').add(data.message || "Form was successfully submitted", "success");
                    
                    // Close modal, refresh assignments, etc.
                    this.closeModal();
                    this.fetchCourses();
                } else {
                    this.closeModal();
                    Alpine.store('notifier').add(data.message || "Something went wrong", "error");
                    // Display error messages to the user
                }
            })
            .catch(error => {
                this.closeModal();
                Alpine.store('notifier').add(error.message || "Network error", "error");
            }).finally(() => {
                this.isLoading = false; // Turn loading off, success or fail
            });
        }
    };
}
