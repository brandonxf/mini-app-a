import random
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(title="Trivia")

BASE = Path(__file__).parent

QUESTIONS = [
    {"q": "¿Cuál es la capital de Australia?", "options": ["Sídney", "Canberra", "Melbourne", "Perth"], "answer": 1},
    {"q": "¿Cuántos planetas tiene el Sistema Solar?", "options": ["7", "8", "9", "10"], "answer": 1},
    {"q": "¿Quién pintó la Mona Lisa?", "options": ["Miguel Ángel", "Rafael", "Leonardo da Vinci", "Botticelli"], "answer": 2},
    {"q": "¿Cuál es el océano más grande?", "options": ["Atlántico", "Índico", "Ártico", "Pacífico"], "answer": 3},
    {"q": "¿En qué año llegó el hombre a la Luna?", "options": ["1965", "1969", "1972", "1975"], "answer": 1},
    {"q": "¿Cuál es el elemento químico con símbolo 'Au'?", "options": ["Plata", "Aluminio", "Oro", "Argón"], "answer": 2},
    {"q": "¿Quién escribió 'Cien años de soledad'?", "options": ["Mario Vargas Llosa", "Gabriel García Márquez", "Julio Cortázar", "Pablo Neruda"], "answer": 1},
    {"q": "¿Cuál es el país más grande del mundo por superficie?", "options": ["China", "Canadá", "Estados Unidos", "Rusia"], "answer": 3},
    {"q": "¿Cuántos huesos tiene el cuerpo humano adulto?", "options": ["206", "180", "250", "300"], "answer": 0},
    {"q": "¿Qué lenguaje de programación creó Guido van Rossum?", "options": ["Ruby", "Python", "Java", "Perl"], "answer": 1},
    {"q": "¿Cuál es el río más largo de Sudamérica?", "options": ["Orinoco", "Paraná", "Amazonas", "Magdalena"], "answer": 2},
    {"q": "¿Qué gas respiramos principalmente para vivir?", "options": ["Nitrógeno", "Oxígeno", "Hidrógeno", "Dióxido de carbono"], "answer": 1},
]
for i, item in enumerate(QUESTIONS):
    item["id"] = i


class Answer(BaseModel):
    question_id: int
    choice: int


@app.get("/api/questions")
def get_questions(n: int = 5):
    """Devuelve n preguntas al azar, sin la respuesta correcta."""
    n = max(1, min(n, len(QUESTIONS)))
    picked = random.sample(QUESTIONS, n)
    return [{"id": p["id"], "q": p["q"], "options": p["options"]} for p in picked]


@app.post("/api/answer")
def check_answer(a: Answer):
    if not 0 <= a.question_id < len(QUESTIONS):
        raise HTTPException(404, "Pregunta no encontrada")
    correct = QUESTIONS[a.question_id]["answer"]
    return {"correct": a.choice == correct, "answer": correct}


@app.get("/")
def index():
    return FileResponse(BASE / "static" / "index.html")


app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")
