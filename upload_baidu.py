"""Upload generated PDFs to Baidu Pan using bypy."""

import json
import os
import threading


def _ensure_token():
    """Load bypy token from BYPY_TOKEN env var if the file doesn't exist."""
    token_path = os.path.expanduser("~/.bypy/bypy.json")
    if os.path.exists(token_path):
        return True

    token_env = os.getenv("BYPY_TOKEN")
    if not token_env:
        return False

    try:
        os.makedirs(os.path.dirname(token_path), exist_ok=True)
        # Support both raw JSON and base64-encoded token
        if token_env.startswith("{"):
            token_data = json.loads(token_env)
        else:
            import base64
            token_data = json.loads(base64.b64decode(token_env))

        with open(token_path, "w") as f:
            json.dump(token_data, f)
        print(f"[Baidu] Token loaded from BYPY_TOKEN env var")
        return True
    except Exception as e:
        print(f"[Baidu] Failed to load token from env: {e}")
        return False


def is_bypy_authorized():
    """Check if bypy has been authorized."""
    _ensure_token()
    token_path = os.path.expanduser("~/.bypy/bypy.json")
    return os.path.exists(token_path)


def upload_to_baidu(local_path, remote_dir="/apps/youtube-english-learner"):
    """
    Upload a file to Baidu Pan.

    Args:
        local_path: Path to the local file
        remote_dir: Remote directory on Baidu Pan (default: /apps/youtube-english-learner)

    Returns:
        True if upload succeeded, False otherwise
    """
    try:
        _ensure_token()
        from bypy import ByPy

        bp = ByPy(verbose=0)
        filename = os.path.basename(local_path)
        remote_path = f"{remote_dir}/{filename}"

        print(f"[Baidu] Uploading {filename} to {remote_dir}...")
        result = bp.upload(local_path, remote_path)

        if result == 0:
            print(f"[Baidu] Upload success: {remote_path}")
            return True
        else:
            print(f"[Baidu] Upload failed with code: {result}")
            return False

    except Exception as e:
        print(f"[Baidu] Upload error: {e}")
        return False


def upload_async(local_path, remote_dir="/apps/youtube-english-learner"):
    """Upload file in a background thread (non-blocking)."""
    t = threading.Thread(
        target=upload_to_baidu,
        args=(local_path, remote_dir),
        daemon=True,
    )
    t.start()
    return t
