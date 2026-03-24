from fastapi import FastAPI

app = FastAPI(
    title="Éditeur Malagasy — Backend IA",
    description="API FastAPI exposant les modules NLP pour le Malagasy.",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "backend-python"}


# ─── Routes (à compléter) ─────────────────────────────────────────
# from app.routes import spellcheck, lemmatize, autocomplete, translate, tts, ner, sentiment, chat
# app.include_router(spellcheck.router)
# app.include_router(lemmatize.router)
# app.include_router(autocomplete.router)
# app.include_router(translate.router)
# app.include_router(tts.router)
# app.include_router(ner.router)
# app.include_router(sentiment.router)
# app.include_router(chat.router)
