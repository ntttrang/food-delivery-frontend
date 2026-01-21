---
name: Food Delivery MVP Sprint Plan
overview: Sprint planning for Food Delivery MVP covering Product Goal, Product Backlog with prioritized epics/user stories, and detailed Sprint breakdown with development tasks for the core order flow (Register, Search, Order, Payment, Delivery, Rating).
todos:
  - id: sprint-0
    content: "Sprint 0: Foundation - Setup infrastructure, CI/CD, base project structure"
    status: pending
  - id: sprint-1
    content: "Sprint 1: User Service - Auth, registration, addresses, payment methods"
    status: pending
  - id: sprint-2
    content: "Sprint 2: Catalog Service - Restaurant registration, menu management"
    status: pending
  - id: sprint-3
    content: "Sprint 3: Search Service + Order Part 1 - Geo-search, cart, coupons"
    status: pending
  - id: sprint-4
    content: "Sprint 4: Order Part 2 + Payment - Order placement, payment processing"
    status: pending
  - id: sprint-5
    content: "Sprint 5: Delivery Service + WebSocket - Driver management, real-time tracking"
    status: pending
  - id: sprint-6
    content: "Sprint 6: Notifications + Saga - Push notifications, distributed transactions"
    status: pending
  - id: sprint-7
    content: "Sprint 7: Rating + Admin - Rating system, admin dashboard, polish"
    status: pending
  - id: sprint-8
    content: "Sprint 8: Testing + Launch - E2E testing, security audit, production deployment"
    status: pending
isProject: false
---

# Food Delivery MVP Sprint Plan

## Product Goal (Release Goal)

**Goal Statement:** Launch a functional food delivery platform in Ho Chi Minh City that enables customers to discover restaurants, place orders, pay securely, and track deliveries in real-time.

**Target Metrics (End of MVP):**

- 50k-100k customers
- 1k-2k restaurants
- 500-1k drivers
- 3k-5k concurrent users
- 99.5% uptime, <500ms API latency

---

## Product Backlog

### Epic 1: Identity & Access Management (Priority: P0)


| ID         | User Story                                       | Priority | Dependencies |
| ---------- | ------------------------------------------------ | -------- | ------------ |
| US-AUTH-01 | As a user, I can register with email/phone + OTP | P0       | None         |
| US-AUTH-02 | As a user, I can login and receive JWT tokens    | P0       | US-AUTH-01   |
| US-AUTH-03 | As a user, I can reset my password               | P1       | US-AUTH-01   |
| US-AUTH-04 | As a user, I can manage my profile               | P1       | US-AUTH-02   |
| US-AUTH-05 | As a user, I can manage delivery addresses       | P0       | US-AUTH-02   |
| US-AUTH-06 | As a user, I can add payment methods             | P0       | US-AUTH-02   |


### Epic 2: Restaurant & Menu Catalog (Priority: P0)


| ID        | User Story                                                   | Priority | Dependencies |
| --------- | ------------------------------------------------------------ | -------- | ------------ |
| US-CAT-01 | As a restaurant owner, I can register my restaurant          | P0       | US-AUTH-01   |
| US-CAT-02 | As a restaurant owner, I can manage menu categories          | P0       | US-CAT-01    |
| US-CAT-03 | As a restaurant owner, I can manage menu items with variants | P0       | US-CAT-02    |
| US-CAT-04 | As a restaurant owner, I can toggle accepting orders         | P0       | US-CAT-01    |
| US-CAT-05 | As a customer, I can view restaurant details and menu        | P0       | US-CAT-03    |


### Epic 3: Search & Discovery (Priority: P0)


| ID           | User Story                                                   | Priority | Dependencies |
| ------------ | ------------------------------------------------------------ | -------- | ------------ |
| US-SEARCH-01 | As a customer, I can search restaurants by location          | P0       | US-CAT-01    |
| US-SEARCH-02 | As a customer, I can filter by rating, distance, open status | P0       | US-SEARCH-01 |
| US-SEARCH-03 | As a customer, I can see search results with pagination      | P1       | US-SEARCH-01 |


### Epic 4: Order Management (Priority: P0)


