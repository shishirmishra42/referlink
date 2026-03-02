from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import sys
sys.path.append("../db")
from db.db_connect import get_connection

app = FastAPI()

@app.post("/create_job")
async def create_job(request: Request):
    data = await request.json()
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Jobs (company, job_title, skills, bonus) VALUES (%s, %s, %s, %s)",
            (data["company"], data["job_title"], data["skills"], data["bonus"])
        )
        conn.commit()
        cur.close()
        conn.close()
        return JSONResponse(content={"message": "Job posted successfully", "data": data})
    except Exception as e:
        return JSONResponse(content={"message": f"Failed to post job: {e}"}, status_code=500)

@app.post("/request_referral")
async def request_referral(request: Request):
    data = await request.json()
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Referrals (job_id, referrer_id) VALUES (%s, %s)",
            (data["job_id"], data["referrer_id"])
        )
        conn.commit()
        cur.close()
        conn.close()
        return JSONResponse(content={"message": "Referral requested successfully", "data": data})
    except Exception as e:
        return JSONResponse(content={"message": f"Failed to request referral: {e}"}, status_code=500)

@app.get("/filter_candidates")
def filter_candidates(score: int):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, score FROM Candidates WHERE score >= %s", (score,))
        candidates = [
            {"id": row[0], "name": row[1], "score": row[2]} for row in cur.fetchall()
        ]
        cur.close()
        conn.close()
        return {"candidates": candidates}
    except Exception as e:
        return JSONResponse(content={"message": f"Failed to filter candidates: {e}"}, status_code=500)

@app.post("/add_work_history")
async def add_work_history(request: Request):
    data = await request.json()
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO WorkHistory (company, position, years) VALUES (%s, %s, %s)",
            (data["company"], data["position"], data["years"])
        )
        conn.commit()
        cur.close()
        conn.close()
        return JSONResponse(content={"message": "Work history added successfully", "data": data})
    except Exception as e:
        return JSONResponse(content={"message": f"Failed to add work history: {e}"}, status_code=500)

@app.get("/jobs")
def get_jobs():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, company, job_title, skills, bonus FROM Jobs")
        jobs = [
            {"id": row[0], "company": row[1], "job_title": row[2], "skills": row[3], "bonus": row[4]} for row in cur.fetchall()
        ]
        cur.close()
        conn.close()
        return {"jobs": jobs}
    except Exception as e:
        return JSONResponse(content={"message": f"Failed to load jobs: {e}"}, status_code=500)

@app.post("/add_skill")
async def add_skill(request: Request):
    data = await request.json()
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Skills (skill) VALUES (%s)",
            (data["skill"],)
        )
        conn.commit()
        cur.close()
        conn.close()
        return JSONResponse(content={"message": "Skill added successfully", "data": data})
    except Exception as e:
        return JSONResponse(content={"message": f"Failed to add skill: {e}"}, status_code=500)

@app.get("/track_application/{application_id}")
def track_application(application_id: int):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT status FROM Applications WHERE id = %s", (application_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row:
            return {"status": row[0]}
        else:
            return JSONResponse(content={"message": "Application not found"}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"message": f"Failed to track application: {e}"}, status_code=500)

@app.post("/submit_application")
async def submit_application(request: Request):
    data = await request.json()
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Applications (status) VALUES (%s) RETURNING id",
            (data["status"],)
        )
        app_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return JSONResponse(content={"message": "Application submitted successfully", "application_id": app_id})
    except Exception as e:
        return JSONResponse(content={"message": f"Failed to submit application: {e}"}, status_code=500)

@app.post("/update_referral_score")
async def update_referral_score(request: Request):
    data = await request.json()
    try:
        conn = get_connection()
        cur = conn.cursor()
        # Example: update score for a referrer by id
        cur.execute(
            "UPDATE Candidates SET score = score + 1 WHERE id = %s",
            (data["referrer_id"],)
        )
        conn.commit()
        cur.close()
        conn.close()
        return JSONResponse(content={"message": "Referral score updated successfully"})
    except Exception as e:
        return JSONResponse(content={"message": f"Failed to update referral score: {e}"}, status_code=500)

@app.get("/referral_requests")
def referral_requests():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, job_id, referrer_id, status FROM Referrals")
        referrals = [
            {"id": row[0], "job_id": row[1], "referrer_id": row[2], "status": row[3]} for row in cur.fetchall()
        ]
        cur.close()
        conn.close()
        return {"referrals": referrals}
    except Exception as e:
        return JSONResponse(content={"message": f"Failed to load referral requests: {e}"}, status_code=500)

@app.post("/approve_referral")
async def approve_referral(request: Request):
    data = await request.json()
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE Referrals SET status = 'approved' WHERE id = %s",
            (data["referral_id"],)
        )
        conn.commit()
        cur.close()
        conn.close()
        return JSONResponse(content={"message": "Referral approved successfully"})
    except Exception as e:
        return JSONResponse(content={"message": f"Failed to approve referral: {e}"}, status_code=500)

@app.post("/reject_referral")
async def reject_referral(request: Request):
    data = await request.json()
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE Referrals SET status = 'rejected' WHERE id = %s",
            (data["referral_id"],)
        )
        conn.commit()
        cur.close()
        conn.close()
        return JSONResponse(content={"message": "Referral rejected successfully"})
    except Exception as e:
        return JSONResponse(content={"message": f"Failed to reject referral: {e}"}, status_code=500)

@app.get("/bonus_status")
def bonus_status():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT status FROM Bonus LIMIT 1")
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row:
            return {"status": row[0]}
        else:
            return JSONResponse(content={"message": "Bonus status not found"}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"message": f"Failed to load bonus status: {e}"}, status_code=500)

@app.post("/update_bonus")
async def update_bonus(request: Request):
    data = await request.json()
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE Jobs SET bonus = %s WHERE job_id = %s",
            (data["bonus"], data["job_id"])
        )
        conn.commit()
        cur.close()
        conn.close()
        return JSONResponse(content={"message": "Bonus updated successfully"})
    except Exception as e:
        return JSONResponse(content={"message": f"Failed to update bonus: {e}"}, status_code=500)

