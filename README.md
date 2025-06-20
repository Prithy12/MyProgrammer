# MyProgrammer - AI-Powered Ideation Agent

An intelligent web application that transforms raw project ideas into structured, actionable requirements using OpenAI's GPT-4. Built with FastAPI, PostgreSQL, and a modern web interface.

## 🚀 Features

- **AI-Powered Ideation**: Transform raw ideas into structured project summaries
- **Context Enrichment**: Automatically identify missing context elements (target users, pain points, value propositions)
- **Requirements Generation**: Generate 5-10 high-level requirements organized by subdomains
- **Interactive Refinement**: Edit and refine individual requirements with AI assistance
- **Conversation Management**: Save, load, and manage multiple ideation sessions
- **Modern Web Interface**: Clean, responsive UI for seamless ideation workflow

## 🏗️ Architecture

- **Backend**: FastAPI with SQLModel for database operations
- **Database**: PostgreSQL with JSONB support for flexible data storage
- **AI Integration**: OpenAI GPT-4 for intelligent content generation
- **Frontend**: Vanilla HTML/CSS/JavaScript with real-time editing capabilities
- **Containerization**: Docker Compose for easy deployment

## 📋 Prerequisites

- Python 3.8+
- Docker and Docker Compose
- OpenAI API key
- PostgreSQL (handled via Docker)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/MyProgrammer.git
   cd MyProgrammer
   ```

2. **Set up environment variables**
   Create a `.env` file in the `ideation_agent` directory:
   ```bash
   cd ideation_agent
   touch .env
   ```
   
   Add the following variables:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   DATABASE_URL=postgresql://ideation:secret@localhost:5433/ideation
   ```

3. **Start the database**
   ```bash
   docker-compose up -d
   ```

4. **Install Python dependencies**
   ```bash
   cd ideation_agent
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Open the web interface**
   Navigate to `http://localhost:8080` in your browser and open `index.html`

## 🎯 Usage

### 1. Start Ideation
Enter your raw project idea in the text area and click "Start Ideation" to get an AI-generated summary.

### 2. Enrich Context
Click "Enrich Context" to identify missing pieces of context like target users, pain points, and value propositions.

### 3. Generate Requirements
Click "Draft Requirements" to generate 5-10 high-level requirements organized by subdomains.

### 4. Refine Requirements
- Edit requirements directly in the interface
- Click "Refine" on individual requirements for AI-powered improvements
- Organize requirements by subdomains

### 5. Save & Load
- Save your ideation session with a custom name
- Load previous sessions from the dropdown menu

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/ideate/start` | POST | Transform raw idea into summary |
| `/ideate/enrich` | POST | Enrich context with missing elements |
| `/ideate/draft` | POST | Generate structured requirements |
| `/ideate/refine` | POST | Refine individual requirements |
| `/ideate/save` | POST | Save conversation to database |
| `/ideate/list` | GET | List all saved conversations |
| `/ideate/load/{id}` | GET | Load specific conversation |

## 📁 Project Structure

```
MyProgrammer/
├── docker-compose.yml          # Database container configuration
├── ideation_agent/
│   ├── main.py                 # FastAPI application and endpoints
│   ├── models.py               # SQLModel database models
│   ├── db.py                   # Database connection and utilities
│   ├── requirements.txt        # Python dependencies
│   └── index.html              # Web interface
└── LICENSE                     # GNU GPL v3 license
```

## 🗄️ Database Schema

The application uses a single `Conversation` table with the following structure:

- `id`: Auto-increment primary key
- `name`: User-defined session name
- `summary`: 1-2 sentence project summary
- `context`: Enriched context text
- `draft`: Full requirements JSON blob (JSONB)
- `created_at`: Timestamp of creation

## 🔒 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |
| `DATABASE_URL` | PostgreSQL connection string | Yes |

## 🐳 Docker Deployment

The project includes Docker Compose configuration for easy database setup:

```bash
# Start database
docker-compose up -d

# Stop database
docker-compose down
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/) for high-performance API development
- Powered by [OpenAI GPT-4](https://openai.com/) for intelligent content generation
- Uses [SQLModel](https://sqlmodel.tiangolo.com/) for modern database operations
- Containerized with [Docker](https://www.docker.com/) for easy deployment

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub or contact the maintainers.

---

**MyProgrammer** - Transforming ideas into structured requirements with AI assistance. 