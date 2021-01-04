"""Main function for lambda."""


def main(event, context):
    """Handle request."""
    print({"event": event, "context": context})  ## allow-print
