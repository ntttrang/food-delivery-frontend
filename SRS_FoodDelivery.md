# Software Requirements Specification (SRS) – Tech Overview
## Food Delivery Platform

**Version:** 2.2  
**Date:** 21 January 2026  
**Status:** Ready for Development Planning  
**Change Log:** 
- v2.1: P0 updates - Exception Flows, WebSocket Architecture, Dispute/Audit Models, Error Schema, JWT RS256
- v2.2: Synced with Food_Delivery_Full.md - Full Database Schema, Complete API Contracts

---

## TABLE OF CONTENTS

1. Functional Requirements by Service
   - 1.1-1.10 Core Services
   - 1.11 Dispute Service (NEW - P0)
2. Non-Functional Requirements
3. System Architecture Overview
   - 3.2 WebSocket Architecture (NEW - P0)
   - 3.3 Saga Compensation Actions (NEW - P0)
4. Data Model Highlights (Full PostgreSQL DDL - Synced)
   - 4.1 Core Entities (17 tables with full schema)
   - 4.2 Key Indexes (complete index definitions)
5. API Contract Summary (Full - Synced with Food_Delivery_Full.md)
   - 5.0 Standardized Error Response Schema (P0)
   - 5.1 Authentication & User APIs
   - 5.2 Catalog & Restaurant APIs
   - 5.3 Order APIs
   - 5.4 Payment APIs
   - 5.5 Delivery APIs
   - 5.6 Rating APIs (NEW - Synced)
   - 5.7 Notification APIs (NEW - Synced)
   - 5.8 Admin APIs (NEW - Synced)
   - 5.9 Dispute APIs (P0)
   - 5.10 WebSocket Events API (P0)
6. Testing & Quality Strategy
7. Security Requirements
   - 7.1 JWT RS256 (UPDATED - P0)
   - 7.3 GDPR Compliance (EXPANDED - P0)
8. Deployment & Operations
9. Change Log & Traceability (NEW - P0)

---

## 1. FUNCTIONAL REQUIREMENTS BY SERVICE

### 1.1 User Service (Identity & Auth)

**Responsibilities:**
- User registration, login, password reset
- JWT token management (24h TTL, refresh rotation)
- User profile CRUD
- Role-based access control (RBAC)
- Delivery addresses management
- Payment methods tokenization

**Key FRs:**
- FR-US-01: Email/phone registration with OTP verification
- FR-US-02: Login with JWT + refresh token pattern
- FR-US-03: Profile update (name, avatar, email, phone)
- FR-US-04: Manage delivery addresses (CRUD, set default)
- FR-US-05: Manage payment methods (CRUD, set default, tokenization)
- FR-US-06: RBAC enforcement (customer, restaurant_owner, driver, admin)
- FR-US-07: Account suspension by admin

**MVP Scope:** ✓ All basic requirements
**Phase 2:** Social login (Facebook, Google), 2FA with OTP

### 1.2 Catalog Service (Restaurant & Menu)

**Responsibilities:**
- Restaurant registration & profile
- Menu management (categories, items, variants)
- Item availability management
- Restaurant operational hours & service zones
- Search indexing & caching

**Key FRs:**
- FR-CAT-01: Restaurant registration with basic info
- FR-CAT-02: Define service zones (geo-fencing)
- FR-CAT-03: Menu CRUD (categories, items)
- FR-CAT-04: Menu item variants (size, topping) with price deltas
- FR-CAT-05: Mark items unavailable (temp disable)
- FR-CAT-06: Restaurant accepting orders on/off toggle
- FR-CAT-07: Search indexing for geo-proximity queries

**MVP Scope:** ✓ All core requirements
**Phase 2:** Bulk CSV upload, advanced filters (cuisine type, price range)

### 1.3 Order Service

**Responsibilities:**
- Order creation & validation
- Cart management
- Order state machine (CREATED → DELIVERED)
- Price calculation (subtotal + tax + fees - discounts)
- Coupon application
- Estimated delivery time (ETD) calculation
- Order history retrieval

**Key FRs:**
- FR-ORD-01: Create order with validation (item availability, price)
- FR-ORD-02: Cart management (add, remove, modify quantity/variants)
- FR-ORD-03: Total calculation (subtotal + tax + delivery fee - coupon)
- FR-ORD-04: Apply coupon with validation
- FR-ORD-05: Order status state machine enforcement
- FR-ORD-06: Order history with filtering
- FR-ORD-07: Order cancellation with refund trigger
- FR-ORD-08: ETD calculation (distance + avg speed)
- FR-ORD-09: Reorder functionality (repeat previous order)
- FR-ORD-10: Order audit trail (event logging)
- FR-ORD-11: Handle customer unreachable scenario (3 call attempts, 5-min wait, auto UNDELIVERABLE)
- FR-ORD-12: Address correction flow (recalculate ETA, additional fee if >2km)
- FR-ORD-13: Dispute ticket creation (issue categories, photo upload, admin review workflow)
- FR-ORD-14: SLA miss auto-cancellation (>60min late → auto-cancel + full refund + discount)

**MVP Scope:** ✓ All core requirements
**Phase 2:** ML-based ETD, batch order operations, automated dispute assessment

### 1.4 Payment Service

**Responsibilities:**
- Payment session creation
- Gateway integration (Stripe/VNPay)
- Authorization & capture flow
- Webhook handling
- Idempotency & double-charge prevention
- Refund processing
- Daily reconciliation
- Transaction history

**Key FRs:**
- FR-PAY-01: Payment session creation
- FR-PAY-02: Multiple payment methods (COD, card, e-wallet)
- FR-PAY-03: Payment gateway integration
- FR-PAY-04: Authorization & capture flow
- FR-PAY-05: Webhook handling (success/failure)
- FR-PAY-06: Refund processing (full, partial)
- FR-PAY-07: Idempotency key enforcement (no double-charge)
- FR-PAY-08: Daily reconciliation job
- FR-PAY-09: Transaction history & receipt
- FR-PAY-10: Chargeback handling (gateway chargeback process, settlement adjustment)
- FR-PAY-11: COD collection verification (driver cash confirmation, end-of-day reconciliation)
- FR-PAY-12: Payment dispute workflow (unauthorized, duplicate charge detection & auto-refund)

**MVP Scope:** ✓ COD + 1 gateway
**Phase 2:** +Momo, +Zalo Pay, +Bank transfer

### 1.5 Delivery Service

**Responsibilities:**
- Driver registration & verification
- GPS tracking & location updates
- Delivery task assignment algorithm
- Real-time ETA calculation
- Delivery status updates
- Driver earnings calculation
- Performance metrics (on-time rate, rating)

**Key FRs:**
- FR-DEL-01: Driver registration with document upload
- FR-DEL-02: Online/offline status with GPS
- FR-DEL-03: Delivery task creation & assignment
- FR-DEL-04: Simple assignment algorithm (nearest available)
- FR-DEL-05: Delivery status updates (PICKED_UP → DELIVERED)
- FR-DEL-06: Real-time GPS tracking
- FR-DEL-07: ETA calculation & updates
- FR-DEL-08: Driver earnings & payout history
- FR-DEL-09: SLA metrics (on-time rate, rating)
- FR-DEL-10: Driver emergency protocol (EMERGENCY status, order reassignment, compensation)
- FR-DEL-11: Customer contact failure handling (3 attempts, 5-min wait timer, UNDELIVERABLE status)
- FR-DEL-12: Address mismatch resolution (driver report, customer confirmation, fee recalculation)

**MVP Scope:** ✓ All core requirements
**Phase 2:** Route optimization, surge pricing, batch routing

### 1.6 Search Service

**Responsibilities:**
- Restaurant search by location, filters, keywords
- Caching & performance optimization
- Ranking (distance, rating, status)
- Geo-proximity queries
- Autocomplete & suggestions (Phase 2)

**Key FRs:**
- FR-SEARCH-01: Geo-search (nearby restaurants)
- FR-SEARCH-02: Basic filtering (open, rating, distance)
- FR-SEARCH-03: Full-text search (restaurant name)
- FR-SEARCH-04: Ranking algorithm (distance + rating + status)
- FR-SEARCH-05: Pagination with facet counts
- FR-SEARCH-06: Search result caching

**MVP Scope:** ✓ Geo-search + basic filter, Redis caching
**Phase 2:** Elasticsearch, personalized ranking, autocomplete

### 1.7 Promotion Service

**Responsibilities:**
- Coupon creation & management
- Coupon validation & usage tracking
- Promotion campaign management (Phase 2)

**Key FRs:**
- FR-COUPON-01: Create coupon (%, fixed, min cart, per-user limit)
- FR-COUPON-02: Apply coupon at checkout
- FR-COUPON-03: Track coupon usage
- FR-COUPON-04: Time-based activation (start/end date)

**MVP Scope:** ✓ Basic coupon (no stacking)
**Phase 2:** Segment-based targeting, stacking rules

### 1.8 Notification Service

**Responsibilities:**
- Push notifications (FCM)
- SMS notifications
- Email notifications (Phase 2)
- Retry logic & delivery guarantees

**Key FRs:**
- FR-NOTIF-01: Push notification on status changes
- FR-NOTIF-02: SMS for critical events
- FR-NOTIF-03: Email notifications (receipt, promo)
- FR-NOTIF-04: Retry logic (exponential backoff)
- FR-NOTIF-05: Template management & localization (Phase 2)

