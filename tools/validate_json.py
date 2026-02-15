import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "quizzes" / "pop" / "build" / "quiz_pop.json"

def die(msg: str):
    raise SystemExit("ERRO: " + msg)

def main():
    if not FILE.exists():
        die("Arquivo build não existe ainda. Rode build_quiz.py primeiro.")

    try:
        data = json.loads(FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        die(f"JSON inválido: {e.msg} (linha {e.lineno}, coluna {e.colno})")

    for k in ("meta", "traits", "start", "questions", "results", "card"):
        if k not in data:
            die(f"Faltando chave obrigatória: {k}")

    if data["start"] not in data["questions"]:
        die("start aponta para uma pergunta que não existe em questions.")

    # valida o encadeamento das perguntas
    for qid, q in data["questions"].items():
        if "options" not in q:
            die(f"Pergunta '{qid}' sem 'options'.")
        for opt in q["options"]:
            nxt = opt.get("next")
            if nxt != "END" and nxt not in data["questions"]:
                die(f"Em '{qid}', opção '{opt.get('id')}' aponta next inválido: {nxt}")

    print("✅ JSON validado e consistente!")

if __name__ == "__main__":
    main()
