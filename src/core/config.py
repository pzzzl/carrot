"""Configuration module for the application.

This module contains mock configurations for authentication,
secret management, and request status tracking.

⚠️ WARNING:
These values are intended for development or testing purposes only.
In production, they must be replaced with secure, persistent, and properly
managed solutions (e.g., environment variables, secret managers, or databases).
"""

# Mock Personal Access Token (PAT) database.
# In production, use a secure authentication provider or database.
PAT_DB: dict[str, str] = {"valid_pat": "user123"}

# Secret key used for JWT signing and encryption mechanisms.
# ⚠️ In production, store this securely (e.g., environment variable or secret manager).
SECRET_KEY: str = "super_secret_key"

# In-memory store to track the status of requests.
# This is ephemeral and resets whenever the server restarts.
# In production, use a persistent storage like Redis or a database.
status_store: dict[str, str] = {}