| ID        | User Story                                                    | Priority | Dependencies          |
| --------- | ------------------------------------------------------------- | -------- | --------------------- |
| US-ORD-01 | As a customer, I can add items to cart                        | P0       | US-CAT-05             |
| US-ORD-02 | As a customer, I can apply coupon codes                       | P0       | US-ORD-01             |
| US-ORD-03 | As a customer, I can place an order                           | P0       | US-ORD-01, US-AUTH-05 |
| US-ORD-04 | As a customer, I can view order history                       | P1       | US-ORD-03             |
| US-ORD-05 | As a customer, I can cancel order before restaurant accepts   | P0       | US-ORD-03             |
| US-ORD-06 | As a customer, I can reorder from history                     | P1       | US-ORD-04             |
| US-ORD-07 | As a restaurant, I can view and accept/reject orders          | P0       | US-ORD-03             |
| US-ORD-08 | As a restaurant, I can update order status (preparing, ready) | P0       | US-ORD-07             |


### Epic 5: Payment Processing (Priority: P0)


| ID        | User Story                                             | Priority | Dependencies          |
| --------- | ------------------------------------------------------ | -------- | --------------------- |
| US-PAY-01 | As a customer, I can pay with COD                      | P0       | US-ORD-03             |
| US-PAY-02 | As a customer, I can pay with card (Stripe/VNPay)      | P0       | US-ORD-03, US-AUTH-06 |
| US-PAY-03 | As a system, I handle refunds on cancellation          | P0       | US-ORD-05             |
| US-PAY-04 | As a system, I prevent double-charges with idempotency | P0       | US-PAY-02             |


### Epic 6: Delivery & Tracking (Priority: P0)


| ID        | User Story                                           | Priority | Dependencies |
| --------- | ---------------------------------------------------- | -------- | ------------ |
| US-DEL-01 | As a driver, I can register with documents           | P0       | US-AUTH-01   |
| US-DEL-02 | As a driver, I can go online/offline                 | P0       | US-DEL-01    |
| US-DEL-03 | As a driver, I can receive and accept delivery tasks | P0       | US-DEL-02    |
| US-DEL-04 | As a driver, I can update delivery status            | P0       | US-DEL-03    |
| US-DEL-05 | As a customer, I can track order status in real-time | P0       | US-DEL-04    |
| US-DEL-06 | As a customer, I can see driver location on map      | P0       | US-DEL-05    |
| US-DEL-07 | As a driver, I can view my earnings                  | P1       | US-DEL-04    |


### Epic 7: Notifications (Priority: P0)


| ID          | User Story                                                | Priority | Dependencies |
| ----------- | --------------------------------------------------------- | -------- | ------------ |
| US-NOTIF-01 | As a user, I receive push notifications on status changes | P0       | US-ORD-03    |
| US-NOTIF-02 | As a user, I receive SMS for critical events              | P1       | US-NOTIF-01  |


### Epic 8: Rating & Review (Priority: P1)


| ID         | User Story                                          | Priority | Dependencies |
| ---------- | --------------------------------------------------- | -------- | ------------ |
| US-RATE-01 | As a customer, I can rate restaurant after delivery | P1       | US-ORD-03    |
| US-RATE-02 | As a customer, I can rate driver after delivery     | P1       | US-DEL-04    |


### Epic 9: Admin Portal (Priority: P1)


| ID        | User Story                                    | Priority | Dependencies |
| --------- | --------------------------------------------- | -------- | ------------ |
| US-ADM-01 | As an admin, I can view dashboard KPIs        | P1       | All services |
| US-ADM-02 | As an admin, I can approve/reject restaurants | P0       | US-CAT-01    |
| US-ADM-03 | As an admin, I can approve/reject drivers     | P0       | US-DEL-01    |
| US-ADM-04 | As an admin, I can manage coupons             | P1       | US-ORD-02    |


### Epic 10: Dispute Management (Priority: P0)


| ID            | User Story                                                          | Priority | Dependencies |
| ------------- | ------------------------------------------------------------------- | -------- | ------------ |
| US-DISPUTE-01 | As a customer, I can create a dispute ticket within 24h of delivery | P0       | US-ORD-03    |
| US-DISPUTE-02 | As a customer, I can upload photo evidence for disputes             | P0       | US-DISPUTE-01|
| US-DISPUTE-03 | As an admin, I can review and resolve disputes                      | P0       | US-DISPUTE-01|


### Epic 11: Exception Flows (Priority: P0)


