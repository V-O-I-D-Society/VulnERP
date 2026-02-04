# =========================================
# Fake session storage (INTENTIONALLY WEAK)
# =========================================

ACTIVE_SESSIONS = {}

# ----------------------------
# Create Session
# ----------------------------
def create_session(user):
    """
    🔴 Predictable session ID
    🔴 No randomness
    🔴 No expiry
    🔴 Stores mutable user object
    """

    # attacker can guess: session-1, session-2 ...
    session_id = f"session-{user.user_id}"

    # storing full user object (dangerous)
    ACTIVE_SESSIONS[session_id] = user

    return session_id


# ----------------------------
# Get user from session
# ----------------------------
def get_user_from_session(session_id):
    """
    🔴 No validation
    🔴 No expiration
    🔴 Trusts session blindly
    """
    return ACTIVE_SESSIONS.get(session_id)


# ----------------------------
# Destroy session
# ----------------------------
def destroy_session(session_id):
    """
    🔴 No ownership check
    Any user can log out any other user
    """
    if session_id in ACTIVE_SESSIONS:
        del ACTIVE_SESSIONS[session_id]


# ----------------------------
# Session Fixation Helper
# ----------------------------
def inject_session(session_id, user):
    """
    🔴 Allows overwriting existing sessions
    Useful for session fixation demos
    """
    ACTIVE_SESSIONS[session_id] = user
