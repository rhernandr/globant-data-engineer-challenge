from flask import request, jsonify
from app.models import Department, Job, HiredEmployee
from app.services import save_csv_to_db
from app.routes import upload_blueprint

@upload_blueprint.route('/upload_csv', methods=['POST'])
def upload_csv() -> object:
    """
    Endpoint to upload a CSV file and insert its data into the database.
    
    Assumes that the uploaded CSV files do not contain headers.

    Returns:
        JSON response with success or error message.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    filename = file.filename.lower()

    model_mapping = {
        'departments.csv': Department,
        'jobs.csv': Job,
        'hired_employees.csv': HiredEmployee
    }

    if filename not in model_mapping:
        return jsonify({'error': 'Invalid file type'}), 400

    return save_csv_to_db(file, model_mapping[filename], filename)