| ID        | User Story                                                         | Priority | Dependencies |
| --------- | ------------------------------------------------------------------ | -------- | ------------ |
| US-EXC-01 | As a driver, I can mark customer unreachable after 3 call attempts | P0       | US-DEL-04    |
| US-EXC-02 | As a driver, I can report address mismatch and request correction  | P0       | US-DEL-04    |
| US-EXC-03 | As a system, I auto-cancel orders when SLA miss >60min             | P0       | US-ORD-03    |
| US-EXC-04 | As a driver, I can report emergency and trigger reassignment       | P1       | US-DEL-03    |


---

## Sprint Planning

### Sprint 0: Foundation (2 weeks)

**Goal:** Setup infrastructure and development environment

**User Stories:** N/A (Infrastructure setup sprint)

**Development Tasks:**

*Backend Tasks:*

| Task       | Description                                                       | Est |
| ---------- | ----------------------------------------------------------------- | --- |
| INFRA-001  | Setup Git repository with branching strategy                      | 2h  |
| INFRA-002  | Setup Docker Compose for local development (PostgreSQL, Redis, Kafka) | 4h  |
| INFRA-003  | Create Kubernetes manifests (Helm charts)                         | 8h  |
| INFRA-004  | Setup CI/CD pipeline (GitHub Actions → Docker Hub → AWS)          | 8h  |
| INFRA-005  | Database migration framework setup (golang-migrate)               | 4h  |
| INFRA-006  | Create base project structure for microservices                   | 6h  |
| INFRA-007  | Setup API Gateway (Nginx/Envoy) with basic routing                | 6h  |
| INFRA-008  | Configure observability stack (Prometheus, Grafana, ELK)          | 8h  |
| INFRA-009  | Create shared Go libraries (logging, errors, middleware)          | 8h  |
| INFRA-010  | Setup JWKS endpoint for JWT RS256 verification                    | 4h  |
| SEC-001    | Security headers middleware (X-Content-Type-Options, HSTS, CSP)   | 4h  |
| INFRA-011  | Audit logging infrastructure setup                                | 4h  |
| INFRA-012  | Redis Pub/Sub verification for WebSocket scaling                  | 4h  |
| DB-000     | Create `cities` and `audit_logs` base tables                      | 3h  |

*Frontend Tasks:*

| Task        | Description                                                     | Est |
| ----------- | --------------------------------------------------------------- | --- |
| [Front]-001 | Setup React Native monorepo (Customer, Restaurant, Driver apps) | 8h  |
| [Front]-002 | Setup React Admin Dashboard project with Vite                   | 4h  |
| [Front]-003 | Configure shared component library (design tokens, themes)      | 6h  |
| [Front]-004 | Setup navigation structure for all mobile apps                  | 6h  |
| [Front]-005 | Configure API client with Axios/React Query + interceptors      | 4h  |
| [Front]-006 | Setup CI/CD for mobile builds (EAS Build / Fastlane)            | 8h  |
| [Front]-007 | Create base UI components (Button, Input, Card, Badge)          | 8h  |

**Deliverables:**

- Working local dev environment
- CI/CD pipeline deploying to staging
- Base service templates
- Security middleware configured

---

### Sprint 1: User Service (2 weeks)

**Goal:** Complete identity and access management

**User Stories:** US-AUTH-01, US-AUTH-02, US-AUTH-03, US-AUTH-05, US-AUTH-06

**Development Tasks:**

*Backend Tasks:*

| Task     | Description                                                                       | Est |
| -------- | --------------------------------------------------------------------------------- | --- |
| DB-001   | Create `users`, `user_addresses`, `user_payment_methods`, `refresh_tokens` tables | 4h  |
| API-001  | POST `/api/v1/auth/register` - Email/phone registration                           | 8h  |
| API-002  | POST `/api/v1/auth/login` - JWT RS256 token generation                            | 8h  |
| API-003  | POST `/api/v1/auth/refresh` - Refresh token rotation                              | 4h  |
| API-004  | CRUD `/api/v1/users/addresses` - Delivery addresses                               | 6h  |
| API-005  | CRUD `/api/v1/users/payment-methods` - Tokenized payment                          | 6h  |
| API-006  | POST `/api/v1/auth/password-reset` - Password reset with OTP                      | 4h  |
| INT-001  | OTP service integration (Twilio SMS)                                              | 4h  |
| INT-002  | Redis integration for JWT blacklist                                               | 4h  |
| TEST-001 | Unit tests for auth logic (80% coverage)                                          | 8h  |
| TEST-002 | Integration tests for auth flow                                                   | 4h  |

