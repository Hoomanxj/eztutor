/**
 * Initializes analytics object for displaying student scores.
 * 
 * @param {string} role - The role of the user, either "student" or "teacher".
 * @returns {object} = An object with methods and properties to handle analytics.
 */
function analytics(role) {
    return {
        role: role,
        courses: [], // List of courses
        selectedCourse: null, // Currently selected course
        students: [], // List of students
        selectedStudent: null, // Currently selected student
        scores: {}, // Object containing all scores
        charts: {}, // Object storing all chart instances

        // Chart configurations
        chartConfigs: [
            {
                id: "categoryScoreChart",
                type: "polarArea",
                title: "Category Scores",
                dataPath: "cat_scores",
                label: "Average Score",
                backgroundOpacity: 0.6,
                borderOpacity: 1,
                plugins: ["ChartDataLabels"],
                colorScheme: [
                    '54, 162, 235',   // Blue
                    '255, 206, 86',    // Yellow
                    '75, 192, 192',    // Teal
                    '255, 99, 132',     // Red
                    '153, 102, 255',    // Purple
                    '255, 159, 64',     // Orange
                    '201, 203, 207',    // Grey
                    '255, 99, 71',      // Tomato
                    '60, 179, 113',     // Medium Sea Green
                    '255, 165, 0'       // Orange
                ]
            },
            {
                id: "speakingScoreChart",
                type: "bar",
                title: "Speaking Scores",
                dataPath: "speaking",
                label: "Speaking Scores",
                backgroundOpacity: 0.6,
                borderOpacity: 1,
                plugins: ["ChartDataLabels"],
                colorScheme: [
                    '54, 162, 235',
                    '255, 206, 86',
                    '75, 192, 192',
                    '255, 99, 132',
                    '153, 102, 255',
                    '255, 159, 64',
                    '201, 203, 207',
                    '255, 99, 71',
                    '60, 179, 113',
                    '255, 165, 0'
                ]
            },
            {
                id: "listeningScoreChart",
                type: "bar",
                title: "Listening Scores",
                dataPath: "listening",
                label: "Listening Scores",
                backgroundOpacity: 0.6,
                borderOpacity: 1,
                plugins: ["ChartDataLabels"],
                colorScheme: [
                    '54, 162, 235',
                    '255, 206, 86',
                    '75, 192, 192',
                    '255, 99, 132',
                    '153, 102, 255',
                    '255, 159, 64',
                    '201, 203, 207',
                    '255, 99, 71',
                    '60, 179, 113',
                    '255, 165, 0'
                ]
            },
            {
                id: "writingScoreChart",
                type: "bar",
                title: "Writing Scores",
                dataPath: "writing",
                label: "Writing Scores",
                backgroundOpacity: 0.6,
                borderOpacity: 1,
                plugins: ["ChartDataLabels"],
                colorScheme: [
                    '54, 162, 235',
                    '255, 206, 86',
                    '75, 192, 192',
                    '255, 99, 132',
                    '153, 102, 255',
                    '255, 159, 64',
                    '201, 203, 207',
                    '255, 99, 71',
                    '60, 179, 113',
                    '255, 165, 0'
                ]
            },
            {
                id: "readingScoreChart",
                type: "bar",
                title: "Reading Scores",
                dataPath: "reading",
                label: "Reading Scores",
                backgroundOpacity: 0.6,
                borderOpacity: 1,
                plugins: ["ChartDataLabels"],
                colorScheme: [
                    '54, 162, 235',
                    '255, 206, 86',
                    '75, 192, 192',
                    '255, 99, 132',
                    '153, 102, 255',
                    '255, 159, 64',
                    '201, 203, 207',
                    '255, 99, 71',
                    '60, 179, 113',
                    '255, 165, 0'
                ]
            }
        ],

        /**
         * Initializes the analytics object.
         * Fetches courses and sets the initial state.
         */
        init() {
            if (!this._initialized) {
                this._initialized = true;
                this.fetchCourses();
            }
        },

        /**
         * Fetches the list of courses for the user.
         * 
         * @async
         * @throws {Error} - Throws an error if the network request fails.
         */
        fetchCourses() {
            fetch("/analytics/get_courses")
                .then((response) => response.json())
                .then((data) => {
                    if (data.success) {
                        this.courses = data.courses;
                        if (this.courses && this.courses.length > 0) {
                            this.selectedCourse = this.courses[0].id;

                            if (this.role === "student") {
                                this.fetchCourseScores({ courseId: this.selectedCourse });
                            } else if (this.role === "teacher") {
                                this.fetchStudents(this.selectedCourse);
                            }
                        } else {
                            // No courses available
                            this.clearAllCharts();
                        }
                    } else {
                        Alpine.store('notifier').add(data.message || "Something went wrong", "error");
                        this.clearAllCharts();
                    }
                })
                .catch((error) => {
                    Alpine.store('notifier').add(error.message || "Network error", "error");
                });
        },

        /**
         * Configuration for charts used in the analytics dashboard.
         * 
         * @type {Array<Object>}
         * @property {string} id - The ID of the chart element.
         * @property {string} type - The type of chart (e.g., "bar", "polarArea").
         * @property {string} title - The title of the chart.
         * @property {string} dataPath - Path to the data in the scores object.
         * @property {string} label - Label for the chart dataset.
         * @property {number} backgroundOpacity - Opacity of the chart background color.
         * @property {number} borderOpacity - Opacity of the chart border color.
         * @property {Array<string>} plugins - List of plugins for the chart.
         * @property {Array<string>} colorScheme - Array of color codes for the chart.
         */
        fetchStudents(courseId) {
            
            // Reset students and selectedStudent immediately
            this.students = [];
            this.selectedStudent = null;

            fetch(`/analytics/get_students?course_id=${courseId}`)
                .then((response) => response.json())
                .then((data) => {
                    if (data.success) {
                        this.students = data.students || []; // Safely assign
                        if (this.students.length > 0) {

                            // Set default selected student
                            this.selectedStudent = this.students[0].id;

                            // Fetch scores for that student
                            this.fetchCourseScores({ courseId: this.selectedCourse, studentId: this.selectedStudent });
                        } else {
                            
                            // clear charts if no students
                            this.clearAllCharts();
                        }
                    } else {
                        Alpine.store('notifier').add(data.message || "Something went wrong", "error");
                        this.clearAllCharts();
                    }
                })
                .catch((error) => {
                    Alpine.store('notifier').add(error.message || "Network error", "error");
                    this.clearAllCharts();
                });
        },

        /**
         * Renders a chart based on the given configuration.
         * 
         * @param {Object} config - Configuration object for the chart.
         * @param {string} config.id - The ID of the chart element.
         * @param {string} config.type - The type of chart (e.g., "bar", "polarArea").
         * @param {string} config.title - The title of the chart.
         * @param {string} config.dataPath - Path to the data in the scores object.
         * @param {string} config.label - Label for the chart dataset.
         * @param {number} config.backgroundOpacity - Opacity of the chart background color.
         * @param {number} config.borderOpacity - Opacity of the chart border color.
         * @param {Array<string>} config.plugins - List of plugins for the chart.
         * @param {Array<string>} config.colorScheme - Array of color codes for the chart.
         */
        fetchCourseScores({ courseId, studentId = null }) {
            if (!courseId) {
                this.clearAllCharts();
                return; // Early exit if no course is selected
            }
            this.selectedCourse = courseId;
            this.selectedStudent = studentId;
            if (this.role === "teacher") {
            }

            let url;
            if (this.role === "teacher" && studentId) {
                url = `/analytics/get_student_scores?course_id=${courseId}&student_id=${studentId}`;
            } else {
                url = `/analytics/get_student_scores?course_id=${courseId}`;
            }
            fetch(url)
                .then((response) => {
                    if (!response.ok) {
                        throw new Error(`Server error: ${response.status}`);
                    }
                    return response.json();
                })
                .then((data) => {
                    if (data.success) {
                        this.scores = data.scores || {};
                        if (Object.keys(this.scores).length > 0) {
                            this.renderAllCharts();
                        } else {
                            this.clearAllCharts();
                        }
                    } else {
                        Alpine.store('notifier').add(data.message || "Something went wrong", "error");
                        this.clearAllCharts();
                    }
                })
                .catch((error) => {
                    Alpine.store('notifier').add(error.message || "Network error", "error");
                    this.clearAllCharts();
                });
        },

        // Render all charts based on chartConfigs
        renderAllCharts() {
            if (!this.chartConfigs || !Array.isArray(this.chartConfigs)) {
                return;
            }
            this.chartConfigs.forEach(config => {
                this.renderChart(config);
            });
        },

        // Generic chart rendering function
        renderChart(config) {
            const { id, type, title, dataPath, label, backgroundOpacity, borderOpacity, plugins, colorScheme } = config;
        
            // Destroy existing chart if it exists to prevent multiple instances
            if (this.charts[id]) {
                this.charts[id].destroy();
            }
        
            // Extract data based on dataPath
            let chartData;
            if (dataPath === "cat_scores") {
                if (!this.scores.cat_scores) {
                    this.clearChart(id);
                    return;
                }
                chartData = {
                    labels: Object.keys(this.scores.cat_scores),
                    data: Object.values(this.scores.cat_scores).map(score => Number(score))
                };
            } else {
                if (!this.scores.tag_scores || !this.scores.tag_scores[dataPath]) {
                    this.clearChart(id);
                    return;
                }
                const specificData = this.scores.tag_scores[dataPath];
                chartData = {
                    labels: Object.keys(specificData),
                    data: Object.values(specificData).map(score => Number(score))
                };
            }
        
            // If there's no data, clear the chart and exit
            if (!chartData.data || chartData.data.length === 0) {
                this.clearChart(id);
                return;
            }

            // Get the context of the canvas where the chart will be rendered
            const canvas = document.getElementById(id);
            if (!canvas) {
                return;
            }
            const ctx = canvas.getContext("2d");
        
            // Create a new Chart instance
            this.charts[id] = new Chart(ctx, {
                type: type,
                data: {
                    labels: chartData.labels,
                    datasets: [{
                        label: label,
                        data: chartData.data,
                        backgroundColor: this.generateColors(chartData.labels.length, backgroundOpacity, colorScheme),
                        borderColor: this.generateColors(chartData.labels.length, borderOpacity, colorScheme),
                        borderWidth: 1
                    }]
                },
                options: this.getChartOptions(type, title),
                plugins: plugins.map(plugin => window[plugin]) // Ensure plugins are accessible globally
            });
        
        },
        

        // Function to get chart options based on chart type
        getChartOptions(type, title) {
            if (type === "polarArea") {
                return {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: "right",
                            labels: {
                                font: {
                                    size: 14
                                }
                            }
                        },
                        title: {
                            display: true,
                            text: title,
                            font: {
                                size: 18
                            }
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    let label = context.label || '';
                                    if (label) {
                                        label += ': ';
                                    }
                                    if (context.raw !== null && typeof context.raw === 'number') {
                                        label += context.raw;
                                    } else if (context.parsed !== null && typeof context.parsed === 'number') {
                                        label += context.parsed;
                                    } else {
                                        label += 'N/A';
                                    }
                                    return label;
                                }
                            }
                        },
                        datalabels: { // Data Labels Configuration
                            color: '#fff',
                            formatter: function(value, context) {
                                return value;
                            },
                            font: {
                                weight: 'bold',
                                size: 14
                            }
                        }
                    },
                    scales: {
                        r: {
                            beginAtZero: true,
                            ticks: {
                                backdropColor: 'transparent'
                            }
                        }
                    }
                };
            } else if (type === "bar") {
                return {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: false
                        },
                        title: {
                            display: true,
                            text: title,
                            font: {
                                size: 18
                            }
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    let label = context.dataset.label || '';
                                    if (label) {
                                        label += ': ';
                                    }
                                    if (context.parsed.y !== null && typeof context.parsed.y === 'number') {
                                        label += context.parsed.y;
                                    } else {
                                        label += 'N/A';
                                    }
                                    return label;
                                }
                            }
                        },
                        datalabels: { // Data Labels Configuration
                            color: '#000',
                            formatter: function(value, context) {
                                return value;
                            },
                            font: {
                                weight: 'bold',
                                size: 14
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Score'
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'Criteria'
                            }
                        }
                    }
                };
            } else {
                // Default options
                return {
                    responsive: true
                };
            }
        },

        // Generic color generator with predefined color schemes
        generateColors(count, opacity, colorScheme) {
            const colors = [];
            for (let i = 0; i < count; i++) {
                const color = colorScheme[i % colorScheme.length];
                colors.push(`rgba(${color}, ${opacity})`);
            }
            return colors;
        },

        // Clear a specific chart by ID and display a message
        clearChart(id) {
            if (this.charts[id]) {
                this.charts[id].destroy();
                delete this.charts[id];
            }

            // Get the canvas element by its ID
            const canvas = document.getElementById(id);
            if (canvas) {
                const ctx = canvas.getContext("2d");

                // Clear the canvas
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                // Set up text properties
                ctx.font = "16px Arial";
                ctx.fillStyle = "#be185d";
                ctx.textAlign = "center";
                ctx.textBaseline = "middle"; // Vertically center the text

                // Display the message in the center of the canvas
                ctx.fillText("You don't have any scores to show!", canvas.width / 2, canvas.height / 2);
            } else {
            }
        },

        // Clear all charts and display messages on each canvas
        clearAllCharts() {
            for (const id in this.charts) {
                if (this.charts.hasOwnProperty(id)) {
                    // Destroy the existing chart instance
                    this.charts[id].destroy();

                    // Get the canvas element by its ID
                    const canvas = document.getElementById(id);
                    if (canvas) {
                        const ctx = canvas.getContext("2d");

                        // Clear the canvas
                        ctx.clearRect(0, 0, canvas.width, canvas.height);

                        // Set up text properties
                        ctx.font = "16px Arial";
                        ctx.fillStyle = "#be185d";
                        ctx.textAlign = "center";
                        ctx.textBaseline = "middle"; // Vertically center the text

                        // Display the message in the center of the canvas
                        ctx.fillText("You don't have any scores to show!", canvas.width / 2, canvas.height / 2);
                    } else {
                    }
                }
            }
            // Reset the charts object
            this.charts = {};
        }
    }
}
