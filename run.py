from app import create_app
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Determine configuration class based on environment
config_class = "app.config.ProductionConfig" if os.getenv("FLASK_ENV") == "production" else "app.config.DevelopmentConfig"

# Create the Flask app instance
app = create_app(config_class=config_class)

# Error handler for production
@app.errorhandler(500)
def internal_error(error):
    return "An error occurred on the server. Please try again later.", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