*Frontend Tasks:*

| Task        | Description                                             | Est |
| ----------- | ------------------------------------------------------- | --- |
| [Front]-008 | Customer: Splash + Onboarding screens (4 screens)       | 6h  |
| [Front]-009 | Customer: Login screen with form validation             | 4h  |
| [Front]-010 | Customer: Registration screen with OTP verification     | 6h  |
| [Front]-011 | Customer: Profile screen                                | 4h  |
| [Front]-012 | Customer: Saved Addresses screen (CRUD)                 | 6h  |
| [Front]-013 | Customer: Payment Methods screen (tokenized cards)      | 6h  |
| [Front]-014 | Restaurant: Login/Registration screens                  | 4h  |
| [Front]-015 | Driver: Login/Registration screens                      | 4h  |
| [Front]-016 | Shared: Auth state management (Zustand/Redux)           | 4h  |
| [Front]-017 | Shared: Secure token storage (AsyncStorage/SecureStore) | 4h  |

**Deliverables:**

- Fully functional user authentication (register, login, logout)
- JWT-based session management with refresh tokens
- Address and payment method management APIs
- OTP verification flow via SMS
- Schema Reference: `[SRS_FoodDelivery.md](SRS_FoodDelivery.md)` lines 571-643

---

### Sprint 2: Catalog Service (2 weeks)

**Goal:** Restaurant registration and menu management

**User Stories:** US-CAT-01, US-CAT-02, US-CAT-03, US-CAT-04, US-CAT-05, US-ADM-02

**Development Tasks:**

*Backend Tasks:*

| Task      | Description                                                                        | Est |
| --------- | ---------------------------------------------------------------------------------- | --- |
| DB-002    | Create `restaurants`, `menu_categories`, `menu_items`, `menu_item_variants` tables | 4h  |
| API-007   | POST `/api/v1/restaurants` - Restaurant registration                               | 6h  |
| API-008   | GET `/api/v1/restaurants/{id}` - Restaurant detail                                 | 4h  |
| API-009   | CRUD `/api/v1/restaurants/{id}/menu-categories`                                    | 6h  |
| API-010   | CRUD `/api/v1/restaurants/{id}/menu-items` with variants                           | 8h  |
| API-011   | PUT `/api/v1/restaurants/{id}/status` - Toggle accepting orders                    | 3h  |
| API-012   | GET `/api/v1/restaurants/{id}/menu` - Full menu view                               | 4h  |
| API-013   | Admin restaurant approval endpoints (PENDING → APPROVED/REJECTED)                  | 6h  |
| INT-003   | S3/MinIO integration for image upload                                              | 6h  |
| CACHE-001 | Redis cache for restaurant/menu data                                               | 4h  |
| TEST-003  | Unit + integration tests                                                           | 8h  |

*Frontend Tasks:*

| Task        | Description                                            | Est |
| ----------- | ------------------------------------------------------ | --- |
| [Front]-018 | Customer: Home screen with featured restaurants        | 8h  |
| [Front]-019 | Customer: Restaurant Detail screen with tabs           | 8h  |
| [Front]-020 | Customer: Food Item Detail modal/bottom sheet          | 4h  |
| [Front]-021 | Restaurant: Dashboard screen                           | 6h  |
| [Front]-022 | Restaurant: Menu List screen                           | 6h  |
| [Front]-023 | Restaurant: Add/Edit Menu Item modal with variants     | 8h  |
| [Front]-024 | Restaurant: Category Management modal                  | 4h  |
| [Front]-025 | Restaurant: Settings screen (toggle accepting orders)  | 4h  |
| [Front]-026 | Admin: Restaurant Management screen (approve/reject)   | 8h  |
| [Front]-027 | Shared: Image upload component with S3                 | 4h  |

**Deliverables:**

- Restaurant registration and profile management
- Full menu management (categories, items, variants)
- Image upload for restaurants and menu items
- Admin restaurant approval workflow
- Schema Reference: `[SRS_FoodDelivery.md](SRS_FoodDelivery.md)` lines 645-718

---

### Sprint 3: Search Service + Order Service Part 1 (2 weeks)

**Goal:** Search restaurants and cart management

**User Stories:** US-SEARCH-01, US-SEARCH-02, US-ORD-01, US-ORD-02

