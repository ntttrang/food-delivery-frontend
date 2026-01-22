# Software Design Document (SDD)
## Food Delivery Platform Architecture & Implementation Design

**Version:** 3.0  
**Date:** 21 January 2026  
**Status:** Aligned with SRS v2.2  
**Change Log:**
- v1.0 (20 Jan 2026): Initial SDD
- v2.0 (21 Jan 2026): Synced with SRS v2.2 - Added WebSocket, Dispute Service, JWT RS256, Full Schema, Exception Flows
- v3.0 (21 Jan 2026): Hexagonal Architecture (Ports & Adapters) + Monorepo structure for 10 microservices, Go 1.25

---

## TABLE OF CONTENTS

1. Architecture & Design Patterns
   - 1.1 Architectural Style: Hexagonal + Event-Driven Microservices
   - 1.2 Monorepo Structure
   - 1.3 Hexagonal Architecture (Ports & Adapters)
   - 1.4 Design Patterns Applied
   - 1.5 Real-Time Layer Architecture
   - 1.6 Saga Compensation Matrix
   - 1.7 Frontend Architecture
2. Service Design Details (10 Microservices - Hexagonal)
   - 2.1 User Service
   - 2.2 Catalog Service
   - 2.3 Order Service
   - 2.4 Payment Service
   - 2.5 Delivery Service
   - 2.6 Search Service
   - 2.7 Promotion Service
   - 2.8 Notification Service
   - 2.9 Rating Service
   - 2.10 Admin Service
3. Database Design & Schema
   - 3.1 Database Schema Reference
   - 3.2 Index Strategy
   - 3.3 Sharding Strategy
   - 3.4 Backup & Recovery
4. API Design & Contracts
   - 4.1 REST API Standards
   - 4.2 Standardized Error Schema
   - 4.3 Complete API Contracts
   - 4.4 WebSocket API Contract
5. Technology Stack
6. Deployment Architecture
7. Security Design
   - 7.1 JWT RS256 Authentication
   - 7.2 Security Headers
   - 7.3 GDPR Compliance
8. Performance & Scalability Design
9. Disaster Recovery & High Availability
10. Code Organization & Best Practices
    - 10.1 Port & Adapter Examples
    - 10.2 Dependency Injection
    - 10.3 Testing Strategy
    - 10.4 Logging & Monitoring

---

## 1. ARCHITECTURE & DESIGN PATTERNS

### 1.1 Architectural Style: Hexagonal + Event-Driven Microservices

**Architecture Overview:**
- **Pattern:** Hexagonal Architecture (Ports & Adapters) for each microservice
- **Repository:** Monorepo containing all 10 microservices
- **Language:** Go 1.25
- **Communication:** REST/gRPC (sync) + Kafka (async events)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CLIENT LAYER                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│     Web (Next.js/React)     │     Mobile (React Native - TypeScript)        │
└──────────────────────────────┬──────────────────────────────────────────────┘
                               │
┌──────────────────────────────┴──────────────────────────────────────────────┐
│                      API GATEWAY (Nginx/Envoy)                               │
│              Auth ✓ │ Rate Limit ✓ │ Routing ✓ │ Tracing ✓                  │
└──────────────────────────────┬──────────────────────────────────────────────┘
                               │
┌──────────────────────────────┴──────────────────────────────────────────────┐
│                   10 MICROSERVICES (Hexagonal Architecture)                  │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐               │
│  │  User   │ │ Catalog │ │  Order  │ │ Payment │ │Delivery │               │
│  │ Service │ │ Service │ │ Service │ │ Service │ │ Service │               │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘               │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐               │
│  │ Search  │ │Promotion│ │ Notif   │ │ Rating  │ │  Admin  │               │
│  │ Service │ │ Service │ │ Service │ │ Service │ │ Service │               │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘               │
└──────────────────────────────┬──────────────────────────────────────────────┘
                               │ (REST/gRPC between services)
┌──────────────────────────────┴──────────────────────────────────────────────┐
│                         KAFKA (Event Bus)                                    │
│    Topics: order.* │ payment.* │ delivery.* │ notification.* │ rating.*     │
└──────────────────────────────┬──────────────────────────────────────────────┘
                               │
┌──────────────────────────────┴──────────────────────────────────────────────┐
│                         DATA STORAGE LAYER                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│   PostgreSQL (Primary)  │  Redis (Cache/Session)  │  S3/MinIO (Storage)     │
│   Elasticsearch (Phase 2: Search)                                           │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                      EXTERNAL INTEGRATIONS                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  Payment Gateway (Stripe/VNPay) │ Google Maps API │ FCM/APNs │ Twilio SMS   │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Key Principles:**
- **Hexagonal Architecture:** Domain logic isolated from infrastructure (Ports & Adapters)
- **Bounded Contexts:** Each service owns its domain and data (no shared DB)
- **Dependency Inversion:** Domain depends on abstractions (ports), not implementations
- **Event-Driven:** Services communicate via Kafka for eventual consistency
- **API Contracts:** REST/gRPC with versioning strategy (v1, v2...)
- **Monorepo:** Single repository with shared packages and independent deployments
- **Resilience:** Circuit breaker, retry, timeout, fallback patterns
- **Real-Time Layer:** WebSocket for order tracking, driver location, notifications

### 1.2 Monorepo Structure

**Root Structure (Go 1.25 Workspace):**

```
food-delivery-platform/
├── go.work                          # Go workspace file
├── go.work.sum
├── Makefile                         # Build all services
├── docker-compose.yml               # Local development
├── docker-compose.prod.yml          # Production compose
│
├── api/                             # API DEFINITIONS (shared)
│   ├── proto/                       # gRPC protobuf definitions
│   │   ├── user/user.proto
│   │   ├── order/order.proto
│   │   ├── payment/payment.proto
│   │   ├── delivery/delivery.proto
│   │   └── common/common.proto
│   └── openapi/                     # OpenAPI/Swagger specs
│       └── swagger.yaml
│
├── pkg/                             # SHARED PACKAGES (used by all services)
│   ├── common/                      # Common utilities
│   │   ├── errors/
│   │   │   ├── errors.go           # Standard error types
│   │   │   └── codes.go            # Error codes (from SRS 5.0)
│   │   ├── logger/
│   │   │   └── logger.go           # Structured logging (JSON)
│   │   ├── config/
│   │   │   └── config.go           # Config loader (env, yaml)
│   │   └── validator/
│   │       └── validator.go        # Request validation
│   │
│   ├── infrastructure/              # Shared infrastructure adapters
│   │   ├── database/
│   │   │   ├── postgresql.go       # PostgreSQL connection pool
│   │   │   └── migration.go        # Migration helper
│   │   ├── cache/
│   │   │   └── redis.go            # Redis client wrapper
│   │   ├── messaging/
│   │   │   ├── kafka_producer.go   # Kafka producer with retry
│   │   │   └── kafka_consumer.go   # Kafka consumer with DLQ
│   │   └── http/
│   │       ├── middleware/
│   │       │   ├── auth.go         # JWT RS256 validation
│   │       │   ├── rate_limit.go   # Token bucket rate limiting
│   │       │   ├── cors.go         # CORS handling
│   │       │   ├── security.go     # Security headers
│   │       │   └── trace.go        # Request tracing (X-Request-ID)
│   │       └── response/
│   │           └── response.go     # Standard API response format
│   │
│   ├── domain/                      # Shared domain types
│   │   ├── vo/                      # Shared value objects
│   │   │   ├── money.go            # Money value object (VND)
│   │   │   ├── address.go          # Address with lat/lng
│   │   │   └── pagination.go       # Pagination params
│   │   └── event/
│   │       └── event.go            # Base domain event interface
│   │
│   └── go.mod                       # Shared package module
│
├── services/                        # 10 MICROSERVICES (Hexagonal)
│   ├── user-service/                # 1. User/Auth Service
│   ├── catalog-service/             # 2. Catalog/Restaurant Service
│   ├── order-service/               # 3. Order Service
│   ├── payment-service/             # 4. Payment Service
│   ├── delivery-service/            # 5. Delivery Service
│   ├── search-service/              # 6. Search Service
│   ├── promotion-service/           # 7. Promotion/Coupon Service
│   ├── notification-service/        # 8. Notification Service
│   ├── rating-service/              # 9. Rating Service
│   └── admin-service/               # 10. Admin Service
│
├── migrations/                      # Database migrations (per service)
│   ├── user/
│   ├── catalog/
│   ├── order/
│   ├── payment/
│   ├── delivery/
│   └── ...
│
├── deployments/                     # Kubernetes manifests
│   ├── base/
│   │   ├── namespace.yaml
│   │   └── configmap.yaml
│   ├── services/
│   │   ├── user-service/
│   │   ├── order-service/
│   │   └── ...
│   └── kustomization.yaml
│
├── scripts/                         # Build & deployment scripts
│   ├── build-all.sh
│   ├── test-all.sh
│   └── deploy.sh
│
└── docs/                            # Documentation
    ├── architecture/
    └── api/
```

**Go Workspace Configuration (go.work):**

```go
go 1.25

use (
    ./pkg
    ./services/user-service
    ./services/catalog-service
    ./services/order-service
    ./services/payment-service
    ./services/delivery-service
    ./services/search-service
    ./services/promotion-service
    ./services/notification-service
    ./services/rating-service
    ./services/admin-service
)
```

### 1.3 Hexagonal Architecture (Ports & Adapters)

**Architecture Diagram for Each Service:**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        HEXAGONAL ARCHITECTURE                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    PRIMARY ADAPTERS (Driving)                         │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐     │   │
│  │  │ HTTP/REST  │  │   gRPC     │  │   Kafka    │  │ WebSocket  │     │   │
│  │  │  Handler   │  │  Handler   │  │  Consumer  │  │  Handler   │     │   │
│  │  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘     │   │
│  └────────┼───────────────┼───────────────┼───────────────┼─────────────┘   │
│           │               │               │               │                  │
│           ▼               ▼               ▼               ▼                  │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                     PRIMARY PORTS (Interfaces)                        │   │
│  │            OrderCommandUseCase  │  OrderQueryUseCase                 │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                    │                                         │
│                                    ▼                                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    APPLICATION LAYER (Use Cases)                      │   │
│  │              OrderCommandService  │  OrderQueryService               │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                    │                                         │
│                                    ▼                                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                      DOMAIN LAYER (Core)                              │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────────┐  │   │
│  │  │  Entities   │  │   Value     │  │   Domain    │  │   Domain   │  │   │
│  │  │  (Order,    │  │  Objects    │  │  Services   │  │   Events   │  │   │
│  │  │  OrderItem) │  │  (Money,    │  │  (Pricing   │  │  (Order    │  │   │
│  │  │             │  │   Status)   │  │  Calculator)│  │   Created) │  │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └────────────┘  │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                    │                                         │
│                                    ▼                                         │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                   SECONDARY PORTS (Interfaces)                        │   │
│  │   OrderRepository │ EventPublisher │ PaymentClient │ CacheRepository │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│           │               │               │               │                  │
│           ▼               ▼               ▼               ▼                  │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                  SECONDARY ADAPTERS (Driven)                          │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐     │   │
│  │  │ PostgreSQL │  │   Kafka    │  │   gRPC     │  │   Redis    │     │   │
│  │  │ Repository │  │ Publisher  │  │   Client   │  │   Cache    │     │   │
│  │  └────────────┘  └────────────┘  └────────────┘  └────────────┘     │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Dependency Rule:** Dependencies point INWARD (Adapters → Application → Domain)
- Domain Layer has ZERO external dependencies
- Application Layer depends only on Domain
- Adapters implement Port interfaces

**Single Service Folder Structure:**

```
services/order-service/
├── cmd/
│   └── main.go                      # Entry point, DI wiring
│
├── internal/
│   ├── domain/                      # CORE DOMAIN (Pure Go, no dependencies)
│   │   ├── entity/
│   │   │   ├── order.go            # Order aggregate root
│   │   │   ├── order_item.go       # Order item entity
│   │   │   └── cart.go             # Cart entity
│   │   ├── vo/                     # Value Objects
│   │   │   ├── order_status.go     # OrderStatus enum
│   │   │   └── delivery_type.go    # DeliveryType enum
│   │   ├── event/                  # Domain events
│   │   │   ├── order_created.go
│   │   │   ├── order_confirmed.go
│   │   │   └── order_cancelled.go
│   │   ├── service/                # Domain services
│   │   │   ├── pricing_calculator.go
│   │   │   └── eta_calculator.go
│   │   └── error/                  # Domain errors
│   │       └── order_errors.go
│   │
│   ├── application/                 # APPLICATION LAYER (Use Cases)
│   │   ├── port/                   # PORTS (Interfaces)
│   │   │   ├── in/                 # Primary/Driving Ports
│   │   │   │   ├── order_command.go      # Commands (CreateOrder, CancelOrder)
│   │   │   │   └── order_query.go        # Queries (GetOrder, ListOrders)
│   │   │   └── out/                # Secondary/Driven Ports
│   │   │       ├── order_repository.go   # Persistence interface
│   │   │       ├── payment_client.go     # Payment service interface
│   │   │       ├── catalog_client.go     # Catalog service interface
│   │   │       ├── delivery_client.go    # Delivery service interface
│   │   │       ├── event_publisher.go    # Kafka publisher interface
│   │   │       └── cache_repository.go   # Redis cache interface
│   │   │
│   │   ├── service/                # Use case implementations
│   │   │   ├── order_command_service.go  # Write operations
│   │   │   └── order_query_service.go    # Read operations (CQRS)
│   │   │
│   │   ├── dto/                    # Data Transfer Objects
│   │   │   ├── request/
│   │   │   │   ├── create_order.go
│   │   │   │   └── cancel_order.go
│   │   │   └── response/
│   │   │       └── order_response.go
│   │   │
│   │   └── saga/                   # Saga orchestration
│   │       └── order_saga.go
│   │
│   └── adapter/                     # ADAPTERS (Infrastructure)
│       ├── in/                     # Primary/Driving Adapters
│       │   ├── http/               # REST API
│       │   │   ├── handler/
│       │   │   │   ├── order_handler.go
│       │   │   │   └── cart_handler.go
│       │   │   └── router.go
│       │   ├── grpc/               # gRPC API
│       │   │   └── order_grpc_handler.go
│       │   └── kafka/              # Event consumers
│       │       ├── payment_event_consumer.go
│       │       └── delivery_event_consumer.go
│       │
│       └── out/                    # Secondary/Driven Adapters
│           ├── persistence/        # Database
│           │   └── postgresql/
│           │       ├── order_repository.go
│           │       ├── model/
│           │       │   ├── order_model.go
│           │       │   └── order_item_model.go
│           │       └── mapper/
│           │           └── order_mapper.go   # Entity <-> Model
│           ├── cache/              # Redis
│           │   └── order_cache.go
│           ├── messaging/          # Kafka producer
│           │   └── event_publisher.go
│           └── client/             # Service clients
│               ├── payment_client.go
│               ├── catalog_client.go
│               └── delivery_client.go
│
├── config/
│   └── config.go                   # Service configuration
│
├── Dockerfile
├── go.mod
└── go.sum
```

### 1.4 Design Patterns Applied

| Pattern | Use Case | Implementation |
|:---|:---|:---|
| **Hexagonal (Ports & Adapters)** | Service architecture isolation | Domain core with port interfaces + adapters |
| **Dependency Injection** | Loose coupling between layers | Constructor injection in main.go |
| **Saga Pattern** | Distributed transactions (order → payment → delivery) | Choreography via Kafka events |
| **CQRS** | Separate read/write models | OrderCommandService + OrderQueryService |
| **Event Sourcing** | Order state changes (audit trail) | Store all state transitions in order_events |
| **Repository Pattern** | Data access abstraction | Port interface + PostgreSQL adapter |
| **Circuit Breaker** | Payment gateway calls (prevent cascading failures) | go-resilience library |
| **Idempotency** | Payment API (prevent double-charge) | Idempotency key in DB + Redis |
| **Outbox Pattern** | Event publishing reliability | Transactional outbox table + background job |
| **API Versioning** | API evolution | URL prefix (/api/v1, /api/v2) |
| **Rate Limiting** | DoS protection | Token bucket algorithm (Nginx) |
| **Cache Aside** | Performance optimization | Read from cache, miss → DB → populate cache |

### 1.5 Real-Time Layer Architecture

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

**WebSocket Connection Flow:**
```
1. Client establishes WebSocket connection
   ws://api.fooddelivery.com/ws?token={jwt_token}

2. Server validates JWT and upgrades connection

3. Client subscribes to channels
   → { "type": "subscribe", "channel": "order:12345" }
   → { "type": "subscribe", "channel": "driver:location:12345" }

4. Server pushes events when state changes
   → Order status updates (PREPARING, READY, ON_THE_WAY, DELIVERED)
   → Driver location updates (every 5 seconds)
   → ETA updates (real-time recalculation)

5. Heartbeat keeps connection alive
   Client → { "type": "ping" }
   Server → { "type": "pong" }
```

**Scalability Requirements:**
- Horizontal scaling via sticky sessions (consistent hashing by user_id)
- Target: 50k concurrent WebSocket connections (MVP)
- Location update frequency: Every 5 seconds (driver app)
- Message latency: <500ms end-to-end
- Redis Pub/Sub for cross-pod message distribution

**Technology Stack:**
- WebSocket Server: `gorilla/websocket` (Go native) or `Socket.io`
- Message Distribution: Redis Pub/Sub
- Session Store: Redis (connection metadata)
- Load Balancing: Nginx with sticky sessions (ip_hash or cookie-based)
- Client (Web): socket.io-client (JavaScript)
- Client (React Native): socket.io-client (compatible with React Native)
  - Auto-reconnection with exponential backoff
  - Background/foreground state handling for mobile
  - Network connectivity awareness via NetInfo

### 1.6 Saga Compensation Matrix

**Order Creation Saga with Compensation Actions:**

| Saga Step | Success Event | Failure Scenario | Compensation Action | SLA |
|:----------|:--------------|:-----------------|:--------------------|:----|
| **1. Order Created** | `order.created` | - | - | - |
| **2. Payment Authorized** | `payment.authorized` | Gateway timeout (3 retries) | Cancel order, notify customer, log incident | <30s |
| **3. Order Confirmed** | `order.confirmed` | Restaurant offline | Release payment auth, full refund, notify customer | <2min |
| **4. Restaurant Accepted** | `order.accepted` | Restaurant rejects order | Full refund + 50k VND discount code, notify customer | <5min |
| **5. Delivery Assigned** | `delivery.assigned` | No driver available (5 min) | Expand search radius to 15km → Queue order → Notify customer of delay | <10min |
| **6. Food Picked Up** | `delivery.picked_up` | Driver emergency | Reassign to nearest driver, compensate original driver, notify customer | <5min |
| **7. Food Delivered** | `delivery.completed` | Customer unreachable (3 calls) | Mark UNDELIVERABLE, hold order 5 min, refund if not resolved | <10min |
| **8. Payment Captured** | `payment.captured` | Capture failed | Retry 3x → Contact customer for alternate payment | <1h |

