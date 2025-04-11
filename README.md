# AgentScape: White Pages for Agents

## Overview
This project is a FastAPI application that serves as a registry for agents, providing functionalities to register, list, and retrieve agent details. It is designed to be compatible with MCP.

## Project Structure
```
agentscape/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── agents.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── init_db.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── agent.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   └── manifest.py
│   └── services/
│       ├── __init__.py
│       └── agent_service.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_agents.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup Instructions
1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd agentscape
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```
   uvicorn app.main:app --reload
   ```

## Usage
- **Register an Agent:** POST `/agents`
- **List Agents:** GET `/agents`
- **Get Agent Details:** GET `/agents/{agent_id}`
- **Register from Manifest:** POST `/agents/from-manifest`

## Testing
To run the tests, use:
```
pytest
```

## License
This project is licensed under the MIT License. See the LICENSE file for details.