**Development Tasks:**

*Backend Tasks:*

| Task      | Description                                               | Est |
| --------- | --------------------------------------------------------- | --- |
| DB-003    | Create `coupons`, `coupon_usages` tables                  | 3h  |
| API-014   | GET `/api/v1/restaurants` - Geo-search with filters       | 10h |
| API-015   | GET `/api/v1/search` - Full-text search                   | 6h  |
| CACHE-002 | Redis caching for search results                          | 4h  |
| API-016   | Cart management (in-memory/Redis per user)                | 8h  |
| API-017   | POST `/api/v1/coupons/validate` - Coupon validation       | 6h  |
| API-018   | Pricing engine (subtotal + tax + delivery fee - discount) | 6h  |
| INDEX-001 | PostgreSQL GiST index for geo-queries                     | 4h  |
| TEST-004  | Unit + integration tests                                  | 8h  |

*Frontend Tasks:*

| Task        | Description                                                    | Est |
| ----------- | -------------------------------------------------------------- | --- |
| [Front]-028 | Customer: Search screen with autocomplete                      | 6h  |
| [Front]-029 | Customer: Search Results with filters (distance, rating, open) | 8h  |
| [Front]-030 | Customer: Filter Modal                                         | 4h  |
| [Front]-031 | Customer: Category View screen                                 | 4h  |
| [Front]-032 | Customer: Cart screen with item management                     | 8h  |
| [Front]-033 | Customer: Coupon input + validation UI                         | 4h  |
| [Front]-034 | Customer: Pricing breakdown component                          | 3h  |
| [Front]-035 | Shared: Map integration (Google Maps / Mapbox)                 | 8h  |

**Deliverables:**

- Geo-based restaurant search with filters (distance, rating, open status)
- Full-text search capability
- Shopping cart with item management
- Coupon validation and pricing calculation
- Key Algorithm: Distance-based search using `ll_to_earth()` PostgreSQL function

---

### Sprint 4: Order Service Part 2 + Payment Service (2 weeks)

**Goal:** Complete order placement and payment processing

**User Stories:** US-ORD-03, US-ORD-05, US-PAY-01, US-PAY-02, US-PAY-03, US-PAY-04

**Development Tasks:**

*Backend Tasks:*

| Task      | Description                                                                                 | Est |
| --------- | ------------------------------------------------------------------------------------------- | --- |
| DB-004    | Create `orders`, `order_items`, `order_item_variants`, `payments`, `payment_refunds` tables | 6h  |
| API-019   | POST `/api/v1/orders` - Create order with validation                                        | 12h |
| API-020   | Order state machine implementation                                                          | 8h  |
| API-021   | PUT `/api/v1/orders/{id}/cancel` - Cancellation with refund                                 | 6h  |
| API-022   | POST `/api/v1/payments/authorize` - Payment authorization                                   | 8h  |
| API-023   | POST `/api/v1/payments/{id}/capture` - Payment capture                                      | 6h  |
| API-024   | POST `/api/v1/payments/{id}/refund` - Refund processing                                     | 6h  |
| INT-004   | Stripe/VNPay gateway integration                                                            | 12h |
| INT-005   | Idempotency key implementation                                                              | 4h  |
| KAFKA-001 | Kafka producer for order events                                                             | 6h  |
| KAFKA-002 | Kafka consumer stubs for notification events                                                | 4h  |
| TEST-005  | Payment idempotency tests (critical)                                                        | 8h  |

*Frontend Tasks:*

| Task        | Description                                            | Est |
| ----------- | ------------------------------------------------------ | --- |
| [Front]-036 | Customer: Checkout Step 1 - Delivery address selection | 6h  |
| [Front]-037 | Customer: Checkout Step 2 - Payment method selection   | 6h  |
| [Front]-038 | Customer: Checkout Step 3 - Order review + place order | 6h  |
| [Front]-039 | Customer: Order Confirmation screen                    | 4h  |
| [Front]-040 | Customer: Order History screen                         | 6h  |
| [Front]-041 | Customer: Order Detail screen                          | 4h  |
| [Front]-042 | Restaurant: Incoming Orders screen with accept/reject  | 8h  |
| [Front]-043 | Restaurant: Order Detail (restaurant view)             | 4h  |
| [Front]-044 | Restaurant: Preparing Orders screen with status updates| 6h  |
| [Front]-045 | Shared: Stripe/VNPay payment integration               | 8h  |