**Compensation Implementation Pattern:**
```go
type SagaStep struct {
    Name           string
    ExecuteFunc    func(ctx context.Context, data interface{}) error
    CompensateFunc func(ctx context.Context, data interface{}) error
    Timeout        time.Duration
    RetryPolicy    RetryPolicy
}

// Example: Payment Authorization Step
paymentAuthStep := SagaStep{
    Name: "PaymentAuthorization",
    ExecuteFunc: func(ctx context.Context, data interface{}) error {
        order := data.(*Order)
        return paymentService.Authorize(ctx, order.PaymentMethodID, order.TotalPrice)
    },
    CompensateFunc: func(ctx context.Context, data interface{}) error {
        order := data.(*Order)
        // Rollback: Release authorization
        if err := paymentService.ReleaseAuth(ctx, order.PaymentID); err != nil {
            return err
        }
        // Cancel order
        order.Status = "CANCELLED"
        order.CancellationReason = "Payment authorization failed"
        return orderRepo.Update(ctx, order)
    },
    Timeout: 30 * time.Second,
    RetryPolicy: RetryPolicy{MaxRetries: 3, Backoff: ExponentialBackoff},
}
```

**Exception Flows Implementation (from SRS FR-ORD-11 to FR-ORD-14):**

**FR-ORD-11: Customer Unreachable**
```
Driver attempts delivery → Customer not available
  1. Driver calls customer (3 attempts)
  2. Wait timer starts (5 minutes)
  3. If no response:
     → Mark delivery as UNDELIVERABLE
     → Notify support team
     → Order held at restaurant (customer can pick up within 30 min)
     → If not picked up: Full refund + 50k discount code
```

**FR-ORD-12: Address Correction**
```
Driver arrives → Address mismatch
  1. Driver reports issue via app
  2. System contacts customer for correction
  3. If new address distance > 2km from original:
     → Recalculate delivery fee
     → Customer confirms additional fee
     → Update ETA
  4. If customer declines:
     → Cancel delivery → Full refund
```

**FR-ORD-14: SLA Miss Auto-Cancellation**
```
Estimated delivery time + 60 min exceeded
  → Auto-cancel order
  → Full refund processed automatically
  → 100k VND discount code issued
  → Incident logged for restaurant/driver review
  → Quality score impact for responsible party
```

### 1.7 Frontend Architecture

**Architecture Overview:**
- **Pattern:** Component-Based Architecture with Atomic Design Principles
- **Repository:** Monorepo structure (Turborepo/Nx) for code sharing between web and mobile
- **State Management:** Zustand (lightweight) + React Query (server state)
- **Communication:** REST API (HTTP/HTTPS) + WebSocket (real-time updates)
- **Code Sharing:** Shared business logic, types, and utilities between web and mobile

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        FRONTEND ARCHITECTURE                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────────────┐      ┌──────────────────────────┐           │
│  │   WEB APP (Next.js)      │      │  MOBILE APP (React Native)│           │
│  │   - SSR/SSG Support      │      │  - iOS & Android          │           │
│  │   - React 18+            │      │  - TypeScript             │           │
│  │   - Tailwind CSS         │      │  - NativeWind             │           │
│  └───────────┬──────────────┘      └───────────┬──────────────┘           │
│              │                                 │                          │
│              └──────────────┬──────────────────┘                          │
│                             │                                              │
│  ┌──────────────────────────┴──────────────────────────┐                 │
│  │           SHARED PACKAGES (Monorepo)                 │                 │
│  ├──────────────────────────────────────────────────────┤                 │
│  │  • @food-delivery/shared-types    (TypeScript types) │                 │
│  │  • @food-delivery/shared-utils    (Business logic)   │                 │
│  │  • @food-delivery/shared-api      (API clients)      │                 │
│  │  • @food-delivery/shared-components (UI components)  │                 │
│  │  • @food-delivery/shared-constants (Constants)       │                 │
│  └──────────────────────────┬──────────────────────────┘                 │
│                             │                                              │
│  ┌──────────────────────────┴──────────────────────────┐                 │
│  │              STATE MANAGEMENT LAYER                  │                 │
│  ├──────────────────────────────────────────────────────┤                 │
│  │  • Zustand Stores (Client state: auth, cart, UI)     │                 │
│  │  • React Query (Server state: API cache, mutations)  │                 │
│  │  • WebSocket Manager (Real-time updates)            │                 │
│  └──────────────────────────┬──────────────────────────┘                 │
│                             │                                              │
│  ┌──────────────────────────┴──────────────────────────┐                 │
│  │              API INTEGRATION LAYER                    │                 │
│  ├──────────────────────────────────────────────────────┤                 │
│  │  • Axios Client (REST API with interceptors)         │                 │
│  │  • WebSocket Client (socket.io-client)               │                 │
│  │  • API Error Handler (Standardized error handling)    │                 │
│  │  • Request/Response Transformers                      │                 │
│  └──────────────────────────┬──────────────────────────┘                 │
│                             │                                              │
│                    ┌─────────┴─────────┐                                   │
│                    │   API GATEWAY     │                                   │
│                    │  (Backend Services)│                                  │
│                    └───────────────────┘                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 1.7.1 Frontend Monorepo Structure

**Root Structure (Turborepo/Nx Monorepo):**

```
food-delivery-frontend/
├── package.json                    # Root workspace config
├── turbo.json                      # Turborepo pipeline config
├── tsconfig.json                   # Shared TypeScript config
│
├── apps/                           # Applications
│   ├── web/                        # Next.js Web Application
│   │   ├── src/
│   │   │   ├── app/                # Next.js App Router (pages)
│   │   │   │   ├── (auth)/
│   │   │   │   │   ├── login/
│   │   │   │   │   └── register/
│   │   │   │   ├── (customer)/
│   │   │   │   │   ├── home/
│   │   │   │   │   ├── restaurants/
│   │   │   │   │   ├── cart/
│   │   │   │   │   ├── orders/
│   │   │   │   │   └── profile/
│   │   │   │   ├── (restaurant)/
│   │   │   │   │   ├── dashboard/
│   │   │   │   │   ├── orders/
│   │   │   │   │   └── menu/
│   │   │   │   └── (admin)/
│   │   │   │       └── admin/
│   │   │   ├── components/         # App-specific components
│   │   │   ├── lib/                # App-specific utilities
│   │   │   └── styles/             # Global styles
│   │   ├── next.config.js
│   │   ├── tailwind.config.js
│   │   └── package.json
│   │
│   └── mobile/                     # React Native Mobile App
│       ├── src/
│       │   ├── navigation/         # React Navigation setup
│       │   │   ├── AppNavigator.tsx
│       │   │   ├── AuthNavigator.tsx
│       │   │   ├── CustomerNavigator.tsx
│       │   │   ├── RestaurantNavigator.tsx
│       │   │   └── DriverNavigator.tsx
│       │   ├── screens/            # Screen components
│       │   │   ├── auth/
│       │   │   ├── customer/
│       │   │   ├── restaurant/
│       │   │   ├── driver/
│       │   │   └── admin/
│       │   ├── components/         # App-specific components
│       │   └── lib/                # App-specific utilities
│       ├── app.json                # Expo config
│       ├── babel.config.js
│       └── package.json
│
├── packages/                       # Shared Packages
│   ├── shared-types/               # TypeScript Type Definitions
│   │   ├── src/
│   │   │   ├── api/                # API request/response types
│   │   │   │   ├── user.types.ts
│   │   │   │   ├── order.types.ts
│   │   │   │   ├── restaurant.types.ts
│   │   │   │   └── payment.types.ts
│   │   │   ├── domain/             # Domain entities
│   │   │   │   ├── user.entity.ts
│   │   │   │   ├── order.entity.ts
│   │   │   │   └── restaurant.entity.ts
│   │   │   └── common/             # Common types
│   │   │       ├── pagination.types.ts
│   │   │       └── error.types.ts
│   │   └── package.json
│   │
│   ├── shared-utils/               # Business Logic & Utilities
│   │   ├── src/
│   │   │   ├── formatters/         # Data formatters
│   │   │   │   ├── currency.ts     # VND formatting
│   │   │   │   ├── date.ts         # Date/time formatting
│   │   │   │   └── phone.ts        # Phone number formatting
│   │   │   ├── validators/         # Validation functions
│   │   │   │   ├── email.ts
│   │   │   │   ├── phone.ts
│   │   │   │   └── address.ts
│   │   │   ├── calculations/       # Business calculations
│   │   │   │   ├── cart.ts         # Cart total calculation
│   │   │   │   ├── delivery.ts     # Delivery fee calculation
│   │   │   │   └── discount.ts     # Discount calculation
│   │   │   └── helpers/            # Helper functions
│   │   │       ├── storage.ts      # LocalStorage/AsyncStorage
│   │   │       └── constants.ts   # App constants
│   │   └── package.json
│   │
│   ├── shared-api/                 # API Client Layer
│   │   ├── src/
│   │   │   ├── client/             # Axios client setup
│   │   │   │   ├── axios-client.ts
│   │   │   │   ├── interceptors.ts # Auth, error handling
│   │   │   │   └── config.ts
│   │   │   ├── services/           # API service modules
│   │   │   │   ├── user.service.ts
│   │   │   │   ├── order.service.ts
│   │   │   │   ├── restaurant.service.ts
│   │   │   │   ├── payment.service.ts
│   │   │   │   └── delivery.service.ts
│   │   │   ├── websocket/          # WebSocket client
│   │   │   │   ├── socket-client.ts
│   │   │   │   └── socket-hooks.ts # React hooks for WebSocket
│   │   │   └── errors/             # Error handling
│   │   │       ├── api-error.ts
│   │   │       └── error-handler.ts
│   │   └── package.json
│   │
│   ├── shared-components/          # Reusable UI Components
│   │   ├── src/
│   │   │   ├── atoms/              # Atomic Design: Atoms
│   │   │   │   ├── Button/
│   │   │   │   ├── Input/
│   │   │   │   ├── Icon/
│   │   │   │   └── Badge/
│   │   │   ├── molecules/          # Atomic Design: Molecules
│   │   │   │   ├── Card/
│   │   │   │   ├── FormField/
│   │   │   │   ├── SearchBar/
│   │   │   │   └── Rating/
│   │   │   ├── organisms/          # Atomic Design: Organisms
│   │   │   │   ├── Header/
│   │   │   │   ├── RestaurantCard/
│   │   │   │   ├── OrderCard/
│   │   │   │   └── CartSummary/
│   │   │   ├── templates/          # Atomic Design: Templates
│   │   │   │   ├── PageLayout/
│   │   │   │   └── AuthLayout/
│   │   │   └── web/                # Web-specific components
│   │   │   └── mobile/             # Mobile-specific components
│   │   └── package.json
│   │
│   ├── shared-constants/           # Constants & Configuration
│   │   ├── src/
│   │   │   ├── api-endpoints.ts    # API endpoint URLs
│   │   │   ├── routes.ts           # Route definitions
│   │   │   ├── colors.ts           # Design system colors
│   │   │   ├── typography.ts       # Typography scale
│   │   │   └── config.ts           # App configuration
│   │   └── package.json
│   │
│   └── shared-state/               # State Management (Optional)
│       ├── src/
│       │   ├── stores/             # Zustand stores
│       │   │   ├── auth.store.ts
│       │   │   ├── cart.store.ts
│       │   │   └── ui.store.ts
│       │   └── hooks/              # Custom React hooks
│       │       ├── useAuth.ts
│       │       └── useCart.ts
│       └── package.json
│
├── .github/workflows/              # CI/CD workflows
│   ├── web-ci.yml
│   └── mobile-ci.yml
│
└── docs/                           # Frontend documentation
    ├── component-guidelines.md
    └── state-management.md
```

#### 1.7.2 Component Architecture (Atomic Design)

**Atomic Design Principles:**

```
┌─────────────────────────────────────────────────────────────┐
│                    ATOMIC DESIGN HIERARCHY                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  PAGES (Customer Home, Restaurant Detail, Order Tracking)  │
│         ↑                                                   │
│  TEMPLATES (PageLayout, AuthLayout, DashboardLayout)       │
│         ↑                                                   │
│  ORGANISMS (Header, RestaurantCard, OrderCard, CartSummary) │
│         ↑                                                   │
│  MOLECULES (Card, FormField, SearchBar, Rating)            │
│         ↑                                                   │
│  ATOMS (Button, Input, Icon, Badge, Text)                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Component Structure Example:**

```typescript
// packages/shared-components/src/atoms/Button/Button.tsx
export interface ButtonProps {
  variant: 'primary' | 'secondary' | 'outline';
  size: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
  onPress?: () => void;
  disabled?: boolean;
}

export const Button: React.FC<ButtonProps> = ({ variant, size, children, ...props }) => {
  // Implementation
};

// packages/shared-components/src/molecules/RestaurantCard/RestaurantCard.tsx
import { Button } from '../../atoms/Button';
import { Rating } from '../Rating';

export interface RestaurantCardProps {
  restaurant: Restaurant;
  onPress: () => void;
}

export const RestaurantCard: React.FC<RestaurantCardProps> = ({ restaurant, onPress }) => {
  // Implementation using atoms and molecules
};
```

#### 1.7.3 State Management Architecture

**State Management Strategy:**

| State Type | Solution | Use Case |
|:-----------|:---------|:---------|
| **Server State** | React Query | API data, caching, mutations, background refetching |
| **Client State (Global)** | Zustand | Auth state, cart, UI preferences, theme |
| **Client State (Local)** | React useState/useReducer | Form state, component-specific state |
| **Real-time State** | WebSocket + React Query | Order tracking, driver location, notifications |

**Zustand Store Example (Auth Store):**

```typescript
// packages/shared-state/src/stores/auth.store.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface AuthState {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  login: (accessToken: string, refreshToken: string, user: User) => void;
  logout: () => void;
  updateUser: (user: Partial<User>) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      accessToken: null,
      refreshToken: null,
      isAuthenticated: false,
      login: (accessToken, refreshToken, user) =>
        set({ accessToken, refreshToken, user, isAuthenticated: true }),
      logout: () =>
        set({ user: null, accessToken: null, refreshToken: null, isAuthenticated: false }),
      updateUser: (user) => set((state) => ({ user: { ...state.user, ...user } })),
    }),
    { name: 'auth-storage' }
  )
);
```

**React Query Integration Example:**

```typescript
// packages/shared-api/src/hooks/useOrders.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { orderService } from '../services/order.service';

export const useOrders = (userId: string) => {
  return useQuery({
    queryKey: ['orders', userId],
    queryFn: () => orderService.getUserOrders(userId),
    staleTime: 30000, // 30 seconds
    refetchOnWindowFocus: true,
  });
};

export const useCreateOrder = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: orderService.createOrder,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['orders'] });
    },
  });
};
```

#### 1.7.4 API Integration Architecture

**API Client Setup:**

```typescript
// packages/shared-api/src/client/axios-client.ts
import axios from 'axios';
import { useAuthStore } from '@food-delivery/shared-state';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'https://api.fooddelivery.com',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor: Add JWT token
apiClient.interceptors.request.use(
  (config) => {
    const token = useAuthStore.getState().accessToken;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor: Handle errors and token refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // Handle 401: Token expired
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = useAuthStore.getState().refreshToken;
        const response = await axios.post('/auth/refresh', { refreshToken });
        const { accessToken } = response.data;
        
        useAuthStore.getState().login(
          accessToken,
          refreshToken,
          useAuthStore.getState().user!
        );
        
        originalRequest.headers.Authorization = `Bearer ${accessToken}`;
        return apiClient(originalRequest);
      } catch (refreshError) {
        useAuthStore.getState().logout();
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    
    // Handle standardized error response (from SDD Section 4.2)
    if (error.response?.data?.error) {
      const apiError = error.response.data.error;
      return Promise.reject({
        code: apiError.code,
        message: apiError.message,
        details: apiError.details,
      });
    }
    
    return Promise.reject(error);
  }
);

export default apiClient;
```

**Service Layer Pattern:**

```typescript
// packages/shared-api/src/services/order.service.ts
import apiClient from '../client/axios-client';
import { CreateOrderRequest, Order, OrderListResponse } from '@food-delivery/shared-types';

export const orderService = {
  getUserOrders: async (userId: string, page = 1, limit = 10): Promise<OrderListResponse> => {
    const response = await apiClient.get(`/orders`, {
      params: { userId, page, limit },
    });
    return response.data;
  },
  
  getOrderById: async (orderId: string): Promise<Order> => {
    const response = await apiClient.get(`/orders/${orderId}`);
    return response.data;
  },
  
  createOrder: async (data: CreateOrderRequest): Promise<Order> => {
    const response = await apiClient.post('/orders', data);
    return response.data;
  },
  
  cancelOrder: async (orderId: string, reason: string): Promise<Order> => {
    const response = await apiClient.post(`/orders/${orderId}/cancel`, { reason });
    return response.data;
  },
};
```

#### 1.7.5 Real-Time Communication (WebSocket)

**WebSocket Client Architecture:**

```typescript
// packages/shared-api/src/websocket/socket-client.ts
import { io, Socket } from 'socket.io-client';
import { useAuthStore } from '@food-delivery/shared-state';

class WebSocketManager {
  private socket: Socket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;

  connect(): void {
    const token = useAuthStore.getState().accessToken;
    if (!token) {
      console.warn('Cannot connect WebSocket: No access token');
      return;
    }

    this.socket = io(process.env.NEXT_PUBLIC_WS_URL || 'wss://api.fooddelivery.com/ws', {
      auth: { token },
      transports: ['websocket'],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: this.maxReconnectAttempts,
    });

    this.socket.on('connect', () => {
      console.log('WebSocket connected');
      this.reconnectAttempts = 0;
    });

    this.socket.on('disconnect', (reason) => {
      console.log('WebSocket disconnected:', reason);
    });

    this.socket.on('error', (error) => {
      console.error('WebSocket error:', error);
    });
  }

