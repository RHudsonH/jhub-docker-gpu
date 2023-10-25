from flask import (
    Blueprint, current_app
)
from hwalloc.db import get_db

bp = Blueprint('healthz', __name__)

@bp.route('/healthz', methods=(['GET']))
def healthz():
    try:
        query = "SELECT 1"
        db = get_db()
        result = db.execute(
            'SELECT 1'
        ).fetchone()
        if result[0] == 1:
            return "Healthy", 200
    except Exception as e:
        current_app.logger.error(f"Health check failed: {e}")
        return "Unhealthy", 500