import csv
from io import TextIOWrapper
from app.database import db
from flask import jsonify
from sqlalchemy import text
from app.database import db

EXPECTED_COLUMNS = {
    "departments.csv": ["id", "department"],
    "jobs.csv": ["id", "job"],
    "hired_employees.csv": ["id", "name", "datetime", "department_id", "job_id"]
}
def clean_row(row: dict, expected_columns: list) -> dict:
    """
    Cleans a row by converting empty strings to None for integer fields.
    
    Args:
        row (dict): A dictionary representing a row from the CSV file.
        expected_columns (list): List of expected column names.

    Returns:
        dict: Cleaned row with empty values replaced by None.
    """
    cleaned_row = {}
    for key in expected_columns:
        value = row.get(key, "").strip()

        if value == "" and key in ["id", "department_id", "job_id"]:
            cleaned_row[key] = None
        else:
            cleaned_row[key] = value
    return cleaned_row

def save_csv_to_db(file: object, model: type, filename: str) -> object:
    """
    Inserts CSV data into the database in batch transactions, assuming files have no headers.
    
    Args:
        file (object): The uploaded CSV file.
        model (type): The SQLAlchemy model corresponding to the table.
        filename (str): The name of the uploaded file to determine column mapping.

    Returns:
        JSON response with success or error message.
    """
    wrapper = TextIOWrapper(file, encoding='utf-8')
    reader = csv.reader(wrapper)
    expected_columns = EXPECTED_COLUMNS.get(filename)

    if expected_columns is None:
        return jsonify({'error': 'Invalid file type'}), 400

    reader = (dict(zip(expected_columns, row)) for row in reader)
    batch_size = 1000
    data_batch = []

    try:
        for row in reader:
            cleaned_row = clean_row(row, expected_columns)
            data_batch.append(cleaned_row)

            if len(data_batch) >= batch_size:
                db.session.bulk_insert_mappings(model, data_batch)
                db.session.commit()
                data_batch.clear()
        
        if data_batch:
            db.session.bulk_insert_mappings(model, data_batch)
            db.session.commit()
        
        return jsonify({'message': 'File processed successfully'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


def get_employees_per_quarter() -> list:
    """
    Retrieves the number of employees hired per quarter, grouped by department and job.

    Returns:
        List response with aggregated hiring data per quarter.
    """

    query = text("""
        SELECT 
            d.department AS department,
            j.job AS job,
            SUM(CASE WHEN EXTRACT(QUARTER FROM CAST(NULLIF(h.datetime, '') AS TIMESTAMP)) = 1 THEN 1 ELSE 0 END) AS Q1,
            SUM(CASE WHEN EXTRACT(QUARTER FROM CAST(NULLIF(h.datetime, '') AS TIMESTAMP)) = 2 THEN 1 ELSE 0 END) AS Q2,
            SUM(CASE WHEN EXTRACT(QUARTER FROM CAST(NULLIF(h.datetime, '') AS TIMESTAMP)) = 3 THEN 1 ELSE 0 END) AS Q3,
            SUM(CASE WHEN EXTRACT(QUARTER FROM CAST(NULLIF(h.datetime, '') AS TIMESTAMP)) = 4 THEN 1 ELSE 0 END) AS Q4
        FROM hired_employee h
        JOIN department d ON h.department_id = d.id
        JOIN job j ON h.job_id = j.id
        GROUP BY d.department, j.job
        ORDER BY d.department, j.job;
    """)

    result = db.session.execute(query)

    
    columns = result.keys()
    return [dict(zip(columns, row)) for row in result]

def get_departments_above_mean() -> list:
    """
    Retrieves the departments adove mean.

    Returns:
        List response with query response.
    """

    query = text("""
        WITH department_hiring AS (
            SELECT department_id, COUNT(*) AS hired_count
            FROM hired_employee
            WHERE EXTRACT(YEAR FROM CAST(NULLIF(datetime, '') AS TIMESTAMP)) = 2021
            GROUP BY department_id
        ), avg_hiring AS (
            SELECT AVG(hired_count) AS avg_hires FROM department_hiring
        )
        SELECT d.id, d.department, dh.hired_count AS hired
        FROM department_hiring dh
        JOIN department d ON dh.department_id = d.id
        WHERE dh.hired_count > (SELECT avg_hires FROM avg_hiring)
        ORDER BY dh.hired_count DESC;
    """)
    result = db.session.execute(query)

    
    columns = result.keys()
    return [dict(zip(columns, row)) for row in result]