  subscribeToOrder(orderId: string, callback: (data: any) => void): void {
    if (!this.socket) {
      this.connect();
    }
    
    this.socket.emit('subscribe', { channel: `order:${orderId}` });
    this.socket.on(`order:${orderId}:status`, callback);
  }

  subscribeToDriverLocation(orderId: string, callback: (data: any) => void): void {
    if (!this.socket) {
      this.connect();
    }
    
    this.socket.emit('subscribe', { channel: `driver:location:${orderId}` });
    this.socket.on(`driver:location:${orderId}`, callback);
  }

  disconnect(): void {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }
}

export const wsManager = new WebSocketManager();
```

**React Hook for WebSocket:**

```typescript
// packages/shared-api/src/websocket/socket-hooks.ts
import { useEffect, useState } from 'react';
import { wsManager } from './socket-client';

export const useOrderTracking = (orderId: string) => {
  const [orderStatus, setOrderStatus] = useState<string | null>(null);
  const [driverLocation, setDriverLocation] = useState<{ lat: number; lng: number } | null>(null);

  useEffect(() => {
    if (!orderId) return;

    wsManager.subscribeToOrder(orderId, (data) => {
      setOrderStatus(data.status);
    });

    wsManager.subscribeToDriverLocation(orderId, (data) => {
      setDriverLocation({ lat: data.lat, lng: data.lng });
    });

    return () => {
      wsManager.disconnect();
    };
  }, [orderId]);

  return { orderStatus, driverLocation };
};
```

#### 1.7.6 Routing & Navigation Architecture

**Web Routing (Next.js App Router):**

```
apps/web/src/app/
├── (auth)/
│   ├── login/page.tsx
│   └── register/page.tsx
├── (customer)/
│   ├── home/page.tsx
│   ├── restaurants/[id]/page.tsx
│   ├── cart/page.tsx
│   ├── orders/[id]/page.tsx
│   └── profile/page.tsx
├── (restaurant)/
│   ├── dashboard/page.tsx
│   ├── orders/page.tsx
│   └── menu/page.tsx
└── layout.tsx
```

**Mobile Navigation (React Navigation):**

```typescript
// apps/mobile/src/navigation/AppNavigator.tsx
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { useAuthStore } from '@food-delivery/shared-state';
import AuthNavigator from './AuthNavigator';
import CustomerNavigator from './CustomerNavigator';
import RestaurantNavigator from './RestaurantNavigator';

const Stack = createStackNavigator();

