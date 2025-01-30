from flask import jsonify
from app.services import get_employees_per_quarter, get_departments_above_mean
from app.routes import metrics_blueprint

@metrics_blueprint.route('/employees_per_quarter', methods=['GET'])
def employees_per_quarter() -> object:
    """
    Retrieves the number of employees hired per quarter, grouped by department and job.

    Returns:
        JSON response with aggregated hiring data per quarter.
    """
    return jsonify(get_employees_per_quarter())

@metrics_blueprint.route('/departments_above_mean', methods=['GET'])
def departments_above_mean() -> object:
    """
    Retrieves departments that have hired more employees than the average hiring across all departments.

    Returns:
        JSON response with departments above the mean hiring rate.
    """
    return jsonify(get_departments_above_mean())
