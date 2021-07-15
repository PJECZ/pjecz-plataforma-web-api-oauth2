"""
Main

Para arrancar ejecute `python main.py`
"""
import uvicorn


if __name__ == '__main__':
    uvicorn.run("plataforma_web.app:app", host="0.0.0.0", port=8001, reload=True)
