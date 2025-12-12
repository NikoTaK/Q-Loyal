# Q-Loyal

A loyalty rewards platform that ingests customer transaction data from multiple merchants, and exposes APIs and dashboards for reward tracking, redemption, and partner management.

## Architecture


### Customer Onboarding & Personal QR Creation
```mermaid
sequenceDiagram
    autonumber
    actor Customer
    participant Bot as Telegram Bot
    participant API as Backend API
    participant DB as Supabase DB

    Customer ->> Bot: /start
    Bot ->> API: registerUser(telegram_id, username)
    API ->> DB: insert/select user
    DB -->> API: user record
    API ->> API: generatePersonalQR(customer_id)
    API ->> DB: store QR metadata
    DB -->> API: saved
    API -->> Bot: personal QR image
    Bot -->> Customer: Welcome! Here is your personal QR
```

### Loyalty Card Creation
```mermaid
sequenceDiagram
    autonumber
    actor Customer
    actor Merchant as Merchant App
    participant API as Backend API
    participant DB as Supabase DB

    Customer ->> Merchant: First visit, shows personal QR
    Merchant ->> API: scanQR(customer_id, business_id)
    API ->> DB: check loyalty card (customer,business)
    DB -->> API: not found

    API ->> DB: create loyalty card (customer_id, business_id)
    DB -->> API: loyalty card created

    API -->> Merchant: "Loyalty card created"
    API ->> DB: insert first stamp
    DB -->> API: stamp saved
    API -->> Customer: (via Bot) "New loyalty card created. First stamp added!"
```

### Business Scans Customer QR to Add Stamp
```mermaid
 sequenceDiagram
    autonumber
    actor Customer
    actor Merchant as Merchant App
    participant API as Backend API
    participant DB as Supabase DB
    participant Fraud as Fraud Engine

    Customer ->> Merchant: Show personal QR
    Merchant ->> API: scanQR(customer_id, business_id)
    API ->> DB: fetch loyalty card (customer,business)
    DB -->> API: card or none
    API ->> Fraud: validateStampRequest(data)
    Fraud -->> API: valid / rejected

    alt Valid Stamp
        API ->> DB: insert stamp + upsert card
        DB -->> API: updated
        API -->> Merchant: Stamp added
        API -->> Customer: (via Bot) You received a stamp
    else Invalid Stamp
        API -->> Merchant: Stamp rejected
    end
```

### Reward Redemption Using Customer QR
```mermaid
sequenceDiagram
    actor Customer
    actor Merchant as Merchant App
    participant API as Backend API
    participant DB as Supabase DB
    autonumber

    Customer ->> Merchant: show QR code
    Merchant ->> API: redeemReward(customer_id, business_id)
    API ->> DB: fetch loyalty card
    DB -->> API: card + stamp count
    API ->> API: check reward eligibility

    alt Eligible
        API ->> DB: mark reward redeemed and deduct stamps
        DB -->> API: updated
        API -->> Merchant: Reward approved
        API ->> Customer: notify customer
    else Not Eligible
        API -->> Merchant: Not enough stamps
    end
```

## 1. Elements of the Project

- **Telegram Bot** – main interface for customers, employees, and business owners.
- **FastAPI Backend** – business logic: QR validation, stamp issuance, user & business logic.
- **Supabase Database** – PostgreSQL + RLS for users, businesses, loyalty cards, stamps.
- **Supabase Auth** – auth system for business owners (and future web dashboard).
- **QR Code System** – static & dynamic QR codes for stamp collection and employee stamping.
- **(Future) Admin Dashboard** – web UI for business management and analytics.

## 2. Architectural Patterns
- **Layered / Clean Architecture**: API layer → service layer → repository layer → DB.
- **Webhook Integration**: Telegram → FastAPI via webhooks.
- **Repository Pattern**: DB access abstracted behind repositories.
- **Stateless API Services**: no server-side sessions; all state in DB.

## 3. Communication Between Components

- **Telegram Bot → FastAPI**  
  - Via Telegram **webhooks** for messages, commands, and QR scan events.
- **FastAPI → Supabase**  
  - Via Supabase client / SQL for CRUD on users, businesses, cards, and stamps.
- **Dashboard → FastAPI → Supabase** (future)  
  - Browser calls REST endpoints on FastAPI; backend queries Supabase.
- **QR Codes → FastAPI**  
  - QR payload is sent by the Telegram Bot to FastAPI, which validates and applies stamps.

## 4. Authentication (AuthN) & Authorization (AuthZ)

### Telegram Users (Customers & Employees)
- **AuthN**
  - Identified by `telegram_id` (Telegram as identity provider).
- **AuthZ**
  - Customers can only view and modify their own loyalty cards.
  - Employees can issue stamps only for cards belonging to their assigned business.

### Business Owners (Dashboard)
- **AuthN**
  - Supabase Auth (email/password or OAuth).
- **AuthZ**
  - Can only access and manage businesses where they are the owner.
  - Can manage employees and view analytics for their own businesses only.

### QR Codes
- **Static QR**
  - Encodes `business_id` for simple “add stamp” flows.
- **Dynamic QR**
  - Encodes `business_id`, `employee_id`, and a nonce/timestamp to prevent replay.
- Validation & permissions checks happen in FastAPI.

### Database-Level Enforcement
- **RLS Policies in Supabase**
  - Restrict access by:
    - `telegram_user_id` for customer data (cards, stamps).
    - `owner_id` for business and analytics data.
    - `employee_id` and `business_id` for stamp issuance.

**Users**

- Customers
- Merchants
- Admins

**Clients**

- Web Dashboard
- Mobile App
- Merchant Portal

**Public Services**

- Customer API
- Merchant API + Analytics

**Internal Services**

- Public Auth (Customers & Merchants)
- Internal Auth (Admins)
- Reward Calculation Engine
- Notification Service
- Reporting Service

**3rd Party Services**
- Email Service (SendGrid/SES)