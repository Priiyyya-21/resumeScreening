import os
import sqlite3
from flask import Flask,request,jsonify
from werkzeug.utils import secure_filename
from resume_parser import parse_resume


app=Flask(__name__)

UPLOAD_FOLDER="uploads"
os.makedir(UPLOAD_FOLDER,exist_ok = True)

#Database Connection
def get_db_connection():
    conn=sqlite3.connect("database/resumes.db")
    conn.row_factory=sqlite3.Row
    return conn

@app.route("/upload",method=["POST"])
def upload_resume():
    """Upload a resume and extract the details"""
    if "file" not in request.files:
        return jsonify({"error":"No file uploaded"}),400 


    file=request.files["file"]
    filename=secure_filename(file.filename)
    filepath=os.path.join(UPLOAD_FOLDER,filename)
    file.save(filepath)

    resume_data = parse_resume(filepath)

    #Insert into database

    conn=get_db_connection()
    cursor= conn.cursor()
    cursor.execute("""
        INSERT INTO resumes (name, email, phone, skills, text) 
        VALUES (?, ?, ?, ?, ?)
    """, (filename, resume_data["email"], resume_data["phone"], resume_data["skills"], resume_data["text"]))
    
    conn.commit()
    conn.close()
    return jsonify({"message": "Resume uploaded successfully", "data": resume_data}), 201

@app.route("/resumes",methods=["GET"])
def get_resumes():
    """Fetch all resumes from the database"""
    conn=get_db_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM resumes")
    resumes=cursor.fetchall()
    conn.close()

    return jsonify([dict(row) for row in resumes])


if __name__ == "__main__":
    app.run(debug=True)