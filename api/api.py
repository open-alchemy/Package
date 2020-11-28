"""Main function for lambda."""

import app
import serverless_wsgi


def main(event, context):
    """Handle request."""
    return serverless_wsgi.handle_request(app.app, event, context)