export default function AppNavigator() {
  const { isAuthenticated, user } = useAuthStore();

  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        {!isAuthenticated ? (
          <Stack.Screen name="Auth" component={AuthNavigator} />
        ) : user?.role === 'CUSTOMER' ? (
          <Stack.Screen name="Customer" component={CustomerNavigator} />
        ) : user?.role === 'RESTAURANT_OWNER' ? (
          <Stack.Screen name="Restaurant" component={RestaurantNavigator} />
        ) : null}
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

#### 1.7.7 Code Organization & Best Practices

**File Naming Conventions:**
- Components: `PascalCase.tsx` (e.g., `RestaurantCard.tsx`)
- Hooks: `camelCase.ts` with `use` prefix (e.g., `useOrders.ts`)
- Utilities: `camelCase.ts` (e.g., `formatCurrency.ts`)
- Types: `camelCase.types.ts` (e.g., `order.types.ts`)
- Constants: `UPPER_SNAKE_CASE.ts` (e.g., `API_ENDPOINTS.ts`)

**Component Structure:**
```typescript
// Component file structure
RestaurantCard/
├── RestaurantCard.tsx        # Main component
├── RestaurantCard.test.tsx   # Unit tests
├── RestaurantCard.stories.tsx # Storybook stories (web only)
└── index.ts                  # Barrel export
```

**Import Organization:**
```typescript
// 1. External libraries
import React from 'react';
import { useQuery } from '@tanstack/react-query';

// 2. Shared packages
import { Button } from '@food-delivery/shared-components';
import { useOrders } from '@food-delivery/shared-api';
import { Order } from '@food-delivery/shared-types';

// 3. Local imports
import { formatCurrency } from '../utils/formatters';
import './RestaurantCard.css';
```

**Performance Optimization:**
- **Code Splitting:** Next.js automatic code splitting, React.lazy() for mobile
- **Memoization:** React.memo() for expensive components, useMemo() for expensive calculations
- **Virtualization:** react-window (web) / FlashList (mobile) for long lists
- **Image Optimization:** Next.js Image component (web), react-native-fast-image (mobile)
- **Bundle Size:** Tree-shaking, dynamic imports for heavy libraries

**Testing Strategy:**
- **Unit Tests:** Jest + React Testing Library (components, hooks, utilities)
- **Integration Tests:** React Testing Library (component interactions)
- **E2E Tests:** Playwright (web), Detox (mobile)
- **Visual Regression:** Chromatic/Percy (web)

---

## 2. SERVICE DESIGN DETAILS (10 Microservices - Hexagonal)

All 10 microservices follow **Hexagonal Architecture** with consistent structure:
- **Domain Layer:** Pure business logic (entities, value objects, domain events)
- **Application Layer:** Use cases with port interfaces
- **Adapter Layer:** Infrastructure implementations (HTTP, gRPC, PostgreSQL, Kafka, Redis)

### 2.1 User Service

**Core Responsibilities:**
- Identity management (registration, login, password reset)
- JWT RS256 token lifecycle (access + refresh tokens)
- User profile management
- Address & payment method tokenization
- RBAC enforcement

**Tech Stack:**
- Language: Go 1.25
- Framework: Gin
- Database: PostgreSQL (own schema)
- Cache: Redis (JWT blacklist, session store)

**Hexagonal Structure:**
Follows Hexagonal Architecture structure as defined in Section 1.3.

**Domain Layer:**
- **Entities:** `user.go` (User aggregate root), `address.go`, `payment_method.go`
- **Value Objects:** `user_role.go` (CUSTOMER, RESTAURANT_OWNER, DRIVER, ADMIN)
- **Domain Events:** `user_registered.go`, `user_suspended.go`
- **Domain Services:** `password_hasher.go` (bcrypt)

**Application Layer:**
- **Primary Ports (in):** `auth_usecase.go` (Register, Login, Refresh), `user_usecase.go` (Profile CRUD), `address_usecase.go` (Address CRUD)
- **Secondary Ports (out):** `user_repository.go`, `token_repository.go`, `cache_repository.go`, `otp_provider.go`, `event_publisher.go`
- **Services:** `auth_service.go`, `user_service.go`, `token_manager.go` (JWT RS256)

**Adapter Layer:**
- **In:** HTTP handlers (`auth_handler.go`, `user_handler.go`), gRPC handler (`user_grpc_handler.go`)
- **Out:** PostgreSQL repositories, Redis cache, Twilio OTP provider

**Database Tables:**
- users, user_addresses, user_payment_methods, refresh_tokens

**Key APIs:**
```
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/refresh
POST   /api/v1/auth/logout
GET    /api/v1/users/profile
PUT    /api/v1/users/profile
GET    /api/v1/users/addresses
POST   /api/v1/users/addresses
PUT    /api/v1/users/addresses/{id}
DELETE /api/v1/users/addresses/{id}
GET    /api/v1/users/payment-methods
POST   /api/v1/users/payment-methods
```

**Port Interfaces:**
```go
// Primary Port
type AuthUseCase interface {
    Register(ctx context.Context, req *RegisterRequest) (*AuthResponse, error)
    Login(ctx context.Context, req *LoginRequest) (*AuthResponse, error)
    RefreshToken(ctx context.Context, refreshToken string) (*AuthResponse, error)
    Logout(ctx context.Context, userID string, refreshToken string) error
}

// Secondary Port
type UserRepository interface {
    Save(ctx context.Context, user *entity.User) error
    FindByID(ctx context.Context, id string) (*entity.User, error)
    FindByEmail(ctx context.Context, email string) (*entity.User, error)
    FindByPhone(ctx context.Context, phone string) (*entity.User, error)
    Update(ctx context.Context, user *entity.User) error
}
```

### 2.2 Catalog Service

**Core Responsibilities:**
- Restaurant registration & profile management
- Menu management (categories, items, variants)
- Item availability management
- Restaurant operational hours & service zones
- Menu indexing for search

**Tech Stack:**
- Language: Go 1.25
- Framework: Gin + gRPC
- Database: PostgreSQL
- Cache: Redis (menu cache)

**Hexagonal Structure:**
Follows Hexagonal Architecture structure as defined in Section 1.3.

**Domain Layer:**
- **Entities:** `restaurant.go` (Restaurant aggregate root), `menu_category.go`, `menu_item.go`, `menu_item_variant.go`
- **Value Objects:** `restaurant_status.go` (PENDING, ACTIVE, INACTIVE, SUSPENDED), `location.go` (Lat/Lng)
- **Domain Events:** `restaurant_created.go`, `menu_updated.go`

**Application Layer:**
- **Primary Ports (in):** `restaurant_usecase.go`, `menu_usecase.go`
- **Secondary Ports (out):** `restaurant_repository.go`, `menu_repository.go`, `cache_repository.go`, `event_publisher.go`
- **Services:** `restaurant_service.go`, `menu_service.go`

**Adapter Layer:**
- **In:** HTTP handlers (`restaurant_handler.go`, `menu_handler.go`), gRPC handler (`catalog_grpc_handler.go`)
- **Out:** PostgreSQL repositories, Redis cache

**Database Tables:**
- restaurants, menu_categories, menu_items, menu_item_variants

### 2.3 Order Service

**Core Responsibilities:**
- Order creation, state machine, lifecycle
- Cart management, pricing calculation
- Coupon validation (via Promotion Service)
- Order history, search, filtering
- Dispute handling (within order context)

**Tech Stack:**
- Language: Go 1.25
- Framework: Gin + gRPC
- Database: PostgreSQL
- Message Broker: Kafka producer/consumer
- Cache: Redis

**Hexagonal Structure:**
Follows Hexagonal Architecture structure as defined in Section 1.3.

**Domain Layer:**
- **Entities:** `order.go` (Order aggregate root), `order_item.go`, `cart.go`, `dispute.go`
- **Value Objects:** `order_status.go` (State machine states), `delivery_type.go`, `dispute_category.go`
- **Domain Events:** `order_created.go`, `order_confirmed.go`, `order_cancelled.go`, `dispute_created.go`
- **Domain Services:** `pricing_calculator.go`, `eta_calculator.go`

**Application Layer:**
- **Primary Ports (in):** `order_command.go` (CreateOrder, CancelOrder), `order_query.go` (GetOrder, ListOrders), `cart_usecase.go`, `dispute_usecase.go`
- **Secondary Ports (out):** `order_repository.go`, `payment_client.go`, `catalog_client.go`, `delivery_client.go`, `promotion_client.go`, `event_publisher.go`, `cache_repository.go`
- **Services:** `order_command_service.go`, `order_query_service.go`, `cart_service.go`, `dispute_service.go`
- **Saga:** `order_saga.go` (Saga orchestrator)

**Adapter Layer:**
- **In:** HTTP handlers (`order_handler.go`, `cart_handler.go`, `dispute_handler.go`), gRPC handler, Kafka consumers (`payment_event_consumer.go`, `delivery_event_consumer.go`)
- **Out:** PostgreSQL repositories, Redis cache, Kafka producer, service clients (payment, catalog, delivery)

**Database Tables:**
- orders, order_items, order_item_variants, order_events (audit trail), disputes

**Kafka Topics:**
- order.created, order.confirmed, order.cancelled, order.delivered, dispute.created

**State Machine (Updated with Exception States):**
```
CREATED
  ├─→ PAYMENT_FAILED (payment auth fails)
  │    └─→ CREATED (retry) or CANCELLED
  └─→ CONFIRMED (payment captured)
      ├─→ PREPARING (restaurant starts)
      ├─→ READY_FOR_PICKUP (restaurant ready)
      ├─→ ON_THE_WAY (driver picked up)
      │   ├─→ DELIVERED (successful delivery)
      │   ├─→ UNDELIVERABLE (customer unreachable - FR-ORD-11)
      │   └─→ DELIVERY_FAILED (address mismatch, driver emergency)
      ├─→ CANCELLED (customer/restaurant/system cancellation)
      └─→ AUTO_CANCELLED (SLA miss >60min - FR-ORD-14)
```

**Exception Flow Handlers:**

```go
// FR-ORD-11: Customer Unreachable Handler
func HandleCustomerUnreachable(ctx context.Context, deliveryTaskID string) error {
    task := getDeliveryTask(deliveryTaskID)
    
    // Driver initiates unreachable flow
    for attempt := 1; attempt <= 3; attempt++ {
        if callCustomer(task.Order.CustomerID, task.Order.ID) {
            return nil // Customer answered
        }
        time.Sleep(1 * time.Minute)
    }
    
    // Start 5-min wait timer
    timer := time.NewTimer(5 * time.Minute)
    select {
    case <-timer.C:
        // Mark as undeliverable
        task.Status = "UNDELIVERABLE"
        task.Order.Status = "DELIVERY_FAILED"
        updateDeliveryTask(ctx, task)
        
        // Notify support
        notificationService.SendToSupport(ctx, "Customer unreachable", task.Order)
        
        // Allow customer pickup within 30 min
        schedulePickupExpiry(ctx, task.Order.ID, 30*time.Minute)
        
        return nil
    case <-ctx.Done():
        return ctx.Err()
    }
}

// FR-ORD-12: Address Correction Handler
func HandleAddressCorrection(ctx context.Context, orderID string, newAddress Address) error {
    order := getOrder(orderID)
    originalAddress := order.DeliveryAddress
    
    // Calculate distance between addresses
    distance := calculateDistance(originalAddress, newAddress)
    
    if distance > 2.0 { // > 2km
        // Recalculate delivery fee
        additionalFee := calculateAdditionalDeliveryFee(distance - 2.0)
        newETA := recalculateETA(order.RestaurantID, newAddress)
        
        // Request customer confirmation
        confirmed := requestCustomerConfirmation(ctx, order.CustomerID, 
            additionalFee, newETA)
        
        if !confirmed {
            // Customer declined → Cancel order
            return cancelOrderWithRefund(ctx, orderID, "Address correction declined")
        }
        
        // Update order with new fee and address
        order.DeliveryFee += additionalFee
        order.TotalPrice += additionalFee
        order.DeliveryAddress = newAddress
        order.EstimatedDeliveryTime = newETA
        updateOrder(ctx, order)
        
        // Charge additional fee
        paymentService.CaptureAdditional(ctx, order.PaymentID, additionalFee)
    } else {
        // Distance ≤ 2km → Free address correction
        order.DeliveryAddress = newAddress
        order.EstimatedDeliveryTime = recalculateETA(order.RestaurantID, newAddress)
        updateOrder(ctx, order)
    }
    
    return nil
}

// FR-ORD-14: SLA Miss Auto-Cancellation
func MonitorOrderSLA(ctx context.Context) {
    ticker := time.NewTicker(1 * time.Minute)
    defer ticker.Stop()
    
    for {
        select {
        case <-ticker.C:
            now := time.Now()
            
            // Get all orders past SLA (estimated_delivery_time + 60 min)
            overdueOrders := orderRepo.FindOverdue(ctx, now)
            
            for _, order := range overdueOrders {
                // Auto-cancel
                order.Status = "AUTO_CANCELLED"
                order.CancellationReason = "SLA breach: Delivery > 60 min late"
                orderRepo.Update(ctx, order)
                
                // Full refund
                paymentService.RefundFull(ctx, order.PaymentID, 
                    "SLA miss auto-cancellation")
                
                // Issue 100k discount code
                couponService.IssueCompensation(ctx, order.CustomerID, 
                    100000, "SLA_BREACH_COMPENSATION")
                
                // Notify customer
                notificationService.Send(ctx, order.CustomerID, 
                    "Order cancelled due to delay. Full refund + 100k discount issued.")
                
                // Log incident for quality review
                auditService.LogIncident(ctx, "SLA_BREACH", order.ID, 
                    map[string]interface{}{
                        "restaurant_id": order.RestaurantID,
                        "driver_id": order.DeliveryTask.DriverID,
                        "delay_minutes": calculateDelay(order),
                    })
            }
        case <-ctx.Done():
            return
        }
    }
}
```

**Key APIs:**
```
POST   /api/v1/orders
GET    /api/v1/orders/{id}
GET    /api/v1/orders (paginated list)
PUT    /api/v1/orders/{id}/cancel
POST   /api/v1/orders/{id}/reorder
```

**Performance Optimization:**
- Index on (customer_id, created_at) for quick history fetch
- Cache recent menu items in Redis (1 hour TTL)
- Batch coupon validation calls to Promotion Service

### 2.4 Payment Service

**Core Responsibilities:**
- Payment session creation
- Gateway integration (Stripe/VNPay)
- Authorization & capture flow
- Webhook handling (gateway callbacks)
- Idempotency enforcement
- Refund processing
- Daily reconciliation

**Tech Stack:**
- Language: Go 1.25
- Framework: Gin + gRPC
- Database: PostgreSQL
- External: Stripe API / VNPay API

**Hexagonal Structure:**
Follows Hexagonal Architecture structure as defined in Section 1.3.

**Domain Layer:**
- **Entities:** `payment.go` (Payment aggregate root), `refund.go`
- **Value Objects:** `payment_status.go` (PENDING, AUTHORIZED, CAPTURED, FAILED, REFUNDED)
- **Domain Events:** `payment_authorized.go`, `payment_captured.go`, `payment_refunded.go`

**Application Layer:**
- **Primary Ports (in):** `payment_usecase.go` (Authorize, Capture, Refund)
- **Secondary Ports (out):** `payment_repository.go`, `payment_gateway.go` (Gateway abstraction for Stripe/VNPay), `idempotency_store.go`, `event_publisher.go`, `cache_repository.go`
- **Services:** `payment_service.go`, `idempotency_manager.go`, `reconciliation_service.go`

**Adapter Layer:**
- **In:** HTTP handlers (`payment_handler.go`, `webhook_handler.go`), gRPC handler, cron job (`reconciliation_job.go`)
- **Out:** PostgreSQL repositories, gateway adapters (`stripe_adapter.go`, `vnpay_adapter.go`), Kafka producer

**Database Tables:**
- payments, payment_refunds, payment_events (audit trail)

**Kafka Topics:**
- payment.authorized, payment.captured, payment.failed, payment.refunded

**Idempotency Pattern:**
```golang
// PaymentRequest includes idempotency_key (hash of request)
request := PaymentRequest{
    OrderID: "order-123",
    Amount: 500000,
    IdempotencyKey: "cust-123_order-123_timestamp_nonce"
}

// Check if idempotency_key already processed
if cached := cache.Get(request.IdempotencyKey); cached != nil {
    return cached  // Return cached response (no charge twice)
}

// Process payment
result := authorizeAndCapture(request)

// Store in idempotency cache (24h TTL)
cache.Set(request.IdempotencyKey, result, 24*time.Hour)

// Also store in database for long-term audit trail
db.Insert(idempotency_record)

return result
```

**Reconciliation Flow:**
```
Daily Job (Scheduled 2 AM):
  1. Query all payments with status=CAPTURED from yesterday
  2. Call Stripe/VNPay API for transaction list
  3. Match by amount + timestamp + customer
  4. Check for discrepancies:
     - Missing in gateway → potential issue, flag for manual review
     - Overcharged → auto-refund + incident
     - Undercharged → log (accept loss)
  5. Generate reconciliation report
  6. Email to finance team
```

**Key APIs:**
```
POST   /api/v1/payments/authorize
POST   /api/v1/payments/{id}/capture
POST   /api/v1/payments/{id}/refund
POST   /api/v1/webhooks/payment (from gateway)
GET    /api/v1/payments/reconciliation (daily report)
POST   /api/v1/payments/{id}/chargeback (handle chargeback - FR-PAY-10)
POST   /api/v1/payments/cod/{id}/verify (COD verification - FR-PAY-11)
POST   /api/v1/payments/disputes (payment dispute - FR-PAY-12)
```

**Exception Handlers (NEW - P0):**

```go
// FR-PAY-10: Chargeback Handling
func HandleChargeback(ctx context.Context, gatewayChargebackID string) error {
    // Received from gateway webhook
    chargeback := fetchChargebackFromGateway(gatewayChargebackID)
    
    payment := paymentRepo.FindByGatewayID(ctx, chargeback.TransactionID)
    if payment == nil {
        return errors.New("payment not found")
    }
    
    // Update payment status
    payment.Status = "CHARGEBACK"
    payment.ChargebackAmount = chargeback.Amount
    payment.ChargebackReason = chargeback.Reason
    paymentRepo.Update(ctx, payment)
    
    // Adjust settlement
    settlementService.AdjustBalance(ctx, payment.RestaurantID, -chargeback.Amount)
    
    // Notify restaurant owner
    notificationService.Send(ctx, payment.Order.Restaurant.OwnerID, 
        "Chargeback received for order #" + payment.OrderID)
    
    // Log for fraud detection
    fraudService.LogChargeback(ctx, payment.CustomerID, payment.OrderID, chargeback)
    
    // If chargeback reason is fraud, suspend customer
    if chargeback.Reason == "fraudulent" {
        userService.SuspendUser(ctx, payment.CustomerID, "Chargeback - fraudulent")
    }
    
    return nil
}

// FR-PAY-11: COD Collection Verification
func VerifyCODCollection(ctx context.Context, paymentID string, driverID string) error {
    payment := paymentRepo.FindByID(ctx, paymentID)
    
    if payment.MethodType != "COD" {
        return errors.New("not a COD payment")
    }
    
    // Driver confirms cash collection
    payment.Status = "CAPTURED"
    payment.CapturedAt = time.Now()
    payment.CapturedBy = driverID
    paymentRepo.Update(ctx, payment)
    
    // Add to driver's cash collection for end-of-day reconciliation
    driverCashService.RecordCollection(ctx, driverID, payment.Amount, payment.OrderID)
    
    // Publish event
    kafkaProducer.Publish("payment.cod_collected", payment)
    
    return nil
}

// End-of-day COD reconciliation
func ReconcileCODDaily(ctx context.Context) error {
    today := time.Now().Format("2006-01-02")
    
    drivers := driverService.GetActiveDrivers(ctx)
    
    for _, driver := range drivers {
        // Get expected COD collections
        expectedCollections := paymentRepo.FindCODByDriver(ctx, driver.ID, today)
        expectedTotal := sumAmounts(expectedCollections)
        
        // Get driver's reported cash
        reportedCash := driverCashService.GetDailyReport(ctx, driver.ID, today)
        
        // Compare
        discrepancy := expectedTotal - reportedCash
        
        if discrepancy != 0 {
            // Log discrepancy
            auditService.LogDiscrepancy(ctx, "COD_RECONCILIATION", map[string]interface{}{
                "driver_id": driver.ID,
                "date": today,
                "expected": expectedTotal,
                "reported": reportedCash,
                "discrepancy": discrepancy,
            })
            
            // Notify admin
            notificationService.SendToAdmin(ctx, 
                fmt.Sprintf("COD discrepancy for driver %s: %d VND", driver.ID, discrepancy))
            
            // Adjust driver balance
            if discrepancy > 0 {
                driverService.DeductBalance(ctx, driver.ID, discrepancy)
            }
        }
    }
    
    return nil
}

// FR-PAY-12: Payment Dispute Workflow
func HandlePaymentDispute(ctx context.Context, dispute PaymentDispute) error {
    payment := paymentRepo.FindByID(ctx, dispute.PaymentID)
    
    // Check dispute type
    switch dispute.Type {
    case "unauthorized":
        // Unauthorized transaction - immediate action
        if isValidUnauthorizedClaim(payment, dispute) {
            // Refund immediately
            refund, err := paymentService.RefundFull(ctx, payment.ID, 
                "Unauthorized transaction claim")
            if err != nil {
                return err
            }
            
            // Cancel order
            orderService.Cancel(ctx, payment.OrderID, "Payment dispute - unauthorized")
            
            // Flag for fraud review
            fraudService.FlagTransaction(ctx, payment.ID, "unauthorized_claim")
            
            // Suspend user if multiple disputes
            disputeCount := paymentRepo.CountDisputesByUser(ctx, payment.CustomerID)
            if disputeCount >= 3 {
                userService.SuspendUser(ctx, payment.CustomerID, 
                    "Multiple payment disputes")
            }
        }
        
    case "duplicate_charge":
        // Check for duplicate
        duplicates := paymentRepo.FindDuplicates(ctx, payment.CustomerID, 
            payment.Amount, payment.CreatedAt)
        
        if len(duplicates) > 1 {
            // Auto-refund duplicate charges
            for i := 1; i < len(duplicates); i++ {
                paymentService.RefundFull(ctx, duplicates[i].ID, 
                    "Duplicate charge detected")
            }
            
            dispute.Status = "RESOLVED"
            dispute.Resolution = "Duplicate refunded automatically"
        } else {
            dispute.Status = "REJECTED"
            dispute.Resolution = "No duplicate found"
        }
        
    default:
        // Other disputes require manual review
        dispute.Status = "UNDER_REVIEW"
        notificationService.SendToAdmin(ctx, "Payment dispute requires review", dispute)
    }
    
    paymentDisputeRepo.Create(ctx, dispute)
    return nil
}
```

### 2.5 Delivery Service

**Core Responsibilities:**
- Driver registration & verification
- GPS location tracking & updates
- Delivery task assignment algorithm
- Real-time ETA calculation
- Delivery status updates
- Driver earnings calculation

**Tech Stack:**
- Language: Go 1.25
- Framework: Gin + gRPC
- Database: PostgreSQL + PostGIS (geo-queries)
- Cache: Redis (driver location, ETA cache)
- Real-time: WebSocket (location streaming)

**Hexagonal Structure:**
Follows Hexagonal Architecture structure as defined in Section 1.3.

**Domain Layer:**
- **Entities:** `driver.go` (Driver aggregate root), `delivery_task.go` (DeliveryTask aggregate)
- **Value Objects:** `driver_status.go` (PENDING, APPROVED, REJECTED, SUSPENDED), `task_status.go` (CREATED, ASSIGNED, PICKED_UP, DELIVERED), `location.go` (Lat/Lng with timestamp)
- **Domain Events:** `driver_online.go`, `delivery_assigned.go`, `delivery_completed.go`
- **Domain Services:** `assignment_algorithm.go` (Nearest driver algorithm), `eta_calculator.go`

**Application Layer:**
- **Primary Ports (in):** `driver_usecase.go` (Register, Status, Location), `delivery_task_usecase.go` (Create, Assign, Update), `location_usecase.go` (GPS tracking)
- **Secondary Ports (out):** `driver_repository.go`, `delivery_task_repository.go`, `location_repository.go` (PostGIS queries), `event_publisher.go`, `maps_client.go` (Google Maps API)
- **Services:** `driver_service.go`, `delivery_task_service.go`, `location_service.go`

**Adapter Layer:**
- **In:** HTTP handlers (`driver_handler.go`, `delivery_task_handler.go`), gRPC handler, WebSocket handler (`location_ws_handler.go`), Kafka consumer (`order_event_consumer.go`)
- **Out:** PostgreSQL repositories (with PostGIS), Redis cache (`driver_location_cache.go`), Google Maps client

**Database Tables:**
- drivers, delivery_tasks
  - delivery_task_events
  - driver_location_history (partitioned)

Kafka Topics:
  - delivery.assigned
  - delivery.picked_up
  - delivery.delivered
  - delivery.cancelled
```

**Assignment Algorithm (MVP - Simple Nearest):**
```golang
func AssignDelivery(task *DeliveryTask) (*Driver, error) {
    // Get ready_for_pickup order
    pickup := task.PickupLocation
    
    // Find eligible drivers:
    // - status = APPROVED
    // - is_online = true
    // - distance ≤ 10km from pickup
    // - acceptance_rate ≥ 50%
    drivers := db.Query(`
        SELECT d.id, d.current_lat, d.current_lng, 
               earth_distance(ll_to_earth(d.current_lat, d.current_lng), 
                            ll_to_earth($1, $2)) / 1000 as distance_km
        FROM drivers d
        WHERE d.status = 'APPROVED'
          AND d.is_online = true
          AND d.acceptance_rate >= 0.5
          AND earth_distance(...) / 1000 <= 10
        ORDER BY distance_km ASC, d.rating DESC
        LIMIT 3
    `, pickup.Lat, pickup.Lng)
    
    // Send offers to top 3 drivers in order
    for _, driver := range drivers {
        offer := SendOfferAndWait(driver, task, 2*time.Second)
        if offer.Status == ACCEPTED {
            AssignTaskToDriver(task, driver)
            return driver, nil
        }
    }
    
    // If no acceptance within 5 min, try expanding radius
    if time.Now().Sub(task.CreatedAt) > 5*time.Minute {
        return AssignDelivery_ExpandedRadius(task, 15)  // 15km radius
    }
    
    return nil, errors.New("no driver available")
}
```

**Location Tracking (WebSocket):**
```
Driver App:
  1. Establish WebSocket connection to DeliveryService
  2. Send location every 10 seconds (lat, lng, timestamp)
  3. Service broadcasts to Order Service + Customer
  
Backend (DeliveryService):
  - Receive location update
  - Calculate ETA (distance to dropoff / avg speed)
  - Update delivery_task.current_location
  - Publish location.updated event to Kafka
  - Broadcast to WebSocket subscribers (customer, order service)

Customer App:
  - Subscribe to delivery task location updates
  - Update map marker in realtime
  - Display ETA countdown
```

**Key APIs:**
```
POST   /api/v1/drivers/register
PUT    /api/v1/drivers/{id}/status (online/offline)
POST   /api/v1/delivery-tasks (create task)
GET    /api/v1/delivery-tasks?driver_id=...
PUT    /api/v1/delivery-tasks/{id}/status
PUT    /api/v1/drivers/{id}/location (GPS update)
WS     /ws/delivery/{task_id}/location (WebSocket stream)
GET    /api/v1/drivers/{id}/earnings
```

### 2.6 Search Service

**Core Responsibilities:**
- Geo-based restaurant search
- Full-text search (restaurant name, cuisine)
- Filtering & ranking
- Caching for performance

**Tech Stack:**
- Language: Go 1.25
- Framework: Gin
- Database: PostgreSQL (read-only replica) + PostGIS
- Search Engine: Redis (MVP), Elasticsearch (Phase 2)
- Cache: Redis

**Hexagonal Structure:**
Follows Hexagonal Architecture structure as defined in Section 1.3.

**Domain Layer:**
- **Entities:** `search_result.go`
- **Value Objects:** `search_filters.go`, `sort_option.go`
- **Domain Services:** `ranking_algorithm.go`

**Application Layer:**
- **Primary Ports (in):** `search_usecase.go`
- **Secondary Ports (out):** `restaurant_repository.go` (Read-only), `geo_repository.go` (PostGIS queries), `cache_repository.go`
- **Services:** `search_service.go`

**Adapter Layer:**
- **In:** HTTP handler (`search_handler.go`)
- **Out:** PostgreSQL repository (`restaurant_search_repository.go`), Redis cache

**Redis Cache Structure:**
- Key: "restaurants:city:{city_id}:within_{radius}km"
- Value: JSON array of restaurants (5 min TTL)

**Search Query (MVP - Geo + Basic Filter):**
```sql
SELECT r.id, r.name, r.rating, r.total_reviews,
       ROUND(earth_distance(ll_to_earth(r.lat, r.lng),
                            ll_to_earth($1, $2)) / 1000, 2) as distance_km,
       COALESCE(r.estimated_delivery_time, 35) as est_delivery_min,
       r.is_accepting_orders, r.min_order_value
FROM restaurants r
WHERE r.status = 'ACTIVE'
  AND r.city_id = $3
  AND earth_distance(ll_to_earth(r.lat, r.lng),
                     ll_to_earth($1, $2)) / 1000 <= $4  -- within radius
  AND ($5 IS NULL OR r.rating >= $5)  -- min rating filter
  AND ($6 IS NULL OR r.is_accepting_orders = $6)  -- open now filter
ORDER BY 
  CASE WHEN $7 = 'distance' THEN distance_km END ASC,
  CASE WHEN $7 = 'rating' THEN r.rating END DESC,
  CASE WHEN $7 = 'delivery_time' THEN est_delivery_min END ASC
LIMIT $8 OFFSET $9;
```

**Key APIs:**
```
GET    /api/v1/search?q={keyword}&lat={lat}&lng={lng}&distance_km={radius}&sort=distance&page=1
GET    /api/v1/restaurants/{id}/menu
```

### 2.7 Promotion Service

**Core Responsibilities:**
- Coupon creation & management
- Coupon validation & usage tracking
- Promotion campaign management (Phase 2)

**Tech Stack:**
- Language: Go 1.25
- Framework: Gin
- Database: PostgreSQL
- Cache: Redis (active coupons)

**Hexagonal Structure:**
Follows Hexagonal Architecture structure as defined in Section 1.3.

**Domain Layer:**
- **Entities:** `coupon.go` (Coupon aggregate)
- **Value Objects:** `coupon_type.go` (PERCENT, FLAT)
- **Domain Services:** `discount_calculator.go`

**Application Layer:**
- **Primary Ports (in):** `coupon_usecase.go` (Validate, Apply)
- **Secondary Ports (out):** `coupon_repository.go`, `usage_repository.go`, `cache_repository.go`, `event_publisher.go`
- **Services:** `coupon_service.go`

**Adapter Layer:**
- **In:** HTTP handler (`coupon_handler.go`), gRPC handler (`promotion_grpc_handler.go`)
- **Out:** PostgreSQL repositories, Redis cache

**Database Tables:**
- coupons, coupon_usages

**Kafka Topics:**
- coupon.applied, coupon.expired

**Coupon Validation Logic:**
```go
func ValidateCoupon(ctx context.Context, code string, userID string, 
    orderAmount float64) (*Coupon, error) {
    
    coupon := couponRepo.FindByCode(ctx, code)
    if coupon == nil {
        return nil, ErrCouponNotFound
    }
    
    // Check active status
    if !coupon.IsActive {
        return nil, ErrCouponInactive
    }
    
    // Check time validity
    now := time.Now()
    if coupon.StartTime != nil && now.Before(*coupon.StartTime) {
        return nil, ErrCouponNotYetValid
    }
    if coupon.EndTime != nil && now.After(*coupon.EndTime) {
        return nil, ErrCouponExpired
    }
    
    // Check minimum order value
    if coupon.MinOrderValue > 0 && orderAmount < coupon.MinOrderValue {
        return nil, ErrMinOrderValueNotMet
    }
    
    // Check global usage limit
    if coupon.GlobalUsageLimit > 0 {
        totalUsage := couponRepo.CountTotalUsage(ctx, coupon.ID)
        if totalUsage >= coupon.GlobalUsageLimit {
            return nil, ErrCouponUsageLimitReached
        }
    }
    
    // Check per-user usage limit
    if coupon.PerUserUsageLimit > 0 {
        userUsage := couponRepo.CountUserUsage(ctx, coupon.ID, userID)
        if userUsage >= coupon.PerUserUsageLimit {
            return nil, ErrUserUsageLimitReached
        }
    }
    
    return coupon, nil
}

func ApplyCoupon(coupon *Coupon, subtotal float64) float64 {
    var discount float64
    
    switch coupon.Type {
    case "PERCENT":
        discount = subtotal * (coupon.DiscountValue / 100.0)
    case "FLAT":
        discount = coupon.DiscountValue
    }
    
    // Apply max discount cap
    if coupon.MaxDiscount > 0 && discount > coupon.MaxDiscount {
        discount = coupon.MaxDiscount
    }
    
    return discount
}
```

**Key APIs:**
```
POST   /api/v1/coupons/validate (validate before order)
POST   /api/v1/orders/{id}/apply-coupon
GET    /api/v1/coupons (active coupons for user)
```

### 2.8 Notification Service

**Core Responsibilities:**
- Push notifications (FCM/APNs)
- SMS notifications (Twilio)
- Email notifications (Phase 2)
- Retry logic & delivery guarantees
- Template management

**Tech Stack:**
- Language: Go 1.25
- Framework: Gin (HTTP) + Background workers
- Message Queue: Kafka consumer
- External: FCM, Twilio, SendGrid

**Hexagonal Structure:**
Follows Hexagonal Architecture structure as defined in Section 1.3.

**Domain Layer:**
- **Entities:** `notification.go`
- **Value Objects:** `channel.go` (PUSH, SMS, EMAIL), `priority.go` (HIGH, MEDIUM, LOW)
- **Domain Services:** `template_renderer.go`

**Application Layer:**
- **Primary Ports (in):** `notification_usecase.go`, `preference_usecase.go`
- **Secondary Ports (out):** `notification_repository.go`, `push_sender.go` (FCM/APNs interface), `sms_sender.go` (Twilio interface), `email_sender.go` (SendGrid interface)
- **Services:** `notification_service.go`, `retry_manager.go`

**Adapter Layer:**
- **In:** HTTP handler (`preference_handler.go`), Kafka consumers (`order_event_consumer.go`, `payment_event_consumer.go`, `delivery_event_consumer.go`)
- **Out:** PostgreSQL repositories, external senders (`fcm_push_sender.go`, `twilio_sms_sender.go`, `sendgrid_email_sender.go`)

**Database Tables:**
- notifications, notification_preferences

**Kafka Topics (consumed):**
- order.*, payment.*, delivery.*

**Event-to-Notification Mapping:**
```go
var notificationRules = map[string]NotificationRule{
    "order.confirmed": {
        Recipient: "customer",
        Channels: []string{"push", "sms"},
        Template: "order_confirmed",
        Priority: "high",
    },
    "order.preparing": {
        Recipient: "customer",
        Channels: []string{"push"},
        Template: "order_preparing",
        Priority: "medium",
    },
    "delivery.assigned": {
        Recipient: "customer",
        Channels: []string{"push"},
        Template: "driver_assigned",
        Priority: "high",
    },
    "delivery.picked_up": {
        Recipient: "customer",
        Channels: []string{"push"},
        Template: "order_on_the_way",
        Priority: "high",
    },
    "delivery.delivered": {
        Recipient: "customer",
        Channels: []string{"push", "sms"},
        Template: "order_delivered",
        Priority: "high",
    },
}

func ProcessEvent(ctx context.Context, event KafkaEvent) error {
    rule, exists := notificationRules[event.Type]
    if !exists {
        return nil // No notification needed
    }
    
    // Get user preferences
    prefs := getNotificationPreferences(event.UserID)
    
    // Send via enabled channels
    for _, channel := range rule.Channels {
        if prefs.IsEnabled(channel, event.Type) {
            notification := buildNotification(event, rule.Template)
            
            switch channel {
            case "push":
                pushSender.Send(ctx, notification)
            case "sms":
                smsSender.Send(ctx, notification)
            case "email":
                emailSender.Send(ctx, notification)
            }
        }
    }
    
    return nil
}
```

**Retry Strategy:**
```go
func SendWithRetry(ctx context.Context, notification *Notification) error {
    maxRetries := 3
    backoff := []time.Duration{1 * time.Second, 5 * time.Second, 15 * time.Second}
    
    for attempt := 0; attempt <= maxRetries; attempt++ {
        err := send(ctx, notification)
        if err == nil {
            notification.Status = "SENT"
            notificationRepo.Update(ctx, notification)
            return nil
        }
        
        if attempt < maxRetries {
            time.Sleep(backoff[attempt])
        }
    }
    
    notification.Status = "FAILED"
    notification.FailureReason = "Max retries exceeded"
    notificationRepo.Update(ctx, notification)
    
    return errors.New("notification delivery failed")
}
```

**Key APIs:**
```
GET    /api/v1/notifications (user's notification history)
PUT    /api/v1/notifications/{id}/read
PUT    /api/v1/notifications/read-all
GET    /api/v1/notification-preferences
PUT    /api/v1/notification-preferences (update preferences)
```

### 2.9 Rating Service

**Core Responsibilities:**
- Rating & review submission (restaurant, driver)
- Aggregate rating calculation
- Review moderation (Phase 2)

**Tech Stack:**
- Language: Go 1.25
- Framework: Gin
- Database: PostgreSQL
- Cache: Redis (aggregate ratings)

**Hexagonal Structure:**
Follows Hexagonal Architecture structure as defined in Section 1.3.

**Domain Layer:**
- **Entities:** `rating.go`
- **Value Objects:** `rating_type.go` (RESTAURANT, DRIVER)
- **Domain Services:** `aggregate_calculator.go`

**Application Layer:**
- **Primary Ports (in):** `rating_usecase.go`
- **Secondary Ports (out):** `rating_repository.go`, `restaurant_client.go` (Update aggregate), `driver_client.go`, `cache_repository.go`, `event_publisher.go`
- **Services:** `rating_service.go`

**Adapter Layer:**
- **In:** HTTP handler (`rating_handler.go`), Kafka consumer (`order_delivered_consumer.go`)
- **Out:** PostgreSQL repositories, Redis cache, service clients

**Database Tables:**
- ratings

**Kafka Topics:**
- rating.submitted

**Aggregate Rating Calculation:**
```go
func UpdateAggregateRating(ctx context.Context, rateeID string, 
    rateeType string) error {
    
    ratings := ratingRepo.FindByRatee(ctx, rateeID, rateeType)
    
    if len(ratings) == 0 {
        return nil
    }
    
    // Calculate weighted average (recent ratings have higher weight)
    var weightedSum float64
    var totalWeight float64
    now := time.Now()
    
    for _, rating := range ratings {
        age := now.Sub(rating.CreatedAt).Hours() / 24 // days
        weight := 1.0 / (1.0 + age/365.0) // Decay over 1 year
        
        weightedSum += float64(rating.Score) * weight
        totalWeight += weight
    }
    
    avgRating := weightedSum / totalWeight
    
    // Update ratee's aggregate rating
    switch rateeType {
    case "RESTAURANT":
        restaurantRepo.UpdateRating(ctx, rateeID, avgRating, len(ratings))
    case "DRIVER":
        driverRepo.UpdateRating(ctx, rateeID, avgRating, len(ratings))
    }
    
    // Invalidate cache
    cacheService.Delete(ctx, fmt.Sprintf("rating:%s:%s", rateeType, rateeID))
    
    return nil
}
```

**Key APIs:**
```
POST   /api/v1/restaurants/{id}/ratings
GET    /api/v1/restaurants/{id}/ratings
POST   /api/v1/drivers/{id}/ratings
GET    /api/v1/drivers/{id}/ratings
GET    /api/v1/orders/{id}/rating (check if user rated)
```

### 2.10 Admin Service

**Core Responsibilities:**
- Dashboard & KPI reporting
- User management (suspension, deletion)
- Restaurant onboarding workflow
- Driver management
- Payment reconciliation
- System configuration

**Tech Stack:**
- Language: Go 1.25
- Framework: Gin
- Database: PostgreSQL (read replicas for reporting)
- Cache: Redis

**Hexagonal Structure:**
Follows Hexagonal Architecture structure as defined in Section 1.3.

**Domain Layer:**
- **Entities:** `system_config.go`
- **Value Objects:** `dashboard_metrics.go`

**Application Layer:**
- **Primary Ports (in):** `dashboard_usecase.go`, `user_management_usecase.go`, `restaurant_management_usecase.go`, `driver_management_usecase.go`, `config_usecase.go`
- **Secondary Ports (out):** `user_repository.go`, `order_repository.go` (Read-only for reports), `payment_repository.go` (Reconciliation), `restaurant_repository.go`, `driver_repository.go`, `audit_repository.go`
- **Services:** `dashboard_service.go`, `user_management_service.go`, `reconciliation_service.go`

**Adapter Layer:**
- **In:** HTTP handlers (`dashboard_handler.go`, `user_management_handler.go`, `restaurant_management_handler.go`, `config_handler.go`)
- **Out:** PostgreSQL repositories

**Database Tables:**
- admin_users, system_config, audit_logs

**Key Components (Legacy reference):**
```
AdminService
  ├── DashboardController (REST)
  ├── UserManagementController
  ├── RestaurantManagementController
  ├── DriverManagementController
  ├── ReportingService (KPIs, analytics)
  ├── ConfigurationService (system settings)
  ├── AuditService (action logging)
  └── AdminRepository (queries)

Database Tables:
  - admin_users (separate from regular users)
  - system_config (fees, rules)
  - admin_audit_logs (all admin actions)
```

**Dashboard KPIs:**
```go
type DashboardMetrics struct {
    TotalOrders         int64   `json:"total_orders"`
    TotalRevenue        float64 `json:"total_revenue"`
    ActiveUsers         int64   `json:"active_users"`
    AverageOrderValue   float64 `json:"average_order_value"`
    OnTimeDeliveryRate  float64 `json:"on_time_delivery_rate"`
    AverageRating       float64 `json:"avg_rating"`
    NewCustomers        int64   `json:"new_customers"`
    NewRestaurants      int64   `json:"new_restaurants"`
    ActiveDrivers       int64   `json:"active_drivers"`
    CancellationRate    float64 `json:"cancellation_rate"`
}

func GenerateDashboard(ctx context.Context, cityID int64, 
    fromDate, toDate time.Time) (*DashboardMetrics, error) {
    
    metrics := &DashboardMetrics{}
    
    // Parallel queries for performance
    var wg sync.WaitGroup
    errChan := make(chan error, 9)
    
    wg.Add(9)
    
    go func() {
        defer wg.Done()
        metrics.TotalOrders = orderRepo.CountBetween(ctx, cityID, fromDate, toDate)
    }()
    
    go func() {
        defer wg.Done()
        metrics.TotalRevenue = orderRepo.SumRevenue(ctx, cityID, fromDate, toDate)
    }()
    
    go func() {
        defer wg.Done()
        metrics.ActiveUsers = userRepo.CountActive(ctx, cityID, fromDate, toDate)
    }()
    
    // ... more parallel queries
    
    wg.Wait()
    close(errChan)
    
    // Check for errors
    for err := range errChan {
        if err != nil {
            return nil, err
        }
    }
    
    return metrics, nil
}
```

**Key APIs:**
```
GET    /api/v1/admin/dashboard
GET    /api/v1/admin/users
PUT    /api/v1/admin/users/{id}/suspend
PUT    /api/v1/admin/users/{id}/activate
GET    /api/v1/admin/restaurants
PUT    /api/v1/admin/restaurants/{id}/approve
PUT    /api/v1/admin/restaurants/{id}/reject
GET    /api/v1/admin/drivers
PUT    /api/v1/admin/drivers/{id}/approve
GET    /api/v1/admin/payments/reconciliation
POST   /api/v1/admin/coupons
GET    /api/v1/admin/reports/revenue
GET    /api/v1/admin/reports/orders
GET    /api/v1/admin/reports/sla
GET    /api/v1/admin/config
PUT    /api/v1/admin/config
```

### 2.11 Dispute Handling (Part of Order Service)

> **Note:** Dispute handling is integrated into Order Service (Section 2.3) following the Hexagonal Architecture pattern. The dispute functionality includes: `domain/entity/dispute.go`, `application/port/in/dispute_usecase.go`, and `adapter/in/http/handler/dispute_handler.go`.

**Key Responsibilities (within Order Service):**
- Dispute ticket lifecycle management
- Issue categorization & evidence collection
- Automated assessment for simple cases
- Admin review workflow (coordinated with Admin Service)
- Resolution & compensation processing
- Quality scoring for restaurants/drivers

**Database Tables (within Order Service):**
- disputes
- (linked to orders, order_items)

**Auto-Resolution Engine:**
```go
type AutoResolutionRule struct {
    Category     string
    CanAutoResolve bool
    Compensation CompensationType
}

var autoResolutionRules = map[string]AutoResolutionRule{
    "missing_item": {
        Category: "missing_item",
        CanAutoResolve: true,
        Compensation: CompensationType{
            Type: "refund_plus_discount",
            RefundAmount: "item_price",
            DiscountAmount: 10000, // 10k VND
        },
    },
    "wrong_item": {
        Category: "wrong_item",
        CanAutoResolve: true,
        Compensation: CompensationType{
            Type: "refund_plus_discount",
            RefundAmount: "item_price",
            DiscountAmount: 20000, // 20k VND
        },
    },
    "late_delivery": {
        Category: "late_delivery",
        CanAutoResolve: true,
        Compensation: CompensationType{
            Type: "discount",
            DiscountAmount: 25000, // 25k VND
        },
    },
    "quality": {
        Category: "quality",
        CanAutoResolve: false, // Requires admin review
    },
    "driver_behavior": {
        Category: "driver_behavior",
        CanAutoResolve: false, // Requires admin review
    },
}

func ProcessDispute(ctx context.Context, dispute *Dispute) error {
    rule, exists := autoResolutionRules[dispute.Category]
    
    if !exists {
        return errors.New("invalid dispute category")
    }
    
    if rule.CanAutoResolve {
        // Auto-resolve
        return autoResolve(ctx, dispute, rule.Compensation)
    } else {
        // Assign to admin review queue
        return assignToAdminQueue(ctx, dispute)
    }
}

func autoResolve(ctx context.Context, dispute *Dispute, 
    comp CompensationType) error {
    
    order := orderRepo.FindByID(ctx, dispute.OrderID)
    
    // Calculate refund amount
    var refundAmount float64
    if comp.RefundAmount == "item_price" {
        // Find disputed item price
        for _, item := range order.Items {
            if item.Name == dispute.ItemName {
                refundAmount = item.Price
                break
            }
        }
    }
    
    // Process refund
    if refundAmount > 0 {
        paymentService.RefundPartial(ctx, order.PaymentID, refundAmount, 
            "Dispute auto-resolved: " + dispute.Category)
    }
    
    // Issue discount code
    if comp.DiscountAmount > 0 {
        couponService.IssueCompensation(ctx, order.CustomerID, 
            comp.DiscountAmount, "DISPUTE_COMPENSATION")
    }
    
    // Update dispute status
    dispute.Status = "resolved"
    dispute.ResolutionType = "auto_resolved"
    dispute.ResolutionAmount = refundAmount + comp.DiscountAmount
    dispute.ResolvedAt = time.Now()
    disputeRepo.Update(ctx, dispute)
    
    // Impact quality scores
    qualityScoreService.RecordDispute(ctx, order.RestaurantID, 
        dispute.Category, "restaurant")
    
    // Notify all parties
    notificationService.NotifyDisputeResolution(ctx, dispute)
    
    // Publish event
    kafkaProducer.Publish("dispute.auto_resolved", dispute)
    
    return nil
}

func assignToAdminQueue(ctx context.Context, dispute *Dispute) error {
    dispute.Status = "investigating"
    dispute.AssignedToAdmin = true
    disputeRepo.Update(ctx, dispute)
    
    // Notify admin team
    notificationService.SendToAdmin(ctx, "New dispute requires review", dispute)
    
    // Set SLA timer (24 hours)
    scheduleService.Schedule(ctx, "dispute_sla_check", dispute.ID, 24*time.Hour)
    
    return nil
}
```

**Key APIs:**
```
POST   /api/v1/disputes (create dispute)
GET    /api/v1/disputes/{id} (get detail)
GET    /api/v1/disputes (list with filters)
PUT    /api/v1/disputes/{id}/resolve (admin only)
POST   /api/v1/disputes/{id}/evidence (upload photo)
```

---

## 3. DATABASE DESIGN & SCHEMA

### 3.1 Database Schema Reference

The complete database schema, including all table definitions, constraints, and data types, is specified in the **SRS Section 4.1 (Data Model Highlights)**.

**Reference**: See [SRS_FoodDelivery.md](SRS_FoodDelivery.md) Section 4.1 for:
- All 17 core entity tables with full PostgreSQL DDL
- Table relationships and foreign key constraints
- Enum types and check constraints
- Default values and column specifications

**Design Notes**:
- Each microservice uses its own PostgreSQL schema (namespace) within the same database instance
- Tables follow the naming convention: `{service}_{entity}` (e.g., `order_orders`, `user_users`)
- All tables include audit fields: `created_by`, `updated_by`, `created_at`, `updated_at`
- Soft delete pattern: `is_deleted` boolean flag instead of physical deletion

### 3.2 Index Strategy

The complete index definitions for all tables are specified in the **SRS Section 4.2 (Key Indexes)**.

**Reference**: See [SRS_FoodDelivery.md](SRS_FoodDelivery.md) Section 4.2 for:
- All index definitions (40+ indexes)
- Partial indexes with WHERE clauses
- GIST indexes for geospatial queries
- Composite indexes for common query patterns

**Design Implementation Notes**:
- Indexes are created via database migrations (Flyway/Liquibase)
- Partial indexes (with WHERE clauses) are used to reduce index size and improve write performance
- GIST indexes on `(lat, lng)` columns use `ll_to_earth()` function for PostGIS geospatial queries
- Index maintenance: Monitor index bloat monthly, REINDEX quarterly
- Index naming: `idx_{table}_{column(s)}` for single/multi-column indexes

### 3.3 Sharding Strategy (Phase 3+)

```
Current (MVP/Phase 2): Single PostgreSQL instance
  - Max capacity: ~1TB data, 10k concurrent connections

Phase 3 (If > 1TB):
  - Shard by city_id (HCM shard, HN shard, BH shard)
  - Each city has own PostgreSQL replica set
  - Queries filtered by city at application layer
  - Cross-city queries handled by aggregation service
```

### 3.4 Backup & Recovery

```
Backup Strategy:
  - Daily: PostgreSQL point-in-time recovery (WAL archiving to S3)
  - Weekly: Full snapshot (S3)
  - Monthly: Cross-region backup (DR)

Recovery:
  - RTO: 30 min (restore from latest WAL)
  - RPO: 0 min (continuous WAL streaming)
  - Test: Monthly DR drills
```

---

## 4. API DESIGN & CONTRACTS

### 4.1 REST API Standards

**Versioning:**
- URL-based: `/api/v1/...`, `/api/v2/...`
- Support 2 major versions simultaneously
- Deprecation notice: 6 months before removal

**Request/Response Format:**
```json
Request:
{
  "customer_id": "uuid",
  "items": [...],
  "coupon_code": "SAVE10"
}

Response (Success - 200):
{
  "data": {
    "order_id": "uuid",
    "status": "CREATED",
    "total": 500000
  },
  "meta": {
    "timestamp": "2026-01-20T10:00:00Z",
    "version": "v1"
  }
}

Response (Error - 400/500):
{
  "error": {
    "code": "INVALID_COUPON",
    "message": "Coupon code not found or expired",
    "details": {...}
  },
  "meta": {
    "timestamp": "2026-01-20T10:00:00Z",
    "request_id": "uuid"
  }
}
```

**Status Codes:**
- 200: OK
- 201: Created
- 400: Bad Request (validation)
- 401: Unauthorized
- 403: Forbidden (no permission)
- 404: Not Found
- 409: Conflict (duplicate, state violation)
- 429: Too Many Requests (rate limit)
- 500: Internal Server Error
- 503: Service Unavailable

### 4.2 Standardized Error Response Schema (NEW - P0)

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
| 422 | `PAYMENT_FAILED` | Payment authorization failed |
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

**Implementation Example:**

```go
// Middleware to inject trace_id
func TraceIDMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        traceID := c.GetHeader("X-Request-ID")
        if traceID == "" {
            traceID = uuid.New().String()
        }
        c.Set("trace_id", traceID)
        c.Header("X-Request-ID", traceID)
        c.Next()
    }
}