**Deliverables:**

- Complete order placement flow with validation
- Order state machine (pending → confirmed → preparing → ready → delivered)
- Payment processing (COD and card payments)
- Refund handling on cancellation
- Idempotency for payment operations
- Schema Reference: `[SRS_FoodDelivery.md](SRS_FoodDelivery.md)` lines 759-865

---

### Sprint 5: Delivery Service + WebSocket (2 weeks)

**Goal:** Driver management and real-time tracking

**User Stories:** US-DEL-01 to US-DEL-06, US-ORD-07, US-ORD-08, US-ADM-03

**Development Tasks:**

*Backend Tasks:*

| Task     | Description                                                                                  | Est |
| -------- | -------------------------------------------------------------------------------------------- | --- |
| DB-005   | Create `drivers`, `delivery_tasks`, `delivery_task_events`, `driver_location_history` tables | 6h  |
| DB-006   | Configure `driver_location_history` table partitioning for performance                       | 4h  |
| API-025  | POST `/api/v1/drivers/register` - Driver registration                                        | 6h  |
| API-026  | PUT `/api/v1/drivers/{id}/status` - Online/offline toggle                                    | 4h  |
| API-027  | Driver assignment algorithm (nearest available)                                              | 10h |
| API-028  | PUT `/api/v1/delivery-tasks/{id}/status` - Status updates                                    | 6h  |
| API-029  | PUT `/api/v1/drivers/{id}/location` - GPS location updates (every 5s)                        | 4h  |
| API-030  | Admin driver approval endpoints (PENDING → APPROVED/REJECTED)                                | 6h  |
| WS-001   | WebSocket gateway setup (gorilla/websocket)                                                  | 10h |
| WS-002   | Order status subscription (order:{id} channel)                                               | 6h  |
| WS-003   | Driver location subscription (driver:location:{id})                                          | 6h  |
| INT-006  | Redis Pub/Sub for WebSocket scaling                                                          | 6h  |
| API-031  | Restaurant order management (accept/reject, status update)                                   | 8h  |
| TEST-006 | WebSocket integration tests                                                                  | 6h  |

*Frontend Tasks:*

| Task        | Description                                               | Est  |
| ----------- | --------------------------------------------------------- | ---- |
| [Front]-046 | Customer: Order Tracking - Live Map screen                | 10h  |
| [Front]-047 | Customer: WebSocket integration for real-time updates     | 6h   |
| [Front]-048 | Driver: Home screen (Online/Offline toggle)               | 6h   |
| [Front]-049 | Driver: Available Deliveries list                         | 4h   |
| [Front]-050 | Driver: Active Delivery - Pickup screen with navigation   | 8h   |
| [Front]-051 | Driver: Active Delivery - Dropoff screen                  | 6h   |
| [Front]-052 | Driver: Delivery Complete screen                          | 3h   |
| [Front]-053 | Driver: GPS location tracking service (background)        | 8h   |
| [Front]-054 | Driver: WebSocket integration for task assignment         | 6h   |
| [Front]-055 | Admin: Driver Management screen (approve/reject)          | 6h   |

**Deliverables:**

- Driver registration and approval workflow
- Driver online/offline status management
- Automatic driver assignment algorithm
- Real-time order tracking via WebSocket
- Live driver location updates on map
- Architecture Reference: `[SDD_FoodDelivery.md](SDD_FoodDelivery.md)` lines 119-178

---

### Sprint 6: Notifications + Saga + Exception Flows (2 weeks)

**Goal:** Push notifications, distributed transaction handling, and exception flows

**User Stories:** US-NOTIF-01, US-NOTIF-02, US-EXC-01, US-EXC-02, US-EXC-03, US-EXC-04, US-DISPUTE-01, US-DISPUTE-02

**Development Tasks:**

*Backend Tasks:*

