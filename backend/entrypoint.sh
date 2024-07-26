#!/bin/sh

 # This line specifies the script interpreter to be /bin/sh, a standard shell on Unix-like systems

# Print a message to indicate that the script is applying database migrations
echo "Applying database migrations..."

# Automatically create new migrations based on the changes detected in models
# Note: This is generally recommended for development environments only
python manage.py makemigrations

# Run Django's migrate command to apply database migrations. This ensures that the database schema is up to date with the latest changes.
python manage.py migrate

# Execute any additional commands passed to the script
# The `exec "$@"` command replaces the shell with the command that follows, allowing the container to run the main process.
# This is useful for running the Django development server or any other commands specified in the Dockerfile or Docker Compose file.
exec "$@"