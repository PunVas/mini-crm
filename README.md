# Mini CRM System

A lightweight Customer Relationship Management (CRM) system built with FastAPI and SQLite.

## Features

✅ **Lead Management**
- Create, read, update, and delete customer leads
- Track lead status (New, Interested, In Progress, Closed, Lost)
- Store contact information (name, company, email, phone)
- Search and filter leads by name, company, or status

✅ **Interaction Logging**
- Log calls, emails, and meetings with leads
- Track interaction history for each lead
- Filter interactions by type or lead

✅ **Reporting & Analytics**
- View leads grouped by status
- Analyze interaction types
- Dashboard with comprehensive statistics
- Top companies by lead count

## Project Structure

```
mini-crm/
├── main.py                 # FastAPI application entry point
├── database.py            # Database configuration
├── models.py              # SQLAlchemy models
├── schemas.py             # Pydantic schemas
├── routers/
│   ├── __init__.py
│   ├── leads.py           # Lead endpoints
│   ├── interactions.py    # Interaction endpoints
│   └── reports.py         # Reporting endpoints
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Installation

1. **Clone or create the project directory:**
```bash
mkdir mini-crm
cd mini-crm
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Create the routers directory:**
```bash
mkdir routers
touch routers/__init__.py  # On Windows: type nul > routers\__init__.py
```

## Running the Application

Start the server:
```bash
python main.py
```

Or use uvicorn directly:
```bash
uvicorn main:app --reload
```

The API will be available at: `http://localhost:8000`

## API Documentation

Interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Leads

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/leads/` | Create a new lead |
| GET | `/leads/` | Get all leads (with filters) |
| GET | `/leads/{id}` | Get a specific lead |
| PUT | `/leads/{id}` | Update a lead |
| DELETE | `/leads/{id}` | Delete a lead |

**Query Parameters for GET /leads/:**
- `name`: Filter by name (partial match)
- `status`: Filter by status (exact match)
- `company`: Filter by company (partial match)
- `skip`: Pagination offset (default: 0)
- `limit`: Pagination limit (default: 100)

**Valid Status Values:**
- New
- Interested
- In Progress
- Closed
- Lost

### Interactions

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/interactions/` | Log a new interaction |
| GET | `/interactions/` | Get all interactions (with filters) |
| GET | `/interactions/{id}` | Get a specific interaction |
| DELETE | `/interactions/{id}` | Delete an interaction |

**Valid Interaction Types:**
- Call
- Email
- Meeting

### Reports

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/reports/leads-by-status` | Count of leads by status |
| GET | `/reports/interactions-summary` | Count of interactions by type |
| GET | `/reports/dashboard` | Comprehensive dashboard data |

## Usage Examples

### Create a Lead
```bash
curl -X POST "http://localhost:8000/leads/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "company": "Tech Corp",
    "email": "john@techcorp.com",
    "phone": "+1234567890",
    "status": "New"
  }'
```

### Get All Leads
```bash
curl "http://localhost:8000/leads/"
```

### Filter Leads by Status
```bash
curl "http://localhost:8000/leads/?status=Interested"
```

### Update Lead Status
```bash
curl -X PUT "http://localhost:8000/leads/1" \
  -H "Content-Type: application/json" \
  -d '{"status": "In Progress"}'
```

### Log an Interaction
```bash
curl -X POST "http://localhost:8000/interactions/" \
  -H "Content-Type: application/json" \
  -d '{
    "lead_id": 1,
    "interaction_type": "Call",
    "notes": "Discussed product features and pricing"
  }'
```

### Get Dashboard Report
```bash
curl "http://localhost:8000/reports/dashboard"
```

## Database

The application uses SQLite with a file named `crm.db` created automatically on first run.

**Tables:**
- `leads`: Stores customer lead information
- `interactions`: Stores interaction logs linked to leads

## Development

### Adding New Features

1. **Add a new model** in `models.py`
2. **Create corresponding schema** in `schemas.py`
3. **Create router** in `routers/` directory
4. **Include router** in `main.py`

### Running Tests

You can add tests using pytest:
```bash
pip install pytest httpx
pytest
```

## Error Handling

The API returns appropriate HTTP status codes:
- `200`: Success
- `201`: Created
- `204`: No Content (successful deletion)
- `400`: Bad Request (validation error, duplicate email)
- `404`: Not Found
- `422`: Unprocessable Entity (validation error)

## Future Enhancements

- [ ] Authentication & Authorization (JWT)
- [ ] Email notifications
- [ ] File attachments for leads
- [ ] Advanced search with multiple filters
- [ ] Export data to CSV/Excel
- [ ] Frontend dashboard UI
- [ ] Activity timeline for each lead
- [ ] Lead assignment to sales reps

## License

MIT License - Feel free to use and modify as needed!