// Error response helper
type APIError struct {
    Code    string                 `json:"code"`
    Message string                 `json:"message"`
    Details map[string]interface{} `json:"details,omitempty"`
    TraceID string                 `json:"trace_id"`
}

func RespondError(c *gin.Context, statusCode int, code string, 
    message string, details map[string]interface{}) {
    
    c.JSON(statusCode, gin.H{
        "error": APIError{
            Code:    code,
            Message: message,
            Details: details,
            TraceID: c.GetString("trace_id"),
        },
    })
}

// Usage
if coupon == nil {
    RespondError(c, 400, "COUPON_INVALID", 
        "Coupon code not found or expired",
        map[string]interface{}{
            "code": requestedCode,
            "reason": "not_found",
        })
    return
}
```

### 4.3 Complete API Contracts

*Note: See SRS Section 5 for full API contract details. Key additions below:*

**Dispute APIs (NEW - P0):**
```
POST   /api/v1/disputes
GET    /api/v1/disputes/{id}
GET    /api/v1/disputes?status=open&customer_id={id}
PUT    /api/v1/disputes/{id}/resolve (admin only)
POST   /api/v1/disputes/{id}/evidence
```

**Admin APIs (NEW):**
```
GET    /api/v1/admin/dashboard?city_id={id}&from_date={date}&to_date={date}
GET    /api/v1/admin/users?role={role}&status={status}
PUT    /api/v1/admin/users/{id}/suspend
GET    /api/v1/admin/restaurants?status=PENDING
PUT    /api/v1/admin/restaurants/{id}/approve
GET    /api/v1/admin/drivers?status=PENDING
PUT    /api/v1/admin/drivers/{id}/approve
GET    /api/v1/admin/payments/reconciliation?date={date}
POST   /api/v1/admin/coupons
GET    /api/v1/admin/reports/revenue
GET    /api/v1/admin/reports/sla
```

### 4.4 WebSocket API Contract (NEW - P0)

**Connection:**
```
wss://api.fooddelivery.com/ws?token={jwt_token}
```

**Client → Server Messages:**
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

**Server → Client Messages:**
```json
// Order status change
{
  "type": "order_status",
  "data": {
    "order_id": "uuid",
    "status": "PREPARING",
    "updated_at": "2026-01-21T10:30:00Z"
  }
}