**MVP Scope:** ✓ Push (FCM) + SMS basic
**Phase 2:** Email, in-app notifications, preferences

### 1.9 Rating Service

**Responsibilities:**
- Rating & review submission
- Aggregate rating calculation
- Review moderation (Phase 2)

**Key FRs:**
- FR-RATING-01: Submit rating & review (restaurant, driver)
- FR-RATING-02: Aggregate rating calculation
- FR-RATING-03: Review display with pagination
- FR-RATING-04: Moderation (flag inappropriate) (Phase 2)

**MVP Scope:** ✓ Star + comment, no moderation
**Phase 2:** Advanced moderation, ML detection, merchant reply

### 1.10 Admin Service

**Responsibilities:**
- Dashboard & KPI reporting
- User management (suspension, deletion)
- Restaurant onboarding workflow
- Driver management
- Payment reconciliation
- System configuration

**Key FRs:**
- FR-ADMIN-01: Dashboard with KPIs
- FR-ADMIN-02: User management
- FR-ADMIN-03: Restaurant onboarding workflow
- FR-ADMIN-04: Driver management
- FR-ADMIN-05: Payment reconciliation
- FR-ADMIN-06: System configuration (fees, rules)

**MVP Scope:** ✓ Basic dashboard + user management
**Phase 2:** Advanced reporting, automation

### 1.11 Dispute Service (NEW - P0)

**Responsibilities:**
- Dispute ticket lifecycle management
- Issue categorization & evidence collection
- Automated assessment for simple cases
- Admin review workflow
- Resolution & compensation processing
- Quality scoring for restaurants/drivers

**Key FRs:**
- FR-DISPUTE-01: Create dispute ticket within 24h of delivery
- FR-DISPUTE-02: Issue categorization (missing_item, wrong_item, quality, late_delivery, driver_behavior)
- FR-DISPUTE-03: Photo/evidence upload with validation (required for quality issues)
- FR-DISPUTE-04: Automated assessment for missing/wrong items (immediate refund + compensation)
- FR-DISPUTE-05: Admin review queue with SLA (resolve within 24h)
- FR-DISPUTE-06: Resolution options (full refund, partial refund, discount code, no action)
- FR-DISPUTE-07: Notification to all parties (customer, restaurant, driver) on resolution
- FR-DISPUTE-08: Quality score impact tracking for restaurants/drivers
- FR-DISPUTE-09: Dispute audit trail (all actions logged)

**Dispute Categories & Auto-Resolution (MVP):**

| Category | Auto-Resolve | Compensation |
|:---------|:------------:|:-------------|
| Missing item (verified from order) | ✓ | Item refund + 10k VND |
| Wrong item (verified) | ✓ | Item refund + 20k VND |
| Quality issue (with photo) | ✗ Admin review | 50-100% refund |
| Late delivery (>60min) | ✓ | 25k VND discount |
| Driver behavior | ✗ Admin review | Case-by-case |

**MVP Scope:** ✓ Basic dispute flow with manual admin review
**Phase 2:** ML-based photo verification, automated quality assessment

---

## 2. NON-FUNCTIONAL REQUIREMENTS

### 2.1 Performance (p95 latency targets)

| Service | Target | Reason |
|:---|:---|:---|
| **Order Service** | <500ms | Core user journey |
| **Search Service** | <800ms | Geo-query complexity |
| **Payment Service** | <800ms | Gateway latency |
| **Delivery Tracking** | <200ms | Realtime requirement |
| **API Gateway** | <100ms | Gateway overhead |

**Page Load Time (Client):**
- Web app: <3s initial load
- Mobile app (React Native): <2s startup (cold start), <1s warm start
  - JavaScript bundle size: <5MB (compressed)
  - Hermes engine enabled for optimized startup
  - Code splitting for lazy-loaded screens

### 2.2 Availability & Reliability

| Metric | Target |
|:---|:---|
| **Uptime (SLA)** | 99.5% (MVP), 99.9% (Phase 2) |
| **Error Rate (5xx)** | <0.1% |
| **Data Loss** | 0 (RTO=0, RPO=0 for orders + payments) |
| **Auto-failover Time** | <30s |
| **Payment Success Rate** | >99.9% |
| **Double-charge Rate** | 0 |

### 2.3 Scalability

| Metric | Target | Timeline |
|:---|:---|:---|
| **Concurrent Users** | 3k-5k (MVP), 10k+ (Phase 2) | Horizontal pod autoscaling |
| **Orders/Second** | 10-20 (MVP), 50+ (Phase 2) | Kafka buffering |
| **Database Connections** | <500 per service | Connection pooling |
| **Cache Hit Rate** | >90% | Redis tuning |
| **Replicas** | 2-5 per service | Min 2 for HA |

### 2.4 Security Requirements

| Requirement | Details |
|:---|:---|
| **Authentication** | JWT (RS256), 24h TTL, refresh token rotation **(UPDATED)** |
| **Authorization** | RBAC, row-level filters on multi-tenant data |
| **Encryption (Transit)** | TLS 1.3, HSTS headers |
| **Encryption (Rest)** | AES-256 for PII, payment tokens |
| **PCI-DSS** | Tokenization via gateway, no raw card data |
| **Rate Limiting** | 100 req/min/user, 1000 req/min/IP |
| **Input Validation** | Server-side, parameterized queries |
| **Audit Logging** | All sensitive ops (login, payment, admin), 6+ months retention |
| **Vulnerability Mgmt** | Quarterly pentest, bug bounty, OWASP Top 10 |

**Mandatory Security Headers (NEW - P0):**

| Header | Value |
|:-------|:------|
| `X-Content-Type-Options` | nosniff |
| `X-Frame-Options` | DENY |
| `X-XSS-Protection` | 1; mode=block |
| `Content-Security-Policy` | default-src 'self' |
| `Strict-Transport-Security` | max-age=31536000; includeSubDomains |
| `X-Request-ID` | {unique-request-id} |

### 2.5 Observability & Monitoring

| Tool | Purpose |
|:---|:---|
| **Prometheus + Grafana** | Metrics & dashboards |
| **ELK / Loki + Kibana** | Centralized logging (30 days hot, 1 year cold) |
| **Jaeger / Tempo** | Distributed tracing |
| **Sentry** | Error & exception tracking |
| **Custom dashboards** | Business KPIs (orders, revenue, SLA) |

### 2.6 Maintainability

| Aspect | Standard |
|:---|:---|
| **Code Coverage** | ≥80% unit, ≥60% integration |
| **Documentation** | ADR (Architecture Decision Records), API docs (OpenAPI) |
| **Deployment** | Blue-green or canary, GitOps (ArgoCD) |
| **Backward Compatibility** | Support 2 major API versions |
| **Deployment Frequency** | 1-2x per week |

---

## 3. SYSTEM ARCHITECTURE OVERVIEW

### 3.1 High-Level Components

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT LAYER                            │
├─────────────────────────────────────────────────────────────┤
│ Web (Next.js/React)  │  Mobile (React Native - TypeScript) │
└──────────────────────┬──────────────┬──────────────────────┘
                       │              │
┌──────────────────────┴──────────────┴──────────────────────┐
│              API GATEWAY (Nginx/Envoy)                     │
│    - Auth check, rate limiting, routing, logging          │
└──────────────┬───────────────────────────────────────────┘
               │
┌──────────────┴───────────────────────────────────────────┐
│           MICROSERVICES LAYER                           │
├──────────────────────────────────────────────────────────┤
│ User Service   │ Catalog Service │ Order Service         │
│ Payment Service │ Delivery Service │ Search Service      │
│ Promotion Svc  │ Notification Svc │ Rating Service      │
│ Admin Service  │                  │                      │
└──────────────┬──────────────────────────────────────────┘
               │ (REST/gRPC)
┌──────────────┴──────────────────────────────────────────┐
│         MESSAGE BROKER (Kafka)                          │
├──────────────────────────────────────────────────────────┤
│ Topics: order.*, payment.*, delivery.*, notification.* │
└──────────────┬──────────────────────────────────────────┘
               │
┌──────────────┴──────────────────────────────────────────┐
│          DATA STORAGE LAYER                            │
├──────────────────────────────────────────────────────────┤
│ PostgreSQL (primary) │ Redis (cache, session)           │
│ Elasticsearch (Phase 2: search index)                   │
│ S3/MinIO (images)                                        │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│         EXTERNAL INTEGRATIONS                           │
├──────────────────────────────────────────────────────────┤
│ Payment Gateway (Stripe/VNPay) │ Google Maps API       │
│ FCM / APNs (push) │ SMS Provider (Twilio)              │
└──────────────────────────────────────────────────────────┘
```

### 3.2 Real-Time Layer - WebSocket Architecture (NEW - P0)

**Purpose:** Enable real-time order tracking, driver location updates, and instant notifications.

```
┌─────────────────────────────────────────────────────────────┐
│                 REAL-TIME LAYER                             │
├─────────────────────────────────────────────────────────────┤
│              WebSocket Gateway (Socket.io/ws)               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ - Client connection management (auth via JWT)       │   │
│  │ - Room-based subscriptions (order:{id}, driver:{id})│   │
│  │ - Heartbeat interval: 30 seconds                    │   │
│  │ - Reconnection: exponential backoff (1s→2s→4s→30s) │   │
│  │ - Max connections per user: 5 (mobile + web)        │   │
│  └─────────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│              Redis Pub/Sub (Event Distribution)             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Channels:                                            │   │
│  │ - order:status:{order_id}    → Status updates       │   │
│  │ - driver:location:{order_id} → GPS coordinates      │   │
│  │ - notification:{user_id}     → Push events          │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**WebSocket Events Contract:**

