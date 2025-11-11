# PostgreSQL Migration Guide

## Overview

This guide helps you migrate from SQLite to PostgreSQL for persistent data storage on Streamlit Cloud.

## Why PostgreSQL?

- ✅ Data persists across app deployments
- ✅ Scales better with multiple users
- ✅ Industry standard for production apps
- ✅ Easy integration with Streamlit Cloud

---

## Option 1: Using Neon (Recommended for Streamlit Cloud)

**Neon** provides free PostgreSQL databases perfect for Streamlit Cloud apps.

### Setup Steps:

1. **Create a Neon Account**

   - Go to [https://neon.tech](https://neon.tech)
   - Sign up for a free account
   - Create a new project (e.g., "emotion-detection")

2. **Get Your Database URL**

   - In Neon dashboard, click your project
   - Copy the **Connection string** (looks like: `postgresql://user:password@host/dbname`)

3. **Add to Streamlit Cloud Secrets**

   - Go to your deployed app on Streamlit Cloud
   - Click ⚙️ → "Secrets"
   - Add:
     ```toml
     DATABASE_URL = "postgresql://user:password@neon.host/dbname"
     ```

4. **Update `requirements.txt`**
   - Add `psycopg2-binary>=2.9.0` (already included below)

---

## Option 2: Using AWS RDS

1. Create an RDS PostgreSQL database
2. Get the connection string from AWS RDS console
3. Add to Streamlit Cloud secrets (same as above)

---

## Option 3: Using Render Database (Alternative)

1. Visit [https://render.com](https://render.com)
2. Create a PostgreSQL database
3. Copy the connection string
4. Add to secrets

---

## Local Development with PostgreSQL

### Setup:

1. **Install PostgreSQL locally** (if not already installed)

   ```bash
   # macOS with Homebrew
   brew install postgresql
   brew services start postgresql
   ```

2. **Create a local database**

   ```bash
   psql postgres
   CREATE DATABASE emotion_app;
   \q
   ```

3. **Test the connection**

   ```bash
   psql -d emotion_app
   \dt  # List tables (should be empty initially)
   \q
   ```

4. **Update your `.env` file** (create if it doesn't exist)

   ```
   DATABASE_URL=postgresql://localhost/emotion_app
   ```

5. **Install Python dependencies**

   ```bash
   pip install -r requirements.txt
   ```

6. **Run the app**
   ```bash
   streamlit run app.py
   ```

---

## Configuration

The app automatically detects the database type:

- If `DATABASE_URL` environment variable is set → Uses PostgreSQL
- Otherwise → Falls back to SQLite

### Environment Variables

**Local development (.env file):**

```
DATABASE_URL=postgresql://localhost/emotion_app
```

**Streamlit Cloud (Secrets):**

```toml
DATABASE_URL = "postgresql://user:password@neon.host/dbname"
```

---

## Database Schema

Both SQLite and PostgreSQL use the same schema:

```sql
CREATE TABLE IF NOT EXISTS usage (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    image BYTEA NOT NULL,
    emotion TEXT NOT NULL,
    confidence REAL NOT NULL
);

CREATE INDEX idx_timestamp ON usage(timestamp DESC);
CREATE INDEX idx_name ON usage(name);
```

---

## Testing the Migration

1. **Backup your SQLite data** (optional):

   ```bash
   cp emotion_app.db emotion_app.db.backup
   ```

2. **Run the app with PostgreSQL**:

   ```bash
   export DATABASE_URL=postgresql://localhost/emotion_app
   streamlit run app.py
   ```

3. **Test the features**:

   - Upload an image
   - Enter your name
   - Click "Save result"
   - Check the history expander

4. **Verify data in PostgreSQL**:
   ```bash
   psql -d emotion_app
   SELECT * FROM usage;
   ```

---

## Troubleshooting

### Connection Error

```
psycopg2.OperationalError: could not connect to server
```

- Ensure PostgreSQL is running: `brew services start postgresql`
- Check DATABASE_URL is correct
- Test with: `psql -d emotion_app`

### "No such table: usage"

- The app will auto-create the table on first run
- If it doesn't, restart the app: `streamlit run app.py`

### Streamlit Cloud Deployment Issues

- Double-check the DATABASE_URL format in Secrets
- Ensure the password doesn't contain special characters (or URL-encode them)
- Test locally first before deploying

---

## Performance Tips

For faster queries on Streamlit Cloud:

1. **Add pagination** (limit results to 100 recent entries):

   ```sql
   SELECT * FROM usage ORDER BY id DESC LIMIT 100;
   ```

   ✅ Already implemented in app.py

2. **Add database indexes** (improves query speed):

   ```sql
   CREATE INDEX idx_timestamp ON usage(timestamp DESC);
   CREATE INDEX idx_name ON usage(name);
   ```

3. **Cache query results** (built into Streamlit):
   ```python
   @st.cache_data
   def get_history():
       # query database
   ```

---

## Migration from SQLite to PostgreSQL

If you have existing SQLite data to migrate:

```python
import sqlite3
import psycopg2

# Read from SQLite
sqlite_conn = sqlite3.connect('emotion_app.db')
sqlite_cursor = sqlite_conn.cursor()
rows = sqlite_cursor.execute('SELECT * FROM usage').fetchall()

# Write to PostgreSQL
pg_conn = psycopg2.connect('postgresql://localhost/emotion_app')
pg_cursor = pg_conn.cursor()
for row in rows:
    pg_cursor.execute(
        'INSERT INTO usage (name, timestamp, image, emotion, confidence) VALUES (%s, %s, %s, %s, %s)',
        row[1:]  # Skip the id column
    )
pg_conn.commit()
```

---

## Support

For issues, check:

- Neon documentation: https://neon.tech/docs
- Streamlit secrets: https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management
- PostgreSQL docs: https://www.postgresql.org/docs/
