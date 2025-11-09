# Mini CRM System

Alright so this is a small CRM thing I built using **FastAPI** and **SQLite**.
It’s like one of those customer management tools where you can keep track of leads, log calls or emails, and check some basic stats.
Nothing crazy, just a simple setup that actually works (most of the time).

---

## Features

### Lead Stuff

* You can add, edit, delete, and look up leads
* Track where they’re at (New, Interested, In Progress, etc)
* Basic info like name, company, email, phone
* You can also filter and search

### Interaction Stuff

* Log when you call, email, or meet someone
* Each lead has their own little history
* You can filter by interaction type

### Reports (aka random stats)

* See how many leads are in each status
* Count how many calls/emails/meetings you’ve logged
* There’s a dashboard thing too
* Shows top companies (aka who you talk to the most)

---

## Folder Setup

```
mini-crm/
├── main.py                 # main FastAPI app
├── database.py             # database setup
├── models.py               # models for SQLAlchemy
├── schemas.py              # pydantic schemas
├── routers/
│   ├── leads.py            # all lead endpoints
│   ├── interactions.py     # all interaction endpoints
│   └── reports.py          # all reporting endpoints
├── requirements.txt         # dependencies
└── README.md               # this file
```

---

## How to Run

### Step 1. make a folder

```bash
mkdir mini-crm
cd mini-crm
```

### Step 2. make a venv

```bash
python -m venv venv
source venv/bin/activate  # windows: venv\Scripts\activate
```

### Step 3. install stuff

```bash
pip install -r requirements.txt
```

### Step 4. setup routers

```bash
mkdir routers
touch routers/__init__.py  # windows: type nul > routers\__init__.py
```

---

## Run It

```bash
python main.py
```

or

```bash
uvicorn main:app --reload
```

then go to [http://localhost:8000](http://localhost:8000)

---

## API Docs

FastAPI gives you docs automatically which is honestly the best part:

* Swagger → [http://localhost:8000/docs](http://localhost:8000/docs)
* ReDoc → [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Endpoints

### Leads

| Method | Endpoint      | What it does  |
| ------ | ------------- | ------------- |
| POST   | `/leads/`     | add new lead  |
| GET    | `/leads/`     | get all leads |
| GET    | `/leads/{id}` | get one lead  |
| PUT    | `/leads/{id}` | update a lead |
| DELETE | `/leads/{id}` | delete a lead |

**filters you can use:**
`name`, `company`, `status`, `skip`, `limit`

**status values:**
New, Interested, In Progress, Closed, Lost

---

### Interactions

| Method | Endpoint             | What it does  |
| ------ | -------------------- | ------------- |
| POST   | `/interactions/`     | log a new one |
| GET    | `/interactions/`     | list all      |
| GET    | `/interactions/{id}` | get one       |
| DELETE | `/interactions/{id}` | delete one    |

**types:** Call, Email, Meeting

---

### Reports

| Method | Endpoint                        | What it does                  |
| ------ | ------------------------------- | ----------------------------- |
| GET    | `/reports/leads-by-status`      | see how many leads per status |
| GET    | `/reports/interactions-summary` | count interactions by type    |
| GET    | `/reports/dashboard`            | everything at once            |

---

## Example Commands

### create a lead

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

### get all leads

```bash
curl "http://localhost:8000/leads/"
```

### filter by status

```bash
curl "http://localhost:8000/leads/?status=Interested"
```

### update a lead

```bash
curl -X PUT "http://localhost:8000/leads/1" \
  -H "Content-Type: application/json" \
  -d '{"status": "In Progress"}'
```

### log an interaction

```bash
curl -X POST "http://localhost:8000/interactions/" \
  -H "Content-Type: application/json" \
  -d '{
    "lead_id": 1,
    "interaction_type": "Call",
    "notes": "talked about pricing"
  }'
```

---

## Database

It uses **SQLite** (because it’s easy).
When you run it for the first time, it makes a file called `crm.db`.

**Tables:**

* `leads` → stores leads
* `interactions` → logs calls/emails/meetings

---

## Dev Notes

If you want to add new stuff:

1. Add the model in `models.py`
2. Add the schema in `schemas.py`
3. Make a new router in `routers/`
4. Import it in `main.py`

### Testing

```bash
pip install pytest httpx
pytest
```

Not gonna lie I didn’t write a ton of tests but it runs fine.

---

## Error Codes

* 200 → OK
* 201 → Created
* 204 → Deleted successfully
* 400 → Bad request (usually bad data)
* 404 → Not found
* 422 → Validation error

---

## Future Stuff (if I ever get to it)

* [ ] JWT auth (so people can log in)
* [ ] Email notifications
* [ ] Upload files to leads
* [ ] More filters
* [ ] Export to CSV or Excel
* [ ] Simple front-end UI
* [ ] Timeline view
* [ ] Assign leads to users