```
// Client → Server (Subscribe)
{ "type": "subscribe", "channel": "order:12345" }
{ "type": "subscribe", "channel": "driver:location:12345" }
{ "type": "unsubscribe", "channel": "order:12345" }
{ "type": "ping" }

// Server → Client (Events)
{ 
  "type": "order_status", 
  "data": { 
    "order_id": "uuid", 
    "status": "PREPARING",
    "updated_at": "2026-01-21T10:30:00Z"
  }
}

{ 
  "type": "driver_location", 
  "data": { 
    "order_id": "uuid",
    "lat": 10.8231,
    "lng": 106.6297,
    "heading": 45,
    "speed_kmh": 25,
    "eta_minutes": 12,
    "updated_at": "2026-01-21T10:30:00Z"
  }
}

{ 
  "type": "eta_update", 
  "data": { 
    "order_id": "uuid",
    "eta_minutes": 8,
    "reason": "traffic_cleared"
  }
}

// Server → Client (Errors)
{
  "type": "error",
  "data": {
    "code": "SUBSCRIPTION_FAILED",
    "message": "Order not found or access denied"
  }
}
```

**Scalability Requirements:**
- Horizontal scaling via sticky sessions (consistent hashing by user_id)
- Target: 50k concurrent WebSocket connections (MVP)
- Location update frequency: Every 5 seconds (driver app)
- Message latency: <500ms end-to-end

### 3.3 Event-Driven Workflows (Saga Pattern)

**Order Creation Saga:**
```
OrderService creates CREATED
  → OrderCreated event to Kafka
  → PaymentService: payment authorization
    → PaymentAuthorized event
  → OrderService: update to CONFIRMED
    → OrderConfirmed event
  → NotificationService: notify restaurant
  → Restaurant accepts
    → OrderAccepted event
  → DeliveryService: assign driver
    → DeliveryAssigned event
  → Driver completes delivery
    → DeliveryCompleted event
  → OrderService: update to DELIVERED
    → PaymentCaptured (if pre-authorized)
  → RatingService: prompt customer
```

**Saga Compensation Actions (NEW - P0):**

| Step | Failure | Compensation Action |
|:-----|:--------|:--------------------|
| PaymentAuthorized | Gateway timeout | Retry 3x → Cancel order, notify customer |
| OrderConfirmed | Restaurant offline | Release auth, refund, notify customer |
| RestaurantAccepted | Restaurant rejects | Full refund + 50k discount code |
| DeliveryAssigned | No driver available (5min) | Expand radius → Queue order → Notify customer of delay |
| DeliveryCompleted | Driver emergency | Reassign driver, compensate original driver |

---

## 4. DATA MODEL HIGHLIGHTS

### 4.1 Core Entities (Full Schema - Synced with Food_Delivery_Full.md)

