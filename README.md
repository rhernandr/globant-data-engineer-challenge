# Globant Data Engineer Challenge

This project is a **Flask API** using **PostgreSQL** as a database.

---

## Requirements

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
---

### **Set Up Environment Variables**

Rename `.env.example` to `.env` and configure database credentials:

```ini
DB_USER=my_user
DB_PASSWORD=my_password
DB_HOST=db
DB_PORT=5432
DB_NAME=my_database
```

### **Build and Run the Containers**

```bash
docker-compose up --build
```

This will:

- Build and start the Flask API and PostgreSQL containers.
- Apply database migrations automatically.

### **Verify Running Containers**

```bash
docker ps
```

You should see the `web` (Flask) and `db` (PostgreSQL) containers running.

---

## License

This project is under the **MIT License**.