| Task      | Description                                                   | Est |
| --------- | ------------------------------------------------------------- | --- |
| DB-007    | Create `disputes` table                                       | 3h  |
| API-032   | Notification service setup                                    | 6h  |
| API-033   | Notification preference APIs                                  | 4h  |
| INT-007   | FCM integration for push notifications                        | 8h  |
| INT-008   | Twilio SMS integration                                        | 4h  |
| KAFKA-003 | Kafka consumers for notification events                       | 8h  |
| SAGA-001  | Order creation saga implementation                            | 12h |
| SAGA-002  | Compensation handlers for each saga step                      | 10h |
| EXC-001   | FR-ORD-11: Customer unreachable flow (mark after 3 attempts)  | 6h  |
| EXC-002   | FR-ORD-12: Address correction flow (driver reports mismatch)  | 6h  |
| EXC-003   | FR-ORD-14: SLA miss auto-cancellation scheduler (>60min)      | 6h  |
| EXC-004   | FR-DEL-10: Driver emergency and reassignment flow             | 6h  |
| API-034   | POST `/api/v1/disputes` - Create dispute ticket               | 6h  |
| API-035   | GET `/api/v1/disputes` - List user disputes                   | 4h  |
| TEST-007  | Saga compensation tests                                       | 8h  |

*Frontend Tasks:*

| Task        | Description                                           | Est |
| ----------- | ----------------------------------------------------- | --- |
| [Front]-056 | Customer: Push notification integration (FCM)         | 6h  |
| [Front]-057 | Customer: Notification Settings screen                | 3h  |
| [Front]-058 | Customer: Create Dispute screen with photo upload     | 6h  |
| [Front]-059 | Driver: Push notification for new delivery tasks      | 4h  |
| [Front]-060 | Driver: Customer unreachable flow UI (3 call attempts)| 4h  |
| [Front]-061 | Driver: Address mismatch report modal                 | 3h  |
| [Front]-062 | Driver: Emergency report flow                         | 3h  |
| [Front]-063 | Restaurant: Push notification for new orders          | 4h  |
| [Front]-064 | Admin: Dispute Management screen                      | 6h  |

**Deliverables:**

- Push notifications (FCM) for all user types
- SMS notifications for critical events
- Saga pattern for distributed transactions
- Exception handling flows (unreachable customer, address mismatch, SLA miss)
- Dispute creation and tracking system
- Saga Pattern Reference: `[SDD_FoodDelivery.md](SDD_FoodDelivery.md)` lines 180-263

---

### Sprint 7: Rating + Admin + Disputes + Polish (2 weeks)

**Goal:** Rating system, admin dashboard, dispute resolution, bug fixes

**User Stories:** US-RATE-01, US-RATE-02, US-ADM-01, US-ADM-04, US-DISPUTE-03

**Development Tasks:**

*Backend Tasks:*

| Task     | Description                                              | Est |
| -------- | -------------------------------------------------------- | --- |
| DB-008   | Create `ratings` table                                   | 3h  |
| API-036  | POST `/api/v1/restaurants/{id}/ratings`                  | 4h  |
| API-037  | POST `/api/v1/drivers/{id}/ratings`                      | 4h  |
| API-038  | Aggregate rating calculation                             | 4h  |
| API-039  | GET `/api/v1/admin/dashboard` - KPI metrics              | 8h  |
| API-040  | PUT `/api/v1/disputes/{id}/resolve` - Admin resolution   | 6h  |
| API-041  | Admin coupon management APIs                             | 6h  |
| API-042  | Dispute metrics in admin dashboard                       | 4h  |
| SEC-002  | Security headers implementation verification             | 4h  |
| SEC-003  | Rate limiting configuration                              | 4h  |
| OPS-001  | Monitoring dashboards (Grafana)                          | 8h  |
| OPS-002  | Alerting rules (P0 incidents)                            | 4h  |
| BUG-XXX  | Bug fixes and performance optimization                   | 16h |
| TEST-008 | E2E tests for critical paths                             | 12h |

*Frontend Tasks:*

| Task        | Description                                        | Est  |
| ----------- | -------------------------------------------------- | ---- |
| [Front]-065 | Customer: Rate Order modal (restaurant + driver)   | 6h   |
| [Front]-066 | Customer: Restaurant Reviews Tab                   | 4h   |
| [Front]-067 | Driver: Driver Profile screen                      | 4h   |
| [Front]-068 | Driver: Delivery History + Earnings screen         | 6h   |
| [Front]-069 | Restaurant: Analytics View screen                  | 6h   |
| [Front]-070 | Restaurant: Order History screen                   | 4h   |
| [Front]-071 | Admin: Dashboard screen with KPIs                  | 8h   |
| [Front]-072 | Admin: User Management screen                      | 6h   |
| [Front]-073 | Admin: Order Management screen                     | 6h   |
| [Front]-074 | Admin: Payment Management screen                   | 4h   |
| [Front]-075 | Admin: Coupon Management screen                    | 6h   |
| [Front]-076 | All Apps: Bug fixes and UI polish                  | 16h  |

