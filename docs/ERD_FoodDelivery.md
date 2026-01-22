# Entity Relationship Diagram (ERD)
## Food Delivery Platform

**Version:** 1.0  
**Date:** 21 January 2026  
**Status:** Ready for Review  
**Database:** PostgreSQL 14+

---

## TABLE OF CONTENTS

1. [Overview](#1-overview)
2. [Entity Relationship Diagram](#2-entity-relationship-diagram)
3. [Entity Definitions](#3-entity-definitions)
4. [Relationship Specifications](#4-relationship-specifications)
5. [Data Types & Constraints](#5-data-types--constraints)
6. [Index Strategy](#6-index-strategy)
7. [Naming Conventions](#7-naming-conventions)

---

## 1. OVERVIEW

### 1.1 Database Architecture

**Database Type:** PostgreSQL 14+  
**Total Tables:** 17 core entities  
**Key Features:**
- UUID primary keys for distributed system compatibility
- Soft delete pattern (`is_deleted` flag)
- Audit columns (`created_by`, `updated_by`, `created_at`, `updated_at`)
- JSONB for flexible schema (snapshots, metadata)
- PostGIS extensions for geospatial queries
- Enum types for state machines (order_status, payment_status, etc.)

### 1.2 ERD Notation

```
Relationship Notation:
├─ 1:1   (One-to-One)
├─ 1:N   (One-to-Many)
├─ N:M   (Many-to-Many via junction table)
└─ Optional: ○──
   Required: │──
```

---

## 2. ENTITY RELATIONSHIP DIAGRAM

### 2.1 Core Domain Model

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          FOOD DELIVERY PLATFORM ERD                             │
└─────────────────────────────────────────────────────────────────────────────────┘

┌──────────────┐
│   cities     │
│──────────────│
│ PK id        │──┐
│    title     │  │
│    status    │  │
└──────────────┘  │
                  │
                  │ 1
                  │
                  │ N
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│  ┌──────────────────┐         ┌──────────────────┐         ┌─────────────────┐│
│  │     users        │    N:1  │ user_addresses   │    N:1  │                 ││
│  │──────────────────│○────────│──────────────────│○────────│     cities      ││
│  │ PK id (UUID)     │         │ PK id (UUID)     │         │ (referenced)    ││
│  │    email         │         │ FK user_id       │         └─────────────────┘│
│  │    phone         │         │ FK city_id       │                            │
│  │    password_hash │         │    label         │                            │
│  │    first_name    │         │    street        │                            │
│  │    last_name     │         │    district      │                            │
│  │    avatar_url    │         │    lat           │                            │
│  │    role (enum)   │         │    lng           │                            │
│  │    is_active     │         │    is_default    │                            │
│  │ FK city_id       │         │    is_deleted    │                            │
│  │    is_deleted    │         └──────────────────┘                            │
│  └──────────────────┘                                                          │
│         │                                                                      │
│         │ 1                                                                    │
│         │                                                                      │
│         │ N                                                                    │
│  ┌──────────────────────────┐                                                 │
│  │  user_payment_methods    │                                                 │
│  │──────────────────────────│                                                 │
│  │ PK id (UUID)             │                                                 │
│  │ FK user_id               │                                                 │
│  │    type (enum)           │                                                 │
│  │    provider              │                                                 │
│  │    token (encrypted)     │                                                 │
│  │    last4                 │                                                 │
│  │    is_default            │                                                 │
│  │    is_deleted            │                                                 │
│  └──────────────────────────┘                                                 │
│                                                                                 │
│  ┌──────────────────┐                                                          │
│  │ refresh_tokens   │                                                          │
│  │──────────────────│                                                          │
│  │ PK id (UUID)     │                                                          │
│  │ FK user_id       │                                                          │
│  │    token         │                                                          │
│  │    expires_at    │                                                          │
│  │    revoked       │                                                          │
│  └──────────────────┘                                                          │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                          RESTAURANT & MENU DOMAIN                               │
└─────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│     users        │
│ (RESTAURANT_     │
│  OWNER role)     │
└──────────────────┘
         │ 1
         │
         │ N
┌─────────────────────┐
│   restaurants       │──────┐
│─────────────────────│      │
│ PK id (UUID)        │      │
│ FK owner_id         │      │
│    name             │      │
│    description      │      │
│    street           │      │
│ FK city_id          │      │
│    district         │      │
│    lat              │      │
│    lng              │      │
│    service_radius_km│      │
│    status (enum)    │      │
│    is_accepting_    │      │
│        orders       │      │
│    average_rating   │      │
│    total_reviews    │      │
│    min_order_value  │      │
│    is_deleted       │      │
└─────────────────────┘      │
         │                   │ 1
         │ 1                 │
         │                   │
         │ N                 │ N
┌─────────────────────┐      │
│  menu_categories    │      │      ┌──────────────────┐
│─────────────────────│      │      │    coupons       │
│ PK id (UUID)        │      │      │──────────────────│
│ FK restaurant_id    │──────┘      │ PK id (UUID)     │
│    name             │             │    code (UNIQUE) │
│    sort_order       │             │    type (enum)   │
│    is_deleted       │             │    discount_value│
└─────────────────────┘             │    min_order_    │
         │ 1                        │        value     │
         │                          │    max_discount  │
         │ N                        │    global_usage_ │
┌─────────────────────┐             │        limit     │
│    menu_items       │             │    per_user_     │
│─────────────────────│             │        usage_    │
│ PK id (UUID)        │             │        limit     │
│ FK restaurant_id    │             │    start_time    │
│ FK category_id      │○            │    end_time      │
│    name             │             │ FK target_       │
│    description      │             │    restaurant_id │○
│    price            │             │ FK city_id       │○
│    is_available     │             │    is_active     │
│    image_url        │             │    is_deleted    │
│    is_deleted       │             └──────────────────┘
└─────────────────────┘                      │ 1
         │ 1                                 │
         │                                   │ N
         │ N                        ┌──────────────────┐
┌─────────────────────┐             │  coupon_usages   │
│ menu_item_variants  │             │──────────────────│
│─────────────────────│             │ PK id (UUID)     │
│ PK id (UUID)        │             │ FK coupon_id     │
│ FK item_id          │             │ FK user_id       │
│    name             │             │ FK order_id      │○
│    price_delta      │             │    used_at       │
│    is_available     │             └──────────────────┘
└─────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                            ORDER & PAYMENT DOMAIN                               │
└─────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│     users        │
│ (CUSTOMER role)  │
└──────────────────┘
         │ 1
         │
         │ N
┌──────────────────────────┐
│       orders             │
│──────────────────────────│
│ PK id (UUID)             │◄───────────┐
│ FK customer_id           │            │ 1:1
│ FK restaurant_id         │            │
│ FK city_id               │   ┌────────────────────┐
│    status (enum)         │   │     payments       │
│    delivery_type (enum)  │   │────────────────────│
│ FK delivery_address_id   │○  │ PK id (UUID)       │
│    delivery_address_     │   │ FK order_id (UNIQ) │
│        snapshot (JSONB)  │   │    amount          │
│    coupon_code           │○  │    currency        │
│    coupon_discount       │   │    status (enum)   │
│    restaurant_fee        │   │    method_type     │
│    tax_amount            │   │    provider        │
│    delivery_fee          │   │    gateway_txn_id  │
│    subtotal              │   │    gateway_response│
│    total_price           │   │        (JSONB)     │
│    payment_status (enum) │   │    idempotency_key │
│ FK payment_method_id     │○  │        (UNIQUE)    │
│    estimated_delivery_   │   │    authorized_at   │
│        time              │   │    captured_at     │
│    actual_delivery_time  │   │    failed_at       │
│    notes                 │   │    is_deleted      │
│ FK delivery_task_id      │○  └────────────────────┘
│    is_deleted            │            │ 1
└──────────────────────────┘            │
         │ 1                            │ N
         │                     ┌─────────────────────┐
         │ N                   │  payment_refunds    │
┌──────────────────────────┐  │─────────────────────│
│     order_items          │  │ PK id (UUID)        │
│──────────────────────────│  │ FK payment_id       │
│ PK id (UUID)             │  │    amount           │
│ FK order_id              │  │    reason           │
│ FK menu_item_id          │○ │    status (enum)    │
│    name_snapshot         │  └─────────────────────┘
│    price_snapshot        │
│    quantity              │
│    subtotal              │
└──────────────────────────┘
         │ 1
         │
         │ N
┌──────────────────────────┐
│  order_item_variants     │
│──────────────────────────│
│ PK id (UUID)             │
│ FK order_item_id         │
│    variant_name          │
│    price_delta           │
└──────────────────────────┘

┌──────────────────────────┐
│     order_events         │
│  (Audit Trail)           │
│──────────────────────────│
│ PK id (UUID)             │
│ FK order_id              │
│    event_type            │
│    previous_status       │
│    new_status            │
│    event_data (JSONB)    │
│ FK actor_id              │○
│    actor_role            │
│    created_at            │
└──────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                          DELIVERY & DRIVER DOMAIN                               │
└─────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│     users        │
│ (DRIVER role)    │
└──────────────────┘
         │ 1
         │
         │ 1
┌─────────────────────┐
│      drivers        │
│─────────────────────│
│ PK id (UUID)        │
│ FK user_id (UNIQUE) │
│    status (enum)    │
│    vehicle_type     │
│    vehicle_plate    │
│    license_number   │
│    document_urls    │
│        (JSONB)      │
│    rating           │
│    total_trips      │
│    is_online        │
│ FK city_id          │○
│    is_deleted       │
└─────────────────────┘
         │ 1
         │
         │ N
┌─────────────────────────┐
│   delivery_tasks        │
│─────────────────────────│
│ PK id (UUID)            │
│ FK order_id (UNIQUE)    │───────┐
│ FK driver_id            │○      │ 1:1
│    status (enum)        │       │
│    pickup_location_     │       │
│        snapshot (JSONB) │       │
│    dropoff_location_    │       │
│        snapshot (JSONB) │       │
│    current_lat          │       │
│    current_lng          │       │
│    current_location_    │       │
│        updated_at       │       │
│    estimated_delivery_  │       │
│        time             │       │
│    actual_delivery_time │       │
│    driver_assignment_   │       │
│        time             │       │
│    pickup_time          │       │
│    is_deleted           │       │
└─────────────────────────┘       │
         │ 1                      │
         │                        │
         │ N                      │
┌─────────────────────────┐       │
│ delivery_task_events    │       │
│─────────────────────────│       │
│ PK id (UUID)            │       │
│ FK delivery_task_id     │       │
│    event_type           │       │
│    event_data (JSONB)   │       │
│    created_at           │       │
└─────────────────────────┘       │
                                  │
┌─────────────────────────┐       │
│       orders            │◄──────┘
│ (FK delivery_task_id)   │
└─────────────────────────┘

┌─────────────────────────────┐
│ driver_location_history     │
│ (Partitioned by time)       │
│─────────────────────────────│
│ PK id (BIGSERIAL)           │
│ FK driver_id                │
│ FK delivery_task_id         │○
│    location (GEOGRAPHY)     │
│    speed_kmh                │
│    heading                  │
│    accuracy_meters          │
│    recorded_at              │
└─────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                       RATING & DISPUTE DOMAIN                                   │
└─────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│     orders       │
└──────────────────┘
         │ 1
         ├─────────────┐
         │ N           │ N
┌────────────────┐     │
│    ratings     │     │
│────────────────│     │
│ PK id (UUID)   │     │
│ FK order_id    │     │
│ FK rater_id    │     │    ┌─────────────────────┐
│ FK ratee_id    │     │    │     disputes        │
│    rating_type │     │    │─────────────────────│
│    score       │     └────│ PK id (UUID)        │
│    comment     │          │ FK order_id         │
│    is_deleted  │          │ FK customer_id      │
└────────────────┘          │    category (enum)  │
                            │    description      │
                            │    photo_urls[]     │
                            │    status (enum)    │
                            │    resolution_type  │
                            │    resolution_amount│
                            │ FK resolved_by      │○
                            │    resolved_at      │
                            │    created_at       │
                            │    updated_at       │
                            └─────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                              AUDIT & COMPLIANCE                                 │
└─────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────┐
│      audit_logs          │
│──────────────────────────│
│ PK id (UUID)             │
│    entity_type           │
│    entity_id (UUID)      │
│    action                │
│ FK actor_id              │○
│    actor_role            │
│    old_values (JSONB)    │
│    new_values (JSONB)    │
│    ip_address            │
│    user_agent            │
│    created_at            │
└──────────────────────────┘
```

---

## 3. ENTITY DEFINITIONS

### 3.1 User Management Domain

#### 3.1.1 cities
**Purpose:** Master table for supported cities

| Column | Type | Constraints | Description |
|:-------|:-----|:------------|:------------|
| id | BIGSERIAL | PK | Unique city identifier |
| title | VARCHAR(255) | NOT NULL, UNIQUE | City name |
| status | VARCHAR(32) | NOT NULL, DEFAULT 'ACTIVE', CHECK | ACTIVE, INACTIVE |
| created_by | UUID | NULLABLE | Admin who created |
| updated_by | UUID | NULLABLE | Admin who last updated |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes:**
- Primary key on `id`
- Unique index on `title`
- Index on `status`

---

#### 3.1.2 users
**Purpose:** Core user entity for all user types

| Column | Type | Constraints | Description |
|:-------|:-----|:------------|:------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique user identifier |
| email | VARCHAR(255) | UNIQUE, NULLABLE | User email (unique if provided) |
| phone | VARCHAR(20) | UNIQUE, NULLABLE | User phone (unique if provided) |
| password_hash | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| first_name | VARCHAR(100) | NULLABLE | User first name |
| last_name | VARCHAR(100) | NULLABLE | User last name |
| avatar_url | TEXT | NULLABLE | Profile picture URL |
| role | VARCHAR(32) | NOT NULL, CHECK | CUSTOMER, RESTAURANT_OWNER, DRIVER, ADMIN |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Account active status |
| city_id | BIGINT | FK → cities(id) | User's primary city |
| is_deleted | BOOLEAN | NOT NULL, DEFAULT FALSE | Soft delete flag |
| created_by | UUID | NULLABLE | Who created this user |
| updated_by | UUID | NULLABLE | Who last updated |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes:**
```sql
CREATE INDEX idx_users_email ON users(email) WHERE is_deleted = FALSE;
CREATE INDEX idx_users_phone ON users(phone) WHERE is_deleted = FALSE;
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_city_id ON users(city_id);
```

**Business Rules:**
- At least one of `email` or `phone` must be provided
- Email must be unique across non-deleted users
- Phone must be unique across non-deleted users
- `role` determines access permissions (RBAC)

---

#### 3.1.3 user_addresses
**Purpose:** Multiple delivery addresses per user

| Column | Type | Constraints | Description |
|:-------|:-----|:------------|:------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique address identifier |
| user_id | UUID | FK → users(id) ON DELETE CASCADE, NOT NULL | Address owner |
| label | VARCHAR(100) | NULLABLE | Address nickname (Home, Office) |
| street | TEXT | NOT NULL | Street address |
| city_id | BIGINT | FK → cities(id) | City reference |
| district | VARCHAR(100) | NULLABLE | District/area name |
| lat | DOUBLE PRECISION | NOT NULL | Latitude for geo queries |
| lng | DOUBLE PRECISION | NOT NULL | Longitude for geo queries |
| is_default | BOOLEAN | NOT NULL, DEFAULT FALSE | Default delivery address |
| is_deleted | BOOLEAN | NOT NULL, DEFAULT FALSE | Soft delete flag |
| created_by | UUID | NULLABLE | Creator |
| updated_by | UUID | NULLABLE | Last updater |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes:**
```sql
CREATE INDEX idx_user_addresses_user_id ON user_addresses(user_id) WHERE is_deleted = FALSE;
CREATE INDEX idx_user_addresses_location ON user_addresses USING gist(ll_to_earth(lat, lng));
```

**Business Rules:**
- Only one `is_default = TRUE` per user
- Must use application logic to enforce single default
- Cascade delete when user is hard-deleted

---

#### 3.1.4 user_payment_methods
**Purpose:** Tokenized payment methods per user

| Column | Type | Constraints | Description |
|:-------|:-----|:------------|:------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique payment method ID |
| user_id | UUID | FK → users(id) ON DELETE CASCADE, NOT NULL | Payment method owner |
| type | VARCHAR(32) | NOT NULL, CHECK | CARD, EWALLET, COD |
| provider | VARCHAR(64) | NULLABLE | stripe, vnpay, momo, etc. |
| token | TEXT | NOT NULL | Gateway-issued token (encrypted) |
| last4 | VARCHAR(4) | NULLABLE | Last 4 digits for display |
| is_default | BOOLEAN | NOT NULL, DEFAULT FALSE | Default payment method |
| is_deleted | BOOLEAN | NOT NULL, DEFAULT FALSE | Soft delete flag |
| created_by | UUID | NULLABLE | Creator |
| updated_by | UUID | NULLABLE | Last updater |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes:**
```sql
CREATE INDEX idx_user_payment_methods_user_id ON user_payment_methods(user_id) WHERE is_deleted = FALSE;
```

**Security Notes:**
- **NEVER store raw card numbers**
- `token` is gateway-issued token (e.g., Stripe `tok_*`)
- `token` should be encrypted at application level (AES-256)
- PCI-DSS compliance: no sensitive card data in database

---

#### 3.1.5 refresh_tokens
**Purpose:** JWT refresh token management

| Column | Type | Constraints | Description |
|:-------|:-----|:------------|:------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique token identifier |
| user_id | UUID | FK → users(id) ON DELETE CASCADE, NOT NULL | Token owner |
| token | TEXT | NOT NULL, UNIQUE | Refresh token (hashed) |
| expires_at | TIMESTAMPTZ | NOT NULL | Token expiration time |
| revoked | BOOLEAN | NOT NULL, DEFAULT FALSE | Revocation flag |
| created_by | UUID | NULLABLE | Creator |
| updated_by | UUID | NULLABLE | Last updater |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes:**
```sql
CREATE INDEX idx_refresh_tokens_user_id ON refresh_tokens(user_id);
CREATE INDEX idx_refresh_tokens_expires_at ON refresh_tokens(expires_at);
```

**Business Rules:**
- Token rotation: new token issued on each refresh, old token revoked
- Expired tokens should be cleaned up periodically
- Revoked tokens cannot be used

---

### 3.2 Restaurant & Menu Domain

#### 3.2.1 restaurants
**Purpose:** Restaurant profiles and operational data

| Column | Type | Constraints | Description |
|:-------|:-----|:------------|:------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique restaurant identifier |
| owner_id | UUID | FK → users(id), NOT NULL | Restaurant owner (RESTAURANT_OWNER role) |
| name | VARCHAR(255) | NOT NULL | Restaurant name |
| description | TEXT | NULLABLE | Restaurant description |
| street | TEXT | NOT NULL | Street address |
| city_id | BIGINT | FK → cities(id), NOT NULL | City reference |
| district | VARCHAR(100) | NULLABLE | District/area |
| lat | DOUBLE PRECISION | NOT NULL | Latitude |
| lng | DOUBLE PRECISION | NOT NULL | Longitude |
| service_radius_km | NUMERIC(5,2) | DEFAULT 5.0 | Delivery service radius |
| status | VARCHAR(32) | NOT NULL, CHECK | PENDING, ACTIVE, INACTIVE, SUSPENDED |
| is_accepting_orders | BOOLEAN | NOT NULL, DEFAULT TRUE | Currently accepting orders |
| average_rating | NUMERIC(3,2) | DEFAULT 0 | Cached average rating |
| total_reviews | INT | NOT NULL, DEFAULT 0 | Cached review count |
| min_order_value | NUMERIC(12,2) | DEFAULT 0 | Minimum order amount |
| is_deleted | BOOLEAN | NOT NULL, DEFAULT FALSE | Soft delete flag |
| created_by | UUID | NULLABLE | Creator |
| updated_by | UUID | NULLABLE | Last updater |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes:**
```sql
CREATE INDEX idx_restaurants_city_id ON restaurants(city_id) WHERE is_deleted = FALSE AND status = 'ACTIVE';
CREATE INDEX idx_restaurants_location ON restaurants USING gist(ll_to_earth(lat, lng)) WHERE status = 'ACTIVE';
CREATE INDEX idx_restaurants_owner_id ON restaurants(owner_id);
CREATE INDEX idx_restaurants_status ON restaurants(status);
```

**Business Rules:**
- New restaurants start with `status = 'PENDING'` (requires admin approval)
- Only `ACTIVE` restaurants appear in search results
- `is_accepting_orders = FALSE` temporarily disables ordering
- `average_rating` and `total_reviews` are denormalized for performance

---

#### 3.2.2 menu_categories
**Purpose:** Menu organization within restaurants

| Column | Type | Constraints | Description |
|:-------|:-----|:------------|:------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique category identifier |
| restaurant_id | UUID | FK → restaurants(id) ON DELETE CASCADE, NOT NULL | Parent restaurant |
| name | VARCHAR(255) | NOT NULL | Category name (Appetizers, Mains, etc.) |
| sort_order | INT | DEFAULT 0 | Display order |
| is_deleted | BOOLEAN | NOT NULL, DEFAULT FALSE | Soft delete flag |
| created_by | UUID | NULLABLE | Creator |
| updated_by | UUID | NULLABLE | Last updater |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes:**
```sql
CREATE INDEX idx_menu_categories_restaurant_id ON menu_categories(restaurant_id) WHERE is_deleted = FALSE;
```

**Business Rules:**
- Categories are scoped to a single restaurant
- `sort_order` determines display order in menu

---

#### 3.2.3 menu_items
**Purpose:** Individual menu items

| Column | Type | Constraints | Description |
|:-------|:-----|:------------|:------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique menu item identifier |
| restaurant_id | UUID | FK → restaurants(id) ON DELETE CASCADE, NOT NULL | Parent restaurant |
| category_id | UUID | FK → menu_categories(id), NULLABLE | Parent category (optional) |
| name | VARCHAR(255) | NOT NULL | Item name |
| description | TEXT | NULLABLE | Item description |
| price | NUMERIC(12,2) | NOT NULL | Base price |
| is_available | BOOLEAN | NOT NULL, DEFAULT TRUE | Currently available |
| image_url | TEXT | NULLABLE | Item image URL |
| is_deleted | BOOLEAN | NOT NULL, DEFAULT FALSE | Soft delete flag |
| created_by | UUID | NULLABLE | Creator |
| updated_by | UUID | NULLABLE | Last updater |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes:**
```sql
CREATE INDEX idx_menu_items_restaurant_id ON menu_items(restaurant_id) WHERE is_deleted = FALSE;
CREATE INDEX idx_menu_items_category_id ON menu_items(category_id) WHERE is_deleted = FALSE;
```

**Business Rules:**
- `is_available = FALSE` temporarily hides item from menu
- `price` is base price; variants add `price_delta`

---

#### 3.2.4 menu_item_variants
**Purpose:** Item variations (size, toppings, etc.)

| Column | Type | Constraints | Description |
|:-------|:-----|:------------|:------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique variant identifier |
| item_id | UUID | FK → menu_items(id) ON DELETE CASCADE, NOT NULL | Parent menu item |
| name | VARCHAR(255) | NOT NULL | Variant name (Large, Extra Cheese) |
| price_delta | NUMERIC(12,2) | NOT NULL, DEFAULT 0 | Price adjustment (+/- base price) |
| is_available | BOOLEAN | NOT NULL, DEFAULT TRUE | Currently available |
| created_by | UUID | NULLABLE | Creator |
| updated_by | UUID | NULLABLE | Last updater |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes:**
```sql
CREATE INDEX idx_menu_item_variants_item_id ON menu_item_variants(item_id);
```

**Business Rules:**
- Final price = item.price + SUM(variant.price_delta)
- Multiple variants can be selected per item

---

### 3.3 Promotion Domain

#### 3.3.1 coupons
**Purpose:** Discount coupons and promotional codes

| Column | Type | Constraints | Description |
|:-------|:-----|:------------|:------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique coupon identifier |
| code | VARCHAR(64) | UNIQUE, NOT NULL | Coupon code (SAVE10, NEWYEAR2026) |
| type | VARCHAR(32) | NOT NULL, CHECK | PERCENT, FLAT |
| discount_value | NUMERIC(12,2) | NOT NULL | Percentage (20) or flat amount (50000) |
| min_order_value | NUMERIC(12,2) | NULLABLE | Minimum cart value required |
| max_discount | NUMERIC(12,2) | NULLABLE | Maximum discount cap (for PERCENT) |
| global_usage_limit | INT | NULLABLE | Total usage limit across all users |
| per_user_usage_limit | INT | DEFAULT 1 | Max uses per user |
| start_time | TIMESTAMPTZ | NULLABLE | Coupon activation time |
| end_time | TIMESTAMPTZ | NULLABLE | Coupon expiration time |
| target_restaurant_id | UUID | FK → restaurants(id), NULLABLE | Restaurant-specific coupon |
| city_id | BIGINT | FK → cities(id), NULLABLE | City-specific coupon |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Active status |
| is_deleted | BOOLEAN | NOT NULL, DEFAULT FALSE | Soft delete flag |
| created_by | UUID | NULLABLE | Creator (admin) |
| updated_by | UUID | NULLABLE | Last updater |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes:**
```sql
CREATE INDEX idx_coupons_code ON coupons(code) WHERE is_active = TRUE AND is_deleted = FALSE;
CREATE INDEX idx_coupons_restaurant_id ON coupons(target_restaurant_id) WHERE is_active = TRUE;
CREATE INDEX idx_coupons_validity ON coupons(start_time, end_time) WHERE is_active = TRUE;
```

**Business Rules:**
- `code` must be unique
- Validation checks:
  - Current time between `start_time` and `end_time`
  - Order total >= `min_order_value`
  - User usage count < `per_user_usage_limit`
  - Global usage count < `global_usage_limit`
- For PERCENT type: discount = MIN(order_total * discount_value/100, max_discount)
- For FLAT type: discount = discount_value

---

#### 3.3.2 coupon_usages
**Purpose:** Track coupon usage per user/order

| Column | Type | Constraints | Description |
|:-------|:-----|:------------|:------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique usage identifier |
| coupon_id | UUID | FK → coupons(id), NOT NULL | Coupon used |
| user_id | UUID | FK → users(id), NOT NULL | User who used coupon |
| order_id | UUID | FK → orders(id), NULLABLE | Associated order (NULL during validation) |
| used_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Usage timestamp |
| created_by | UUID | NULLABLE | Creator |
| updated_by | UUID | NULLABLE | Last updater |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes:**
```sql
CREATE INDEX idx_coupon_usages_coupon_id ON coupon_usages(coupon_id);
CREATE INDEX idx_coupon_usages_user_id ON coupon_usages(user_id);
```

**Business Rules:**
- Record created when coupon is applied to order
- Used to enforce `per_user_usage_limit` and `global_usage_limit`

---

### 3.4 Order Domain

#### 3.4.1 orders
**Purpose:** Core order entity

| Column | Type | Constraints | Description |
|:-------|:-----|:------------|:------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique order identifier |
| customer_id | UUID | FK → users(id), NOT NULL | Order customer |
| restaurant_id | UUID | FK → restaurants(id), NOT NULL | Order restaurant |
| city_id | BIGINT | FK → cities(id), NOT NULL | Order city |
| status | order_status_enum | NOT NULL, DEFAULT 'CREATED' | Order state machine |
| delivery_type | VARCHAR(16) | NOT NULL, DEFAULT 'DELIVERY', CHECK | DELIVERY, PICKUP |
| delivery_address_id | UUID | FK → user_addresses(id), NULLABLE | Selected delivery address |
| delivery_address_snapshot | JSONB | NULLABLE | Address snapshot (audit trail) |
| coupon_code | VARCHAR(64) | NULLABLE | Applied coupon code |
| coupon_discount | NUMERIC(12,2) | DEFAULT 0 | Coupon discount amount |
| restaurant_fee | NUMERIC(12,2) | DEFAULT 0 | Restaurant service fee |
| tax_amount | NUMERIC(12,2) | DEFAULT 0 | Tax amount |
| delivery_fee | NUMERIC(12,2) | DEFAULT 0 | Delivery fee |
| subtotal | NUMERIC(12,2) | NOT NULL | Items subtotal |
| total_price | NUMERIC(12,2) | NOT NULL | Final total |
| payment_status | payment_status_enum | NOT NULL, DEFAULT 'PENDING' | Payment state |
| payment_method_id | UUID | FK → user_payment_methods(id), NULLABLE | Selected payment method |
| estimated_delivery_time | TIMESTAMPTZ | NULLABLE | ETA |
| actual_delivery_time | TIMESTAMPTZ | NULLABLE | Actual delivery timestamp |
| notes | TEXT | NULLABLE | Customer notes |
| delivery_task_id | UUID | NULLABLE | Linked delivery task |
| is_deleted | BOOLEAN | NOT NULL, DEFAULT FALSE | Soft delete flag |
| created_by | UUID | NULLABLE | Creator |
| updated_by | UUID | NULLABLE | Last updater |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Enum Types:**
```sql
CREATE TYPE order_status_enum AS ENUM (
    'CREATED', 'PAYMENT_FAILED', 'CONFIRMED', 'PREPARING', 
    'READY_FOR_PICKUP', 'ON_THE_WAY', 'DELIVERED', 
    'CANCELLED', 'DELIVERY_FAILED'
);

CREATE TYPE payment_status_enum AS ENUM (
    'PENDING', 'AUTHORIZED', 'CAPTURED', 'FAILED', 'REFUNDED'
);
```

**Indexes:**
```sql
CREATE INDEX idx_orders_customer_id ON orders(customer_id) WHERE is_deleted = FALSE;
CREATE INDEX idx_orders_restaurant_id ON orders(restaurant_id) WHERE is_deleted = FALSE;
CREATE INDEX idx_orders_city_id ON orders(city_id) WHERE is_deleted = FALSE;
CREATE INDEX idx_orders_status ON orders(status) WHERE is_deleted = FALSE;
CREATE INDEX idx_orders_created_at ON orders(created_at DESC) WHERE is_deleted = FALSE;
CREATE INDEX idx_orders_payment_status ON orders(payment_status) WHERE is_deleted = FALSE;
```

**Business Rules:**
- State machine validation (see Order State Diagram in Section 4)
- `total_price = subtotal + tax_amount + delivery_fee + restaurant_fee - coupon_discount`
- `delivery_address_snapshot` preserves address at order time (immutable audit trail)

---

#### 3.4.2 order_items
**Purpose:** Line items within an order

| Column | Type | Constraints | Description |
|:-------|:-----|:------------|:------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique order item identifier |
| order_id | UUID | FK → orders(id) ON DELETE CASCADE, NOT NULL | Parent order |
| menu_item_id | UUID | FK → menu_items(id), NULLABLE | Reference to menu item |
| name_snapshot | VARCHAR(255) | NOT NULL | Item name at order time |
| price_snapshot | NUMERIC(12,2) | NOT NULL | Item price at order time |
| quantity | INT | NOT NULL, CHECK (quantity > 0) | Quantity ordered |
| subtotal | NUMERIC(12,2) | NOT NULL | Line item subtotal |
| created_by | UUID | NULLABLE | Creator |
| updated_by | UUID | NULLABLE | Last updater |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes:**
```sql
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
```

**Business Rules:**
- `subtotal = (price_snapshot + SUM(variant.price_delta)) * quantity`
- Snapshots preserve pricing at order time (immutable)

---

#### 3.4.3 order_item_variants
**Purpose:** Selected variants per order item

| Column | Type | Constraints | Description |
|:-------|:-----|:------------|:------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique variant selection identifier |
| order_item_id | UUID | FK → order_items(id) ON DELETE CASCADE, NOT NULL | Parent order item |
| variant_name | VARCHAR(255) | NOT NULL | Variant name snapshot |
| price_delta | NUMERIC(12,2) | NOT NULL | Variant price delta snapshot |
| created_by | UUID | NULLABLE | Creator |
| updated_by | UUID | NULLABLE | Last updater |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes:**
```sql
CREATE INDEX idx_order_item_variants_order_item_id ON order_item_variants(order_item_id);
```

---

#### 3.4.4 order_events
**Purpose:** Order audit trail

| Column | Type | Constraints | Description |
|:-------|:-----|:------------|:------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique event identifier |
| order_id | UUID | FK → orders(id) ON DELETE CASCADE, NOT NULL | Parent order |
| event_type | VARCHAR(64) | NOT NULL | Event type (CREATED, CONFIRMED, etc.) |
| previous_status | VARCHAR(32) | NULLABLE | Previous order status |
| new_status | VARCHAR(32) | NULLABLE | New order status |
| event_data | JSONB | NULLABLE | Additional event metadata |
| actor_id | UUID | NULLABLE | User who triggered event |
| actor_role | VARCHAR(32) | NULLABLE | Actor's role |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Event timestamp |

**Indexes:**
```sql
CREATE INDEX idx_order_events_order_id ON order_events(order_id);
CREATE INDEX idx_order_events_created_at ON order_events(created_at DESC);
```

**Business Rules:**
- Immutable log of all order state changes
- Used for compliance and debugging

---

### 3.5 Payment Domain

#### 3.5.1 payments
**Purpose:** Payment transaction records

| Column | Type | Constraints | Description |
|:-------|:-----|:------------|:------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique payment identifier |
| order_id | UUID | FK → orders(id), UNIQUE, NOT NULL | One payment per order |
| amount | NUMERIC(12,2) | NOT NULL | Payment amount |
| currency | VARCHAR(8) | NOT NULL, DEFAULT 'VND' | Currency code |
| status | payment_status_enum | NOT NULL, DEFAULT 'PENDING' | Payment state |
| method_type | VARCHAR(32) | NOT NULL | CARD, EWALLET, COD |
| provider | VARCHAR(64) | NULLABLE | stripe, vnpay, momo |
| gateway_transaction_id | VARCHAR(128) | NULLABLE | Gateway transaction ID |
| gateway_response | JSONB | NULLABLE | Full gateway response |
| idempotency_key | VARCHAR(128) | UNIQUE, NOT NULL | Prevents double-charge |
| authorized_at | TIMESTAMPTZ | NULLABLE | Authorization timestamp |
| captured_at | TIMESTAMPTZ | NULLABLE | Capture timestamp |
| failed_at | TIMESTAMPTZ | NULLABLE | Failure timestamp |
| is_deleted | BOOLEAN | NOT NULL, DEFAULT FALSE | Soft delete flag |
| created_by | UUID | NULLABLE | Creator |
| updated_by | UUID | NULLABLE | Last updater |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes:**
```sql
CREATE INDEX idx_payments_order_id ON payments(order_id);
CREATE INDEX idx_payments_status ON payments(status) WHERE is_deleted = FALSE;
CREATE INDEX idx_payments_idempotency_key ON payments(idempotency_key) WHERE is_deleted = FALSE;
```

**Business Rules:**
- 1:1 relationship with orders (one payment per order)
- `idempotency_key` prevents duplicate payment attempts
- Auth & Capture flow: PENDING → AUTHORIZED → CAPTURED
- Direct flow: PENDING → CAPTURED

---

#### 3.5.2 payment_refunds
**Purpose:** Payment refund records

| Column | Type | Constraints | Description |
|:-------|:-----|:------------|:------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique refund identifier |
| payment_id | UUID | FK → payments(id), NOT NULL | Parent payment |
| amount | NUMERIC(12,2) | NOT NULL | Refund amount (can be partial) |
| reason | TEXT | NULLABLE | Refund reason |
| status | VARCHAR(32) | DEFAULT 'PENDING', CHECK | PENDING, COMPLETED, FAILED |
| created_by | UUID | NULLABLE | Creator |
| updated_by | UUID | NULLABLE | Last updater |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes:**
```sql
CREATE INDEX idx_payment_refunds_payment_id ON payment_refunds(payment_id);
```

**Business Rules:**
- Multiple partial refunds allowed
- SUM(refunds.amount) <= payment.amount

---

### 3.6 Delivery Domain

#### 3.6.1 drivers
**Purpose:** Driver profiles

| Column | Type | Constraints | Description |
|:-------|:-----|:------------|:------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique driver identifier |
| user_id | UUID | FK → users(id), UNIQUE, NOT NULL | Driver user account |
| status | driver_status_enum | NOT NULL, DEFAULT 'PENDING' | Driver verification status |
| vehicle_type | VARCHAR(32) | NULLABLE | BIKE, MOTORBIKE, CAR |
| vehicle_plate | VARCHAR(32) | NULLABLE | Vehicle license plate |
| license_number | VARCHAR(64) | NULLABLE | Driver's license number |
| document_urls | JSONB | NULLABLE | Verification documents |
| rating | NUMERIC(3,2) | DEFAULT 0 | Cached average rating |
| total_trips | INT | DEFAULT 0 | Cached trip count |
| is_online | BOOLEAN | NOT NULL, DEFAULT FALSE | Current online status |
| city_id | BIGINT | FK → cities(id), NULLABLE | Operating city |
| is_deleted | BOOLEAN | NOT NULL, DEFAULT FALSE | Soft delete flag |
| created_by | UUID | NULLABLE | Creator |
| updated_by | UUID | NULLABLE | Last updater |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Enum Types:**
```sql
CREATE TYPE driver_status_enum AS ENUM ('PENDING', 'APPROVED', 'REJECTED', 'SUSPENDED');
```

**Indexes:**
```sql
CREATE INDEX idx_drivers_user_id ON drivers(user_id);
CREATE INDEX idx_drivers_status ON drivers(status) WHERE is_deleted = FALSE;
CREATE INDEX idx_drivers_city_id ON drivers(city_id) WHERE status = 'APPROVED';
CREATE INDEX idx_drivers_online ON drivers(is_online, status) WHERE is_online = TRUE AND status = 'APPROVED';
```

**Business Rules:**
- 1:1 relationship with users (user.role = 'DRIVER')
- Only `APPROVED` drivers can accept deliveries
- `is_online = TRUE` indicates driver is available

---

#### 3.6.2 delivery_tasks
**Purpose:** Delivery assignments

| Column | Type | Constraints | Description |
|:-------|:-----|:------------|:------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique delivery task identifier |
| order_id | UUID | FK → orders(id), UNIQUE, NOT NULL | One delivery per order |
| driver_id | UUID | FK → drivers(id), NULLABLE | Assigned driver |
| status | delivery_task_status_enum | NOT NULL, DEFAULT 'CREATED' | Delivery state |
| pickup_location_snapshot | JSONB | NOT NULL | Restaurant location snapshot |
| dropoff_location_snapshot | JSONB | NOT NULL | Customer location snapshot |
| current_lat | DOUBLE PRECISION | NULLABLE | Driver's current latitude |
| current_lng | DOUBLE PRECISION | NULLABLE | Driver's current longitude |
| current_location_updated_at | TIMESTAMPTZ | NULLABLE | Last location update |
| estimated_delivery_time | TIMESTAMPTZ | NULLABLE | ETA |
| actual_delivery_time | TIMESTAMPTZ | NULLABLE | Actual delivery timestamp |
| driver_assignment_time | TIMESTAMPTZ | NULLABLE | Driver assignment timestamp |
| pickup_time | TIMESTAMPTZ | NULLABLE | Order pickup timestamp |
| is_deleted | BOOLEAN | NOT NULL, DEFAULT FALSE | Soft delete flag |
| created_by | UUID | NULLABLE | Creator |
| updated_by | UUID | NULLABLE | Last updater |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Enum Types:**
```sql
CREATE TYPE delivery_task_status_enum AS ENUM (
    'CREATED', 'ASSIGNED', 'PICKED_UP', 'IN_TRANSIT', 'DELIVERED', 'CANCELLED'
);
```

**Indexes:**
```sql
CREATE INDEX idx_delivery_tasks_order_id ON delivery_tasks(order_id);
CREATE INDEX idx_delivery_tasks_driver_id ON delivery_tasks(driver_id) WHERE status IN ('ASSIGNED', 'PICKED_UP', 'IN_TRANSIT');
CREATE INDEX idx_delivery_tasks_status ON delivery_tasks(status) WHERE is_deleted = FALSE;
CREATE INDEX idx_delivery_tasks_location ON delivery_tasks USING gist(ll_to_earth(current_lat, current_lng));
```

**Business Rules:**
- 1:1 relationship with orders
- Location snapshots preserve pickup/dropoff at task creation
- Current location updated via driver app

---

#### 3.6.3 delivery_task_events
**Purpose:** Delivery task audit trail

| Column | Type | Constraints | Description |
|:-------|:-----|:------------|:------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique event identifier |
| delivery_task_id | UUID | FK → delivery_tasks(id) ON DELETE CASCADE, NOT NULL | Parent delivery task |
| event_type | VARCHAR(32) | NOT NULL | ASSIGNED, PICKED_UP, IN_TRANSIT, DELIVERED |
| event_data | JSONB | NULLABLE | Additional event metadata |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Event timestamp |

**Indexes:**
```sql
CREATE INDEX idx_delivery_task_events_task_id ON delivery_task_events(delivery_task_id);
CREATE INDEX idx_delivery_task_events_created_at ON delivery_task_events(created_at DESC);
```

---

#### 3.6.4 driver_location_history
**Purpose:** GPS tracking history (partitioned for performance)

| Column | Type | Constraints | Description |
|:-------|:-----|:------------|:------------|
| id | BIGSERIAL | PK | Unique location record identifier |
| driver_id | UUID | FK → drivers(id), NOT NULL | Driver |
| delivery_task_id | UUID | FK → delivery_tasks(id), NULLABLE | Associated delivery task |
| location | GEOGRAPHY(POINT) | NOT NULL | PostGIS geography point |
| speed_kmh | NUMERIC(5,2) | NULLABLE | Speed in km/h |
| heading | INTEGER | NULLABLE | Compass heading (0-359) |
| accuracy_meters | NUMERIC(6,2) | NULLABLE | GPS accuracy |
| recorded_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Recording timestamp |

**Partitioning:**
```sql
PARTITION BY RANGE (recorded_at);
-- Create monthly partitions
-- Retention: 30 days (auto-delete old partitions)
```

**Indexes:**
```sql
CREATE INDEX idx_driver_location_history_task ON driver_location_history(delivery_task_id, recorded_at DESC);
```

**Business Rules:**
- High-frequency inserts (every 5 seconds when driver is on delivery)
- Time-series partitioning for performance
- Old partitions dropped after retention period

---

### 3.7 Rating Domain

#### 3.7.1 ratings
**Purpose:** Customer ratings for restaurants and drivers

| Column | Type | Constraints | Description |
|:-------|:-----|:------------|:------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique rating identifier |
| order_id | UUID | FK → orders(id), NOT NULL | Rated order |
| rater_id | UUID | FK → users(id), NOT NULL | User who rated |
| ratee_id | UUID | FK → users(id), NOT NULL | User/restaurant being rated |
| rating_type | VARCHAR(32) | NOT NULL, CHECK | RESTAURANT, DRIVER |
| score | SMALLINT | NOT NULL, CHECK (1-5) | Star rating (1-5) |
| comment | TEXT | NULLABLE | Review comment |
| is_deleted | BOOLEAN | NOT NULL, DEFAULT FALSE | Soft delete flag |
| created_by | UUID | NULLABLE | Creator |
| updated_by | UUID | NULLABLE | Last updater |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes:**
```sql
CREATE INDEX idx_ratings_order_id ON ratings(order_id);
CREATE INDEX idx_ratings_rater_id ON ratings(rater_id);
CREATE INDEX idx_ratings_ratee_id ON ratings(ratee_id) WHERE rating_type = 'RESTAURANT';
CREATE INDEX idx_ratings_created_at ON ratings(created_at DESC);
```

**Business Rules:**
- One rating per order per type (RESTAURANT + DRIVER)
- `ratee_id` references restaurant owner for RESTAURANT type
- `ratee_id` references driver user for DRIVER type
- Triggers update `restaurants.average_rating` and `drivers.rating`

---

### 3.8 Dispute Domain

#### 3.8.1 disputes
**Purpose:** Customer dispute management

| Column | Type | Constraints | Description |
|:-------|:-----|:------------|:------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique dispute identifier |
| order_id | UUID | FK → orders(id), NOT NULL | Disputed order |
| customer_id | UUID | FK → users(id), NOT NULL | Disputing customer |
| category | VARCHAR(50) | NOT NULL, CHECK | missing_item, wrong_item, quality, late_delivery, driver_behavior |
| description | TEXT | NULLABLE | Dispute description |
| photo_urls | TEXT[] | NULLABLE | Evidence photo URLs (array) |
| status | VARCHAR(32) | NOT NULL, DEFAULT 'open', CHECK | open, investigating, resolved, rejected |
| resolution_type | VARCHAR(32) | NULLABLE | full_refund, partial_refund, discount_code, no_action |
| resolution_amount | NUMERIC(12,2) | NULLABLE | Refund/compensation amount |
| resolved_by | UUID | FK → users(id), NULLABLE | Admin who resolved |
| resolved_at | TIMESTAMPTZ | NULLABLE | Resolution timestamp |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Dispute creation timestamp |
| updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes:**
```sql
CREATE INDEX idx_disputes_order_id ON disputes(order_id);
CREATE INDEX idx_disputes_customer_id ON disputes(customer_id, created_at DESC);
CREATE INDEX idx_disputes_status ON disputes(status);
```

**Business Rules:**
- Can be created within 24h of delivery
- Auto-resolution for some categories (missing_item, wrong_item)
- Admin review for quality issues and driver behavior

---

### 3.9 Audit Domain

#### 3.9.1 audit_logs
**Purpose:** System-wide audit trail

| Column | Type | Constraints | Description |
|:-------|:-----|:------------|:------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique audit log identifier |
| entity_type | VARCHAR(50) | NOT NULL | order, payment, user, dispute, restaurant |
| entity_id | UUID | NOT NULL | ID of affected entity |
| action | VARCHAR(50) | NOT NULL | create, update, delete, cancel, refund |
| actor_id | UUID | NULLABLE | User who performed action |
| actor_role | VARCHAR(32) | NULLABLE | Actor's role |
| old_values | JSONB | NULLABLE | Previous state |
| new_values | JSONB | NULLABLE | New state |
| ip_address | INET | NULLABLE | Request IP address |
| user_agent | TEXT | NULLABLE | Request user agent |
| created_at | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Action timestamp |

**Indexes:**
```sql
CREATE INDEX idx_audit_logs_entity ON audit_logs(entity_type, entity_id, created_at DESC);
CREATE INDEX idx_audit_logs_actor ON audit_logs(actor_id, created_at DESC);
```

**Business Rules:**
- Immutable audit trail
- Retention: 6 months hot storage, 1 year cold storage
- Used for compliance (GDPR, PCI-DSS)

---

## 4. RELATIONSHIP SPECIFICATIONS

### 4.1 Relationship Cardinalities

| Parent Entity | Relationship | Child Entity | Cardinality | Notes |
|:--------------|:-------------|:-------------|:------------|:------|
| cities | HAS | users | 1:N | Users belong to one city |
| cities | HAS | restaurants | 1:N | Restaurants operate in one city |
| users | HAS | user_addresses | 1:N | Users can have multiple addresses |
| users | HAS | user_payment_methods | 1:N | Users can have multiple payment methods |
| users | HAS | refresh_tokens | 1:N | Users can have multiple active tokens |
| users (owner) | OWNS | restaurants | 1:N | Owner can have multiple restaurants |
| users (customer) | PLACES | orders | 1:N | Customers place multiple orders |
| users (driver) | HAS | drivers | 1:1 | One driver profile per user |
| users (rater) | RATES | ratings | 1:N | Users can rate multiple orders |
| restaurants | HAS | menu_categories | 1:N | Restaurants have multiple categories |
| restaurants | HAS | menu_items | 1:N | Restaurants have multiple items |
| restaurants | RECEIVES | orders | 1:N | Restaurants receive multiple orders |
| restaurants | TARGETED_BY | coupons | 1:N | Restaurant-specific coupons (optional) |
| menu_categories | CONTAINS | menu_items | 1:N | Categories contain items (optional) |
| menu_items | HAS | menu_item_variants | 1:N | Items have variants |
| coupons | USED_IN | coupon_usages | 1:N | Coupons tracked via usages |
| orders | CONTAINS | order_items | 1:N | Orders have line items |
| orders | HAS | payments | 1:1 | One payment per order |
| orders | HAS | delivery_tasks | 1:1 | One delivery per order |
| orders | HAS | order_events | 1:N | Orders have event history |
| orders | HAS | ratings | 1:2 | One rating each for restaurant/driver |
| orders | HAS | disputes | 1:N | Orders can have disputes |
| order_items | HAS | order_item_variants | 1:N | Order items have variant selections |
| payments | HAS | payment_refunds | 1:N | Payments can have multiple refunds |
| drivers | ASSIGNED | delivery_tasks | 1:N | Drivers handle multiple deliveries |
| delivery_tasks | HAS | delivery_task_events | 1:N | Delivery tasks have event history |
| drivers | HAS | driver_location_history | 1:N | Drivers have location history |

### 4.2 Order State Machine

```
┌─────────────────────────────────────────────────────────────────────┐
│                         ORDER STATE MACHINE                         │
└─────────────────────────────────────────────────────────────────────┘

                    ┌──────────────┐
                    │   CREATED    │ (Order placed)
                    └──────┬───────┘
                           │
                ┌──────────┴──────────┐
                │                     │
        ┌───────▼────────┐   ┌───────▼────────┐
        │ PAYMENT_FAILED │   │   CONFIRMED    │ (Payment authorized)
        └────────────────┘   └───────┬────────┘
                                     │
                            ┌────────▼────────┐
                            │   PREPARING     │ (Restaurant accepted)
                            └────────┬────────┘
                                     │
                            ┌────────▼────────┐
                            │ READY_FOR_PICKUP│ (Food ready)
                            └────────┬────────┘
                                     │
                            ┌────────▼────────┐
                            │  ON_THE_WAY     │ (Driver picked up)
                            └────────┬────────┘
                                     │
                            ┌────────▼────────┐
                            │   DELIVERED     │ (Delivery complete)
                            └─────────────────┘

                 (Any state can transition to:)
                            ┌─────────────┐
                            │  CANCELLED  │
                            └─────────────┘
                            ┌─────────────┐
                            │DELIVERY_     │
                            │  FAILED     │
                            └─────────────┘
```

**Valid Transitions:**
- CREATED → PAYMENT_FAILED (payment fails)
- CREATED → CONFIRMED (payment authorized)
- CREATED → CANCELLED (customer cancels before payment)
- CONFIRMED → PREPARING (restaurant accepts)
- CONFIRMED → CANCELLED (restaurant rejects, customer cancels)
- PREPARING → READY_FOR_PICKUP (food ready)
- PREPARING → CANCELLED (restaurant cancels)
- READY_FOR_PICKUP → ON_THE_WAY (driver picks up)
- ON_THE_WAY → DELIVERED (driver completes delivery)
- ON_THE_WAY → DELIVERY_FAILED (delivery fails)
- ON_THE_WAY → CANCELLED (cancelled during delivery)

### 4.3 Payment State Machine

```
┌─────────────────────────────────────────────────────────────────────┐
│                        PAYMENT STATE MACHINE                        │
└─────────────────────────────────────────────────────────────────────┘

            ┌──────────────┐
            │   PENDING    │ (Payment initiated)
            └──────┬───────┘
                   │
        ┌──────────┴──────────┐
        │                     │
┌───────▼────────┐   ┌───────▼────────┐
│    FAILED      │   │  AUTHORIZED    │ (Hold placed)
└────────────────┘   └───────┬────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
            ┌───────▼────────┐   ┌───▼────┐
            │   CAPTURED     │   │REFUNDED│
            └───────┬────────┘   └────────┘
                    │
                    │
            ┌───────▼────────┐
            │   REFUNDED     │
            └────────────────┘
```

**Valid Transitions:**
- PENDING → AUTHORIZED (auth success)
- PENDING → FAILED (auth failed)
- AUTHORIZED → CAPTURED (capture success)
- AUTHORIZED → REFUNDED (refund before capture)
- CAPTURED → REFUNDED (refund after capture)

### 4.4 Delivery Task State Machine

```
┌─────────────────────────────────────────────────────────────────────┐
│                   DELIVERY TASK STATE MACHINE                       │
└─────────────────────────────────────────────────────────────────────┘

        ┌──────────────┐
        │   CREATED    │ (Task created)
        └──────┬───────┘
               │
        ┌──────▼───────┐
        │   ASSIGNED   │ (Driver assigned)
        └──────┬───────┘
               │
        ┌──────▼───────┐
        │  PICKED_UP   │ (Driver picked up food)
        └──────┬───────┘
               │
        ┌──────▼───────┐
        │  IN_TRANSIT  │ (Driver en route)
        └──────┬───────┘
               │
        ┌──────▼───────┐
        │  DELIVERED   │ (Delivery complete)
        └──────────────┘

     (Any state except DELIVERED can transition to:)
        ┌──────────────┐
        │  CANCELLED   │
        └──────────────┘
```

---

## 5. DATA TYPES & CONSTRAINTS

### 5.1 Common Data Types

| Type | Usage | Notes |
|:-----|:------|:------|
| UUID | Primary keys, foreign keys | Distributed system friendly |
| VARCHAR(N) | Short strings (names, codes) | Variable length, indexed |
| TEXT | Long strings (descriptions, comments) | No length limit |
| NUMERIC(12,2) | Money (prices, amounts) | Precise decimal, no floating point errors |
| BOOLEAN | Flags (is_active, is_deleted) | TRUE/FALSE/NULL |
| TIMESTAMPTZ | Timestamps | Timezone-aware, UTC storage |
| JSONB | Flexible schema (snapshots, metadata) | Binary JSON, indexable |
| DOUBLE PRECISION | GPS coordinates (lat, lng) | 15 decimal digit precision |
| ENUM | State machines (order_status, etc.) | Type-safe, performant |
| TEXT[] | Arrays (photo_urls) | Native PostgreSQL array |
| GEOGRAPHY(POINT) | Geospatial (location) | PostGIS extension |

### 5.2 Common Constraints

| Constraint | Usage | Notes |
|:-----------|:------|:------|
| PRIMARY KEY | Uniqueness + not null | UUID or BIGSERIAL |
| FOREIGN KEY | Referential integrity | ON DELETE CASCADE/SET NULL |
| UNIQUE | Uniqueness (email, code) | Can be composite |
| NOT NULL | Required field | Cannot be null |
| CHECK | Value validation | Enum values, ranges |
| DEFAULT | Default value | NOW(), FALSE, 0, gen_random_uuid() |

### 5.3 Audit Columns (Standard Pattern)

All tables include these audit columns:

```sql
created_by    UUID              NULLABLE         -- Who created
updated_by    UUID              NULLABLE         -- Who last updated
created_at    TIMESTAMPTZ       NOT NULL DEFAULT NOW()  -- When created
updated_at    TIMESTAMPTZ       NOT NULL DEFAULT NOW()  -- When last updated
```

**Trigger for auto-updating `updated_at`:**

```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply to each table:
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

### 5.4 Soft Delete Pattern

Tables with `is_deleted` flag:

```sql
is_deleted    BOOLEAN           NOT NULL DEFAULT FALSE
```

**Usage:**
- Soft delete: `UPDATE users SET is_deleted = TRUE WHERE id = ?`
- Filter in queries: `WHERE is_deleted = FALSE`
- Partial indexes: `CREATE INDEX idx_users_email ON users(email) WHERE is_deleted = FALSE`

---

## 6. INDEX STRATEGY

### 6.1 Index Types

| Index Type | Usage | Example |
|:-----------|:------|:--------|
| B-Tree (default) | Equality, range queries | `CREATE INDEX idx_users_email ON users(email)` |
| GiST | Geospatial, full-text | `CREATE INDEX idx_restaurants_location USING gist(...)` |
| Partial Index | Filtered queries | `CREATE INDEX ... WHERE is_deleted = FALSE` |
| Composite Index | Multi-column queries | `CREATE INDEX idx_orders_customer_status ON orders(customer_id, status)` |
| UNIQUE Index | Uniqueness constraint | `CREATE UNIQUE INDEX idx_coupons_code ON coupons(code)` |

### 6.2 Indexing Guidelines

**Always index:**
- Primary keys (automatic)
- Foreign keys (explicit)
- Columns in WHERE clauses
- Columns in JOIN conditions
- Columns in ORDER BY
- UNIQUE constraints

**Consider partial indexes for:**
- Queries with common filters (`WHERE is_deleted = FALSE`)
- Status-based queries (`WHERE status = 'ACTIVE'`)

**Avoid over-indexing:**
- Each index adds write overhead
- Monitor index usage: `pg_stat_user_indexes`
- Drop unused indexes

### 6.3 Index Maintenance

```sql
-- Rebuild indexes (during maintenance window)
REINDEX TABLE users;

-- Check bloat
SELECT schemaname, tablename, indexname, pg_size_pretty(pg_relation_size(indexrelid))
FROM pg_stat_user_indexes
ORDER BY pg_relation_size(indexrelid) DESC;

-- Drop unused indexes
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0 AND indexrelname NOT LIKE '%_pkey';
```

---

## 7. NAMING CONVENTIONS

### 7.1 Table Naming

- **Plural nouns:** `users`, `orders`, `menu_items`
- **Lowercase with underscores:** `user_addresses`, `order_events`
- **Junction tables:** `coupon_usages`, `order_item_variants`

### 7.2 Column Naming

- **Lowercase with underscores:** `first_name`, `is_active`
- **Boolean fields:** Prefix with `is_`, `has_`, `can_` (e.g., `is_deleted`, `is_online`)
- **Timestamps:** Suffix with `_at` (e.g., `created_at`, `authorized_at`)
- **Foreign keys:** `{referenced_table_singular}_id` (e.g., `user_id`, `restaurant_id`)
- **Enums:** Singular noun (e.g., `status`, `role`, `type`)

### 7.3 Index Naming

- **Pattern:** `idx_{table}_{columns}[_{condition}]`
- **Examples:**
  - `idx_users_email`
  - `idx_orders_customer_id`
  - `idx_orders_status_active` (for partial index)
  - `idx_restaurants_location` (for GiST index)

### 7.4 Constraint Naming

- **Primary Key:** `{table}_pkey` (automatic)
- **Foreign Key:** `{table}_{column}_fkey` (automatic)
- **Unique:** `{table}_{column}_key` (automatic)
- **Check:** `{table}_{column}_check` (automatic)

### 7.5 Enum Naming

- **Pattern:** `{description}_enum`
- **Examples:**
  - `order_status_enum`
  - `payment_status_enum`
  - `driver_status_enum`

---

## 8. ERD GENERATION COMMANDS

### 8.1 Generate ERD from Database

**Using SchemaSpy:**
```bash
java -jar schemaspy.jar \
  -t pgsql \
  -host localhost \
  -port 5432 \
  -db food_delivery \
  -u postgres \
  -p password \
  -o ./schema_output
```

**Using pgModeler:**
```bash
# Export from PostgreSQL
pg_dump -s food_delivery > schema.sql

# Import into pgModeler for visualization
```

**Using dbdiagram.io (DBML):**
```dbml
// Generate DBML from schema
// Import into dbdiagram.io for visualization
Table users {
  id uuid [pk]
  email varchar(255) [unique]
  // ... rest of schema
}
```

### 8.2 Generate Database from ERD

**From SQL DDL:**
```bash
psql -U postgres -d food_delivery -f schema.sql
```

**From migration tool (e.g., Flyway):**
```bash
flyway -url=jdbc:postgresql://localhost:5432/food_delivery -user=postgres migrate
```

---

## 9. MIGRATION STRATEGY

### 9.1 Initial Schema Creation

**Order of table creation (respecting FK dependencies):**

1. **Independent tables:**
   - `cities`

2. **User domain:**
   - `users` (FK → cities)
   - `user_addresses` (FK → users, cities)
   - `user_payment_methods` (FK → users)
   - `refresh_tokens` (FK → users)

3. **Restaurant domain:**
   - `restaurants` (FK → users, cities)
   - `menu_categories` (FK → restaurants)
   - `menu_items` (FK → restaurants, menu_categories)
   - `menu_item_variants` (FK → menu_items)

4. **Promotion domain:**
   - `coupons` (FK → restaurants, cities)
   - `coupon_usages` (FK → coupons, users, orders) *-- defer orders FK*

5. **Driver domain:**
   - `drivers` (FK → users, cities)

6. **Order domain:**
   - `orders` (FK → users, restaurants, cities, user_addresses, user_payment_methods)
   - `order_items` (FK → orders, menu_items)
   - `order_item_variants` (FK → order_items)
   - `order_events` (FK → orders, users)

7. **Payment domain:**
   - `payments` (FK → orders)
   - `payment_refunds` (FK → payments)

8. **Delivery domain:**
   - `delivery_tasks` (FK → orders, drivers)
   - `delivery_task_events` (FK → delivery_tasks)
   - `driver_location_history` (FK → drivers, delivery_tasks)

9. **Rating & Dispute domain:**
   - `ratings` (FK → orders, users)
   - `disputes` (FK → orders, users)

10. **Audit domain:**
    - `audit_logs` (FK → users)

**Note:** Add `orders.delivery_task_id` FK after `delivery_tasks` is created.

### 9.2 Migration Tools

**Recommended:** Flyway or Liquibase for version-controlled migrations

**Flyway example:**
```
V1__create_cities.sql
V2__create_users.sql
V3__create_user_addresses.sql
...
V20__create_indexes.sql
```

### 9.3 Rollback Strategy

- Maintain DOWN migrations for each UP migration
- Test rollback scripts in staging
- Backup before production migrations

---

## 10. PERFORMANCE CONSIDERATIONS

### 10.1 Query Optimization

**Common slow queries:**
1. **Restaurant search by location:**
   - Use GiST index on lat/lng
   - Consider materialized view for popular searches

2. **Order history with joins:**
   - Denormalize frequently accessed data (e.g., restaurant name in order snapshot)
   - Use read replicas for reporting

3. **Real-time driver location:**
   - Partition `driver_location_history` by time
   - Use Redis for current location cache

### 10.2 Scaling Strategies

**Vertical Scaling (MVP):**
- Increase PostgreSQL instance size
- Tune `shared_buffers`, `work_mem`, `effective_cache_size`

**Horizontal Scaling (Phase 2+):**
- Read replicas for read-heavy workloads
- Sharding by city_id (multi-tenant)
- CQRS pattern: separate read/write databases

### 10.3 Connection Pooling

**Use PgBouncer:**
```ini
[databases]
food_delivery = host=localhost port=5432 dbname=food_delivery

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 20
```

---

## 11. SECURITY CONSIDERATIONS

### 11.1 Row-Level Security (RLS)

**Example: Users can only see own data:**
```sql
ALTER TABLE user_addresses ENABLE ROW LEVEL SECURITY;

CREATE POLICY user_addresses_policy ON user_addresses
FOR ALL
USING (user_id = current_setting('app.current_user_id')::uuid);
```

### 11.2 Encryption

- **At-rest:** PostgreSQL TDE or filesystem-level encryption
- **In-transit:** TLS 1.3 for all connections
- **Application-level:** Encrypt `user_payment_methods.token` before INSERT

### 11.3 Least Privilege

```sql
-- Application user (read/write)
CREATE ROLE app_user LOGIN PASSWORD 'secure_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;

-- Read-only user (reporting)
CREATE ROLE readonly_user LOGIN PASSWORD 'secure_password';
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_user;

-- No direct DELETE (use soft delete)
REVOKE DELETE ON ALL TABLES IN SCHEMA public FROM app_user;
```

---

## 12. CONCLUSION

This ERD provides a comprehensive blueprint for the Food Delivery Platform database. Key highlights:

**Scalability:**
- UUID primary keys for distributed systems
- Partitioning for high-volume tables
- Efficient indexing strategy

**Data Integrity:**
- Foreign key constraints
- Check constraints for enums
- State machine validation

**Compliance:**
- Audit trail (order_events, delivery_task_events, audit_logs)
- Soft delete pattern for GDPR compliance
- Encrypted sensitive data (payment tokens)

**Performance:**
- GiST indexes for geospatial queries
- Partial indexes for common filters
- Denormalized aggregates (average_rating, total_reviews)

**Next Steps:**
1. Review ERD with engineering team
2. Generate DDL scripts with proper ordering
3. Set up Flyway/Liquibase for migrations
4. Create test data scripts
5. Performance testing with realistic data volumes
6. Set up monitoring for slow queries

---

**Document Metadata:**

| Field | Value |
|:------|:------|
| Version | 1.0 |
| Date | 21 January 2026 |
| Author | Senior Database Architect |
| Status | Ready for Review |
| Database | PostgreSQL 14+ |
| Total Tables | 17 core entities |
| Total Indexes | 50+ optimized indexes |

---

**END OF ERD DOCUMENTATION**
