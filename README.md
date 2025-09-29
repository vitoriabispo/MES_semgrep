# 🛡️ Demonstração da utilização do Semgrep 🛡️
- Esse experimento foi desenvolvido para compreender os pontos fortes do Semgrep e como ele pode auxiliar na descoberta de vulnerabilidades em projetos de software. O script `app.py` foi implementado com vulnerabilidades intencionais para que o Semgrep possa detetá-las.
---

## ⚙️ 1. Configuração e Execução do Projeto
**1. Crie o Ambiente Virtual**

   Navegue para a pasta do projeto e crie um ambiente virtual Python.
```bash
    python -m venv venv
```

**2. Ative o Ambiente Virtual**
- Windows
 ```bash
    .\venv\Scripts\Activate.ps1
```
- Linux
```bash
    source venv/bin/activate
```

**3. Instale as Dependências**
   
   Navege para a pasta ```src``` do repositório e execute:
```bash
    pip install -r requirements.txt
```

**4. Execute a Aplicação**
```bash
    python app.py
```
----
## 🔍 2. Análise com Semgrep
Para garantir uma análise consistente e contornar problemas de rede ou de cache, utilizou-se o Semgrep através do Docker e as regras foram fornecidas localmente.

**1. Clone o repositório de regras do Semgrep**
  
   Na raíz do repositório, execute:
```bash
    git clone https://github.com/semgrep/semgrep-rules.git

```
**2. Execute a análise via Docker**
```bash
    cd src
    docker run --rm -v "${pwd}:/src" -v "../semgrep-rules:/regras" semgrep/semgrep semgrep scan --config "/regras/python" --config "/regras/generic" --config "/src/rules.yml" /src

```
----
## 🚩 3. Vulnerabilidades
**VULNERABILIDADE 1: Segredo hardcoded**
- *Problema*: Uma informação sensível (o token da API `HF_TOKEN`) está escrita diretamente no código-fonte.
- *Risco*: Qualquer pessoa com acesso ao código pode roubar esta credencial.
- *Solução*: Mover o segredo para um arquivo `.env` e carregá-lo como uma variável de ambiente.
- *Detecção*: Encontrada pelas regras do conjunto `generic/secrets`.

**VULNERABILIDADE 2: Padrão de código inseguro**
- *Problema*: A chamada à API externa com a biblioteca requests não define um tempo limite de espera.
- *Risco*: Se a API do Hugging Face estiver indisponível, a aplicação pode ficar "congelada" indefinidamente, causando uma Negação de Serviço (DoS).
- *Solução*: Adicionar um parâmetro `timeout` à chamada `requests.get()`.
- *Detecção*: Encontrada pela nossa regra personalizada em `rules.yml` e também pela regra comunitária `python.requests.best-practice.use-timeout`.

**VULNERABILIDADE 3: SQL Injection**
- *Problema*: Os dados externos são inseridos diretamente na query do banco de dados através da formatação de uma string.
- *Risco*: Um atacante pode fornecer uma entrada maliciosa (ex: `'; DROP TABLE models; --"`) para manipular ou destruir o banco de dados. O uso de `cursor.executescript` agrava o risco.
- *Solução*: Usar consultas parametrizadas, passando os valores como um tuplo separado do comando SQL (ex: `cursor.execute(query, (var1, var2))`).
- *Detecção*: Encontrada pelas regras do conjunto `python/lang/security`.

**VULNERABILIDADE 4: Execução de código remoto**
- *Problema*: A função `eval(`) executa qualquer texto como se fosse um comando Python.
- *Risco*: Esta é uma vulnerabilidade crítica. Se um atacante controlar a entrada da função, ele pode executar qualquer comando no servidor, obtendo controlo total sobre a máquina.
- *Solução*: `eval()` por uma alternativa segura e específica, como `ast.literal_eval`, que avalia apenas estruturas de dados literais (listas, dicionários, etc.) e não executa código.
- *Detecção*: Encontrada pelas regras do conjunto `python/lang/security`.

**VULNERABILIDADE 5: Bug de lógica com implicações de segurança**
- *Problema*:  A função `cache_model_results` usa um dicionário mutável (`{}`) como valor padrão para um argumento.
- *Risco*: O mesmo dicionário é partilhado entre todas as chamadas à função, causando bugs e permitindo que os dados de um utilizador vazem para o cache de outro num ambiente multi-utilizador.
- *Solução*: Usar `None` como valor padrão e criar um novo dicionário dentro da função se o argumento não for fornecido.
- *Detecção*: Encontrada pelas regras do conjunto `python/lang/correctness`.
