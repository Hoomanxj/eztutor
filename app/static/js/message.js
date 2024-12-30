/**
 * 
 * Handles JSON messages using Alpine. Inserted in layout.html
 */
document.addEventListener('alpine:init', () => {
    Alpine.store('notifier', {
        messages: [],

        // Add a new alert
        // Type can be 'success', 'error', 'info', etc.
        add(message, type = 'info') {
            this.messages.push({ text: message, type: type });

            // Scroll the messages container into view so the user sees the newest message
            const notifierContainer = document.getElementById('notifier-container');
            if (notifierContainer) {
                notifierContainer.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }

            // Auto-remove after X ms (just as you already had)
            setTimeout(() => { 
                this.remove(0);
            }, 5000);
        },

        // Remove an alert by index
        remove(index) {
            this.messages.splice(index, 1);
        }
    });
});
