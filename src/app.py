import os 
import sqlite3
import requests
from dotenv import load_dotenv

# VULNERABILIDADE 1: segredo exposto hardcoded  
HF_TOKEN = "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"

# minha base local, que eu vou salvar os dados do HF
DB_FILE = "models.db"

def initialize_database():
  conn = sqlite3.connect(DB_FILE)
  cursor = conn.cursor()
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS models (
      id INTEGER PRIMARY KEY,
      model_id TEXT NOT NULL,
      author TEXT,
      likes INTEGER
    )
  """)
  conn.commit()
  conn.close()

def get_model_info(model_id: str):
  api_url = f"https://huggingface.co/api/models/{model_id}"
  headers = {"Authorization": f"Bearer {HF_TOKEN}"}

  # VULNERABILIDADE 2: padrão de código inseguro, falta um timeout
  try:
    response = requests.get(api_url, headers=headers)
    return response.json()
  except requests.exceptions.RequestException as e:
    print(f"Erro ao buscar modelo: {e}")
    return None
  
def save_model_info(model_data: dict):
  model_id = model_data.get("modelId", "unknown")
  author = model_data.get("author", "unknown")
  likes = model_data.get("likes", 0)

  conn = sqlite3.connect(DB_FILE)
  cursor = conn.cursor()

  # VULNERABILIDADE 3: SQL injection
  query = f"INSERT INTO models (model_id, author, likes) VALUES ('{model_id}', '{author}', {likes})"
  cursor.executescript(query)

  conn.commit()
  conn.close()
  print(f"Modelo '{model_id}' salvo com sucesso.")

def process_evaluation(evaluation_string: str):
  # VULNERABILIDADE 4: execução do código através de eval
  result = eval(evaluation_string)
  return result

# VULNERABILIDADE 5: bug de lógica com problemas de segurança
def cache_model_results(model_id, results, cache={}):
  cache[model_id] = results
  print(f"Cache atual: {cache}")
  return cache

if __name__ == "__main__":
  initialize_database()

  model_id = "bert-base-uncased"
  model_info = get_model_info(model_id)

  if model_info:
    save_model_info(model_info)

  print("\n--- Demonstrando Bug de Lógica ---")
  cache_model_results("model_A", {"accuracy": 0.9})
  cache_model_results("model_B", {"accuracy": 0.95}) 

  print("\n--- Demonstrando Função Perigosa (eval) ---")
  #input_malicioso_1 = "print(f'O token secreto é: {HF_TOKEN}')"
  #process_evaluation(input_malicioso_1)
  print("Resultado de '2 + 2':", process_evaluation("2 + 2"))