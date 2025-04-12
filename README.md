# AgentScape: An Open and Lightweight Directory for AI Agents

## Overview
This project is a FastAPI application that serves as a registry for agents, providing functionalities to register, list, and retrieve agent details.

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

## License
This project is licensed under the MIT License. See the LICENSE file for details.