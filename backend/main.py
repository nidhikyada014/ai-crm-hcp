from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import SessionLocal, Base, engine
import models

from pydantic import BaseModel

# ✅ IMPORT LANGGRAPH AGENT
from agent import app_graph

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# DB Dependency
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =========================
# SCHEMA
# =========================
class InteractionInput(BaseModel):
    hcp_name: str
    interaction_type: str
    notes: str

# =========================
# HOME
# =========================
@app.get("/")
def home():
    return {"message": "Backend working!"}

@app.post("/agent")
def run_agent(data: dict):
    return app_graph.invoke({"input": data["input"]})

# =========================
# TOOL 1: LOG INTERACTION
# =========================
@app.post("/log-interaction")
def log_interaction(data: InteractionInput, db: Session = Depends(get_db)):
    summary = f"Summary: {data.notes}"

    new_entry = models.Interaction(
        hcp_name=data.hcp_name,
        interaction_type=data.interaction_type,
        notes=data.notes,
        summary=summary
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return {"message": "Interaction logged", "id": new_entry.id}

# =========================
# TOOL 2: GET ALL
# =========================
@app.get("/interactions")
def get_all(db: Session = Depends(get_db)):
    return db.query(models.Interaction).all()

# =========================
# TOOL 3: EDIT INTERACTION
# =========================
@app.put("/edit-interaction/{id}")
def edit_interaction(id: int, data: InteractionInput, db: Session = Depends(get_db)):
    record = db.query(models.Interaction).filter(models.Interaction.id == id).first()

    if not record:
        raise HTTPException(status_code=404, detail="Not found")

    record.hcp_name = data.hcp_name
    record.interaction_type = data.interaction_type
    record.notes = data.notes
    record.summary = f"Updated Summary: {data.notes}"

    db.commit()

    return {"message": "Updated successfully"}

# =========================
# TOOL 4: DELETE INTERACTION
# =========================
@app.delete("/delete-interaction/{id}")
def delete_interaction(id: int, db: Session = Depends(get_db)):
    record = db.query(models.Interaction).filter(models.Interaction.id == id).first()

    if not record:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(record)
    db.commit()

    return {"message": "Deleted successfully"}

# =========================
# TOOL 5: LANGGRAPH AI AGENT
# =========================
@app.post("/ai-agent")
def ai_agent(data: dict):
    """
    This endpoint connects your frontend to LangGraph agent.
    It decides which tool to call and returns result.
    """

    result = app_graph.invoke({
        "input": data["input"]
    })

    return result
