# Fake session storage (learning purpose)
ACTIVE_SESSIONS = {}


def create_session(user):
    session_id = f"session-{user.user_id}"
    ACTIVE_SESSIONS[session_id] = user
    return session_id


def get_user_from_session(session_id):
    return ACTIVE_SESSIONS.get(session_id)


def destroy_session(session_id):
    if session_id in ACTIVE_SESSIONS:
        del ACTIVE_SESSIONS[session_id]
