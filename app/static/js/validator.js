/**
 * 
 * @returns - Returns and object with methods and properties to handle validations for all forms
 *      Included in layout.html to apply to all pages
 */
function fieldValidator() {
    return {
        error: '', // Error property
        
        // Field validator
        validateField(el, label, required) {
            if (required && el.value.trim() === '') {
                this.error = `${label} is required.`;
            } else {
                this.error = '';
            }
        },

        // Number validatior
        validateNumber(el, label, required) {
            const value = el.value.trim();
            if (required && value === '') {
                this.error = `${label} is required.`;
            } else if (value !== '' && isNaN(value)) {
                this.error = `${label} must be a valid number.`;
            } else {
                const min = el.min ? parseFloat(el.min) : null;
                const max = el.max ? parseFloat(el.max) : null;
                const numValue = parseFloat(value);
                if (min !== null && numValue < min) {
                    this.error = `${label} must be at least ${min}.`;
                } else if (max !== null && numValue > max) {
                    this.error = `${label} must be at most ${max}.`;
                } else {
                    this.error = '';
                }
            }
        },

        // File validatior
        validateFile(el, label, required) {
            if (required && (!el.files || el.files.length === 0)) {
                this.error = `${label} is required.`;
            } else {
                this.error = '';
            }
        },

        // Select validatior
        validateSelect(el, label, required) {
            if (required && el.value === '') {
                this.error = `Please select a ${label}.`;
            } else {
                this.error = '';
            }
        },

        // Time validatior
        validateTime(el, label, required) {
            if (required && el.value === '') {
                this.error = `Please select a ${label}.`;
            } else {
                this.error = '';
            }
        },

        // Multiple selector validatior
        validateSelectMultiple(target, label, required) {
            const checkboxes = document.querySelectorAll(`input[name="${target.name}[]"]`);
            const checked = Array.from(checkboxes).filter(checkbox => checkbox.checked);
            if (required && checked.length === 0) {
                this.error = `${label} is required.`;
            } else {
                this.error = '';
            }
        },

        // Email validatior
        validateEmail(el, label, required) {
            const email = el.value.trim();
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (required && email === '') {
                this.error = `${label} is required.`;
            } else if (email !== '' && !emailPattern.test(email)) {
                this.error = `Please enter a valid email address.`;
            } else {
                this.error = '';
            }
        },

        // Password validatior
        validatePassword(el, label, required) {
            const password = el.value;
            if (required && password === '') {
                this.error = `${label} is required.`;
            } else {
                this.error = '';
            }
        },

        // Date validator
        validateDate(el, label, required) {
            if (required && el.value === '') {
                this.error = `Please select a ${label}.`;
            } else {
                this.error = '';
            }
        },

        // URL validatior
        validateURL(el, label, required) {
            const url = el.value.trim();

            // If required and empty
            if (required && url === '') {
                this.error = `${label} is required.`;
            }
            // If not empty, check format
            else if (url !== '') {
                // A simple pattern checking it starts with http:// or https://
                const pattern = /^https?:\/\/.+$/i;
                if (!pattern.test(url)) {
                    this.error = `Please enter a valid URL that starts with http:// or https://.`;
                } else {
                    this.error = '';
                }
            } else {
                this.error = '';
            }
        },
    }
}
