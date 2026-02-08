# Keycloak + Django Multi‑Client Dummy Project

This project is a **learning / dummy setup** to understand how an **Identity and Access Management (IAM)** tool like **Keycloak** works with **multiple clients** and **Django applications**.

The goal is to clearly understand the concepts of:

* Realm
* Clients (multiple apps)
* Users
* Roles & permissions
* Token‑based authentication (OAuth2 / OpenID Connect)

---

## 🧠 What this project demonstrates

* One **Keycloak Realm** managing identity
* Multiple **clients** inside the same realm
* Separate Django apps acting as **resource servers**
* Role‑based access control using **JWT access tokens**
* Token validation using Keycloak `/userinfo` endpoint

---

## 🏗 Architecture Overview

```
User
  ↓ (login)
Keycloak (Realm: universe-realm)
  ↓ (JWT Access Token)
Django App (student-client)
```

---

## 📦 Tech Stack

* **Keycloak** (Docker image)
* **Django** (Python 3.11)
* **Docker & Docker Compose**
* **Postman / curl** for testing

---

## 📁 Project Structure

```
keycloak-django-multi-client/
│
├── docker-compose.yml
│
├── student-app/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── manage.py
│   └── app/
│       ├── views.py
│       └── urls.py
│
└── README.md
```

---

## 🚀 Step 1: Start Keycloak

Run the containers:

```bash
docker-compose up --build
```

Keycloak will be available at:

```
http://localhost:8080
```

---

## 🔐 Step 2: Keycloak Setup (Admin UI)

### 1️⃣ Create Realm

* Realm name: `universe-realm`

### 2️⃣ Create Client

**Client ID:** `student-client`

Settings:

* Client type: `OpenID Connect`
* Access type: `Confidential`
* Direct Access Grants: ✅ Enabled

➡️ Save

### 3️⃣ Get Client Secret

* Open client → **Credentials tab**
* Copy the **Client Secret**

This is used by Django / Postman.

---

## 👤 Step 3: Create User

* Username: `hariom`
* Set password
* Disable **Temporary password**

⚠️ IMPORTANT:

> If password is temporary, login will fail with:
> `Account is not fully set up`

---

## 🏷 Step 4: Create Roles

Inside **student-client**:

* Role name: `view_courses`

Assign this role to the user `hariom`.

---

## 🧪 Step 5: Testing Login (Token Generation)

### Option A: Using curl

```bash
curl -X POST http://localhost:8080/realms/universe-realm/protocol/openid-connect/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=password" \
  -d "client_id=student-client" \
  -d "client_secret=<CLIENT_SECRET>" \
  -d "username=hariom" \
  -d "password=hariom"
```

### Successful Response

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIs...",
  "expires_in": 300,
  "token_type": "Bearer"
}
```

Copy the **access_token**.

---

## 🧪 Step 6: Testing via Postman

### 🔑 Login (Token Request)

**Method:** POST
**URL:**

```
http://localhost:8080/realms/universe-realm/protocol/openid-connect/token
```

**Headers:**

```
Content-Type: application/x-www-form-urlencoded
```

**Body (x-www-form-urlencoded):**

```
grant_type=password
client_id=student-client
client_secret=<CLIENT_SECRET>
username=hariom
password=hariom
```

---

### 🔒 Protected Endpoint Test

**Method:** GET
**URL:**

```
http://localhost:8000/protected/
```

**Headers:**

```
Authorization: Bearer <ACCESS_TOKEN>
```

### ✅ Expected Success Response

```json
{
  "message": "Student protected data",
  "user": "hariom",
  "roles": ["view_courses"]
}
```

---

## ❌ Common Errors & Fixes

### ❌ `invalid_grant: Account is not fully set up`

✔ Disable temporary password

---

### ❌ `401 Authorization header missing`

✔ Add Authorization header

---

### ❌ `401 Invalid Authorization header format`

✔ Header must be exactly:

```
Authorization: Bearer <token>
```

---

### ❌ `403 Forbidden`

✔ User does not have required role

---

## 🧠 Key Learnings

* Keycloak manages **authentication**, not your app
* Django validates **access tokens**
* Roles are client‑specific
* JWT tokens are the core of modern IAM

---

## 🔮 Next Improvements (Optional)

* Use JWT signature verification instead of `/userinfo`
* Create multiple Django apps (faculty, admin)
* Add role‑based decorators or middleware
* Replace password grant with Authorization Code flow

---

## 📌 Conclusion

This dummy project successfully demonstrates how **Keycloak integrates with Django** for **multi‑client identity management**, helping understand real‑world IAM systems used in production.

---

Happy experimenting with Keycloak 🚀