**Cities (NEW - Synced)**
```sql
CREATE TABLE cities (
    id          BIGSERIAL PRIMARY KEY,
    title       VARCHAR(255) NOT NULL UNIQUE,
    status      VARCHAR(32) NOT NULL DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE','INACTIVE')),
    created_by  UUID,
    updated_by  UUID,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

**Users**
```sql
CREATE TABLE users (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email             VARCHAR(255) UNIQUE,
    phone             VARCHAR(20) UNIQUE,
    password_hash     VARCHAR(255) NOT NULL,
    first_name        VARCHAR(100),
    last_name         VARCHAR(100),
    avatar_url        TEXT,
    role              VARCHAR(32) NOT NULL CHECK (role IN ('CUSTOMER','RESTAURANT_OWNER','DRIVER','ADMIN')),
    is_active         BOOLEAN NOT NULL DEFAULT TRUE,
    city_id           BIGINT REFERENCES cities(id),
    is_deleted        BOOLEAN NOT NULL DEFAULT FALSE,
    created_by        UUID,
    updated_by        UUID,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

**User Addresses**
```sql
CREATE TABLE user_addresses (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id           UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    label             VARCHAR(100),
    street            TEXT NOT NULL,
    city_id           BIGINT REFERENCES cities(id),
    district          VARCHAR(100),
    lat               DOUBLE PRECISION NOT NULL,
    lng               DOUBLE PRECISION NOT NULL,
    is_default        BOOLEAN NOT NULL DEFAULT FALSE,
    is_deleted        BOOLEAN NOT NULL DEFAULT FALSE,
    created_by        UUID,
    updated_by        UUID,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

**User Payment Methods (NEW - Synced)**
```sql
CREATE TABLE user_payment_methods (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id           UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type              VARCHAR(32) NOT NULL CHECK (type IN ('CARD','EWALLET','COD')),
    provider          VARCHAR(64),
    token             TEXT NOT NULL,  -- tokenized via gateway, never raw card
    last4             VARCHAR(4),
    is_default        BOOLEAN NOT NULL DEFAULT FALSE,
    is_deleted        BOOLEAN NOT NULL DEFAULT FALSE,
    created_by        UUID,
    updated_by        UUID,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

**Refresh Tokens (NEW - Synced)**
```sql
CREATE TABLE refresh_tokens (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id           UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token             TEXT NOT NULL UNIQUE,
    expires_at        TIMESTAMPTZ NOT NULL,
    revoked           BOOLEAN NOT NULL DEFAULT FALSE,
    created_by        UUID,
    updated_by        UUID,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

**Restaurants**
```sql
CREATE TABLE restaurants (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id            UUID NOT NULL REFERENCES users(id),
    name                VARCHAR(255) NOT NULL,
    description         TEXT,
    street              TEXT NOT NULL,
    city_id             BIGINT NOT NULL REFERENCES cities(id),
    district            VARCHAR(100),
    lat                 DOUBLE PRECISION NOT NULL,
    lng                 DOUBLE PRECISION NOT NULL,
    service_radius_km   NUMERIC(5,2) DEFAULT 5.0,
    status              VARCHAR(32) NOT NULL CHECK (status IN ('PENDING','ACTIVE','INACTIVE','SUSPENDED')),
    is_accepting_orders BOOLEAN NOT NULL DEFAULT TRUE,
    average_rating      NUMERIC(3,2) DEFAULT 0,
    total_reviews       INT NOT NULL DEFAULT 0,
    min_order_value     NUMERIC(12,2) DEFAULT 0,
    is_deleted          BOOLEAN NOT NULL DEFAULT FALSE,
    created_by          UUID,
    updated_by          UUID,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

**Menu Categories (NEW - Synced)**
```sql
CREATE TABLE menu_categories (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    restaurant_id   UUID NOT NULL REFERENCES restaurants(id) ON DELETE CASCADE,
    name            VARCHAR(255) NOT NULL,
    sort_order      INT DEFAULT 0,
    is_deleted      BOOLEAN NOT NULL DEFAULT FALSE,
    created_by      UUID,
    updated_by      UUID,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

**Menu Items**
```sql
CREATE TABLE menu_items (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    restaurant_id   UUID NOT NULL REFERENCES restaurants(id) ON DELETE CASCADE,
    category_id     UUID REFERENCES menu_categories(id),
    name            VARCHAR(255) NOT NULL,
    description     TEXT,
    price           NUMERIC(12,2) NOT NULL,
    is_available    BOOLEAN NOT NULL DEFAULT TRUE,
    image_url       TEXT,
    is_deleted      BOOLEAN NOT NULL DEFAULT FALSE,
    created_by      UUID,
    updated_by      UUID,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

**Menu Item Variants (NEW - Synced)**
```sql
CREATE TABLE menu_item_variants (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    item_id         UUID NOT NULL REFERENCES menu_items(id) ON DELETE CASCADE,
    name            VARCHAR(255) NOT NULL,
    price_delta     NUMERIC(12,2) NOT NULL DEFAULT 0,
    is_available    BOOLEAN NOT NULL DEFAULT TRUE,
    created_by      UUID,
    updated_by      UUID,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

**Coupons**
```sql
CREATE TABLE coupons (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code                    VARCHAR(64) UNIQUE NOT NULL,
    type                    VARCHAR(32) NOT NULL CHECK (type IN ('PERCENT','FLAT')),
    discount_value          NUMERIC(12,2) NOT NULL,
    min_order_value         NUMERIC(12,2),
    max_discount            NUMERIC(12,2),
    global_usage_limit      INT,
    per_user_usage_limit    INT DEFAULT 1,
    start_time              TIMESTAMPTZ,
    end_time                TIMESTAMPTZ,
    target_restaurant_id    UUID REFERENCES restaurants(id),
    city_id                 BIGINT REFERENCES cities(id),
    is_active               BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted              BOOLEAN NOT NULL DEFAULT FALSE,
    created_by              UUID,
    updated_by              UUID,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

**Coupon Usages (NEW - Synced)**
```sql
CREATE TABLE coupon_usages (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    coupon_id       UUID NOT NULL REFERENCES coupons(id),
    user_id         UUID NOT NULL REFERENCES users(id),
    order_id        UUID REFERENCES orders(id),
    used_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by      UUID,
    updated_by      UUID,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

**Orders**
```sql
CREATE TYPE order_status_enum AS ENUM (
    'CREATED','PAYMENT_FAILED','CONFIRMED','PREPARING','READY_FOR_PICKUP',
    'ON_THE_WAY','DELIVERED','CANCELLED','DELIVERY_FAILED'
);

CREATE TYPE payment_status_enum AS ENUM (
    'PENDING','AUTHORIZED','CAPTURED','FAILED','REFUNDED'
);

CREATE TABLE orders (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id             UUID NOT NULL REFERENCES users(id),
    restaurant_id           UUID NOT NULL REFERENCES restaurants(id),
    city_id                 BIGINT NOT NULL REFERENCES cities(id),
    status                  order_status_enum NOT NULL DEFAULT 'CREATED',
    delivery_type           VARCHAR(16) NOT NULL DEFAULT 'DELIVERY' CHECK (delivery_type IN ('DELIVERY','PICKUP')),
    delivery_address_id     UUID REFERENCES user_addresses(id),
    delivery_address_snapshot JSONB,  -- snapshot for audit trail
    coupon_code             VARCHAR(64),
    coupon_discount         NUMERIC(12,2) DEFAULT 0,
    restaurant_fee          NUMERIC(12,2) DEFAULT 0,
    tax_amount              NUMERIC(12,2) DEFAULT 0,
    delivery_fee            NUMERIC(12,2) DEFAULT 0,
    subtotal                NUMERIC(12,2) NOT NULL,
    total_price             NUMERIC(12,2) NOT NULL,
    payment_status          payment_status_enum NOT NULL DEFAULT 'PENDING',
    payment_method_id       UUID REFERENCES user_payment_methods(id),
    estimated_delivery_time TIMESTAMPTZ,
    actual_delivery_time    TIMESTAMPTZ,
    notes                   TEXT,
    delivery_task_id        UUID,
    is_deleted              BOOLEAN NOT NULL DEFAULT FALSE,
    created_by              UUID,
    updated_by              UUID,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

**Order Items (NEW - Synced)**
```sql
CREATE TABLE order_items (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id        UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    menu_item_id    UUID REFERENCES menu_items(id),
    name_snapshot   VARCHAR(255) NOT NULL,
    price_snapshot  NUMERIC(12,2) NOT NULL,
    quantity        INT NOT NULL CHECK (quantity > 0),
    subtotal        NUMERIC(12,2) NOT NULL,
    created_by      UUID,
    updated_by      UUID,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE order_item_variants (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_item_id   UUID NOT NULL REFERENCES order_items(id) ON DELETE CASCADE,
    variant_name    VARCHAR(255) NOT NULL,
    price_delta     NUMERIC(12,2) NOT NULL,
    created_by      UUID,
    updated_by      UUID,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

**Payments**
```sql
CREATE TABLE payments (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id                UUID NOT NULL UNIQUE REFERENCES orders(id),
    amount                  NUMERIC(12,2) NOT NULL,
    currency                VARCHAR(8) NOT NULL DEFAULT 'VND',
    status                  payment_status_enum NOT NULL DEFAULT 'PENDING',
    method_type             VARCHAR(32) NOT NULL,
    provider                VARCHAR(64),
    gateway_transaction_id  VARCHAR(128),
    gateway_response        JSONB,
    idempotency_key         VARCHAR(128) UNIQUE NOT NULL,
    authorized_at           TIMESTAMPTZ,
    captured_at             TIMESTAMPTZ,
    failed_at               TIMESTAMPTZ,
    is_deleted              BOOLEAN NOT NULL DEFAULT FALSE,
    created_by              UUID,
    updated_by              UUID,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

**Payment Refunds (NEW - Synced)**
```sql
CREATE TABLE payment_refunds (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    payment_id      UUID NOT NULL REFERENCES payments(id),
    amount          NUMERIC(12,2) NOT NULL,
    reason          TEXT,
    status          VARCHAR(32) DEFAULT 'PENDING' CHECK (status IN ('PENDING','COMPLETED','FAILED')),
    created_by      UUID,
    updated_by      UUID,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

**Drivers (NEW - Synced)**
```sql
CREATE TYPE driver_status_enum AS ENUM ('PENDING','APPROVED','REJECTED','SUSPENDED');

CREATE TABLE drivers (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID UNIQUE NOT NULL REFERENCES users(id),
    status          driver_status_enum NOT NULL DEFAULT 'PENDING',
    vehicle_type    VARCHAR(32),
    vehicle_plate   VARCHAR(32),
    license_number  VARCHAR(64),
    document_urls   JSONB,
    rating          NUMERIC(3,2) DEFAULT 0,
    total_trips     INT DEFAULT 0,
    is_online       BOOLEAN NOT NULL DEFAULT FALSE,
    city_id         BIGINT REFERENCES cities(id),
    is_deleted      BOOLEAN NOT NULL DEFAULT FALSE,
    created_by      UUID,
    updated_by      UUID,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

**Delivery Tasks**
```sql
CREATE TYPE delivery_task_status_enum AS ENUM (
    'CREATED','ASSIGNED','PICKED_UP','IN_TRANSIT','DELIVERED','CANCELLED'
);

CREATE TABLE delivery_tasks (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id            UUID NOT NULL UNIQUE REFERENCES orders(id),
    driver_id           UUID REFERENCES drivers(id),
    status              delivery_task_status_enum NOT NULL DEFAULT 'CREATED',
    pickup_location_snapshot JSONB NOT NULL,   -- {address, lat, lng, contact}
    dropoff_location_snapshot JSONB NOT NULL,  -- {address, lat, lng, contact}
    current_lat         DOUBLE PRECISION,
    current_lng         DOUBLE PRECISION,
    current_location_updated_at TIMESTAMPTZ,
    estimated_delivery_time TIMESTAMPTZ,
    actual_delivery_time TIMESTAMPTZ,
    driver_assignment_time TIMESTAMPTZ,
    pickup_time         TIMESTAMPTZ,
    is_deleted          BOOLEAN NOT NULL DEFAULT FALSE,
    created_by          UUID,
    updated_by          UUID,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

**Delivery Task Events (NEW - Synced)**
```sql
CREATE TABLE delivery_task_events (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    delivery_task_id    UUID NOT NULL REFERENCES delivery_tasks(id) ON DELETE CASCADE,
    event_type          VARCHAR(32) NOT NULL,  -- ASSIGNED, PICKED_UP, IN_TRANSIT, DELIVERED, CANCELLED
    event_data          JSONB,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

**Ratings**
```sql
CREATE TABLE ratings (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id        UUID NOT NULL REFERENCES orders(id),
    rater_id        UUID NOT NULL REFERENCES users(id),
    ratee_id        UUID NOT NULL REFERENCES users(id),
    rating_type     VARCHAR(32) NOT NULL CHECK (rating_type IN ('RESTAURANT','DRIVER')),
    score           SMALLINT NOT NULL CHECK (score BETWEEN 1 AND 5),
    comment         TEXT,
    is_deleted      BOOLEAN NOT NULL DEFAULT FALSE,
    created_by      UUID,
    updated_by      UUID,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

**Order Events - Audit Trail (NEW - Synced)**
```sql
CREATE TABLE order_events (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id        UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    event_type      VARCHAR(64) NOT NULL,  -- CREATED, CONFIRMED, PREPARING, etc.
    previous_status VARCHAR(32),
    new_status      VARCHAR(32),
    event_data      JSONB,
    actor_id        UUID,
    actor_role      VARCHAR(32),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

**Disputes (P0)**
```sql
CREATE TABLE disputes (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id            UUID NOT NULL REFERENCES orders(id),
    customer_id         UUID NOT NULL REFERENCES users(id),
    category            VARCHAR(50) NOT NULL CHECK (category IN ('missing_item','wrong_item','quality','late_delivery','driver_behavior')),
    description         TEXT,
    photo_urls          TEXT[],
    status              VARCHAR(32) NOT NULL DEFAULT 'open' CHECK (status IN ('open','investigating','resolved','rejected')),
    resolution_type     VARCHAR(32),
    resolution_amount   NUMERIC(12,2),
    resolved_by         UUID REFERENCES users(id),
    resolved_at         TIMESTAMPTZ,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

**Audit Logs (P0)**
```sql
CREATE TABLE audit_logs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type     VARCHAR(50) NOT NULL,  -- order, payment, user, dispute, restaurant
    entity_id       UUID NOT NULL,
    action          VARCHAR(50) NOT NULL,  -- create, update, delete, cancel, refund
    actor_id        UUID,
    actor_role      VARCHAR(32),
    old_values      JSONB,
    new_values      JSONB,
    ip_address      INET,
    user_agent      TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

**Driver Location History (P0)**
```sql
CREATE TABLE driver_location_history (
    id                  BIGSERIAL PRIMARY KEY,
    driver_id           UUID NOT NULL REFERENCES drivers(id),
    delivery_task_id    UUID REFERENCES delivery_tasks(id),
    location            GEOGRAPHY(POINT) NOT NULL,
    speed_kmh           NUMERIC(5,2),
    heading             INTEGER,
    accuracy_meters     NUMERIC(6,2),
    recorded_at         TIMESTAMPTZ NOT NULL DEFAULT NOW()
) PARTITION BY RANGE (recorded_at);
-- Create monthly partitions, retention: 30 days
```

### 4.2 Key Indexes (Full - Synced with Food_Delivery_Full.md)

**User & Auth Indexes:**
```sql
CREATE INDEX idx_users_email ON users(email) WHERE is_deleted = FALSE;
CREATE INDEX idx_users_phone ON users(phone) WHERE is_deleted = FALSE;
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_city_id ON users(city_id);
CREATE INDEX idx_user_addresses_user_id ON user_addresses(user_id) WHERE is_deleted = FALSE;
CREATE INDEX idx_user_addresses_location ON user_addresses USING gist(ll_to_earth(lat, lng));
CREATE INDEX idx_user_payment_methods_user_id ON user_payment_methods(user_id) WHERE is_deleted = FALSE;
CREATE INDEX idx_refresh_tokens_user_id ON refresh_tokens(user_id);
CREATE INDEX idx_refresh_tokens_expires_at ON refresh_tokens(expires_at);
```

**Restaurant & Menu Indexes:**
```sql
CREATE INDEX idx_restaurants_city_id ON restaurants(city_id) WHERE is_deleted = FALSE AND status = 'ACTIVE';
CREATE INDEX idx_restaurants_location ON restaurants USING gist(ll_to_earth(lat, lng)) WHERE status = 'ACTIVE';
CREATE INDEX idx_restaurants_owner_id ON restaurants(owner_id);
CREATE INDEX idx_restaurants_status ON restaurants(status);
CREATE INDEX idx_menu_categories_restaurant_id ON menu_categories(restaurant_id) WHERE is_deleted = FALSE;
CREATE INDEX idx_menu_items_restaurant_id ON menu_items(restaurant_id) WHERE is_deleted = FALSE;
CREATE INDEX idx_menu_items_category_id ON menu_items(category_id) WHERE is_deleted = FALSE;
CREATE INDEX idx_menu_item_variants_item_id ON menu_item_variants(item_id);
```

**Order & Payment Indexes:**
```sql
CREATE INDEX idx_orders_customer_id ON orders(customer_id) WHERE is_deleted = FALSE;
CREATE INDEX idx_orders_restaurant_id ON orders(restaurant_id) WHERE is_deleted = FALSE;
CREATE INDEX idx_orders_city_id ON orders(city_id) WHERE is_deleted = FALSE;
CREATE INDEX idx_orders_status ON orders(status) WHERE is_deleted = FALSE;
CREATE INDEX idx_orders_created_at ON orders(created_at DESC) WHERE is_deleted = FALSE;
CREATE INDEX idx_orders_payment_status ON orders(payment_status) WHERE is_deleted = FALSE;
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_item_variants_order_item_id ON order_item_variants(order_item_id);
CREATE INDEX idx_payments_order_id ON payments(order_id);
CREATE INDEX idx_payments_status ON payments(status) WHERE is_deleted = FALSE;
CREATE INDEX idx_payments_idempotency_key ON payments(idempotency_key) WHERE is_deleted = FALSE;
CREATE INDEX idx_payment_refunds_payment_id ON payment_refunds(payment_id);
```

**Coupon Indexes:**
```sql
CREATE INDEX idx_coupons_code ON coupons(code) WHERE is_active = TRUE AND is_deleted = FALSE;
CREATE INDEX idx_coupons_restaurant_id ON coupons(target_restaurant_id) WHERE is_active = TRUE;
CREATE INDEX idx_coupons_validity ON coupons(start_time, end_time) WHERE is_active = TRUE;
CREATE INDEX idx_coupon_usages_coupon_id ON coupon_usages(coupon_id);
CREATE INDEX idx_coupon_usages_user_id ON coupon_usages(user_id);
```

**Driver & Delivery Indexes:**
```sql
CREATE INDEX idx_drivers_user_id ON drivers(user_id);
CREATE INDEX idx_drivers_status ON drivers(status) WHERE is_deleted = FALSE;
CREATE INDEX idx_drivers_city_id ON drivers(city_id) WHERE status = 'APPROVED';
CREATE INDEX idx_drivers_online ON drivers(is_online, status) WHERE is_online = TRUE AND status = 'APPROVED';
CREATE INDEX idx_delivery_tasks_order_id ON delivery_tasks(order_id);
CREATE INDEX idx_delivery_tasks_driver_id ON delivery_tasks(driver_id) WHERE status IN ('ASSIGNED', 'PICKED_UP', 'IN_TRANSIT');
CREATE INDEX idx_delivery_tasks_status ON delivery_tasks(status) WHERE is_deleted = FALSE;
CREATE INDEX idx_delivery_tasks_location ON delivery_tasks USING gist(ll_to_earth(current_lat, current_lng));
CREATE INDEX idx_delivery_task_events_task_id ON delivery_task_events(delivery_task_id);
CREATE INDEX idx_delivery_task_events_created_at ON delivery_task_events(created_at DESC);
```

**Rating Indexes:**
```sql
CREATE INDEX idx_ratings_order_id ON ratings(order_id);
CREATE INDEX idx_ratings_rater_id ON ratings(rater_id);
CREATE INDEX idx_ratings_ratee_id ON ratings(ratee_id) WHERE rating_type = 'RESTAURANT';
CREATE INDEX idx_ratings_created_at ON ratings(created_at DESC);
```

**Audit & Events Indexes:**
```sql
CREATE INDEX idx_order_events_order_id ON order_events(order_id);
CREATE INDEX idx_order_events_created_at ON order_events(created_at DESC);
CREATE INDEX idx_disputes_order_id ON disputes(order_id);
CREATE INDEX idx_disputes_customer_id ON disputes(customer_id, created_at DESC);
CREATE INDEX idx_disputes_status ON disputes(status);
CREATE INDEX idx_audit_logs_entity ON audit_logs(entity_type, entity_id, created_at DESC);
CREATE INDEX idx_audit_logs_actor ON audit_logs(actor_id, created_at DESC);
CREATE INDEX idx_driver_location_history_task ON driver_location_history(delivery_task_id, recorded_at DESC);
```

---

## 5. API CONTRACT SUMMARY

### 5.0 Standardized Error Response Schema (NEW - P0)

**All API errors MUST follow this format:**

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "specific_field",
      "reason": "validation_failed",
      "metadata": {}
    },
    "trace_id": "abc-123-xyz-456"
  }
}
```

**Common Error Codes:**

| HTTP Status | Error Code | Description |
|:-----------:|:-----------|:------------|
| 400 | `VALIDATION_ERROR` | Request validation failed |
| 400 | `ORDER_MINIMUM_NOT_MET` | Cart below minimum order value |
| 400 | `COUPON_INVALID` | Coupon code invalid or expired |
| 400 | `ITEM_UNAVAILABLE` | Menu item no longer available |
| 401 | `AUTH_TOKEN_EXPIRED` | JWT token expired |
| 401 | `AUTH_TOKEN_INVALID` | JWT token malformed or invalid |
| 403 | `ACCESS_DENIED` | User lacks permission for resource |
| 404 | `RESOURCE_NOT_FOUND` | Requested resource does not exist |
| 409 | `ORDER_ALREADY_CANCELLED` | Order already in cancelled state |
| 409 | `DUPLICATE_REQUEST` | Idempotency key already processed |
| 422 | `RESTAURANT_CLOSED` | Restaurant not accepting orders |
| 422 | `DRIVER_UNAVAILABLE` | No drivers available in area |
| 429 | `RATE_LIMIT_EXCEEDED` | Too many requests |
| 500 | `INTERNAL_ERROR` | Server error, retry later |
| 502 | `GATEWAY_ERROR` | Payment gateway unavailable |
| 503 | `SERVICE_UNAVAILABLE` | Service temporarily down |

**Rate Limit Headers (all responses):**

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1640000000
X-Request-ID: abc-123-xyz
```

**Pagination Response Format:**

```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total_count": 150,
    "total_pages": 8,
    "next_cursor": "eyJpZCI6MTIzfQ==",
    "has_more": true
  }
}
```

### 5.1 Authentication & User APIs (Synced with Food_Delivery_Full.md)

```http
# Registration & Login
POST /api/v1/auth/register
{
  "email": "customer@example.com",
  "phone": "+84123456789",
  "password": "hashedOrSentSecurely",
  "first_name": "John",
  "last_name": "Doe",
  "role": "CUSTOMER"
}
→ { user_id, email, phone, role, access_token, refresh_token, created_at }

POST /api/v1/auth/login
{ "email": "...", "password": "..." }
→ { access_token (JWT 24h), refresh_token, user }

POST /api/v1/auth/refresh
{ "refresh_token": "..." }
→ { access_token (new), refresh_token (rotated) }

# User Profile (NEW - Synced)
GET /api/v1/users/profile
→ { user_id, email, phone, first_name, last_name, avatar_url, role }

PUT /api/v1/users/profile
{ "first_name": "...", "last_name": "...", "avatar_url": "..." }
→ { updated user }

# User Addresses (NEW - Synced)
POST /api/v1/users/addresses
{ "label": "Home", "street": "...", "city_id": 1, "district": "...", "lat": 10.8, "lng": 106.7, "is_default": true }
→ { address_id, ... }

GET /api/v1/users/addresses
→ { addresses: [...] }

PUT /api/v1/users/addresses/{id}
{ "label": "Office", "is_default": true }
→ { updated address }

DELETE /api/v1/users/addresses/{id}
→ { success: true }

# User Payment Methods (NEW - Synced)
POST /api/v1/users/payment-methods
{ "type": "CARD", "provider": "stripe", "token": "tok_xxx", "last4": "4242", "is_default": true }
→ { payment_method_id, type, last4, is_default }

GET /api/v1/users/payment-methods
→ { payment_methods: [...] }

DELETE /api/v1/users/payment-methods/{id}
→ { success: true }
```

### 5.2 Catalog & Restaurant APIs (NEW - Synced)

```http
# Search Restaurants
GET /api/v1/restaurants?lat=10.8&lng=106.7&distance_km=5&keyword=pizza
?city_id=1&rating_min=3.5&sort=distance&page=1&page_size=10
→ {
  restaurants: [
    { id, name, description, lat, lng, rating, total_reviews, is_accepting_orders, min_order_value, est_delivery_time }
  ],
  total, page, page_size
}

# Restaurant Detail
GET /api/v1/restaurants/{id}
→ { id, name, description, street, lat, lng, rating, cuisines[], opening_hours[], is_accepting_orders, menu_categories[] }

# Restaurant Menu
GET /api/v1/restaurants/{id}/menu
→ {
  menu_categories: [
    { id, name, items: [{ id, name, description, price, image_url, variants: [...] }] }
  ]
}

# Restaurant Owner - Create Restaurant
POST /api/v1/restaurants
{ name, description, street, city_id, lat, lng, service_radius_km, cuisines[] }
→ { restaurant_id, status: 'PENDING' }

# Restaurant Owner - Update Restaurant
PUT /api/v1/restaurants/{id}
{ name, description, is_accepting_orders, opening_hours[] }
→ { updated restaurant }

# Restaurant Owner - Menu Management
POST /api/v1/restaurants/{id}/menu-categories
{ "name": "Appetizers", "sort_order": 1 }
→ { category_id, name, sort_order }

POST /api/v1/restaurants/{id}/menu-items
{ name, description, price, category_id, image_url, variants: [{ name, price_delta }] }
→ { menu_item_id }

PUT /api/v1/menu-items/{id}
{ name, price, is_available, image_url }
→ { updated menu_item }

DELETE /api/v1/menu-items/{id}
→ { success: true }

# Restaurant Owner - Toggle Status
PUT /api/v1/restaurants/{id}/status
{ is_accepting_orders: true/false }
→ { success: true }

# Discovery (NEW - Synced)
GET /api/v1/discovery?city_id=1
→ { featured: [...], trending: [...], promotions: [...] }

# Search
GET /api/v1/search?q=pizza&lat=10.8&lng=106.7&distance_km=3&sort=distance&page=1
→ { restaurants: [...], total, page, page_size }
```

### 5.3 Order APIs (Expanded - Synced)

```http
# Create Order
POST /api/v1/orders
{
  restaurant_id: UUID,
  delivery_address_id: UUID,
  delivery_type: "DELIVERY" | "PICKUP",
  items: [{ menu_item_id, quantity, selected_variants: [...] }],
  coupon_code?: "SAVE10",
  notes?: "No spicy"
}
→ {
  order_id, customer_id, restaurant_id, status: 'CREATED',
  items, subtotal, coupon_discount, tax_amount, delivery_fee, total_price,
  payment_method_id, estimated_delivery_time
}

# Get Order
GET /api/v1/orders/{id}
→ { full order details with items, delivery_task, payment_status }

# List Orders (NEW - Synced)
GET /api/v1/orders?customer_id=...&status=DELIVERED&limit=10&page=1
→ { orders: [...], total, page, page_size }

# Cancel Order
PUT /api/v1/orders/{id}/cancel
{ reason: "Changed my mind" }
→ { order_id, status: 'CANCELLED', refund_amount, refund_reason, refund_initiated_at }

# Reorder (NEW - Synced)
POST /api/v1/orders/{id}/reorder
{ delivery_address_id?: UUID }
→ { new_order_id, items (same as previous), total }

# Restaurant - Get Orders (NEW - Synced)
GET /api/v1/restaurants/{id}/orders?status=CONFIRMED&limit=20
→ { orders: [...], total, page }

# Restaurant - Update Order Status (NEW - Synced)
PUT /api/v1/restaurants/{id}/orders/{oid}/status
{ status: 'PREPARING' | 'READY_FOR_PICKUP' | 'CANCELLED_BY_RESTAURANT', reason?: "..." }
→ { order_id, status, reason }
```

### 5.4 Payment APIs (Expanded - Synced)

```http
# Authorize Payment
POST /api/v1/payments/authorize
{
  order_id: UUID,
  payment_method_id: UUID,
  amount: 150000,
  currency: "VND",
  idempotency_key: "hash(...)"
}
→ { payment_id, order_id, status: 'AUTHORIZED', gateway_transaction_id, authorized_at }

# Capture Payment
POST /api/v1/payments/{id}/capture
{ idempotency_key: "same as auth" }
→ { payment_id, status: 'CAPTURED', captured_at }

# Refund Payment (NEW - Synced)
POST /api/v1/payments/{id}/refund
{ amount: 150000, reason: "Order cancelled" }
→ { refund_id, payment_id, amount, reason, status: 'PENDING' }

# Payment Webhook (NEW - Synced)
POST /api/v1/webhooks/payment (from gateway)
{ gateway_transaction_id, status, timestamp, signature }
→ { received: true }
```

### 5.5 Delivery APIs (Expanded - Synced)

```http
# Driver Registration (NEW - Synced)
POST /api/v1/drivers/register
{
  user_id: UUID,
  vehicle_type: "BIKE" | "MOTORBIKE" | "CAR",
  vehicle_plate: "ABC123",
  license_number: "DL123456",
  document_urls: { front_id: "url", back_id: "url", license: "url" }
}
→ { driver_id, user_id, status: 'PENDING' }

# Driver Online/Offline Status (NEW - Synced)
PUT /api/v1/drivers/{id}/status
{ is_online: true/false }
→ { driver_id, is_online, current_location, available_tasks_count }

# Create Delivery Task (NEW - Synced)
POST /api/v1/delivery-tasks
{
  order_id: UUID,
  pickup_location: { lat, lng, address, contact },
  dropoff_location: { lat, lng, address, contact },
  est_delivery_time: "ISO8601"
}
→ { delivery_task_id, order_id, status: 'CREATED' }

# Get Delivery Tasks
GET /api/v1/delivery-tasks?driver_id=...&status=ASSIGNED
→ { delivery_tasks: [...] }

# Update Delivery Task Status
PUT /api/v1/delivery-tasks/{id}/status
{ status: 'ASSIGNED' | 'PICKED_UP' | 'IN_TRANSIT' | 'DELIVERED' | 'CANCELLED' }
→ { delivery_task_id, status, updated_at }

# Update Driver Location
PUT /api/v1/drivers/{id}/location
{ lat: 10.81, lng: 106.71, timestamp: "ISO8601" }
→ { driver_id, current_location, updated_at }

# Driver Earnings (NEW - Synced)
GET /api/v1/drivers/{id}/earnings?from_date=2026-01-01&to_date=2026-01-31
→ {
  total_earnings: 5000000,  // VND
  total_trips: 50,
  breakdown: [{ date, earnings, trips, avg_rating }]
}
```

### 5.6 Rating APIs (NEW - Synced)

```http
# Rate Restaurant
POST /api/v1/restaurants/{id}/ratings
{
  order_id: UUID,
  score: 5,
  comment: "Great food and fast delivery!",
  rating_type: "RESTAURANT"
}
→ { rating_id, order_id, score, comment, created_at }

# Get Restaurant Ratings
GET /api/v1/restaurants/{id}/ratings?limit=10&page=1
→ {
  ratings: [{ rating_id, rater_id, rater_name, score, comment, created_at }],
  total, average_score
}

# Rate Driver
POST /api/v1/drivers/{id}/ratings
{
  order_id: UUID,
  score: 4,
  comment: "Driver was friendly",
  rating_type: "DRIVER"
}
→ { rating_id, order_id, score, comment, created_at }

# Get Driver Ratings
GET /api/v1/drivers/{id}/ratings?limit=10&page=1
→ { ratings: [...], total, average_score }
```

### 5.7 Notification APIs (NEW - Synced)

```http
# Get Notifications
GET /api/v1/notifications?user_id=...&limit=20&offset=0
→ {
  notifications: [
    { id, type, title, message, read, created_at, action_url? }
  ],
  total, unread_count
}

# Mark Notification as Read
PUT /api/v1/notifications/{id}/read
→ { success: true }

# Mark All as Read
PUT /api/v1/notifications/read-all
→ { success: true, count: 15 }

# Get Notification Preferences
GET /api/v1/notification-preferences?user_id=...
→ {
  preferences: [
    { channel: "PUSH", type: "ORDER_STATUS", enabled: true },
    { channel: "SMS", type: "PROMO", enabled: false },
    { channel: "EMAIL", type: "RECEIPT", enabled: true }
  ]
}

# Update Notification Preferences
PUT /api/v1/notification-preferences
{
  preferences: [
    { channel: "PUSH", type: "ORDER_STATUS", enabled: true },
    { channel: "SMS", type: "PROMO", enabled: false }
  ]
}
→ { success: true }
```

### 5.8 Admin APIs (NEW - Synced)

```http
# Dashboard
GET /api/v1/admin/dashboard?city_id=1&from_date=2026-01-01&to_date=2026-01-31
→ {
  metrics: {
    total_orders: 5000,
    total_revenue: 1500000000,  // VND
    active_users: 50000,
    average_order_value: 300000,
    on_time_delivery_rate: 0.95,
    avg_rating: 4.6,
    new_customers: 1200,
    new_restaurants: 50,
    active_drivers: 500
  }
}

# User Management
GET /api/v1/admin/users?role=CUSTOMER&status=active&limit=20&page=1
→ { users: [...], total, page }

PUT /api/v1/admin/users/{id}/suspend
{ reason: "Violation of terms", duration_days: 30 }
→ { user_id, status: 'SUSPENDED', suspended_until }

PUT /api/v1/admin/users/{id}/activate
→ { user_id, status: 'ACTIVE' }

# Restaurant Management
GET /api/v1/admin/restaurants?status=PENDING&limit=20
→ { restaurants: [...], total, page }

PUT /api/v1/admin/restaurants/{id}/approve
{ notes: "KYC verified" }
→ { restaurant_id, status: 'ACTIVE' }

PUT /api/v1/admin/restaurants/{id}/reject
{ reason: "Invalid documents" }
→ { restaurant_id, status: 'REJECTED' }

PUT /api/v1/admin/restaurants/{id}/suspend
{ reason: "Multiple complaints", duration_days: 7 }
→ { restaurant_id, status: 'SUSPENDED' }

# Driver Management
GET /api/v1/admin/drivers?status=PENDING&limit=20
→ { drivers: [...], total, page }

PUT /api/v1/admin/drivers/{id}/approve
{ notes: "Documents verified" }
→ { driver_id, status: 'APPROVED' }

PUT /api/v1/admin/drivers/{id}/reject
{ reason: "Invalid license" }
→ { driver_id, status: 'REJECTED' }

# Payment Reconciliation
GET /api/v1/admin/payments/reconciliation?date=2026-01-20
→ {
  reconciled: 450,
  pending: 5,
  discrepancies: [{ payment_id, expected_amount, actual_amount, status, reason }]
}

# Coupon Management
POST /api/v1/admin/coupons
{
  code: "NEWYEAR2026",
  type: "PERCENT",
  discount_value: 20,
  min_order_value: 100000,
  max_discount: 50000,
  per_user_usage_limit: 2,
  global_usage_limit: 1000,
  start_time: "2026-01-01T00:00:00Z",
  end_time: "2026-01-31T23:59:59Z",
  city_id: 1
}
→ { coupon_id, code, status: 'active' }

GET /api/v1/admin/coupons?is_active=true&limit=20
→ { coupons: [...], total }

PUT /api/v1/admin/coupons/{id}
{ is_active: false }
→ { coupon_id, is_active: false }

# Reports
GET /api/v1/admin/reports/revenue?city_id=1&granularity=daily&from_date=2026-01-01&to_date=2026-01-31
→ {
  data: [{ date, revenue, orders, avg_order_value, top_restaurants: [...] }],
  summary: { total_revenue, total_orders, avg_daily_revenue }
}

GET /api/v1/admin/reports/orders?city_id=1&granularity=hourly&date=2026-01-20
→ {
  data: [{ hour, orders, revenue, cancellation_rate }],
  peak_hours: ["12:00", "19:00"]
}

GET /api/v1/admin/reports/sla?from_date=2026-01-01&to_date=2026-01-31
→ {
  on_time_delivery_rate: 0.95,
  avg_delivery_time_minutes: 35,
  sla_breaches: 120,
  by_restaurant: [...],
  by_driver: [...]
}

# System Configuration
GET /api/v1/admin/config
→ { delivery_fee_base, delivery_fee_per_km, min_order_value, tax_rate, ... }

PUT /api/v1/admin/config
{ delivery_fee_base: 15000, delivery_fee_per_km: 3000 }
→ { success: true, updated_fields: [...] }
```

### 5.9 Dispute APIs (P0)

```http
# Create Dispute
POST /api/v1/disputes
{
  order_id: UUID, 
  category: "missing_item|wrong_item|quality|late_delivery|driver_behavior",
  description: "max 500 chars",
  photo_urls?: ["url1", "url2"]
}
→ {
  dispute_id, 
  status: "open", 
  estimated_resolution: "24 hours",
  auto_resolved?: boolean,
  compensation?: { type, amount }
}

# Get Dispute Detail
GET /api/v1/disputes/{id}
→ { 
  dispute_id, order_id, customer_id, category, description, photo_urls,
  status, resolution_type, resolution_amount, resolved_by, resolved_at,
  timeline: [{ event, timestamp, actor }],
  created_at, updated_at
}

# List Disputes
GET /api/v1/disputes?customer_id=...&status=open&limit=10&page=1
→ { disputes: [...], pagination }

# Resolve Dispute (Admin only)
PUT /api/v1/disputes/{id}/resolve
{
  resolution_type: "full_refund|partial_refund|discount_code|no_action",
  resolution_amount?: number,
  resolution_notes: "string"
}
→ { dispute_id, status: "resolved", resolution }
```

### 5.10 WebSocket Events API (P0)

**Connection:**
```
wss://api.fooddelivery.com/ws?token={jwt_token}
```

**Client Messages:**
```json
// Subscribe to order updates
{"type": "subscribe", "channel": "order:{order_id}"}

// Subscribe to driver location
{"type": "subscribe", "channel": "driver:location:{order_id}"}

// Unsubscribe
{"type": "unsubscribe", "channel": "order:{order_id}"}

// Keep-alive
{"type": "ping"}
```

**Server Messages:**
```json
// Order status change
{
  "type": "order_status",
  "data": {
    "order_id": "uuid",
    "status": "PREPARING|READY|PICKED_UP|ON_THE_WAY|DELIVERED",
    "updated_at": "ISO8601"
  }
}

// Driver location update (every 5s when ON_THE_WAY)
{
  "type": "driver_location",
  "data": {
    "order_id": "uuid",
    "lat": 10.8231,
    "lng": 106.6297,
    "eta_minutes": 12,
    "distance_km": 2.5
  }
}

// Connection acknowledgment
{"type": "pong"}

// Subscription confirmation
{"type": "subscribed", "channel": "order:12345"}
```

---

## 6. TESTING & QUALITY STRATEGY

### 6.1 Test Pyramid

```
         / \
        /E2E \       5-10% (Playwright)
       /______\
      /         \
     /Integration\  20-30% (testify + Docker)
    /____________\
   /               \
  / Unit Tests 80%  /
 /___________________\
```

### 6.2 Test Coverage Goals

- **Unit:** ≥80% (business logic, domain models)
- **Integration:** ≥60% (core workflows: order → payment → delivery)
- **E2E:** ≥40% (critical journeys: signup → search → order → track)

### 6.3 Key Test Scenarios

**Critical Paths:**
1. Customer: register → search → order → pay → track → rate
2. Restaurant: accept order → prepare → mark ready
3. Driver: go online → receive task → pickup → deliver
4. Payment: idempotency, no double-charge, refund on cancellation
5. SLA: delivery on-time, alert if late

---

## 7. SECURITY REQUIREMENTS

### 7.1 Authentication (UPDATED - P0: JWT RS256)

**JWT Configuration:**
- **Algorithm:** RS256 (asymmetric) - **Changed from HS256**
  - *Reason:* HS256 shares secret across services → single point of compromise
  - *RS256:* Private key only in Auth Service, public key distributed to other services
- **Token TTL:** Access token 24 hours, Refresh token 30 days
- **Refresh token rotation:** New refresh token issued on each use, old one invalidated
- **Token storage:** 
  - Web: Secure HTTP-only cookie with SameSite=Strict
  - Mobile (React Native): 
    - iOS: iOS Keychain via react-native-keychain
    - Android: Android Keystore via react-native-keychain

**JWT Payload Structure:**
```json
{
  "sub": "user_uuid",
  "role": "customer|restaurant_owner|driver|admin",
  "email": "user@example.com",
  "permissions": ["read:orders", "write:orders"],
  "iat": 1640000000,
  "exp": 1640086400,
  "jti": "unique_token_id"
}
```

**Key Management:**
- RSA key pair: 2048-bit minimum
- Key rotation: Every 90 days
- Public key endpoint: `GET /api/v1/.well-known/jwks.json`
- Support for multiple active keys during rotation period

### 7.2 Authorization

- Role-based access control (RBAC)
- Row-level security for multi-tenant data
- Customer can only access own orders/addresses
- Driver can only accept/track assigned deliveries
- Admin has read/write access to all resources

### 7.3 Data Protection

- TLS 1.3 for all traffic
- AES-256 encryption for PII (at-rest)
- Tokenization via payment gateway (no raw card data)

**GDPR Compliance Requirements (EXPANDED - P0):**

| Requirement | Implementation |
|:------------|:---------------|
| **Data Export** | `GET /api/v1/users/me/export` - Download all user data in JSON/CSV |
| **Data Deletion** | `DELETE /api/v1/users/me` - Right to be forgotten (30-day grace period) |
| **Consent Management** | Explicit opt-in for marketing, tracking; granular preferences |
| **Data Retention** | Auto-delete inactive accounts after 2 years; anonymize after deletion |
| **Access Logging** | Log all PII access with timestamp, accessor, purpose |
| **Data Minimization** | Collect only necessary data; mask sensitive fields in logs |

**Data Retention Policy:**

| Data Type | Retention Period | After Expiry |
|:----------|:-----------------|:-------------|
| Order history | 3 years | Anonymize customer info |
| Payment records | 7 years (legal) | Archive to cold storage |
| Location history | 30 days | Auto-delete |
| Audit logs | 6 months hot, 1 year cold | Archive then delete |
| Support tickets | 2 years | Anonymize |

### 7.4 Compliance

- **PCI-DSS:** No raw card data storage
- **GDPR:** User data subject to privacy laws
- **Vietnam:** Data residency, tax compliance

---

## 8. DEPLOYMENT & OPERATIONS

### 8.1 Infrastructure

- **Orchestration:** Kubernetes (EKS/GKE)
- **CI/CD:** GitHub Actions / GitLab CI → Docker → Kubernetes
- **Image Registry:** ECR / Artifact Registry
- **Configuration:** Helm charts
- **GitOps:** ArgoCD for declarative deployment

### 8.2 Deployment Strategy

- **Blue-Green:** Route traffic gradually to new version
- **Canary:** 10% → 50% → 100% traffic shift
- **Rollback:** Automatic if SLO breached
- **Frequency:** 1-2x per week (MVP), daily (Phase 2+)

### 8.3 Monitoring & Alerting

- **On-call:** Weekly rotation, 24/7 coverage
- **Incident Response:** P0 war room within 15 min
- **SLA Dashboard:** Real-time uptime, latency, error rate
- **Alert Escalation:** Slack → SMS → phone call (P0)

### 8.4 Disaster Recovery

- **RTO:** 30 min (Recovery Time Objective)
- **RPO:** 0 (Recovery Point Objective for orders/payments)
- **Daily Backups:** PostgreSQL snapshots
- **DR Test:** Quarterly drills
- **Multi-region:** Phase 2+

---

## 9. CHANGE LOG & TRACEABILITY

### 9.1 Version 2.1 Changes (P0 Updates)

| Change ID | Section | Description | BRD/PRD Reference |
|:----------|:--------|:------------|:------------------|
| P0-001 | 1.3 Order Service | Added FR-ORD-11 to FR-ORD-14 for exception flows | BRD 5.2 Flow E, F, G |
| P0-002 | 1.4 Payment Service | Added FR-PAY-10 to FR-PAY-12 for disputes | BRD 5.2 Flow I |
| P0-003 | 1.5 Delivery Service | Added FR-DEL-10 to FR-DEL-12 for emergency handling | BRD 5.2 Flow H |
| P0-004 | 1.11 Dispute Service | New service for dispute lifecycle | PRD 3.8 EP-DISPUTE-01 |
| P0-005 | 3.2 WebSocket Architecture | Real-time layer specification | PRD US-TRK-01.1 |
| P0-006 | 3.3 Saga Compensation | Failure handling for each saga step | BRD 5.2 all flows |
| P0-007 | 4.1 Data Model | Added Disputes, Audit Logs, Driver Location History | BRD requirement |
| P0-008 | 4.2 Indexes | Added 8 new indexes for new entities | Performance optimization |
| P0-009 | 5.0 Error Schema | Standardized error response format | API consistency |
| P0-010 | 5.6 Dispute APIs | New endpoints for dispute management | FR-DISPUTE-* |
| P0-011 | 5.7 WebSocket API | Real-time event contract specification | FR-DEL-06 |
| P0-012 | 7.1 Authentication | Changed from HS256 to RS256 | Security best practice |
| P0-013 | 7.3 GDPR | Expanded data protection requirements | Compliance |
| P0-014 | 2.4 Security Headers | Mandatory HTTP security headers | OWASP |

### 9.2 Version 2.2 Changes (Sync with Food_Delivery_Full.md)

| Change ID | Section | Description | Source |
|:----------|:--------|:------------|:-------|
| SYNC-001 | 4.1 Data Model | Full PostgreSQL DDL for all 17 tables | Food_Delivery_Full.md Section 9 |
| SYNC-002 | 4.1 | Added cities table | Food_Delivery_Full.md |
| SYNC-003 | 4.1 | Added refresh_tokens table | Food_Delivery_Full.md |
| SYNC-004 | 4.1 | Added user_payment_methods table | Food_Delivery_Full.md |
| SYNC-005 | 4.1 | Added menu_categories table | Food_Delivery_Full.md |
| SYNC-006 | 4.1 | Added menu_item_variants table | Food_Delivery_Full.md |
| SYNC-007 | 4.1 | Added coupon_usages table | Food_Delivery_Full.md |
| SYNC-008 | 4.1 | Added order_items, order_item_variants tables | Food_Delivery_Full.md |
| SYNC-009 | 4.1 | Added payment_refunds table | Food_Delivery_Full.md |
| SYNC-010 | 4.1 | Added drivers table | Food_Delivery_Full.md |
| SYNC-011 | 4.1 | Added delivery_task_events table | Food_Delivery_Full.md |
| SYNC-012 | 4.1 | Added order_events table | Food_Delivery_Full.md |
| SYNC-013 | 4.2 | Full index definitions for all tables | Food_Delivery_Full.md |
| SYNC-014 | 5.1 | Expanded Auth APIs (profile, addresses, payment methods) | Food_Delivery_Full.md Section 10.1 |
| SYNC-015 | 5.2 | Full Catalog & Restaurant APIs | Food_Delivery_Full.md Section 10.2 |
| SYNC-016 | 5.3 | Expanded Order APIs (list, reorder, restaurant orders) | Food_Delivery_Full.md Section 10.3 |
| SYNC-017 | 5.4 | Added refund and webhook APIs | Food_Delivery_Full.md Section 10.4 |
| SYNC-018 | 5.5 | Expanded Delivery APIs (driver register, status, earnings) | Food_Delivery_Full.md Section 10.5 |
| SYNC-019 | 5.6 | Added Rating APIs | Food_Delivery_Full.md Section 10.8 |
| SYNC-020 | 5.7 | Added Notification APIs | Food_Delivery_Full.md Section 10.7 |
| SYNC-021 | 5.8 | Added Admin APIs (dashboard, management, reports) | Food_Delivery_Full.md Section 10.9 |

### 9.3 Traceability Matrix (BRD → SRS)

| BRD Section | BRD ID | SRS FR | Status |
|:------------|:-------|:-------|:------:|
| 5.2 Flow E: Customer Unreachable | BR-DRIVER-002 | FR-ORD-11, FR-DEL-11 | ✅ Added |
| 5.2 Flow F: Incorrect Address | BR-PRI-002 | FR-ORD-12, FR-DEL-12 | ✅ Added |
| 5.2 Flow G: Food Quality Issue | BR-CANCEL-002 | FR-DISPUTE-01~09 | ✅ Added |
| 5.2 Flow H: Driver Emergency | BR-DRIVER-001 | FR-DEL-10 | ✅ Added |
| 5.2 Flow I: Payment Dispute | BR-PAY-001 | FR-PAY-10~12 | ✅ Added |
| 6.3 Cancellation Rules | BR-CANCEL-001~003 | FR-ORD-14 | ✅ Added |

### 9.4 Sync Status (SRS vs Food_Delivery_Full.md)

| Component | Status | Notes |
|:----------|:------:|:------|
| Database Schema | ✅ Synced | All 17 tables with full DDL |
| API Contracts | ✅ Synced | All endpoints from both documents |
| Indexes | ✅ Synced | Complete index definitions |
| Error Schema | ✅ SRS only | P0 addition, needs to add to Full |
| WebSocket API | ✅ SRS only | P0 addition, needs to add to Full |
| Dispute Service | ✅ SRS only | P0 addition, needs to add to Full |

---

## CONCLUSION

SRS v2.2 provides comprehensive technical specification for Food Delivery Platform MVP. This version:

**Version 2.1 Additions (P0):**
1. ✅ **Exception Flow FRs** - Full coverage of BRD Section 5.2 flows
2. ✅ **WebSocket Architecture** - Real-time tracking infrastructure defined
3. ✅ **Dispute/Audit Tables** - Data model complete for compliance
4. ✅ **Error Response Schema** - API consistency ensured
5. ✅ **JWT RS256** - Security hardened with asymmetric signing

**Version 2.2 Additions (Sync):**
6. ✅ **Full Database Schema** - 17 tables with complete PostgreSQL DDL
7. ✅ **Complete Index Definitions** - All indexes for performance optimization
8. ✅ **Expanded API Contracts** - All endpoints synced with Food_Delivery_Full.md
9. ✅ **Rating APIs** - Restaurant and Driver rating endpoints
10. ✅ **Notification APIs** - Push, SMS, email preference management
11. ✅ **Admin APIs** - Dashboard, user/restaurant/driver management, reports

Implementation follows microservices architecture with event-driven patterns for scalability and reliability.

**Next Steps:**
1. Engineering review & feasibility sign-off (1 week)
2. Database schema finalization (1 week)
3. API contract testing setup (2 weeks)
4. Unit test framework & guidelines (1 week)
5. Sprint planning & task breakdown (Week 2)
6. Sync P0 additions back to Food_Delivery_Full.md

---

**Document History:**

| Version | Date | Author | Changes |
|:--------|:-----|:-------|:--------|
| 2.0 | 20 Jan 2026 | Tech Lead | Initial SRS |
| 2.1 | 21 Jan 2026 | Solution Architect | P0 updates - Exception Flows, WebSocket, Dispute, Error Schema, JWT RS256 |
| 2.2 | 21 Jan 2026 | Solution Architect | Synced with Food_Delivery_Full.md - Full Database Schema, Complete API Contracts |