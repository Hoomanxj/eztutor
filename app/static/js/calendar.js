/**
 * 
 * @returns - Returns and object with methods and properties to handle assignments
 */
function calendar() {
    return {
        _initialized:false,
        currentDate: new Date(), // Date object
        customTasks: [], // Custom tasks
        classSchedules: [], // Class schedules
        newTaskDescription: '', // New task description
        showTaskModal: false, // Toggle task modal view
        selectedDateForTask: null, // Store selected day for task
        allSchedule: [], // Store all types of schedule
        selectedDayEvents: [], // Store all events for a particular day
        timelineInstance: null, // Not needed for custom timeline
        showDayModal: false, // Toggle day modal view
        formHtml: null, // Store form html

        // Getters
        get date() {
            return this.currentDate.getDate();
        },
        get month() {
            return this.currentDate.getMonth();
        },
        get year() {
            return this.currentDate.getFullYear();
        },
        get monthName() {
            return this.currentDate.toLocaleString('default', { month: 'long' });
        },
        get daysOfWeek() {
            return ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
        },
        get currentMonthDays() {
            let firstDayOfMonth = new Date(this.year, this.month, 1);
            let lastDayOfMonth = new Date(this.year, this.month + 1, 0);
            let days = [];

            // Add leading empty days for the first week
            let dayOfWeek = firstDayOfMonth.getDay();
            for (let i = 0; i < dayOfWeek; i++) {
                days.push({});
            }

            // Add actual days
            for (let day = 1; day <= lastDayOfMonth.getDate(); day++) {
                days.push({
                    date: `${this.year}-${(this.month + 1).toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`,
                });
            }

            return days;
        },

        /**
         * Intializes the calendar object.
         * Fetches all schedule along with each schedule type separately.
         */
        init() {
            if(!this._initialized) {
                this._initialized = true;
                this.fetchAllSchedule();
                this.fetchClassSchedules();
                this.fetchTasks();
            }
            
        },

        /**
         * Fetches class schedule.
         * 
         * @async
         * @throws {Error} - Throws an error if the network request fails.
         */
        fetchClassSchedules() {
            fetch("/calendar/get_class_schedule")
                .then((response) => response.json())
                .then((data) => {
                    if (data.success) {
                        this.classSchedules = data.class_schedule;
                    }
                })
                .catch((error) => {
                    Alpine.store('notifier').add(error.message || "Error fetching class schedule", "error");
                });
        },

        /**
         * Fetches task schedule.
         * 
         * @async
         * @throws {Error} - Throws an error if the network request fails.
         */
        fetchTasks() {
            fetch("/calendar/get_custom_schedule")
                .then((response) => response.json())
                .then((data) => {
                    if (data.success) {
                        this.customTasks = data.custom_schedule;
                    }
                })
                .catch((error) => {
                    Alpine.store('notifier').add(error.message || "Error fetching custom schedule", "error");
                });
        },

        /**
         * Fetches all schedule schedule.
         * 
         * @async
         * @throws {Error} - Throws an error if the network request fails.
         */
        fetchAllSchedule() {
            fetch("/calendar/get_all_schedule")
                .then((response) => response.json())
                .then((data) => {
                    if (data.success) {
                        this.allSchedule = data.all_schedule;
                    }
                })
                .catch((error) => {
                    Alpine.store('notifier').add(error.message || "Error fetching all schedule", "error");
                });
        },

        
        // Show previouse month
        prevMonth() {
            const newDate = new Date(this.currentDate);
            newDate.setMonth(newDate.getMonth() - 1);
            this.currentDate = newDate;
        },

        // Show next month
        nextMonth() {
            const newDate = new Date(this.currentDate);
            newDate.setMonth(newDate.getMonth() + 1);
            this.currentDate = newDate;
        },

        // Check if a class or task exists for a specific date
        hasClass(date) {
            return this.classSchedules.some((schedule) => schedule.date === date);
        },

        hasTask(date) {
            return this.customTasks.some((task) => task.date === date);
        },

        // Get the class schedule or task for a specific date
        getClassSchedule(date) {
            const schedules = this.classSchedules.filter((schedule) => schedule.date === date);
            return schedules.map(s => s.name).join(', ');
        },

        getTask(date) {
            const tasks = this.customTasks.filter((task) => task.date === date);
            return tasks.map(t => t.name).join(', ');
        },

        /**
         * Open a modal to add new tasks.
         * 
         * @async
         * @throws {Error} - Throws an error if the network request fails.
         */
        openTaskModal(date) {

            this.selectedDateForTask= date;

            fetch("/calendar/get_task_form")
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    this.formHtml = data.html;
                    this.showTaskModal = true;
                }
            })
            .catch((error) => {
                Alpine.store('notifier').add(error.message || "Error fetching custom task form", "error");
            });
        },

        /**
         * Send new task to backend.
         * 
         * @async
         * @throws {Error} - Throws an error if the network request fails.
         */
        saveTask() {
            
            const formElement = this.$refs.customTaskForm;
            const formData = new FormData(formElement)
            
            formData.append('date', this.selectedDateForTask)
            fetch("/calendar/add_task", {
                method: "POST",
                body: formData,
                credentials: 'include'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    Alpine.store('notifier').add(data.message || "Custom task successfully created", "success");
                    // Close modal, refresh assignments, etc.
                    this.closeTaskModal();
                    this.fetchAllSchedule();
                    this.fetchClassSchedules();
                    this.fetchTasks();
                    
                } else {
                    Alpine.store('notifier').add(data.message || "Date could not be determined", "error");
                    // Display error messages to the user
                }
            })
            .catch(error => {
                Alpine.store('notifier').add(error.message || "Error submitting custom task", "error");
            });
  
        },

        // Get events for a specific day
        getDayEvents(date) {
            const dayEvents = this.allSchedule
                .filter(e => e.date === date)
                .map(e => ({
                    ...e,
                    start_time: e.time_from,
                    end_time: e.time_to,
                    name: e.name
                }))
                .filter(e => e.start_time && e.end_time); // Ensure times are defined

            return dayEvents;
        },

        // Open the modal to display day's events
        openDayModal(date) {
            this.selectedDayEvents = this.getDayEvents(date);
            this.selectedDateForTask = date;
            this.showDayModal = true;
        },
        // Close the modal
        closeTaskModal() {
            this.showTaskModal = false;
            this.formHtml = null;

        },
    };
}
