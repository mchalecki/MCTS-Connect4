# MCTS backend
Webserver written in Python FastAPI
## Requirements
python > 3.5 
## Running server
1. Instal requirements
```bash
pip install -r requirements.txt
```
2. Launch webserver
```bash
uvicorn server:app
```

### Dev setup
Main antrypoint is file connect4.py.
It either does compete_2_models or train_one_tree.