// Driver location update (every 5s when ON_THE_WAY)
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

// ETA update
{
  "type": "eta_update",
  "data": {
    "order_id": "uuid",
    "eta_minutes": 8,
    "reason": "traffic_cleared"
  }
}

// Connection acknowledgment
{"type": "pong"}

// Subscription confirmation
{"type": "subscribed", "channel": "order:12345"}

// Error
{
  "type": "error",
  "data": {
    "code": "SUBSCRIPTION_FAILED",
    "message": "Order not found or access denied"
  }
}
```

**WebSocket Implementation (Go):**
```go
import (
    "github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
    CheckOrigin: func(r *http.Request) bool {
        return true // Validate origin properly in production
    },
}

func HandleWebSocket(w http.ResponseWriter, r *http.Request) {
    // Validate JWT
    token := r.URL.Query().Get("token")
    userID, err := validateJWT(token)
    if err != nil {
        http.Error(w, "Unauthorized", 401)
        return
    }
    
    // Upgrade connection
    conn, err := upgrader.Upgrade(w, r, nil)
    if err != nil {
        return
    }
    defer conn.Close()
    
    // Create client
    client := &Client{
        UserID: userID,
        Conn:   conn,
        Send:   make(chan []byte, 256),
    }
    
    // Register client
    hub.Register <- client
    
    // Start read/write pumps
    go client.WritePump()
    go client.ReadPump()
}

// Redis Pub/Sub listener
func ListenToRedisChannel(channel string) {
    pubsub := redisClient.Subscribe(ctx, channel)
    defer pubsub.Close()
    
    for msg := range pubsub.Channel() {
        // Broadcast to connected WebSocket clients
        hub.Broadcast <- []byte(msg.Payload)
    }
}
```

### 4.2 OpenAPI Specification

```yaml
openapi: 3.0.0
info:
  title: Food Delivery API
  version: 1.0.0
paths:
  /api/v1/orders:
    post:
      summary: Create new order
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                restaurant_id:
                  type: string
                  format: uuid
                items:
                  type: array
                  items:
                    type: object
      responses:
        '201':
          description: Order created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Order'
        '400':
          description: Invalid request
```

---

## 5. TECHNOLOGY STACK

### 5.1 Backend

| Layer | Technology | Rationale |
|:---|:---|:---|
| **Language** | Go 1.21+ | Performance, concurrency, fast startup, easy deployment |
| **Framework** | Gin / Echo | Lightweight, fast, good ecosystem |
| **RPC** | gRPC | Service-to-service, high performance |
| **Database** | PostgreSQL 14+ | Mature, reliable, ACID, JSON support, PostGIS |
| **Cache** | Redis 7+ | Fast in-memory cache, pub/sub, session store |
| **Message Broker** | Kafka 3+ | Event streaming, durability, scalability |
| **Search (Phase 2)** | Elasticsearch 8+ | Full-text, geo-search, analytics |
| **Object Storage** | S3 / MinIO | Images, documents, backups |
| **Container** | Docker | Reproducible builds, easy deployment |
| **Orchestration** | Kubernetes | HA, autoscaling, self-healing |

### 5.2 Frontend

| Layer | Technology | Rationale |
|:---|:---|:---|
| **Web** | React 18+ / Next.js | Modern, component-based, SSR support |
| **Mobile (iOS & Android)** | React Native 0.73+ (TypeScript) | Cross-platform, code sharing, faster development |
| **JS Engine (Mobile)** | Hermes | Optimized for React Native, faster startup |
| **State Management** | Redux / Zustand / React Query | Shared across web and mobile codebases |
| **HTTP Client** | Axios / fetch | Consistent API, Promise-based, interceptors |
| **Navigation (Mobile)** | React Navigation 6+ | Native-feeling navigation stack |
| **Styling (Web)** | Tailwind CSS | Utility-first, responsive, fast |
| **Styling (Mobile)** | StyleSheet / NativeWind | React Native styling, Tailwind-like syntax |
| **Map Integration** | react-native-maps / Google Maps SDK | Cross-platform geo-location, directions |
| **Real-time** | socket.io-client | React Native compatible WebSocket client |
| **Build Tools (Web)** | Vite | Fast builds, optimized bundling |
| **Build Tools (Mobile)** | Metro Bundler / Fastlane | React Native bundler, automated builds |
| **Native Modules** | react-native-keychain, react-native-firebase | Bridge to native platform APIs |
| **OTA Updates** | CodePush (optional) | Hot updates without app store release |
| **Code Sharing** | Monorepo (Turborepo/Nx) | Share code between web and mobile |

### 5.3 DevOps & Monitoring

| Tool | Purpose |
|:---|:---|
| **CI/CD** | GitHub Actions / GitLab CI |
| **Container Registry** | Amazon ECR / Google Artifact Registry |
| **Orchestration** | Kubernetes (EKS / GKE) |
| **Configuration** | Helm, Kustomize |
| **GitOps** | ArgoCD |
| **Monitoring** | Prometheus + Grafana |
| **Logging** | ELK (Elasticsearch, Logstash, Kibana) or Loki |
| **Tracing** | Jaeger / Tempo |
| **Error Tracking** | Sentry |
| **Infrastructure as Code** | Terraform / CloudFormation |

---

## 6. DEPLOYMENT ARCHITECTURE

### 6.1 Infrastructure Layout

```
┌─────────────────────────────────────────────────────────────┐
│                     AWS / GCP                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────┐    ┌──────────────────────────────┐  │
│  │ CDN (CloudFront) │    │ Domain (Route 53)            │  │
│  └────────┬─────────┘    └─────────────┬────────────────┘  │
│           │                            │                    │
│  ┌────────▼────────────────────────────▼──────────────┐    │
│  │              Application Load Balancer              │    │
│  │         (HTTPS, SSL termination, routing)          │    │
│  └────────┬──────────────────────────────────────────┘    │
│           │                                                 │
│  ┌────────▼────────────────────────────────────────────┐   │
│  │           Kubernetes Cluster (EKS)                 │   │
│  │                                                     │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐             │   │
│  │  │ User    │  │ Order   │  │ Search  │  (Services) │   │
│  │  │ Service │  │ Service │  │ Service │             │   │
│  │  └─────────┘  └─────────┘  └─────────┘             │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐             │   │
│  │  │ Payment │  │Delivery │  │Notif    │             │   │
│  │  │ Service │  │ Service │  │ Service │             │   │
│  │  └─────────┘  └─────────┘  └─────────┘             │   │
│  │                                                     │   │
│  │  Min Replicas: 2, Max: 10 (HPA by CPU%)            │   │
│  └────────┬────────────────────────────────────────────┘   │
│           │                                                 │
│  ┌────────▼────────────────────────────────────────────┐   │
│  │          StatefulSet (Data Layer)                  │   │
│  │  ┌──────────────────────────────────────────────┐  │   │
│  │  │ PostgreSQL (Primary + 2 Read Replicas)      │  │   │
│  │  │ - Multi-AZ deployment                       │  │   │
│  │  │ - Automated backup (daily)                  │  │   │
│  │  │ - WAL archiving to S3                       │  │   │
│  │  └──────────────────────────────────────────────┘  │   │
│  │  ┌──────────────────────────────────────────────┐  │   │
│  │  │ Redis Cluster (Master + Replicas)           │  │   │
│  │  │ - Cache & session store                      │  │   │
│  │  │ - Automatic failover                         │  │   │
│  │  └──────────────────────────────────────────────┘  │   │
│  │  ┌──────────────────────────────────────────────┐  │   │
│  │  │ Kafka Broker Cluster (3+ nodes)             │  │   │
│  │  │ - Event streaming                            │  │   │
│  │  │ - Partition replication (RF=3)               │  │   │
│  │  └──────────────────────────────────────────────┘  │   │
│  └────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │          External Services                          │  │
│  │  ┌────────────┐ ┌────────────┐ ┌──────────────┐    │  │
│  │  │ Stripe API │ │ Google Maps│ │ FCM/APNs     │    │  │
│  │  └────────────┘ └────────────┘ └──────────────┘    │  │
│  │  ┌────────────┐ ┌──────────────────────────────┐    │  │
│  │  │ Twilio SMS │ │ S3 (Images, Backups)         │    │  │
│  │  └────────────┘ └──────────────────────────────┘    │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**React Native Push Notification Integration:**

| Component | Technology | Description |
|:----------|:-----------|:------------|
| **Push Library** | react-native-firebase / Notifee | Cross-platform push notification handling |
| **iOS** | APNs via Firebase Cloud Messaging | Requires APNs certificate in Apple Developer |
| **Android** | FCM (Firebase Cloud Messaging) | Requires google-services.json |
| **Local Notifications** | Notifee | Scheduled/local notifications (order updates) |
| **Deep Linking** | React Navigation linking | Handle notification tap → navigate to order |

**Push Notification Flow (React Native):**
```
1. App startup → Initialize Firebase
2. Request notification permissions (iOS prompt)
3. Get FCM token → Send to backend (User Service)
4. Backend stores token per device (user_devices table)
5. Order status change → Notification Service → FCM/APNs
6. Device receives push → Display notification
7. User taps notification → Deep link to Order Tracking screen
```

### 6.2 Deployment Pipeline

```
Commit → GitHub Actions
  ├─ Lint (golangci-lint, eslint)
  ├─ Unit tests (go test -cover)
  ├─ Integration tests (Docker Compose)
  ├─ Build Docker image
  ├─ Push to ECR
  └─ Trigger ArgoCD

ArgoCD
  ├─ Fetch manifests from Git repo
  ├─ Compare with cluster state
  ├─ Apply Helm charts
  └─ Monitor rollout

Kubernetes
  ├─ Create new ReplicaSets (5 replicas)
  ├─ Perform canary (10% traffic first)
  ├─ Monitor SLO (latency, error rate, uptime)
  ├─ If SLO breached → auto-rollback
  └─ Gradually shift to 100% if stable
```

### 6.3 Mobile CI/CD Pipeline (React Native)

```
Commit → GitHub Actions (Mobile)
  ├─ TypeScript lint (eslint, prettier)
  ├─ Type check (tsc --noEmit)
  ├─ Unit tests (Jest, React Native Testing Library)
  ├─ E2E tests (Detox - iOS Simulator, Android Emulator)
  └─ Trigger platform builds

iOS Build (Fastlane / Xcode Cloud)
  ├─ Install dependencies (CocoaPods)
  ├─ Build iOS app (Release)
  ├─ Run iOS-specific tests
  ├─ Sign with distribution certificate
  ├─ Upload to TestFlight (beta)
  └─ Submit to App Store (production)

Android Build (Fastlane / Gradle)
  ├─ Install dependencies
  ├─ Build Android app (Release AAB)
  ├─ Run Android-specific tests
  ├─ Sign with upload key
  ├─ Upload to Play Console (internal track)
  └─ Promote to production track

CodePush (Optional - OTA Updates)
  ├─ Build JS bundle
  ├─ Deploy to CodePush staging
  ├─ Promote to production after validation
  └─ Rollback if crash rate increases
```

**Mobile Release Environments:**

| Environment | iOS | Android | Purpose |
|:------------|:----|:--------|:--------|
| **Development** | Debug build | Debug APK | Local testing |
| **Staging** | TestFlight (internal) | Play Console (internal) | QA testing |
| **Production** | App Store | Play Store | End users |

---

## 7. SECURITY DESIGN

### 7.1 JWT RS256 Authentication (UPDATED - P0)

**Why RS256 (Asymmetric) instead of HS256 (Symmetric)?**

| Aspect | HS256 (OLD) | RS256 (NEW) |
|:-------|:------------|:------------|
| **Key Type** | Shared secret | Private/Public key pair |
| **Security Risk** | Single point of compromise | Private key only in Auth Service |
| **Service Trust** | All services have secret | Services only need public key |
| **Key Rotation** | Requires updating all services | Only Auth Service needs private key update |
| **Best Practice** | Not recommended for microservices | Industry standard for distributed systems |

**JWT Configuration:**
```
- Algorithm: RS256 (RSA with SHA-256)
- Private Key: 2048-bit RSA key (only in Auth Service)
- Public Key: Distributed to all services via JWKS endpoint
- Access Token TTL: 24 hours
- Refresh Token TTL: 30 days
- Refresh Token Rotation: New refresh token issued on each use
- Key Rotation: Every 90 days
```

**JWT Payload Structure:**
```json
{
  "sub": "user_uuid",
  "role": "customer|restaurant_owner|driver|admin",
  "email": "user@example.com",
  "city_id": 1,
  "permissions": ["read:orders", "write:orders"],
  "iat": 1640000000,
  "exp": 1640086400,
  "jti": "unique_token_id"
}
```

**Authentication Flow (RS256):**

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT (Mobile/Web)                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. POST /api/v1/auth/login                                  │
│    Request: { email, password }                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  AUTH SERVICE                               │
│ ┌─────────────────────────────────────────────────────┐    │
│ │ 2. Validate credentials                              │    │
│ │ 3. Sign JWT with PRIVATE KEY (RS256)                │    │
│ │    - Header: { "alg": "RS256", "typ": "JWT" }       │    │
│ │    - Payload: { sub, role, email, ... }             │    │
│ │    - Signature: RSA-SHA256(header.payload, privKey) │    │
│ │ 4. Store refresh_token in database                   │    │
│ └─────────────────────────────────────────────────────┘    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ Response:                                                   │
│ {                                                            │
│   "access_token": "eyJhbGc...",                             │
│   "refresh_token": "secure_random_string",                  │
│   "expires_in": 86400                                        │
│ }                                                            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Client stores tokens:                                    │
│    - Access Token: Memory (never localStorage)              │
│    - Refresh Token: Secure HTTP-only cookie                 │
│      (SameSite=Strict, Secure=true)                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. Subsequent Requests:                                     │
│    Authorization: Bearer {access_token}                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  API GATEWAY                                │
│ ┌─────────────────────────────────────────────────────┐    │
│ │ 7. Extract JWT from Authorization header             │    │
│ │ 8. Fetch PUBLIC KEY from Auth Service JWKS endpoint │    │
│ │    GET /.well-known/jwks.json (cached 1 hour)       │    │
│ │ 9. Verify signature with PUBLIC KEY                  │    │
│ │    - If invalid → 401 AUTH_TOKEN_INVALID             │    │
│ │    - If expired → 401 AUTH_TOKEN_EXPIRED             │    │
│ │ 10. Extract claims (user_id, role, permissions)     │    │
│ │ 11. Forward request with claims in headers           │    │
│ └─────────────────────────────────────────────────────┘    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              DOWNSTREAM SERVICES                            │
│  (Order, Payment, Delivery, etc.)                           │
│  - Trust claims in request headers (already validated)      │
│  - No need for private key                                   │
└─────────────────────────────────────────────────────────────┘
```

**JWKS Endpoint (Public Key Distribution):**
```json
GET /.well-known/jwks.json

Response:
{
  "keys": [
    {
      "kty": "RSA",
      "use": "sig",
      "kid": "2024-Q1",
      "alg": "RS256",
      "n": "0vx7agoebGcQSuuPiLJXZptN9nndrQmbXEps2aiAFbWhM78...",
      "e": "AQAB"
    },
    {
      "kty": "RSA",
      "use": "sig",
      "kid": "2024-Q2",
      "alg": "RS256",
      "n": "xjlCRBqkgVvC3OKxGGxGzFIqMmOWvXczqvqrxQX...",
      "e": "AQAB"
    }
  ]
}
```

**Key Rotation Strategy:**
```
Every 90 days:
1. Auth Service generates new RSA key pair
2. Add new public key to JWKS endpoint (keep old key)
3. Start signing new JWTs with new private key (include "kid" in header)
4. Keep old key active for 24 hours (grace period for existing tokens)
5. After 24h, remove old key from JWKS
6. Services automatically fetch updated JWKS (cache TTL = 1 hour)
```

**Implementation (Go):**
```go
import (
    "crypto/rsa"
    "github.com/golang-jwt/jwt/v5"
)