**Deliverables:**

- Restaurant and driver rating system
- Admin dashboard with KPI metrics
- Dispute resolution workflow for admins
- Coupon management system
- Monitoring and alerting setup
- Bug fixes and performance optimization

---

### Sprint 8: Integration Testing + UAT + Launch Prep (2 weeks)

**Goal:** Final testing, security audit, production deployment

**User Stories:** All user stories from previous sprints (UAT validation)

**Development Tasks:**

*Backend Tasks:*

| Task      | Description                                           | Est  |
| --------- | ----------------------------------------------------- | ---- |
| TEST-009  | Full E2E testing of all user journeys                 | 16h  |
| TEST-010  | Load testing (target: 5k concurrent users)            | 12h  |
| SEC-004   | Security penetration testing                          | 12h  |
| PERF-001  | Performance optimization based on test results        | 12h  |
| OPS-003   | Production environment setup (AWS EKS)                | 8h   |
| OPS-004   | Database migration to production                      | 4h   |
| OPS-005   | SSL/TLS certificate setup                             | 2h   |
| OPS-006   | DNS configuration                                     | 2h   |
| OPS-007   | Monitoring and alerting verification                  | 4h   |
| DOC-001   | Runbook documentation                                 | 8h   |
| OPS-008   | On-call rotation setup                                | 2h   |
| LAUNCH-01 | Go-live checklist completion                          | 4h   |

*Frontend Tasks:*

| Task        | Description                                                  | Est  |
| ----------- | ------------------------------------------------------------ | ---- |
| [Front]-077 | Admin: Revenue Reports screen                                | 6h   |
| [Front]-078 | Admin: Performance Reports screen                            | 4h   |
| [Front]-079 | Admin: User Analytics screen                                 | 4h   |
| [Front]-080 | All Apps: E2E testing with Detox (mobile) / Cypress (web)    | 16h  |
| [Front]-081 | All Apps: Accessibility audit and fixes                      | 8h   |
| [Front]-082 | Mobile: App Store / Play Store submission preparation        | 8h   |
| [Front]-083 | Admin: Production deployment (Vercel/AWS)                    | 4h   |
| [Front]-084 | All Apps: Performance optimization                           | 8h   |

**Deliverables:**

- All E2E tests passing
- Load test results meeting targets (5k concurrent users)
- Security audit completed with no critical issues
- Production environment fully configured
- App store submissions prepared
- Runbook and on-call rotation documented
- Go-live checklist completed

---

## Key Technical References

**Database Schema:** `[SRS_FoodDelivery.md](SRS_FoodDelivery.md)` Section 4.1 (lines 556-1013)

**API Contracts:** `[SRS_FoodDelivery.md](SRS_FoodDelivery.md)` Section 5 (lines 1102-1710)

**Architecture:** `[SDD_FoodDelivery.md](SDD_FoodDelivery.md)` Section 1 (lines 54-263)

**Tech Stack:**

**Backend:**
- **Language:** Go 1.21+
- **Framework:** Gin/Echo
- **Database:** PostgreSQL
- **Cache:** Redis
- **Message Broker:** Kafka
- **WebSocket:** gorilla/websocket
- **Container:** Docker + Kubernetes
- **CI/CD:** GitHub Actions → Docker Hub → AWS EKS

**Frontend:**
- **Mobile Framework:** React Native (Expo)
- **Web Framework:** React 18 + Vite
- **State Management:** Zustand + React Query
- **UI Components:** React Native Paper / shadcn/ui (web)
- **Maps:** React Native Maps / Google Maps API
- **WebSocket:** socket.io-client
- **Testing:** Detox (mobile), Cypress (web)
- **Build:** EAS Build (mobile), Vercel (web)

---

## Definition of Ready (DoR)

- User story has acceptance criteria
- Dependencies identified
- API contract defined in SRS
- Database schema defined
- Estimated by team

## Definition of Done (DoD)

- Code reviewed and merged
- Unit tests passing (80%+ coverage)
- Integration tests passing
- API documented (OpenAPI)
- No critical/high linter warnings
- Deployed to staging
- QA sign-off