// Auth Service - Generate JWT
func GenerateAccessToken(user *User) (string, error) {
    // Load private key
    privateKey, err := loadPrivateKey()
    if err != nil {
        return "", err
    }
    
    claims := jwt.MapClaims{
        "sub":   user.ID,
        "role":  user.Role,
        "email": user.Email,
        "city_id": user.CityID,
        "iat":   time.Now().Unix(),
        "exp":   time.Now().Add(24 * time.Hour).Unix(),
        "jti":   uuid.New().String(),
    }
    
    token := jwt.NewWithClaims(jwt.SigningMethodRS256, claims)
    token.Header["kid"] = "2024-Q1" // Key ID
    
    return token.SignedString(privateKey)
}

// API Gateway - Verify JWT
func VerifyAccessToken(tokenString string) (*jwt.Token, error) {
    // Fetch JWKS (cached)
    jwks := fetchJWKS()
    
    token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
        // Validate algorithm
        if _, ok := token.Method.(*jwt.SigningMethodRSA); !ok {
            return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
        }
        
        // Get key ID from header
        kid, ok := token.Header["kid"].(string)
        if !ok {
            return nil, errors.New("missing kid in token header")
        }
        
        // Find matching public key in JWKS
        publicKey := jwks.GetKey(kid)
        if publicKey == nil {
            return nil, errors.New("public key not found for kid: " + kid)
        }
        
        return publicKey, nil
    })
    
    if err != nil {
        return nil, err
    }
    
    if !token.Valid {
        return nil, errors.New("invalid token")
    }
    
    return token, nil
}
```

**Token Storage Best Practices:**

| Platform | Access Token | Refresh Token |
|:---------|:-------------|:--------------|
| **Web** | Memory (React state) | Secure HTTP-only cookie |
| **iOS (React Native)** | Memory (React state) | iOS Keychain via react-native-keychain |
| **Android (React Native)** | Memory (React state) | Android Keystore via react-native-keychain |

**NEVER:**
- Store tokens in localStorage (XSS vulnerable)
- Store tokens in sessionStorage (XSS vulnerable)
- Log tokens in console/logs
- Send tokens in URL query params

### 7.2 Security Headers (NEW - P0)

**Mandatory HTTP Security Headers:**

```go
func SecurityHeadersMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        // Prevent MIME type sniffing
        c.Header("X-Content-Type-Options", "nosniff")
        
        // Prevent clickjacking
        c.Header("X-Frame-Options", "DENY")
        
        // Enable XSS protection
        c.Header("X-XSS-Protection", "1; mode=block")
        
        // Content Security Policy
        c.Header("Content-Security-Policy", "default-src 'self'")
        
        // Force HTTPS for 1 year
        c.Header("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
        
        // Request tracking
        c.Header("X-Request-ID", c.GetString("trace_id"))
        
        c.Next()
    }
}
```

### 7.3 GDPR Compliance (NEW - P0)

**Data Export (Right to Access):**
```
GET /api/v1/users/me/export

Response: ZIP file containing:
- personal_info.json (name, email, phone, addresses)
- order_history.json (all orders)
- payment_history.json (transactions)
- ratings_reviews.json (submitted ratings)
- notifications.json (notification history)
```

**Data Deletion (Right to be Forgotten):**
```
DELETE /api/v1/users/me

Flow:
1. Mark account for deletion (30-day grace period)
2. Send confirmation email
3. After 30 days:
   - Anonymize personal data (replace with "User-{uuid}")
   - Keep transactional data for legal requirements (7 years)
   - Delete PII: name, email, phone, addresses
   - Retain: order IDs, amounts, timestamps (anonymized)
```

**Implementation:**
```go
func AnonymizeUser(ctx context.Context, userID string) error {
    tx := db.BeginTx(ctx, nil)
    defer tx.Rollback()
    
    // Anonymize user
    _, err := tx.Exec(`
        UPDATE users 
        SET email = 'deleted-' || id || '@anonymized.com',
            phone = NULL,
            first_name = 'Deleted',
            last_name = 'User',
            avatar_url = NULL,
            is_deleted = TRUE
        WHERE id = $1
    `, userID)
    if err != nil {
        return err
    }
    
    // Delete addresses
    _, err = tx.Exec(`
        UPDATE user_addresses 
        SET is_deleted = TRUE,
            street = 'DELETED',
            lat = 0,
            lng = 0
        WHERE user_id = $1
    `, userID)
    if err != nil {
        return err
    }
    
    // Delete payment methods
    _, err = tx.Exec(`
        UPDATE user_payment_methods 
        SET is_deleted = TRUE,
            token = 'DELETED'
        WHERE user_id = $1
    `, userID)
    if err != nil {
        return err
    }
    
    // Anonymize ratings (keep score, delete comment)
    _, err = tx.Exec(`
        UPDATE ratings 
        SET comment = NULL,
            is_deleted = TRUE
        WHERE rater_id = $1
    `, userID)
    if err != nil {
        return err
    }
    
    return tx.Commit()
}
```

**Data Retention Policy:**

| Data Type | Retention Period | After Expiry | Reason |
|:----------|:-----------------|:-------------|:-------|
| Order history | 3 years | Anonymize customer info | Business analytics |
| Payment records | 7 years | Archive to cold storage | Legal requirement |
| Location history | 30 days | Auto-delete | GDPR data minimization |
| Audit logs | 6 months hot, 1 year cold | Delete | Security compliance |
| Support tickets | 2 years | Anonymize | Customer service |
| Driver location (partitioned) | 30 days | Drop partition | Real-time tracking only |

**Consent Management:**
```
User Preferences:
- Marketing emails: Opt-in required
- SMS notifications: Opt-in required
- Push notifications: Opt-in (can disable per category)
- Location tracking: Explicit consent (drivers only)
- Analytics cookies: Opt-in required (non-essential)
```

### 7.4 Data Security

**In Transit (TLS 1.3):**
```
- All API requests over HTTPS
- Certificate via Let's Encrypt (auto-renewal)
- HSTS header (force HTTPS for 1 year)
- Perfect Forward Secrecy (ECDHE key exchange)
```

**At Rest (AES-256):**
```
- PII Fields: encrypted in database
  - first_name, last_name
  - email, phone (searchable, indexed before encryption)
  
- Never store raw card data
  - Use gateway tokenization (Stripe tokens)
  - Store only last 4 digits + token
  
- Encryption key management:
  - Master key stored in AWS KMS
  - Rotate keys annually
  - Separate keys per environment (dev, staging, prod)
```

### 7.5 Rate Limiting & DDoS Protection

```
Rate Limits (per IP/user):
- Login: 5 attempts per minute (then 15 min block)
- API: 100 req/min per user, 1000 req/min per IP
- Search: 50 req/min (to prevent scraping)
- Payment: 5 attempts per minute

Implementation:
- Nginx rate limiting (Token Bucket)
- Redis counter tracking
- Return 429 (Too Many Requests) when exceeded
```

---

## 8. PERFORMANCE & SCALABILITY DESIGN

### 8.1 Caching Strategy

```
L1: CDN (CloudFront)
  - Static assets (JS, CSS, images)
  - TTL: 30 days
  - Invalidate on new deployment

L2: HTTP Cache (Nginx)
  - Cacheable GET requests (search, restaurant details)
  - TTL: 5-60 min based on data volatility

L3: Redis Cache
  - Restaurant details: 30 min TTL
  - Search results: 5 min TTL
  - Menu categories: 1 hour TTL
  - Session data: 24 hours TTL
  - Cache-aside pattern: if miss → query DB → populate cache

L4: Database Query Cache
  - Index optimization
  - Query result pagination (limit 20-100)
```

### 8.2 Load Distribution

```
Traffic Distribution:
  - API Gateway balances across 3+ service replicas
  - Each service has 2+ replicas minimum
  - Horizontal Pod Autoscaler (HPA) scales by CPU% or request rate

Example HPA Policy (Order Service):
  - Min replicas: 2
  - Max replicas: 10
  - Target CPU: 70%
  - Target memory: 80%
  - Scale-up: 1 min
  - Scale-down: 5 min (to prevent flapping)
```

### 8.3 Database Optimization

```
Query Optimization:
  - Use prepared statements (prevent SQL injection)
  - Batch queries when possible
  - Use database-level pagination

Indexing Strategy:
  - Composite indexes on frequently filtered columns
  - Geo-spatial indexes for location queries (PostGIS)
  - Partial indexes for status=ACTIVE rows

Example Indexes:
  CREATE INDEX idx_orders_customer_created 
    ON orders(customer_id, created_at DESC);
  
  CREATE INDEX idx_restaurants_location 
    ON restaurants USING GIST (ll_to_earth(lat, lng));
```

### 8.4 WebSocket Performance (NEW - P0)

**Scalability Requirements (from SRS v2.2):**

| Metric | Target | Strategy |
|:-------|:-------|:---------|
| Concurrent WebSocket connections | 50k (MVP) | Horizontal scaling + sticky sessions |
| Location update frequency | Every 5 seconds | Redis Pub/Sub for distribution |
| Message latency (end-to-end) | <500ms | Optimized message routing |
| Reconnection backoff | 1s→2s→4s→30s (max) | Client-side exponential backoff |
| Max connections per user | 5 (mobile + web) | Connection tracking in Redis |

**Sticky Session Configuration (Nginx):**
```nginx
upstream websocket_backend {
    # Consistent hashing by user_id (passed in cookie/query param)
    hash $arg_user_id consistent;
    
    server ws-server-1:8080;
    server ws-server-2:8080;
    server ws-server-3:8080;
    
    # Session affinity timeout
    keepalive_timeout 1800s; # 30 minutes
}

server {
    location /ws {
        proxy_pass http://websocket_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        
        # Timeouts for WebSocket
        proxy_connect_timeout 7d;
        proxy_send_timeout 7d;
        proxy_read_timeout 7d;
    }
}
```

**Redis Pub/Sub for Cross-Pod Messaging:**
```go
// When driver updates location
func BroadcastLocationUpdate(orderID string, location Location) {
    msg := LocationUpdateMessage{
        Type: "driver_location",
        Data: location,
    }
    
    // Publish to Redis (all WebSocket pods subscribe)
    redisClient.Publish(ctx, 
        "driver:location:"+orderID, 
        json.Marshal(msg))
}

// WebSocket server subscribes to Redis channels
func (h *Hub) ListenToRedis() {
    pubsub := redisClient.Subscribe(ctx, "driver:location:*", "order:status:*")
    
    for msg := range pubsub.Channel() {
        // Find clients subscribed to this channel
        clients := h.GetSubscribedClients(msg.Channel)
        
        // Send to all subscribed clients
        for _, client := range clients {
            client.Send <- []byte(msg.Payload)
        }
    }
}
```

**Connection Tracking (Prevent Abuse):**
```go
func (h *Hub) RegisterClient(client *Client) error {
    // Check max connections per user
    userConnections := h.Redis.SCard(ctx, "ws:user:"+client.UserID).Val()
    
    if userConnections >= 5 {
        return errors.New("max connections reached")
    }
    
    // Add to user's connection set
    h.Redis.SAdd(ctx, "ws:user:"+client.UserID, client.ConnectionID)
    h.Redis.Expire(ctx, "ws:user:"+client.UserID, 30*time.Minute)
    
    h.Clients[client.ConnectionID] = client
    return nil
}
```

**Performance Monitoring:**
```
Key Metrics:
- Active WebSocket connections (gauge)
- Messages sent per second (counter)
- Message latency p95/p99 (histogram)
- Connection open/close rate (counter)
- Redis Pub/Sub lag (gauge)
- Memory per connection (gauge)
```

---

## 9. DISASTER RECOVERY & HIGH AVAILABILITY

### 9.1 High Availability Design

**Multi-AZ Deployment:**
```
Availability Zones (AWS): us-east-1a, us-east-1b, us-east-1c
  - Kubernetes nodes spread across 3 AZs
  - PostgreSQL replicas in different AZs
  - Kafka brokers distributed
  - Load Balancer spans all AZs
  
Result: Can sustain failure of 1 AZ with 0 downtime
```

**Service Resilience:**
```
Circuit Breaker (for external calls):
  - Call payment gateway
  - If 3 failures in 10 sec → open circuit
  - Return cached response or fail gracefully
  - Half-open state: retry after 30 sec
  
Timeout & Retry:
  - Default timeout: 5 seconds
  - Retry: 2 times with exponential backoff (1s, 2s)
  - Implement idempotency for safe retries
```

### 9.2 Disaster Recovery Plan

```
RTO (Recovery Time Objective): 30 minutes
RPO (Recovery Point Objective): 0 (for critical data)

Backup Strategy:
  - PostgreSQL continuous archiving (WAL to S3)
  - Snapshots: daily full backup
  - Cross-region replication: daily
  - Backup retention: 30 days

Recovery Procedure:
  1. Detect failure (monitoring alert)
  2. Initiate war room (on-call team)
  3. Restore PostgreSQL from latest WAL
  4. Verify data integrity
  5. Spin up new Kubernetes cluster
  6. Restore from backup, sync Kafka offsets
  7. Redirect traffic via DNS (Route 53)
  
Failover Time: 5-10 min (auto DNS switch + warmup)
```

---

## 10. CODE ORGANIZATION & BEST PRACTICES

> **Note:** All 10 microservices follow the Hexagonal Architecture structure as defined in Section 1.3. Each service has the same folder structure with `internal/domain/`, `internal/application/`, and `internal/adapter/` layers.

### 10.1 Port & Adapter Examples

**Primary Port (Use Case Interface):**

```go
// internal/application/port/in/order_command.go
package in

import (
    "context"
    "github.com/fooddelivery/order-service/internal/application/dto/request"
    "github.com/fooddelivery/order-service/internal/application/dto/response"
)

// OrderCommandUseCase - Primary Port for write operations
type OrderCommandUseCase interface {
    CreateOrder(ctx context.Context, req *request.CreateOrderRequest) (*response.OrderResponse, error)
    CancelOrder(ctx context.Context, orderID string, reason string) error
    UpdateOrderStatus(ctx context.Context, orderID string, status string) error
}

// OrderQueryUseCase - Primary Port for read operations (CQRS)
type OrderQueryUseCase interface {
    GetOrder(ctx context.Context, orderID string) (*response.OrderResponse, error)
    ListOrders(ctx context.Context, customerID string, pagination *dto.Pagination) (*response.OrderListResponse, error)
    GetOrdersByRestaurant(ctx context.Context, restaurantID string, status string) ([]*response.OrderResponse, error)
}
```

**Secondary Port (Repository Interface):**

```go
// internal/application/port/out/order_repository.go
package out

import (
    "context"
    "github.com/fooddelivery/order-service/internal/domain/entity"
)

// OrderRepository - Secondary Port for persistence
type OrderRepository interface {
    Save(ctx context.Context, order *entity.Order) error
    FindByID(ctx context.Context, id string) (*entity.Order, error)
    FindByCustomerID(ctx context.Context, customerID string, limit, offset int) ([]*entity.Order, int64, error)
    FindByRestaurantID(ctx context.Context, restaurantID string, status string) ([]*entity.Order, error)
    Update(ctx context.Context, order *entity.Order) error
    Delete(ctx context.Context, id string) error
}

// EventPublisher - Secondary Port for messaging
type EventPublisher interface {
    Publish(ctx context.Context, topic string, event interface{}) error
    PublishWithKey(ctx context.Context, topic string, key string, event interface{}) error
}

// PaymentClient - Secondary Port for Payment service
type PaymentClient interface {
    AuthorizePayment(ctx context.Context, orderID string, amount float64, paymentMethodID string) (*PaymentResult, error)
    CapturePayment(ctx context.Context, paymentID string) error
    RefundPayment(ctx context.Context, paymentID string, amount float64, reason string) error
}

// CatalogClient - Secondary Port for Catalog service
type CatalogClient interface {
    GetMenuItem(ctx context.Context, menuItemID string) (*MenuItem, error)
    ValidateMenuItems(ctx context.Context, items []MenuItemRequest) (*ValidationResult, error)
}
```

**Domain Entity (Pure Go, No Dependencies):**

```go
// internal/domain/entity/order.go
package entity

import (
    "errors"
    "time"
    "github.com/fooddelivery/order-service/internal/domain/vo"
    "github.com/fooddelivery/order-service/internal/domain/event"
)

// Order - Aggregate Root
type Order struct {
    ID                    string
    CustomerID            string
    RestaurantID          string
    CityID                int64
    Status                vo.OrderStatus
    DeliveryType          vo.DeliveryType
    Items                 []OrderItem
    Subtotal              vo.Money
    DeliveryFee           vo.Money
    TaxAmount             vo.Money
    CouponDiscount        vo.Money
    TotalPrice            vo.Money
    DeliveryAddressID     string
    PaymentMethodID       string
    EstimatedDeliveryTime time.Time
    Notes                 string
    CancellationReason    string
    CreatedAt             time.Time
    UpdatedAt             time.Time
    
    // Domain events to be published
    domainEvents []event.DomainEvent
}

// NewOrder - Factory method with business rules
func NewOrder(customerID, restaurantID string, cityID int64, items []OrderItem) (*Order, error) {
    if len(items) == 0 {
        return nil, errors.New("order must have at least one item")
    }
    
    order := &Order{
        ID:           generateUUID(),
        CustomerID:   customerID,
        RestaurantID: restaurantID,
        CityID:       cityID,
        Status:       vo.StatusCreated,
        DeliveryType: vo.DeliveryTypeDelivery,
        Items:        items,
        CreatedAt:    time.Now(),
        UpdatedAt:    time.Now(),
    }
    
    order.calculateTotal()
    order.addDomainEvent(event.NewOrderCreated(order.ID, customerID, restaurantID))
    
    return order, nil
}

// Cancel - Business rule: can only cancel if not yet preparing
func (o *Order) Cancel(reason string) error {
    if o.Status == vo.StatusPreparing || 
       o.Status == vo.StatusOnTheWay || 
       o.Status == vo.StatusDelivered {
        return errors.New("cannot cancel order in current status")
    }
    
    o.Status = vo.StatusCancelled
    o.CancellationReason = reason
    o.UpdatedAt = time.Now()
    o.addDomainEvent(event.NewOrderCancelled(o.ID, reason))
    
    return nil
}

// Confirm - Transition to confirmed status
func (o *Order) Confirm() error {
    if o.Status != vo.StatusCreated {
        return errors.New("can only confirm orders in CREATED status")
    }
    o.Status = vo.StatusConfirmed
    o.UpdatedAt = time.Now()
    o.addDomainEvent(event.NewOrderConfirmed(o.ID))
    return nil
}

// calculateTotal - Domain logic for pricing
func (o *Order) calculateTotal() {
    subtotal := vo.NewMoney(0)
    for _, item := range o.Items {
        subtotal = subtotal.Add(item.Subtotal)
    }
    o.Subtotal = subtotal
    o.TotalPrice = o.Subtotal.Add(o.DeliveryFee).Add(o.TaxAmount).Subtract(o.CouponDiscount)
}

// GetDomainEvents - Return and clear domain events
func (o *Order) GetDomainEvents() []event.DomainEvent {
    events := o.domainEvents
    o.domainEvents = nil
    return events
}

func (o *Order) addDomainEvent(e event.DomainEvent) {
    o.domainEvents = append(o.domainEvents, e)
}
```

**Use Case Implementation:**

```go
// internal/application/service/order_command_service.go
package service

import (
    "context"
    "github.com/fooddelivery/order-service/internal/application/dto/request"
    "github.com/fooddelivery/order-service/internal/application/dto/response"
    "github.com/fooddelivery/order-service/internal/application/port/in"
    "github.com/fooddelivery/order-service/internal/application/port/out"
    "github.com/fooddelivery/order-service/internal/domain/entity"
    "github.com/fooddelivery/pkg/common/errors"
)

// OrderCommandService implements OrderCommandUseCase
type OrderCommandService struct {
    orderRepo      out.OrderRepository
    paymentClient  out.PaymentClient
    catalogClient  out.CatalogClient
    eventPublisher out.EventPublisher
    cacheRepo      out.CacheRepository
}

// NewOrderCommandService - Constructor with dependency injection
func NewOrderCommandService(
    orderRepo out.OrderRepository,
    paymentClient out.PaymentClient,
    catalogClient out.CatalogClient,
    eventPublisher out.EventPublisher,
    cacheRepo out.CacheRepository,
) in.OrderCommandUseCase {
    return &OrderCommandService{
        orderRepo:      orderRepo,
        paymentClient:  paymentClient,
        catalogClient:  catalogClient,
        eventPublisher: eventPublisher,
        cacheRepo:      cacheRepo,
    }
}

func (s *OrderCommandService) CreateOrder(ctx context.Context, req *request.CreateOrderRequest) (*response.OrderResponse, error) {
    // 1. Validate menu items via Catalog service
    validation, err := s.catalogClient.ValidateMenuItems(ctx, req.Items)
    if err != nil {
        return nil, errors.Wrap(err, "failed to validate menu items")
    }
    if !validation.Valid {
        return nil, errors.NewValidationError("ITEM_UNAVAILABLE", validation.Message)
    }
    
    // 2. Build order items from validated data
    orderItems := buildOrderItems(req.Items, validation.Items)
    
    // 3. Create domain entity (business rules applied)
    order, err := entity.NewOrder(req.CustomerID, req.RestaurantID, req.CityID, orderItems)
    if err != nil {
        return nil, errors.Wrap(err, "failed to create order")
    }
    
    // 4. Set additional fields
    order.DeliveryAddressID = req.DeliveryAddressID
    order.PaymentMethodID = req.PaymentMethodID
    order.Notes = req.Notes
    
    // 5. Apply coupon if provided
    if req.CouponCode != "" {
        // Coupon validation logic...
    }
    
    // 6. Save to repository (via port)
    if err := s.orderRepo.Save(ctx, order); err != nil {
        return nil, errors.Wrap(err, "failed to save order")
    }
    
    // 7. Publish domain events (via port)
    for _, event := range order.GetDomainEvents() {
        if err := s.eventPublisher.Publish(ctx, "order.events", event); err != nil {
            // Log error but don't fail - events can be retried
            log.Error("failed to publish event", "error", err)
        }
    }
    
    // 8. Return response DTO
    return response.OrderResponseFromEntity(order), nil
}

func (s *OrderCommandService) CancelOrder(ctx context.Context, orderID string, reason string) error {
    // 1. Fetch order from repository
    order, err := s.orderRepo.FindByID(ctx, orderID)
    if err != nil {
        return errors.NewNotFoundError("ORDER", orderID)
    }
    
    // 2. Apply domain logic (business rule validation happens here)
    if err := order.Cancel(reason); err != nil {
        return errors.NewBusinessError("ORDER_ALREADY_CANCELLED", err.Error())
    }
    
    // 3. Update in repository
    if err := s.orderRepo.Update(ctx, order); err != nil {
        return errors.Wrap(err, "failed to update order")
    }
    
    // 4. Publish domain events
    for _, event := range order.GetDomainEvents() {
        s.eventPublisher.Publish(ctx, "order.events", event)
    }
    
    // 5. Invalidate cache
    s.cacheRepo.Delete(ctx, "order:"+orderID)
    
    return nil
}
```

**Adapter Implementation (PostgreSQL Repository):**

```go
// internal/adapter/out/persistence/postgresql/order_repository.go
package postgresql

import (
    "context"
    "database/sql"
    "github.com/fooddelivery/order-service/internal/application/port/out"
    "github.com/fooddelivery/order-service/internal/domain/entity"
    "github.com/fooddelivery/order-service/internal/adapter/out/persistence/postgresql/model"
    "github.com/fooddelivery/order-service/internal/adapter/out/persistence/postgresql/mapper"
)

// OrderRepositoryImpl implements OrderRepository port
type OrderRepositoryImpl struct {
    db *sql.DB
}

// NewOrderRepository - Constructor
func NewOrderRepository(db *sql.DB) out.OrderRepository {
    return &OrderRepositoryImpl{db: db}
}

func (r *OrderRepositoryImpl) Save(ctx context.Context, order *entity.Order) error {
    // Convert domain entity to database model
    orderModel := mapper.ToOrderModel(order)
    
    tx, err := r.db.BeginTx(ctx, nil)
    if err != nil {
        return err
    }
    defer tx.Rollback()
    
    // Insert order
    _, err = tx.ExecContext(ctx, `
        INSERT INTO orders (
            id, customer_id, restaurant_id, city_id, status, delivery_type,
            subtotal, delivery_fee, tax_amount, coupon_discount, total_price,
            delivery_address_id, payment_method_id, estimated_delivery_time,
            notes, created_at, updated_at
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17)
    `, orderModel.ID, orderModel.CustomerID, orderModel.RestaurantID, orderModel.CityID,
       orderModel.Status, orderModel.DeliveryType, orderModel.Subtotal,
       orderModel.DeliveryFee, orderModel.TaxAmount, orderModel.CouponDiscount,
       orderModel.TotalPrice, orderModel.DeliveryAddressID, orderModel.PaymentMethodID,
       orderModel.EstimatedDeliveryTime, orderModel.Notes, orderModel.CreatedAt, orderModel.UpdatedAt)
    
    if err != nil {
        return err
    }
    
    // Insert order items
    for _, item := range order.Items {
        itemModel := mapper.ToOrderItemModel(&item, order.ID)
        _, err = tx.ExecContext(ctx, `
            INSERT INTO order_items (id, order_id, menu_item_id, name_snapshot, price_snapshot, quantity, subtotal)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
        `, itemModel.ID, itemModel.OrderID, itemModel.MenuItemID, itemModel.NameSnapshot,
           itemModel.PriceSnapshot, itemModel.Quantity, itemModel.Subtotal)
        if err != nil {
            return err
        }
    }
    
    return tx.Commit()
}

func (r *OrderRepositoryImpl) FindByID(ctx context.Context, id string) (*entity.Order, error) {
    var orderModel model.OrderModel
    err := r.db.QueryRowContext(ctx, `
        SELECT id, customer_id, restaurant_id, city_id, status, delivery_type,
               subtotal, delivery_fee, tax_amount, coupon_discount, total_price,
               delivery_address_id, payment_method_id, estimated_delivery_time,
               notes, cancellation_reason, created_at, updated_at
        FROM orders WHERE id = $1 AND is_deleted = false
    `, id).Scan(&orderModel.ID, &orderModel.CustomerID, &orderModel.RestaurantID,
        &orderModel.CityID, &orderModel.Status, &orderModel.DeliveryType,
        &orderModel.Subtotal, &orderModel.DeliveryFee, &orderModel.TaxAmount,
        &orderModel.CouponDiscount, &orderModel.TotalPrice, &orderModel.DeliveryAddressID,
        &orderModel.PaymentMethodID, &orderModel.EstimatedDeliveryTime,
        &orderModel.Notes, &orderModel.CancellationReason, &orderModel.CreatedAt, &orderModel.UpdatedAt)
    
    if err == sql.ErrNoRows {
        return nil, nil
    }
    if err != nil {
        return nil, err
    }
    
    // Load order items
    items, err := r.loadOrderItems(ctx, id)
    if err != nil {
        return nil, err
    }
    orderModel.Items = items
    
    // Convert model to domain entity
    return mapper.ToOrderEntity(&orderModel), nil
}
```

### 10.2 Dependency Injection (main.go)

```go
// cmd/main.go
package main

import (
    "context"
    "log"
    "os"
    "os/signal"
    "syscall"
    
    "github.com/gin-gonic/gin"
    "github.com/fooddelivery/order-service/config"
    "github.com/fooddelivery/order-service/internal/adapter/in/http/handler"
    "github.com/fooddelivery/order-service/internal/adapter/out/cache"
    "github.com/fooddelivery/order-service/internal/adapter/out/client"
    "github.com/fooddelivery/order-service/internal/adapter/out/messaging"
    "github.com/fooddelivery/order-service/internal/adapter/out/persistence/postgresql"
    "github.com/fooddelivery/order-service/internal/application/service"
    "github.com/fooddelivery/pkg/infrastructure/database"
    infraCache "github.com/fooddelivery/pkg/infrastructure/cache"
    infraMessaging "github.com/fooddelivery/pkg/infrastructure/messaging"
    "github.com/fooddelivery/pkg/infrastructure/http/middleware"
)

func main() {
    // Load configuration
    cfg := config.Load()
    
    // ==========================================
    // INFRASTRUCTURE SETUP
    // ==========================================
    
    // Database connection
    db, err := database.NewPostgreSQLConnection(cfg.Database)
    if err != nil {
        log.Fatalf("Failed to connect to database: %v", err)
    }
    defer db.Close()
    
    // Redis connection
    redisClient := infraCache.NewRedisClient(cfg.Redis)
    defer redisClient.Close()
    
    // Kafka producer
    kafkaProducer := infraMessaging.NewKafkaProducer(cfg.Kafka)
    defer kafkaProducer.Close()
    
    // ==========================================
    // SECONDARY ADAPTERS (Driven)
    // ==========================================
    
    // Repository adapters
    orderRepo := postgresql.NewOrderRepository(db)
    cacheRepo := cache.NewOrderCacheRepository(redisClient)
    
    // Messaging adapter
    eventPublisher := messaging.NewKafkaEventPublisher(kafkaProducer)
    
    // Service client adapters (gRPC)
    paymentClient := client.NewPaymentClient(cfg.Services.PaymentURL)
    catalogClient := client.NewCatalogClient(cfg.Services.CatalogURL)
    deliveryClient := client.NewDeliveryClient(cfg.Services.DeliveryURL)
    
    // ==========================================
    // APPLICATION LAYER (Use Cases)
    // ==========================================
    
    // Command service (write operations)
    orderCommandService := service.NewOrderCommandService(
        orderRepo,
        paymentClient,
        catalogClient,
        eventPublisher,
        cacheRepo,
    )
    
    // Query service (read operations - CQRS)
    orderQueryService := service.NewOrderQueryService(
        orderRepo,
        cacheRepo,
    )
    
    // Saga orchestrator
    orderSaga := service.NewOrderSaga(
        orderRepo,
        paymentClient,
        deliveryClient,
        eventPublisher,
    )
    
    // ==========================================
    // PRIMARY ADAPTERS (Driving)
    // ==========================================
    
    // HTTP handlers
    orderHandler := handler.NewOrderHandler(orderCommandService, orderQueryService)
    cartHandler := handler.NewCartHandler(catalogClient, cacheRepo)
    
    // Setup Gin router
    router := gin.New()
    router.Use(gin.Recovery())
    router.Use(middleware.Logger())
    router.Use(middleware.TraceID())
    router.Use(middleware.SecurityHeaders())
    router.Use(middleware.CORS(cfg.CORS))
    router.Use(middleware.RateLimit(cfg.RateLimit))
    
    // API routes
    v1 := router.Group("/api/v1")
    {
        // Public routes
        v1.GET("/health", handler.HealthCheck)
        
        // Protected routes
        orders := v1.Group("/orders")
        orders.Use(middleware.JWTAuth(cfg.JWT))
        {
            orders.POST("", orderHandler.CreateOrder)
            orders.GET("/:id", orderHandler.GetOrder)
            orders.GET("", orderHandler.ListOrders)
            orders.PUT("/:id/cancel", orderHandler.CancelOrder)
            orders.POST("/:id/reorder", orderHandler.Reorder)
        }
        
        cart := v1.Group("/cart")
        cart.Use(middleware.JWTAuth(cfg.JWT))
        {
            cart.GET("", cartHandler.GetCart)
            cart.POST("/items", cartHandler.AddItem)
            cart.DELETE("/items/:id", cartHandler.RemoveItem)
        }
    }
    
    // ==========================================
    // KAFKA CONSUMERS (Event-Driven)
    // ==========================================
    
    // Start Kafka consumers in goroutines
    go startPaymentEventConsumer(cfg.Kafka, orderSaga)
    go startDeliveryEventConsumer(cfg.Kafka, orderSaga)
    
    // ==========================================
    // SERVER STARTUP
    // ==========================================
    
    // Graceful shutdown
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()
    
    go func() {
        sigChan := make(chan os.Signal, 1)
        signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)
        <-sigChan
        log.Println("Shutting down gracefully...")
        cancel()
    }()
    
    // Start HTTP server
    log.Printf("Order Service starting on port %s", cfg.Server.Port)
    if err := router.Run(":" + cfg.Server.Port); err != nil {
        log.Fatalf("Failed to start server: %v", err)
    }
}
```

### 10.3 Testing Strategy (Hexagonal Benefits)

**Testing Pyramid with Hexagonal Architecture:**

```
┌─────────────────────────────────────────────────────────────────┐
│                    E2E Tests (5%)                                │
│              Full user journey (Playwright)                      │
├─────────────────────────────────────────────────────────────────┤
│                Integration Tests (15%)                           │
│        Use Case + Real Adapters (Docker Compose)                │
├─────────────────────────────────────────────────────────────────┤
│                   Unit Tests (80%)                               │
│    Domain Entities + Use Cases with Mocked Ports                │
└─────────────────────────────────────────────────────────────────┘
```

**Unit Testing Domain (Pure Logic, No Mocks Needed):**

```go
// internal/domain/entity/order_test.go
func TestOrder_Cancel_WhenStatusIsCreated_ShouldSucceed(t *testing.T) {
    order := &entity.Order{
        ID:     "order-123",
        Status: vo.StatusCreated,
    }
    
    err := order.Cancel("Customer changed mind")
    
    assert.NoError(t, err)
    assert.Equal(t, vo.StatusCancelled, order.Status)
    assert.Equal(t, "Customer changed mind", order.CancellationReason)
}

func TestOrder_Cancel_WhenStatusIsPreparing_ShouldFail(t *testing.T) {
    order := &entity.Order{
        ID:     "order-123",
        Status: vo.StatusPreparing,
    }
    
    err := order.Cancel("Customer changed mind")
    
    assert.Error(t, err)
    assert.Equal(t, vo.StatusPreparing, order.Status) // Status unchanged
}
```

**Unit Testing Use Cases (Mock Ports):**

```go
// internal/application/service/order_command_service_test.go
func TestOrderCommandService_CreateOrder_Success(t *testing.T) {
    // Arrange - Create mock ports
    mockOrderRepo := mocks.NewMockOrderRepository(t)
    mockPaymentClient := mocks.NewMockPaymentClient(t)
    mockCatalogClient := mocks.NewMockCatalogClient(t)
    mockEventPublisher := mocks.NewMockEventPublisher(t)
    mockCacheRepo := mocks.NewMockCacheRepository(t)
    
    // Setup expectations
    mockCatalogClient.EXPECT().
        ValidateMenuItems(mock.Anything, mock.Anything).
        Return(&out.ValidationResult{Valid: true}, nil)
    
    mockOrderRepo.EXPECT().
        Save(mock.Anything, mock.Anything).
        Return(nil)
    
    mockEventPublisher.EXPECT().
        Publish(mock.Anything, "order.events", mock.Anything).
        Return(nil)
    
    // Create service with mocked ports
    svc := service.NewOrderCommandService(
        mockOrderRepo,
        mockPaymentClient,
        mockCatalogClient,
        mockEventPublisher,
        mockCacheRepo,
    )
    
    // Act
    req := &request.CreateOrderRequest{
        CustomerID:   "customer-123",
        RestaurantID: "restaurant-456",
        Items:        []request.OrderItemRequest{{MenuItemID: "item-1", Quantity: 2}},
    }
    
    result, err := svc.CreateOrder(context.Background(), req)
    
    // Assert
    assert.NoError(t, err)
    assert.NotEmpty(t, result.OrderID)
    assert.Equal(t, "CREATED", result.Status)
}
```

### 10.4 Logging & Monitoring

**Structured Logging (JSON format):**

```go
// pkg/common/logger/logger.go
logger.Info("order_created", 
    "order_id", order.ID,
    "customer_id", order.CustomerID,
    "restaurant_id", order.RestaurantID,
    "total", order.TotalPrice.Amount,
    "currency", order.TotalPrice.Currency,
    "trace_id", ctx.Value("trace_id"),
)

// Sensitive data masking
logger.Info("payment_authorized",
    "payment_id", payment.ID,
    "card_last4", "****" + payment.Last4, // Never log full card
    "amount", payment.Amount,
)

// Retention: 30 days hot (searchable), 1 year cold (archive)
```

**Key Metrics per Service:**

```
- Request count (by endpoint, status code)
- Latency (p50, p95, p99)
- Error rate (5xx %)
- CPU & memory usage
- Database connection pool saturation
- Cache hit rate
- Message queue depth (Kafka lag)
- Domain event publishing success rate
```

**Alerts:**

```
Critical (P0 - page immediately):
  - Error rate > 1% for 5 min
  - Latency p95 > 2s for 5 min
  - Service down (0 replicas)
  - Database replication lag > 10s
  - Kafka consumer lag > 10,000 messages

Warning (P1 - within 30 min):
  - Error rate > 0.5% for 10 min
  - Latency p95 > 1s for 10 min
  - Disk usage > 80%
  - Cache hit rate < 70%
```



