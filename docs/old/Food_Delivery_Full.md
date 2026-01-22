# Software Requirements Specification (SRS) – Food Delivery Platform
(Tài liệu đặc tả yêu cầu phần mềm / hệ thống cho nền tảng food delivery)
## High-Performance, Scalable Food Delivery Platform
**Document Version:** 2.0 (Refined)  
**Date:** 20 Jan 2026  
**Location:** Ho Chi Minh City, Vietnam  
**Status:** Ready for Development Planning  

---

## TABLE OF CONTENTS
1. Executive Summary
2. Business Requirements & Objectives
3. Scope Definition: MVP vs Phase 2+
4. User Roles & Business Process
5. Functional Requirements (FR)
6. Business Rules
7. Non-Functional Requirements
8. SLO/SLI & Error Budget
9. System Architecture
10. Data Model & Schema
11. API Contracts
12. Testing Strategy
13. Security Requirements
14. Deployment & Operations
15. Roadmap & Phase Planning
16. Risk & Mitigation
17. KPIs & Success Metrics

---

## 1. EXECUTIVE SUMMARY

### 1.1 Project Overview
Phát triển hệ thống platform food delivery high-performance, scalable sử dụng kiến trúc microservices với Golang backend, React/Next.js frontend. Hệ thống phục vụ ba nhóm người dùng chính: **Khách hàng (Customer)**, **Nhà hàng (Restaurant Partner)**, và **Tài xế giao hàng (Delivery Driver)**.

### 1.2 Business Objectives
- Cung cấp trải nghiệm gọi đồ ăn nhanh, đơn giản, với thời gian phản hồi < 500ms cho API lõi
- Hỗ trợ 99.9% uptime availability; xử lý spike traffic (giờ trưa/tối) mà không sụt hiệu năng
- Tối ưu khám phá nhà hàng/món ăn thông qua search & ranking (early stage dùng ranking đơn giản)
- Đảm bảo tính toàn vẹn dữ liệu payment: 0 double-charge, >99% reconciliation trong 24h
- Xây dựng nền tảng dễ mở rộng sang multi-city, multi-vertical (grocery, pharmacy)

### 1.3 Target Market & Scale

**Phase 1 (MVP):**
- Thị trường: TP. HCM (1 city)
- Mục tiêu người dùng: 50k–100k khách hàng, 1k–2k nhà hàng, 500–1k tài xế
- Peak traffic: 3k–5k concurrent users; 10–20 orders/giây

**Phase 2 (Expansion):**
- Mở rộng Hà Nội, TP. HCM mở rộng
- 500k customers, 5k restaurants, 2k drivers
- Peak: 10k concurrent users, 50 orders/giây

---

## 2. BUSINESS REQUIREMENTS & OBJECTIVES

### 2.1 Capability Map (Thể hiện các capability theo từng role)

| Capability | Customer | Merchant | Driver | Admin | MVP | Phase 2+ |
|:-----------|:--------:|:--------:|:-------:|:-----:|:---:|:--------:|
| Authentication & Profile | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Search & Browse Restaurants | ✓ | - | - | - | ✓ (basic) | ✓ (personalized) |
| View Menu & Place Order | ✓ | - | - | - | ✓ | ✓ |
| Manage Payment Methods | ✓ | - | - | - | ✓ (1–2 methods) | ✓ (multi-method) |
| Track Order in Real-time | ✓ | - | - | - | ✓ | ✓ |
| Rate & Review | ✓ | ✓ (reply) | - | - | ✓ (basic) | ✓ (advanced moderation) |
| Manage Menu & Categories | - | ✓ | - | - | ✓ | ✓ |
| Accept/Reject Orders | - | ✓ | - | - | ✓ | ✓ |
| Dashboard & Analytics | - | ✓ | - | - | ✓ (basic) | ✓ (advanced) |
| Receive & Deliver Orders | - | - | ✓ | - | ✓ | ✓ |
| Track Earnings | - | - | ✓ | - | ✓ (basic) | ✓ (detailed) |
| Onboarding Workflow | - | - | - | ✓ | ✓ | ✓ |
| KPI Dashboard | - | - | - | ✓ | ✓ | ✓ |
| Dispute Resolution | - | - | - | ✓ | ✓ (basic) | ✓ (advanced) |

### 2.2 User Roles & Primary Use Cases

#### 2.2.1 Customer (Khách hàng)
**Primary Use Cases:**
- Đăng ký/đăng nhập (email, phone, social login)
- Quản lý profile, địa chỉ giao hàng, phương thức thanh toán
- Tìm kiếm/duyệt nhà hàng theo vị trí, loại hình, giá (MVP: basic filtering)
- Xem menu, thêm/sửa giỏ hàng, áp dụng mã khuyến mãi
- Đặt hàng: chọn thời gian ASAP/lên lịch, thanh toán (COD + 1 gateway)
- Theo dõi trạng thái đơn realtime, liên hệ driver/merchant
- Đánh giá & review sau khi nhận hàng
- Xem lịch sử, tái đặt (reorder) đơn cũ

**MVP Scope:** Tất cả use case cơ bản trên, search basic (location-based), 1–2 payment method, tracking realtime

**Phase 2+:** Personalized recommendations, advanced filtering, multi-method payment, loyalty points

#### 2.2.2 Restaurant Partner (Chủ nhà hàng)
**Primary Use Cases:**
- Onboarding: thông tin cơ bản, địa chỉ, khu vực phục vụ
- Quản lý menu: thêm/sửa/xóa món, giá, hình ảnh, tùy chọn (size, topping)
- Cập nhật trạng thái: bật/tắt nhận đơn, đóng cửa tạm thời
- Xem & xử lý order incoming: xác nhận/từ chối, báo "ready for pickup"
- Xem thống kê: số đơn, doanh thu, rating, feedback (ngày/tuần/tháng)
- Quản lý khuyến mãi cơ bản: discount, voucher, khoảng thời gian

**MVP Scope:** Onboarding đơn giản, menu CRUD, order management, thống kê basic

**Phase 2+:** Bulk upload menu, advanced promotion targeting, item-level analytics, multi-branch support

#### 2.2.3 Delivery Driver (Tài xế giao hàng)
**Primary Use Cases:**
- Đăng ký/xác minh: thông tin cá nhân, phương tiện, bằng lái
- Online/offline status; bật để nhận đơn
- Xem danh sách đơn được gán, chi tiết pickup/dropoff
- Điều hướng GPS, cập nhật trạng thái giao (picked-up, in-transit, delivered)
- Liên hệ customer khi cần xác nhận địa chỉ
- Xem doanh thu, lịch giao hàng, rating từ khách

**MVP Scope:** Onboarding cơ bản, online/offline, assignment simple (nearest available), tracking GPS basic, earnings summary

**Phase 2+:** Route optimization, surge pricing, performance analytics, advanced incentive

#### 2.2.4 Admin / Super Admin
**Primary Use Cases:**
- Duyệt onboarding merchant/driver, khóa/mở tài khoản
- Cấu hình hệ thống: khu vực giao, fee mặc định, holiday
- Xem báo cáo: doanh thu, số đơn, user growth, SLA metrics
- Quản lý global campaigns & promotions
- Xem logs, incident, SLI/SLO metrics, alert

**MVP Scope:** Quản lý user/restaurant/driver, duyệt onboarding, suspend account, dashboard KPI cơ bản

**Phase 2+:** Advanced reporting, campaign management, incident automation

### 2.3 Business Process Flow

#### 2.3.1 Primary Flow: "Place Order" (Happy Path)

```
1. Customer login
   ↓
2. Search restaurant (browse/filter by location) → select restaurant
   ↓
3. View menu → add items to cart → adjust quantity
   ↓
4. Confirm cart → [optional] apply coupon code
   ↓
5. Input/select delivery address
   ↓
6. Select payment method (COD or card/e-wallet)
   ↓
7. Confirm order (Order status: CREATED)
   ↓
8. Payment processing (if not COD): authorize → capture
   ↓
9. Payment status: CAPTURED
   ↓
10. Order status: CONFIRMED
    ↓ (send notification to Restaurant)
11. Restaurant receives notification → review order
    ↓
12. Restaurant accepts → order status: PREPARING
    ↓
13. Restaurant updates: ready for pickup → order status: READY_FOR_PICKUP
    ↓
14. Dispatch system assigns driver → create DeliveryTask
    ↓
15. Driver receives notification → accepts delivery
    ↓
16. Driver picks up from restaurant → order status: ON_THE_WAY
    ↓
17. Driver location updated realtime (customer can track)
    ↓
18. Driver delivers to customer → order status: DELIVERED
    ↓
19. Payment: final settlement recorded
    ↓
20. Customer rates restaurant, items, driver
```

#### 2.3.2 Key Exception Flows

**Flow A: Customer Cancels (Before Restaurant Accept)**
```
Order (CREATED/CONFIRMED) → Customer initiates cancel
→ Check: if restaurant not yet accepted → cancel immediately
→ Refund: full amount + notify restaurant (optional discount offer)
→ Order status: CANCELLED
```

**Flow B: Restaurant Rejects/Cannot Fulfill**
```
Order (CONFIRMED) → Restaurant rejects
→ Refund: full amount immediately
→ Notify: Customer + system
→ Dispatch: Previous driver cancelled, reassign or fail order gracefully
→ Offer: Customer gets discount code for next order
```

**Flow C: Payment Failure**
```
Order (CREATED) → Payment processing fails
→ Retry: 1–2 times automatically (with backoff)
→ If still fail → Order status: PAYMENT_FAILED
→ Notify: Customer + allow retry or cancel
→ If customer cancels: order → CANCELLED
```

**Flow D: Delivery Not Completed in SLA**
```
Order (ON_THE_WAY, estimated_delivery_time passed)
→ If actual_delivery_time > estimated + buffer (15min) 
→ Trigger alert for support team
→ If delivery takes 3+ hours → auto-cancel + full refund + incident
```

**Flow E: Payment Dispute / Customer Complaint**
```
Order (DELIVERED) → Customer reports issue within 24h
→ Create Dispute ticket
→ Admin review: (a) auto refund if order arrived late, (b) manual if quality issue
→ Settlement: refund to customer payment method
```

---

## 3. SCOPE DEFINITION: MVP vs PHASE 2+

### 3.1 MVP (Phase 1) – Go-Live Target

**GO-LIVE SCOPE (3–4 tháng):**

| Component | MVP Include | Details |
|:----------|:-----------:|:---------|
| **Auth** | YES | Email/phone/OTP, JWT, basic role RBAC |
| **Customer** | YES | Profile, 2 addresses, 1–2 payment methods (COD + 1 card/e-wallet) |
| **Search** | MINIMAL | Geo-search (nearby restaurants by location), basic filter (open, rating), no ranking algo yet |
| **Catalog** | YES | Menu CRUD, categories, basic item variants (size, topping) |
| **Order** | YES | Cart, apply simple coupon (% or flat), total calc, state machine (CREATED→DELIVERED) |
| **Payment** | YES | COD + 1 gateway (Stripe/VNPay), basic reconciliation, refund full only |
| **Delivery** | YES | Driver assignment simple (nearest available + acceptance), GPS tracking basic |
| **Notification** | YES | Push (via FCM), SMS for critical events, basic retry |
| **Rating** | YES | Star + comment after delivery (no moderation yet) |
| **Admin** | YES | Dashboard KPI (orders, revenue, users), onboarding approval, user suspend |
| **Merchant** | YES | Menu management, accept/reject orders, basic stats (orders, revenue per day) |
| **Driver** | YES | Online/offline, assign+pickup+deliver flow, earning summary |
| **Performance** | 99.5–99.9% | p95 < 500ms for core API, uptime target |
| **Search Engine** | NO | Redis for simple caching, no Elasticsearch yet |
| **Recommendation** | NO | Manual featured list from admin |
| **Advanced Promo** | NO | Only basic coupon (per-user limit + date range) |
| **Route Optimization** | NO | Google Maps direction only |
| **Multi-City** | NO | Single city (HCM) deployment |

### 3.2 Phase 2 (Months 5–8) – Scale & Personalization

| Feature | Phase 2+ Include |
|:--------|:----------------:|
| Elasticsearch integration for advanced search & discovery | YES |
| Personalized recommendation engine (collaborative filtering) | YES |
| Advanced promotion: segment targeting, multi-city, promo stacking | YES |
| Multi-method payment: +Momo, +ZaloPay, +Bank transfer | YES |
| Loyalty points & subscription | YES |
| Driver earnings dashboard (detailed breakdown, payout schedule) | YES |
| Merchant analytics (item-level, promo ROI, peak hours) | YES |
| Multi-city expansion (Hà Nội, Biên Hòa, etc.) | YES |
| Service mesh (Istio) for canary deployment | YES |
| Advanced observability: distributed tracing, APM | YES |

### 3.3 Phase 3+ (Months 12+) – Ecosystem Expansion

| Feature | Phase 3+ Include |
|:--------|:----------------:|
| Grocery/Pharmacy vertical (same platform) | YES |
| B2B ordering (corporate lunch) | YES |
| White-label solution for regional partners | YES |
| Chat between customer/merchant/driver | YES |
| Advanced SLA & penalty automation | YES |
| Route optimization (vehicle routing problem solver) | YES |
| Real-time inventory sync with POS systems | YES |

---

## 4. BUSINESS RULES

### 4.1 Pricing & Fee Rules

**BR-PRI-001: Order Total Calculation**
- Total = Subtotal + Tax + Delivery Fee - Coupon Discount + Restaurant Fee (if any)
- Subtotal = SUM(item_price * quantity + variant_price_delta * quantity)
- Tax = Subtotal × tax_rate (to be configured per city/restaurant)
- Delivery Fee = calculated based on distance, time, weather, surge multiplier
- **Exception:** If coupon_discount > (Subtotal + Restaurant Fee), cap discount to avoid negative total

**BR-PRI-002: Delivery Fee Logic (MVP)**
- Base fee: 15,000 VND for distance ≤ 3km
- For distance > 3km: 15,000 + (distance - 3) × 3,000/km (rounded up)
- **Spike surcharge (Phase 2):** 1.2–1.5x multiplier during 11:30–13:30 and 17:00–19:30
- Exception: Free delivery for orders > 200,000 VND (configurable per restaurant)

**BR-PRI-003: Minimum Order Value**
- Restaurant can set minimum order value (default: 50,000 VND)
- System validates at checkout; if cart < minimum, show error "Please add more items"

### 4.2 Coupon & Promotion Rules

**BR-COUPON-001: Coupon Eligibility**
- Coupon is valid only if:
  - current_time is within coupon [start_time, end_time]
  - Order subtotal ≥ coupon.min_order_value
  - Customer usage < coupon.per_user_usage_limit (or global_usage_limit not exceeded)
  - Coupon.target_restaurant_id is NULL or matches order.restaurant_id
- Apply discount: if type="PERCENT" → discount = subtotal × (value/100), capped at max_discount; if type="FLAT" → discount = value

**BR-COUPON-002: Usage Tracking**
- Each coupon_usage record tied to (coupon_id, user_id, order_id)
- Reconciliation job daily: mark payment as CAPTURED → coupon_usage count incremented
- If payment fails/order cancels: usage record removed

**BR-COUPON-003: Stacking Policy (MVP)**
- Only 1 coupon per order (no stacking in MVP)
- Phase 2: introduce stacking rules (e.g., platform coupon + merchant coupon)

### 4.3 Cancellation & Refund Policy

**BR-CANCEL-001: Customer Cancellation**
- Before restaurant accepts (order in CREATED/CONFIRMED): cancel immediately, full refund + no penalty
- After restaurant accepts (order in PREPARING+): 
  - MVP: allow cancel with 10% penalty (of total)
  - Phase 2: vary penalty by elapsed time (0–5min: free, 5–15min: 5%, 15+min: 10%)
- If order in ON_THE_WAY/DELIVERED: cannot cancel (only dispute)

**BR-CANCEL-002: Restaurant Cancellation**
- Restaurant can reject/cancel order while in CONFIRMED status only
- Refund: 100% to customer
- Compensation: offer 50,000 VND discount code to customer
- Notification: customer receives SMS + push about cancellation + discount code

**BR-CANCEL-003: Driver Cancellation**
- If driver cancels after assigned (before PICKED_UP):
  - Refund driver commission (if paid upfront)
  - Reassign delivery task to another driver
  - If no driver available within 5 min → auto-cancel order + refund customer + penalty tracking on driver

**BR-CANCEL-004: System Auto-Cancel (SLA Miss)**
- If delivery not completed within (estimated_delivery_time + 60 min):
  - Status: DELIVERY_FAILED
  - Refund: 100% to customer + mark as "Failed delivery"
  - Compensation: 25k VND discount code
  - Incident: alert support team to investigate

### 4.4 Payment & Reconciliation

**BR-PAY-001: Idempotency & Double-Charge Prevention**
- Every order creation generates idempotency_key = hash(customer_id, restaurant_id, created_at, nonce)
- Payment request includes idempotency_key; if duplicate request received → return cached response (no charge twice)
- Outbox pattern: after payment CAPTURED, insert event into outbox table; background job dequeues and publishes to Kafka
- Daily reconciliation: read all orders with payment_status=CAPTURED; verify with gateway; fix discrepancy (if any) via manual refund

**BR-PAY-002: Payment Success Criteria**
- Status flow: PENDING → AUTHORIZED → CAPTURED (for card) or directly CAPTURED (for COD)
- For COD: payment_status marked CAPTURED only after driver confirms delivery
- For gateway: payment_status=AUTHORIZED when gateway pre-auth succeeds; CAPTURED when gateway confirm capture succeeds
- Timeout: if capture not confirmed within 30 min → mark FAILED, refund authorized amount

**BR-PAY-003: Refund Rules**
- Full refund: available anytime before settlement (admin triggers or auto on cancellation)
- Partial refund: admin-triggered for dispute resolution only
- Refund timeline: initiate immediately; appears in customer account within 1–2 business days (gateway dependent)
- Refund must link to original payment_id (no orphan refunds)

### 4.5 Order Lifecycle & State Machine

**BR-ORDER-001: Order Status Transitions**

```
CREATED 
  → [Payment fails] → PAYMENT_FAILED 
  → [Retry successful] → back to CREATED
  
CREATED 
  → [Restaurant accepts] → CONFIRMED
  → [Restaurant starts prep] → PREPARING
  → [Ready for pickup] → READY_FOR_PICKUP
  → [Driver assigned & picks up] → ON_THE_WAY
  → [Driver delivers] → DELIVERED
  → [Customer rates] → RATED (optional end state)

CREATED/CONFIRMED/PREPARING 
  → [Customer/restaurant/system cancels] → CANCELLED
  
ON_THE_WAY 
  → [SLA missed (60 min after ETA)] → DELIVERY_FAILED (auto-cancel)
```

**BR-ORDER-002: State Transition Permissions**
- Customer can transition: CREATED→CANCELLED (before confirm), DELIVERED→RATED
- Restaurant can transition: CONFIRMED→PREPARING, PREPARING→READY_FOR_PICKUP, any→CANCELLED_BY_RESTAURANT (with reason)
- Driver can transition: READY_FOR_PICKUP→ON_THE_WAY, ON_THE_WAY→DELIVERED
- System can transition: CREATED→CONFIRMED (payment success), ON_THE_WAY→DELIVERY_FAILED (SLA miss), etc.

### 4.6 Driver Assignment & Delivery SLA

**BR-DRIVER-001: Assignment Algorithm (MVP – Simple)**
- When order status → READY_FOR_PICKUP:
  1. Get all drivers with status=APPROVED and is_online=true
  2. Calculate distance from driver.current_location to restaurant.location
  3. Filter: distance ≤ 10km AND driver.acceptance_rate ≥ 50%
  4. Rank by: distance ASC, rating DESC
  5. Send delivery offer to top 3 drivers (in order); first to accept gets delivery
  6. Timeout: if no acceptance within 2 min → expand radius to 15km, try again
  7. If no driver found after 5 min → queue order, retry every 30 sec or notify restaurant/customer

**BR-DRIVER-002: Driver Earnings & Commission**
- Commission per delivery = 30% of delivery_fee (MVP flat rate; Phase 2: tier-based)
- Calculation: (delivery_fee - platform_commission) = net_amount → driver payout
- Payment: settled weekly (Monday for previous 7 days)

**BR-DRIVER-003: SLA & Performance Metrics**
- On-time delivery target: ≥ 95% of orders delivered within estimated_delivery_time + 10 min buffer
- Quality metric: average rating ≥ 4.5 stars (if < 4.0 → review status, if < 3.5 → suspend)
- Acceptance rate: ≥ 70% (if < 50% → lower priority in assignment, if < 20% → suspend)
- Incident rate: < 5% cancelled/failed deliveries per month

### 4.7 Restaurant Onboarding & Suspension

**BR-REST-001: Onboarding Workflow**
- Restaurant owner registers → submits basic info (name, address, phone, tax ID if available)
- Admin reviews (manual step MVP, auto-verify Phase 2) → approves/rejects
- Approved → restaurant added to system, can start uploading menu
- First order: within 48h after approval (prompt to upload menu)

**BR-REST-002: Suspension Policy**
- Restaurant auto-suspended if:
  - Closure rate > 30% (cancel orders / total received) per month → 7-day suspension + warning
  - Average rating drops < 3.0 → email warning, review required
  - Multiple customer complaints (quality, hygiene) → manual review by admin
- Manual suspension: admin can suspend for regulatory/compliance reasons (no order reason needed)

---

## 5. FUNCTIONAL REQUIREMENTS

### 5.1 User Service (Identity & Profile)

| ID | Requirement | Priority | MVP | Effort |
|:---|:-----------|:--------:|:---:|:-------:|
| FR-US-01 | User registration (email/phone with verification) | HIGH | YES | M |
| FR-US-02 | Login/logout, JWT + refresh token management | HIGH | YES | M |
| FR-US-03 | Forgot password, reset password flow | MEDIUM | YES | S |
| FR-US-04 | User profile CRUD: name, avatar, email, phone | HIGH | YES | S |
| FR-US-05 | Manage delivery addresses (CRUD, set default) | HIGH | YES | M |
| FR-US-06 | Manage payment methods (CRUD, set default) | HIGH | YES | M |
| FR-US-07 | Role-based access control (RBAC) | HIGH | YES | S |
| FR-US-08 | Account suspension/reactivation by admin | MEDIUM | YES | S |
| FR-US-09 | Two-factor authentication (OTP) for sensitive ops | MEDIUM | NO | M |
| FR-US-10 | Social login (Facebook, Google) | LOW | NO | M |

**Notes:**
- MVP: email/phone + OTP verification, basic JWT flow
- Phase 2: social login, advanced 2FA, biometric (for mobile)

### 5.2 Catalog Service (Restaurant & Menu)

| ID | Requirement | Priority | MVP | Effort |
|:---|:-----------|:--------:|:---:|:-------:|
| FR-CAT-01 | Restaurant registration & basic info | HIGH | YES | M |
| FR-CAT-02 | Restaurant operational zone management | HIGH | YES | M |
| FR-CAT-03 | Menu CRUD: items, categories, pricing | HIGH | YES | M |
| FR-CAT-04 | Menu item variants/options (size, toppings) | MEDIUM | YES | M |
| FR-CAT-05 | Item availability: mark unavailable, temp disable | HIGH | YES | S |
| FR-CAT-06 | Restaurant status: accepting orders on/off | HIGH | YES | S |
| FR-CAT-07 | Menu bulk upload (CSV) | LOW | NO | M |
| FR-CAT-08 | Restaurant search indexing & caching | HIGH | YES | M |
| FR-CAT-09 | Menu photo upload & management | MEDIUM | YES | M |

**Notes:**
- MVP: single language, basic image upload
- Phase 2: multi-language, bulk upload, image optimization

### 5.3 Order Service

| ID | Requirement | Priority | MVP | Effort |
|:---|:-----------|:--------:|:---:|:-------:|
| FR-ORD-01 | Create order: validate items, prices, stock | HIGH | YES | L |
| FR-ORD-02 | Order cart management | HIGH | YES | M |
| FR-ORD-03 | Calculate total: subtotal + fees + tax - discount | HIGH | YES | M |
| FR-ORD-04 | Apply coupon with validation | HIGH | YES | M |
| FR-ORD-05 | Order status lifecycle (state machine) | HIGH | YES | L |
| FR-ORD-06 | Order history & retrieval | HIGH | YES | M |
| FR-ORD-07 | Order cancellation with refund trigger | HIGH | YES | L |
| FR-ORD-08 | Estimated delivery time (ETD) calculation | HIGH | YES | M |
| FR-ORD-09 | Reorder: quick repeat previous order | MEDIUM | YES | S |
| FR-ORD-10 | Order notes/special instructions | MEDIUM | YES | S |
| FR-ORD-11 | Order audit trail (event log) | MEDIUM | YES | M |

**Notes:**
- MVP: basic ETD (distance + avg speed); Phase 2: ML-based
- State machine: keep in Order Service; event-driven via Kafka

### 5.4 Payment Service

| ID | Requirement | Priority | MVP | Effort |
|:---|:-----------|:--------:|:---:|:-------:|
| FR-PAY-01 | Payment session creation | HIGH | YES | M |
| FR-PAY-02 | Multiple payment methods (COD, card, e-wallet) | HIGH | YES (2) | L |
| FR-PAY-03 | Integration with payment gateway | HIGH | YES (1) | L |
| FR-PAY-04 | Payment authorization & capture | HIGH | YES | M |
| FR-PAY-05 | Webhook handling for success/failure | HIGH | YES | M |
| FR-PAY-06 | Refund processing (full/partial) | HIGH | YES | L |
| FR-PAY-07 | Idempotency for payment API | HIGH | YES | M |
| FR-PAY-08 | Daily reconciliation job | MEDIUM | YES | L |
| FR-PAY-09 | Transaction history & receipt | MEDIUM | YES | M |

**Notes:**
- MVP: COD + 1 gateway (Stripe or VNPay)
- Phase 2: +Momo, +ZaloPay, +Bank transfer

### 5.5 Delivery Service (Dispatch & Tracking)

| ID | Requirement | Priority | MVP | Effort |
|:---|:-----------|:--------:|:---:|:-------:|
| FR-DEL-01 | Driver registration & profile | HIGH | YES | M |
| FR-DEL-02 | Driver online/offline status with GPS | HIGH | YES | L |
| FR-DEL-03 | Delivery task creation & assignment | HIGH | YES | L |
| FR-DEL-04 | Driver assignment algorithm (simple) | HIGH | YES | M |
| FR-DEL-05 | Delivery status updates | HIGH | YES | M |
| FR-DEL-06 | Real-time GPS tracking | HIGH | YES | M |
| FR-DEL-07 | ETA calculation & updates | MEDIUM | YES | M |
| FR-DEL-08 | Driver earnings & payout history | MEDIUM | YES | M |
| FR-DEL-09 | Delivery SLA metrics & alerts | MEDIUM | YES | M |
| FR-DEL-10 | Route optimization | LOW | NO | L |

**Notes:**
- MVP: simple assignment (nearest + available)
- Phase 2: route optimization, surge pricing, advanced analytics

### 5.6 Search & Discovery Service

| ID | Requirement | Priority | MVP | Effort |
|:---|:-----------|:--------:|:---:|:-------:|
| FR-SEARCH-01 | Geo-search: nearby restaurants | HIGH | YES | M |
| FR-SEARCH-02 | Basic filter: open status, rating, distance | HIGH | YES | M |
| FR-SEARCH-03 | Full-text search on restaurant/item names | MEDIUM | YES (basic) | M |
| FR-SEARCH-04 | Auto-complete & suggestion | LOW | NO | M |
| FR-SEARCH-05 | Ranking algorithm (distance, rating, status) | MEDIUM | YES (basic) | M |
| FR-SEARCH-06 | Discovery page (featured, trending) | LOW | NO | S |
| FR-SEARCH-07 | Personalized recommendations | LOW | NO | L |
| FR-SEARCH-08 | Pagination with facet counts | HIGH | YES | S |

**Notes:**
- MVP: Redis caching, no Elasticsearch
- Phase 2: Elasticsearch, ML-based ranking, personalization

### 5.7 Notification Service

| ID | Requirement | Priority | MVP | Effort |
|:---|:-----------|:--------:|:---:|:-------:|
| FR-NOTIF-01 | Push notification on status changes | HIGH | YES | M |
| FR-NOTIF-02 | SMS for critical events | HIGH | YES | M |
| FR-NOTIF-03 | Email notifications (receipt, promo) | MEDIUM | YES | M |
| FR-NOTIF-04 | In-app notification center | MEDIUM | NO | M |
| FR-NOTIF-05 | Notification preferences per channel | MEDIUM | NO | M |
| FR-NOTIF-06 | Retry logic when provider fails | HIGH | YES | S |
| FR-NOTIF-07 | Template management & localization | MEDIUM | NO | M |

**Notes:**
- MVP: Push (FCM), SMS, basic email
- Phase 2: notification center, preference management, multi-language

### 5.8 Rating & Review Service

| ID | Requirement | Priority | MVP | Effort |
|:---|:-----------|:--------:|:---:|:-------:|
| FR-RATING-01 | Submit rating & review for restaurant | MEDIUM | YES | M |
| FR-RATING-02 | Submit rating & review for driver | MEDIUM | YES | M |
| FR-RATING-03 | Item-level rating | LOW | NO | M |
| FR-RATING-04 | Aggregate rating calculation | MEDIUM | YES | S |
| FR-RATING-05 | Display reviews with pagination | MEDIUM | YES | S |
| FR-RATING-06 | Moderation: flag/hide inappropriate | MEDIUM | NO | M |
| FR-RATING-07 | Restaurant owner reply to reviews | LOW | NO | S |

**Notes:**
- MVP: simple star + comment, basic moderation (filter by admin manual)
- Phase 2: advanced moderation, ML-based inappropriate detection, merchant replies

### 5.9 Coupon & Promotion Service
Các yêu cầu sau do **Promotion Service** phụ trách; Order Service sẽ gọi Promotion Service để validate và áp dụng coupon trong quá trình checkout.


| ID | Requirement | Priority | MVP | Effort |
|:---|:-----------|:--------:|:---:|:-------:|
| FR-COUPON-01 | Create coupon: %, flat, min cart, per-user limit | MEDIUM | YES | M |
| FR-COUPON-02 | Apply coupon at checkout | HIGH | YES | M |
| FR-COUPON-03 | Track coupon usage | MEDIUM | YES | S |
| FR-COUPON-04 | Time-based activation | MEDIUM | YES | S |
| FR-COUPON-05 | Target coupon by restaurant/segment | MEDIUM | NO | M |

**Notes:**
- MVP: basic coupon (no stacking, no segmentation)
- Phase 2: stacking, segment targeting, tiered pricing

### 5.10 Admin & Reporting Service

| ID | Requirement | Priority | MVP | Effort |
|:---|:-----------|:--------:|:---:|:-------:|
| FR-ADMIN-01 | Dashboard: KPIs (orders, revenue, users) | HIGH | YES | L |
| FR-ADMIN-02 | User management: view, suspend | HIGH | YES | M |
| FR-ADMIN-03 | Restaurant onboarding workflow | MEDIUM | YES | L |
| FR-ADMIN-04 | Driver management & performance | MEDIUM | YES | M |
| FR-ADMIN-05 | Payment reconciliation & disputes | MEDIUM | YES | L |
| FR-ADMIN-06 | Reports: revenue, orders, SLA | MEDIUM | YES (basic) | L |
| FR-ADMIN-07 | System configuration | MEDIUM | YES | M |
| FR-ADMIN-08 | Incident logging & SLA metrics | MEDIUM | YES | M |

**Notes:**
- MVP: basic dashboard, manual onboarding, basic reconciliation
- Phase 2: advanced reporting, automation, AI-based insights

---

## 6. NON-FUNCTIONAL REQUIREMENTS

### 6.1 Performance

| NFR-ID | Requirement | Target | Scope |
|:-------|:-----------|:-------:|:-----:|
| NFR-PERF-01 | API response time (p95) | < 500ms | core APIs (order, search, catalog) |
| NFR-PERF-02 | API response time (p99) | < 1s | core APIs |
| NFR-PERF-03 | Search query latency (p95) | < 800ms | search, discovery |
| NFR-PERF-04 | Real-time GPS tracking latency | < 200ms | delivery tracking |
| NFR-PERF-05 | Page load time (FE) | < 3s | web app initial load |
| NFR-PERF-06 | Mobile app load time | < 2s | app startup |

### 6.2 Availability & Reliability

| NFR-ID | Requirement | Target | Scope |
|:-------|:-----------|:-------:|:-----:|
| NFR-AVAIL-01 | Uptime (availability) | 99.5–99.9% | core services (Order, Payment, Delivery) |
| NFR-AVAIL-02 | Error rate (5xx) | < 0.1% | all APIs |
| NFR-AVAIL-03 | Data loss | 0 (RTO=0, RPO=0) | payments, orders |
| NFR-AVAIL-04 | Auto-failover time | < 30s | database, cache, service replicas |
| NFR-AVAIL-05 | Backup frequency | Daily | production database, snapshots |
| NFR-AVAIL-06 | DR test frequency | Quarterly | disaster recovery drills |

### 6.3 Security

| NFR-ID | Requirement | Details |
|:-------|:-----------|:-------:|
| NFR-SEC-01 | Authentication | JWT (HS256), TTL 24h, refresh token pattern |
| NFR-SEC-02 | Authorization | RBAC, row-level security for multi-tenant data |
| NFR-SEC-03 | Encryption in transit | TLS 1.3, HSTS header |
| NFR-SEC-04 | Encryption at rest | AES-256 for PII, payment tokens |
| NFR-SEC-05 | PCI-DSS compliance | No raw card data; tokenization via gateway |
| NFR-SEC-06 | GDPR compliance | Data export, deletion, consent management |
| NFR-SEC-07 | Input validation | Server-side validation, parameterized queries |
| NFR-SEC-08 | Rate limiting | 100 req/min/user, 1000 req/min/IP, 5 login attempts/min |
| NFR-SEC-09 | Audit logging | Log: login, payment, admin action, retention 6+ months |
| NFR-SEC-10 | Vulnerability management | Pentest quarterly, bug bounty program, OWASP Top 10 checks |

### 6.4 Scalability

| NFR-ID | Requirement | Target |
|:-------|:-----------|:-------:|
| NFR-SCALE-01 | Concurrent users | 3k–5k (MVP), 10k+ (Phase 2) |
| NFR-SCALE-02 | Orders per second | 10–20 (MVP), 50+ (Phase 2) |
| NFR-SCALE-03 | DB connections | Connection pooling, max 500 per service |
| NFR-SCALE-04 | Horizontal scaling | ≥ 2 replicas/service, up to 20 with HPA |
| NFR-SCALE-05 | Cache miss rate | < 10% (Redis hit rate > 90%) |
| NFR-SCALE-06 | Data growth | Database sharding if > 1TB (Phase 3) |

### 6.5 Maintainability & Observability

| NFR-ID | Requirement | Details |
|:-------|:-----------|:-------:|
| NFR-OBS-01 | Logging | ELK or Loki, structured logs (JSON), retention 30 days (hot), 1 year (cold) |
| NFR-OBS-02 | Metrics | Prometheus, Grafana dashboards per service |
| NFR-OBS-03 | Tracing | Jaeger/Tempo, trace every request, span sampling if high volume |
| NFR-OBS-04 | Error tracking | Sentry for exceptions, categorization by severity |
| NFR-OBS-05 | APM (optional) | Datadog or New Relic for Phase 2+ |
| NFR-OBS-06 | Code coverage | ≥ 80% unit test coverage, ≥ 60% integration |
| NFR-OBS-07 | Documentation | ADR, API docs (OpenAPI), deployment runbook |

### 6.6 Compatibility

| NFR-ID | Requirement | Details |
|:-------|:-----------|:-------:|
| NFR-COMPAT-01 | Browser support | Chrome, Firefox, Safari, Edge (latest 2 versions) |
| NFR-COMPAT-02 | Mobile OS | iOS 13+, Android 10+ |
| NFR-COMPAT-03 | API versioning | Semantic versioning, backward compat for 2 major versions |
| NFR-COMPAT-04 | Database | PostgreSQL 14+, backward compat to 12 during migration |

---

## 7. SLO/SLI & ERROR BUDGET

### 7.1 Core SLIs & SLOs (per service, monthly basis)

#### SLI-1: Request Success Rate

**Definition:** Tỷ lệ request hoàn thành thành công (2xx/3xx or business-valid error) / tổng request (exclude 5xx errors).

| Service | SLO | Error Budget/Month |
|:--------|:---:|:------------------:|
| Order Service | 99.9% | 43.2 min |
| Payment Service | 99.95% | 21.6 min |
| Delivery Service | 99.9% | 43.2 min |
| Search Service | 99.5% | 216 min |
| API Gateway (aggregate) | 99.9% | 43.2 min |

#### SLI-2: Latency (Response Time)

| Service | p95 Target | p99 Target | SLO |
|:--------|:----------:|:----------:|:----:|
| Order Service | < 500ms | < 1s | 99% of requests p95 < 500ms |
| Payment Service | < 800ms | < 2s | 99% of requests p95 < 800ms |
| Search Service | < 800ms | < 2s | 95% of requests p95 < 800ms |
| Delivery tracking | < 200ms | < 500ms | 99.5% p95 < 200ms |

#### SLI-3: Availability (Uptime)

| Service | SLO | Downtime Budget/Month |
|:--------|:---:|:--------------------:|
| Order Service | 99.9% | 43.2 min |
| Payment Service | 99.95% | 21.6 min |
| Delivery Service | 99.9% | 43.2 min |
| Search Service | 99.5% | 216 min |
| **System overall** | **99.5%** | **216 min** |

#### SLI-4: Data Integrity & Business Correctness

| Metric | Target |
|:-------|:------:|
| Double-charge incidents | 0 per month |
| Payment reconciliation completion | 100% within 24h |
| Order pricing accuracy | ≥ 99.99% correct totals |
| Delivery task assignment success | ≥ 98% (not cancelled before pickup) |

### 7.2 Alert Thresholds & Escalation

| Metric | Threshold | Severity | Action |
|:-------|:---------:|:--------:|:-------:|
| Error rate (5xx) > 0.2% | BREACH | P1 | On-call page immediately |
| p95 latency > 1s | WARNING | P2 | Check DB/cache/downstream |
| Uptime < 99% (per hour) | BREACH | P1 | Escalate |
| Payment success rate < 99% | BREACH | P0 | Liaise with gateway, consider rollback |
| Replication lag > 10s | WARNING | P2 | DBA check |
| Order cancellation rate > 15% | WARNING | P2 | Support review |

---

## 8. SYSTEM ARCHITECTURE

### 8.1 Architecture Overview (C4 Level 2: Containers)

```
┌─────────────────────────────────────────────────────────────────┐
│                       CLIENT LAYER                              │
├─────────────────────────────────────────────────────────────────┤
│ Web (Next.js/React)  │  iOS App (Swift)  │  Android App (Kotlin) │
└──────────────────────┬──────────────────┬──────────────────────┘
                       │                  │
┌──────────────────────┴──────────────────┴──────────────────────┐
│                    API GATEWAY (Nginx/Envoy)                   │
│        - Auth check, rate limiting, routing, logging           │
└──────────────┬──────────────────────────────────────────────────┘
               │
┌──────────────┴──────────────────────────────────────────────────┐
│                   MICROSERVICES LAYER                          │
├──────────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ User Service │ Catalog Service │ Order Service             │ │
│ │              │ (Menu CRUD)     │ (Cart, checkout)          │ │
│ └─────────────────────────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ Payment Service │ Delivery Service │ Search Service        │ │
│ │ (Gateway int.)  │ (Dispatch, GPS)  │ (Geo-search, Redis)  │ │
│ └─────────────────────────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ Promotion Service │ Notification Svc │ Rating Service      │ │
│ │ (Coupon, Campaign)│ (Push, SMS, Email)│                    │ │
│ └─────────────────────────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ Admin Service                                             │ │
│ └─────────────────────────────────────────────────────────────┘ │
└──────────────┬──────────────────────────────────────────────────┘
               │ (REST/gRPC)
┌──────────────┴──────────────────────────────────────────────────┐
│              MESSAGE BROKER & EVENT LAYER                      │
├──────────────────────────────────────────────────────────────────┤
│ Kafka Topics:                                                    │
│  - order.created, order.confirmed, order.ready, order.delivered │
│  - payment.authorized, payment.captured, payment.failed         │
│  - delivery.assigned, delivery.picked_up, delivery.completed    |
|  - promotion.coupon_created, promotion.coupon_updated,          |
|    promotion.coupon_expired                                     │
│  - notification.* (for async notifications)                     │
└──────────────┬──────────────────────────────────────────────────┘
               │
┌──────────────┴──────────────────────────────────────────────────┐
│                    DATA & STORAGE LAYER                         │
├──────────────────────────────────────────────────────────────────┤
│ ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│ │ PostgreSQL   │  │ Redis        │  │ Elasticsearch        │   │
│ │ (primary DB) │  │ (cache,      │  │ (search, discovery)  │   │
│ │              │  │  session)    │  │ [Phase 2+]           │   │
│ └──────────────┘  └──────────────┘  └──────────────────────┘   │
│ ┌──────────────┐                                                 │
│ │ S3/MinIO     │  (images, documents)                            │
│ └──────────────┘                                                 │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│              EXTERNAL INTEGRATIONS                              │
├──────────────────────────────────────────────────────────────────┤
│ Payment Gateway (Stripe/VNPay)  │  Google Maps API             │
│ FCM / APNs (push)               │  SMS Provider (Twilio/local) │
│ Email Service (SendGrid/SES)    │                              │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│           OBSERVABILITY & OPERATIONS                            │
├──────────────────────────────────────────────────────────────────┤
│ Prometheus + Grafana  │  ELK/Loki + Kibana                      │
│ Jaeger/Tempo (tracing) │  Sentry (error tracking)               │
│ Kubernetes (orchestration), Helm (deployment)                   │
└──────────────────────────────────────────────────────────────────┘
```

### 8.2 Bounded Context & Service Responsibility

| Service              | Primary Domain              | Ownership              | Dependencies                                  |
|:---------------------|:---------------------------|:----------------------:|:----------------------------------------------:|
| **User Service**     | Identity, auth, profile    | User, auth            | -                                             |
| **Catalog Service**  | Restaurant, menu           | Restaurant, menu      | User (owner_id)                               |
| **Order Service**    | Order lifecycle, cart      | Order                 | Catalog, User, Payment, Delivery, Promotion   |
| **Payment Service**  | Payment, reconciliation    | Payment, billing      | Order                                         |
| **Delivery Service** | Driver, assignment, tracking | Delivery, logistics | Order, User (driver)                          |
| **Search Service**   | Restaurant search, discovery | Search, discovery    | Catalog (read-model), Promotion (boost promo) |
| **Promotion Service**| Coupons, promotions        | Coupon, campaign      | Order, User, Restaurant                       |
| **Notification Service** | Push, SMS, email      | Notification          | All (event listeners, incl. promotion.*)      |
| **Rating Service**   | Reviews, ratings           | Rating, feedback      | Order, User                                   |
| **Admin Service**    | Admin portal, reporting    | Admin, operations     | All (read-model)                              |


### 8.3 Event-Driven Architecture & Saga Pattern

**Order Placement Saga:**

```
1. Customer initiates checkout
   → Order Service creates order (status: CREATED)
   → Event: OrderCreated published to Kafka
   
2. Payment Service listens to OrderCreated
   → Creates payment session
   → Calls payment gateway for authorization
   → On success → Event: PaymentAuthorized published
   
3. Order Service listens to PaymentAuthorized
   → Updates order status → CONFIRMED
   → Event: OrderConfirmed published
   
4. Restaurant Service listens to OrderConfirmed
   → Notifies restaurant (push, SMS)
   → Waits for restaurant acceptance
   
5. When restaurant accepts
   → Event: OrderAccepted published
   → Order status → PREPARING
   
6. When order ready
   → Event: OrderReadyForPickup published
   
7. Delivery Service listens to OrderReadyForPickup
   → Triggers driver assignment algorithm
   → On driver assigned → Event: DeliveryAssigned published
   
8. Delivery Service updates status → ON_THE_WAY, then DELIVERED
   → Event: DeliveryCompleted published
   
9. On successful delivery
   → Payment Service confirms capture (if pre-authorized)
   → Event: PaymentCaptured published
   
10. Rating Service listens to DeliveryCompleted
    → Prompts customer for rating
```

**Compensating Transactions (on failure):**

- If Payment fails → Order Service cancels order → Event: OrderCancelled → Notification
- If Driver cancels after assignment → Delivery Service reassigns → Event: DriverCancelled → OrderReassigned
- If delivery SLA missed → Order Service auto-cancels → Event: OrderFailedDelivery → Refund payment

---

## 9. DATA MODEL & DATABASE SCHEMA

### 9.1 Entity-Relationship Overview

```
users (CUSTOMER, RESTAURANT_OWNER, DRIVER, ADMIN)
  ├─ user_addresses
  ├─ user_payment_methods
  └─ refresh_tokens

restaurants (owned by RESTAURANT_OWNER)
  ├─ restaurant_opening_hours
  ├─ restaurant_cuisines
  ├─ menu_categories
  │   └─ menu_items
  │       └─ menu_item_variants
  └─ order* (foreign key)

orders
  ├─ order_items
  │   └─ order_item_variants
  ├─ payments (1-to-1)
  │   └─ payment_refunds
  └─ delivery_tasks (1-to-1)
      └─ delivery_task_events

coupons
  └─ coupon_usages

drivers (DRIVER role + user profile)
  └─ delivery_tasks

ratings
  ├─ restaurant_ratings
  └─ driver_ratings

order_events (audit trail)
payment_events (audit trail)
delivery_task_events (audit trail)
```

### 9.2 Key Tables (PostgreSQL Schema)

#### Cities
```sql
CREATE TABLE cities (
    id          BIGSERIAL PRIMARY KEY,
    title       VARCHAR(255) NOT NULL UNIQUE,
    status      VARCHAR(32) NOT NULL DEFAULT 'ACTIVE' 
                CHECK (status IN ('ACTIVE','INACTIVE')),
    created_by  UUID,
    updated_by  UUID,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_cities_status ON cities(status);
```

#### Users
```sql
CREATE TABLE users (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email             VARCHAR(255) UNIQUE,
    phone             VARCHAR(20) UNIQUE,
    password_hash     VARCHAR(255) NOT NULL,
    first_name        VARCHAR(100),
    last_name         VARCHAR(100),
    avatar_url        TEXT,
    role              VARCHAR(32) NOT NULL 
                      CHECK (role IN ('CUSTOMER','RESTAURANT_OWNER','DRIVER','ADMIN')),
    is_active         BOOLEAN NOT NULL DEFAULT TRUE,
    city_id           BIGINT REFERENCES cities(id),
    is_deleted        BOOLEAN NOT NULL DEFAULT FALSE,
    created_by        UUID,
    updated_by        UUID,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email) WHERE is_deleted = FALSE;
CREATE INDEX idx_users_phone ON users(phone) WHERE is_deleted = FALSE;
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_city_id ON users(city_id);
```

#### User Addresses
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

CREATE INDEX idx_user_addresses_user_id ON user_addresses(user_id) WHERE is_deleted = FALSE;
CREATE INDEX idx_user_addresses_location ON user_addresses USING gist(ll_to_earth(lat, lng));
```

#### User Payment Methods
```sql
CREATE TABLE user_payment_methods (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id           UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type              VARCHAR(32) NOT NULL 
                      CHECK (type IN ('CARD','EWALLET','COD')),
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

CREATE INDEX idx_user_payment_methods_user_id ON user_payment_methods(user_id) WHERE is_deleted = FALSE;
```

#### Refresh Tokens
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

CREATE INDEX idx_refresh_tokens_user_id ON refresh_tokens(user_id);
CREATE INDEX idx_refresh_tokens_expires_at ON refresh_tokens(expires_at);
```

#### Restaurants
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
    status              VARCHAR(32) NOT NULL 
                        CHECK (status IN ('PENDING','ACTIVE','INACTIVE','SUSPENDED')),
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

CREATE INDEX idx_restaurants_city_id ON restaurants(city_id) WHERE is_deleted = FALSE AND status = 'ACTIVE';
CREATE INDEX idx_restaurants_location ON restaurants USING gist(ll_to_earth(lat, lng)) WHERE status = 'ACTIVE';
CREATE INDEX idx_restaurants_owner_id ON restaurants(owner_id);
CREATE INDEX idx_restaurants_status ON restaurants(status);
```

#### Menu Categories & Items
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

CREATE INDEX idx_menu_categories_restaurant_id ON menu_categories(restaurant_id) WHERE is_deleted = FALSE;

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

CREATE INDEX idx_menu_items_restaurant_id ON menu_items(restaurant_id) WHERE is_deleted = FALSE;
CREATE INDEX idx_menu_items_category_id ON menu_items(category_id) WHERE is_deleted = FALSE;

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

CREATE INDEX idx_menu_item_variants_item_id ON menu_item_variants(item_id);
```

#### Coupons
> Ghi chú: `coupons` và `coupon_usages` thuộc **Promotion Service**; Order Service chỉ lưu `coupon_code` và `coupon_discount` dạng snapshot trong bảng `orders`.

```sql
CREATE TABLE coupons (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code                    VARCHAR(64) UNIQUE NOT NULL,
    type                    VARCHAR(32) NOT NULL 
                            CHECK (type IN ('PERCENT','FLAT')),
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

CREATE INDEX idx_coupons_code ON coupons(code) WHERE is_active = TRUE AND is_deleted = FALSE;
CREATE INDEX idx_coupons_restaurant_id ON coupons(target_restaurant_id) WHERE is_active = TRUE;
CREATE INDEX idx_coupons_validity ON coupons(start_time, end_time) WHERE is_active = TRUE;

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

CREATE INDEX idx_coupon_usages_coupon_id ON coupon_usages(coupon_id);
CREATE INDEX idx_coupon_usages_user_id ON coupon_usages(user_id);
```

#### Orders (Core)
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
    delivery_type           VARCHAR(16) NOT NULL DEFAULT 'DELIVERY'
                            CHECK (delivery_type IN ('DELIVERY','PICKUP')),
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

CREATE INDEX idx_orders_customer_id ON orders(customer_id) WHERE is_deleted = FALSE;
CREATE INDEX idx_orders_restaurant_id ON orders(restaurant_id) WHERE is_deleted = FALSE;
CREATE INDEX idx_orders_city_id ON orders(city_id) WHERE is_deleted = FALSE;
CREATE INDEX idx_orders_status ON orders(status) WHERE is_deleted = FALSE;
CREATE INDEX idx_orders_created_at ON orders(created_at DESC) WHERE is_deleted = FALSE;
CREATE INDEX idx_orders_payment_status ON orders(payment_status) WHERE is_deleted = FALSE;
```

#### Order Items
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

CREATE INDEX idx_order_items_order_id ON order_items(order_id);

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

CREATE INDEX idx_order_item_variants_order_item_id ON order_item_variants(order_item_id);
```

#### Payments
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

CREATE INDEX idx_payments_order_id ON payments(order_id);
CREATE INDEX idx_payments_status ON payments(status) WHERE is_deleted = FALSE;
CREATE INDEX idx_payments_idempotency_key ON payments(idempotency_key) WHERE is_deleted = FALSE;

CREATE TABLE payment_refunds (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    payment_id      UUID NOT NULL REFERENCES payments(id),
    amount          NUMERIC(12,2) NOT NULL,
    reason          TEXT,
    created_by      UUID,
    updated_by      UUID,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_payment_refunds_payment_id ON payment_refunds(payment_id);
```

#### Drivers & Delivery
```sql
CREATE TYPE driver_status_enum AS ENUM ('PENDING','APPROVED','REJECTED','SUSPENDED');

CREATE TYPE delivery_task_status_enum AS ENUM (
    'CREATED','ASSIGNED','PICKED_UP','IN_TRANSIT','DELIVERED','CANCELLED'
);

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
    city_id         BIGINT REFERENCES cities(id),
    is_deleted      BOOLEAN NOT NULL DEFAULT FALSE,
    created_by      UUID,
    updated_by      UUID,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_drivers_user_id ON drivers(user_id);
CREATE INDEX idx_drivers_status ON drivers(status) WHERE is_deleted = FALSE;
CREATE INDEX idx_drivers_city_id ON drivers(city_id) WHERE status = 'APPROVED';

CREATE TABLE delivery_tasks (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id            UUID NOT NULL UNIQUE REFERENCES orders(id),
    driver_id           UUID REFERENCES drivers(id),
    status              delivery_task_status_enum NOT NULL DEFAULT 'CREATED',
    pickup_location_snapshot JSONB NOT NULL,  -- {address, lat, lng, contact}
    dropoff_location_snapshot JSONB NOT NULL, -- {address, lat, lng, contact}
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

CREATE INDEX idx_delivery_tasks_order_id ON delivery_tasks(order_id);
CREATE INDEX idx_delivery_tasks_driver_id ON delivery_tasks(driver_id) WHERE status IN ('ASSIGNED', 'PICKED_UP', 'IN_TRANSIT');
CREATE INDEX idx_delivery_tasks_status ON delivery_tasks(status) WHERE is_deleted = FALSE;
CREATE INDEX idx_delivery_tasks_location ON delivery_tasks USING gist(ll_to_earth(current_lat, current_lng));

CREATE TABLE delivery_task_events (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    delivery_task_id    UUID NOT NULL REFERENCES delivery_tasks(id) ON DELETE CASCADE,
    event_type          VARCHAR(32) NOT NULL,  -- ASSIGNED, PICKED_UP, IN_TRANSIT, DELIVERED, CANCELLED
    event_data          JSONB,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_delivery_task_events_task_id ON delivery_task_events(delivery_task_id);
CREATE INDEX idx_delivery_task_events_created_at ON delivery_task_events(created_at DESC);
```

#### Ratings
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

CREATE INDEX idx_ratings_order_id ON ratings(order_id);
CREATE INDEX idx_ratings_rater_id ON ratings(rater_id);
CREATE INDEX idx_ratings_ratee_id ON ratings(ratee_id) WHERE rating_type = 'RESTAURANT';
CREATE INDEX idx_ratings_created_at ON ratings(created_at DESC);
```

#### Audit Trail (Events)
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

CREATE INDEX idx_order_events_order_id ON order_events(order_id);
CREATE INDEX idx_order_events_created_at ON order_events(created_at DESC);
```

### 9.3 Indexing Strategy

**High-traffic queries (MVP):**
- Search restaurants by city + location: `idx_restaurants_location`, `idx_restaurants_city_id`
- Fetch user orders: `idx_orders_customer_id` + `idx_orders_created_at`
- Fetch restaurant orders: `idx_orders_restaurant_id` + `idx_orders_status`
- Fetch active delivery tasks: `idx_delivery_tasks_driver_id` + `idx_delivery_tasks_status`
- Coupon validation: `idx_coupons_code`, `idx_coupons_validity`

**Secondary queries:**
- User address geo-search: `idx_user_addresses_location`
- Driver location tracking: `idx_delivery_tasks_location`
- Payment reconciliation: `idx_payments_status`

---

## 10. API CONTRACTS

*(Reduced for brevity, but includes core endpoints)*

### 10.1 User Service APIs

```http
POST   /api/v1/auth/register
{
  "email": "customer@example.com",
  "phone": "+84123456789",
  "password": "hashedOrSentSecurely",
  "first_name": "John",
  "last_name": "Doe",
  "role": "CUSTOMER"
}
→ Response: { user_id, email, phone, role, created_at }

POST   /api/v1/auth/login
{ "email": "...", "password": "..." }
→ Response: { access_token (JWT 24h), refresh_token, user }

POST   /api/v1/auth/refresh
{ "refresh_token": "..." }
→ Response: { access_token (new), refresh_token (rotated) }

GET    /api/v1/users/profile
→ Response: { user_id, email, phone, first_name, avatar_url, role }

PUT    /api/v1/users/profile
{ "first_name": "...", "avatar_url": "..." }
→ Response: { updated user }

POST   /api/v1/users/addresses
{ "label": "Home", "street": "...", "lat": 10.8, "lng": 106.7, "is_default": true }
→ Response: { address_id, ... }

GET    /api/v1/users/addresses
→ Response: { addresses: [...] }

PUT    /api/v1/users/addresses/{id}
{ "label": "Office", "is_default": true }
→ Response: { updated address }

DELETE /api/v1/users/addresses/{id}
→ Response: { success: true }
```

### 10.2 Catalog Service APIs

```http
GET    /api/v1/restaurants?lat=10.8&lng=106.7&keyword=pizza
?city_id=1&distance_km=5&rating_min=3.5&sort=distance
→ Response: {
  restaurants: [
    {
      id, name, description, lat, lng, rating, total_reviews,
      is_accepting_orders, min_order_value, est_delivery_time
    }
  ],
  total, page, page_size
}

GET    /api/v1/restaurants/{id}
→ Response: {
  id, name, description, street, lat, lng, rating, cuisines[],
  opening_hours[],  is_accepting_orders, menu_categories[]
}

GET    /api/v1/restaurants/{id}/menu
→ Response: {
  menu_categories: [
    {
      id, name, items: [
        { id, name, price, image_url, variants: [...] }
      ]
    }
  ]
}

POST   /api/v1/restaurants (for restaurant owner)
{ name, description, street, lat, lng, service_radius_km, cuisines[] }
→ Response: { restaurant_id, status: 'PENDING' }

PUT    /api/v1/restaurants/{id} (for restaurant owner)
{ name, description, opening_hours[] }
→ Response: { updated restaurant }

POST   /api/v1/restaurants/{id}/menu (for restaurant owner)
{ name, description, price, category_id, variants[] }
→ Response: { menu_item_id }

PUT    /api/v1/menu-items/{id} (for restaurant owner)
{ name, price, is_available, image_url }
→ Response: { updated menu_item }

DELETE /api/v1/menu-items/{id}
→ Response: { success: true }

PUT    /api/v1/restaurants/{id}/status (for restaurant owner)
{ is_accepting_orders: true/false }
→ Response: { success: true }
```

### 10.3 Order Service APIs

```http
POST   /api/v1/orders (create order)
{
  restaurant_id: UUID,
  delivery_address_id: UUID,
  items: [
    { menu_item_id, quantity, selected_variants: [...] }
  ],
  coupon_code?: "SAVE10",
  notes?: "No spicy",
  delivery_type: "DELIVERY"
}
→ Response: {
  order_id, customer_id, restaurant_id, status: 'CREATED',
  items, subtotal, coupon_discount, tax, delivery_fee, total_price,
  payment_method_id, estimated_delivery_time
}

GET    /api/v1/orders/{id}
→ Response: { full order details }

GET    /api/v1/orders?customer_id=...&status=DELIVERED&limit=10
→ Response: { orders: [...], total, page, page_size }

PUT    /api/v1/orders/{id}/cancel
{ reason: "Changed my mind" }
→ Response: {
  order_id, status: 'CANCELLED', refund_amount,
  refund_reason, refund_initiated_at
}

GET    /api/v1/restaurants/{id}/orders (for restaurant owner)
?status=CONFIRMED&limit=20
→ Response: { orders: [...] }

PUT    /api/v1/restaurants/{id}/orders/{oid}/status (for restaurant owner)
{ status: 'PREPARING' | 'READY_FOR_PICKUP' | 'CANCELLED_BY_RESTAURANT' }
→ Response: { order_id, status, reason }

POST   /api/v1/orders/{id}/reorder (quick reorder)
{ delivery_address_id?: UUID }
→ Response: { new_order_id, items (same as previous), total }
```

### 10.4 Payment Service APIs

```http
POST   /api/v1/payments/authorize
{
  order_id: UUID,
  payment_method_id: UUID,
  amount: 150000,
  currency: "VND",
  idempotency_key: "hash(...)"
}
→ Response: {
  payment_id, order_id, status: 'AUTHORIZED',
  gateway_transaction_id, authorized_at
}

POST   /api/v1/payments/{id}/capture
{ idempotency_key: "same as auth" }
→ Response: {
  payment_id, status: 'CAPTURED', captured_at
}

POST   /api/v1/payments/{id}/refund
{ amount: 150000, reason: "Order cancelled" }
→ Response: {
  refund_id, payment_id, amount, reason, status: 'PENDING'
}

POST   /api/v1/webhooks/payment (from gateway)
{
  gateway_transaction_id, status, timestamp, signature
}
→ Response: { received: true }
```

### 10.5 Delivery Service APIs

```http
POST   /api/v1/drivers/register
{
  user_id: UUID,
  vehicle_type: "BIKE",
  vehicle_plate: "ABC123",
  license_number: "DL123456",
  document_urls: { front_id: "url", back_id: "url" }
}
→ Response: { driver_id, user_id, status: 'PENDING' }

PUT    /api/v1/drivers/{id}/status
{ is_online: true/false }
→ Response: { driver_id, is_online, current_location, available_tasks_count }

POST   /api/v1/delivery-tasks (for dispatch system)
{
  order_id: UUID,
  pickup_location: { lat, lng, address, contact },
  dropoff_location: { lat, lng, address, contact },
  est_delivery_time: "ISO8601"
}
→ Response: { delivery_task_id, order_id, status: 'CREATED' }

GET    /api/v1/delivery-tasks?driver_id=...&status=ASSIGNED
→ Response: { delivery_tasks: [...] }

PUT    /api/v1/delivery-tasks/{id}/status
{ status: 'ASSIGNED' | 'PICKED_UP' | 'IN_TRANSIT' | 'DELIVERED' | 'CANCELLED' }
→ Response: { delivery_task_id, status, updated_at }

PUT    /api/v1/drivers/{id}/location
{ lat: 10.81, lng: 106.71, timestamp: "ISO8601" }
→ Response: { driver_id, current_location, updated_at }

GET    /api/v1/drivers/{id}/earnings
?from_date=2026-01-01&to_date=2026-01-31
→ Response: {
  total_earnings: 5000000,  // VND
  total_trips: 50,
  breakdown: [
    { date, earnings, trips, avg_rating }
  ]
}
```

### 10.6 Search Service APIs

```http
GET    /api/v1/search
?q=pizza&lat=10.8&lng=106.7&distance_km=3
&sort=distance&page=1&page_size=10
→ Response: {
  restaurants: [
    {
      id, name, rating, distance_km,
      min_order, est_delivery_time, is_open
    }
  ],
  total, page, page_size
}

GET    /api/v1/discovery?city_id=1
→ Response: {
  featured: [...],
  trending: [...],
  promotions: [...]
}
```

### 10.7 Notification Service APIs

```http
GET    /api/v1/notifications
?user_id=...&limit=20&offset=0
→ Response: {
  notifications: [
    { id, type, title, message, read, created_at }
  ],
  total
}

PUT    /api/v1/notifications/{id}/read
→ Response: { success: true }

GET    /api/v1/notification-preferences
?user_id=...
→ Response: {
  preferences: [
    { channel: "PUSH", type: "ORDER_STATUS", enabled: true },
    { channel: "SMS", type: "PROMO", enabled: false }
  ]
}

PUT    /api/v1/notification-preferences
{
  preferences: [
    { channel: "PUSH", type: "ORDER_STATUS", enabled: true }
  ]
}
→ Response: { success: true }
```

### 10.8 Rating Service APIs

```http
POST   /api/v1/restaurants/{id}/ratings
{
  order_id: UUID,
  score: 5,
  comment: "Great food and fast delivery!",
  rating_type: "RESTAURANT"
}
→ Response: { rating_id, order_id, score, comment, created_at }

GET    /api/v1/restaurants/{id}/ratings
?limit=10&page=1
→ Response: {
  ratings: [
    { rating_id, rater_id, score, comment, created_at }
  ],
  total, average_score
}

POST   /api/v1/drivers/{id}/ratings
{
  order_id: UUID,
  score: 4,
  comment: "Driver was friendly",
  rating_type: "DRIVER"
}
→ Response: { rating_id, ... }
```

### 10.9 Admin Service APIs

```http
GET    /api/v1/admin/dashboard
?city_id=1&from_date=2026-01-01&to_date=2026-01-31
→ Response: {
  metrics: {
    total_orders: 5000,
    total_revenue: 1500000000,  // VND
    active_users: 50000,
    average_order_value: 300000,
    on_time_delivery_rate: 0.95,
    avg_rating: 4.6
  }
}

GET    /api/v1/admin/users?role=RESTAURANT_OWNER&limit=20
→ Response: { users: [...], total, page }

PUT    /api/v1/admin/users/{id}/suspend
{ reason: "Violation of terms", duration_days: 30 }
→ Response: { user_id, status: 'SUSPENDED', suspended_until }

GET    /api/v1/admin/restaurants?status=PENDING&limit=20
→ Response: { restaurants: [...] }

PUT    /api/v1/admin/restaurants/{id}/approve
{ notes: "KYC verified" }
→ Response: { restaurant_id, status: 'ACTIVE' }

PUT    /api/v1/admin/restaurants/{id}/reject
{ reason: "Invalid documents" }
→ Response: { restaurant_id, status: 'REJECTED' }

GET    /api/v1/admin/payments/reconciliation
?date=2026-01-20
→ Response: {
  reconciled: 450,
  pending: 5,
  discrepancies: [
    { payment_id, expected_amount, actual_amount, status }
  ]
}

GET    /api/v1/admin/reports/revenue
?city_id=1&granularity=daily&from_date=2026-01-01&to_date=2026-01-31
→ Response: {
  data: [
    { date, revenue, orders, avg_order_value, top_restaurants }
  ]
}
```

---

## 11. TESTING STRATEGY

### 11.1 Test Pyramid & Coverage

```
          / \
         /   \
        /  E2E \       5–10% (Playwright)
       /_________\
      /           \
     / Integration \ 20–30% (Docker + testify)
    /_______________\
   /                 \
  / Unit Tests (80%) /
 /___________________\
```

**Target Coverage:**
- Unit: ≥ 80% business logic
- Integration: ≥ 60% core workflows (Order→Payment→Delivery)
- E2E: ≥ 40% critical journeys (signup, search, order, track, rate)

### 11.2 Test Levels

| Level | Tool | Focus | Examples |
|:------|:----:|:-----:|:--------:|
| Unit | Go testing, testify | Business logic, domain models | Order calculation, coupon validation, driver assignment |
| Integration | Docker Compose + testify | Service + real DB/Redis/Kafka | Order creation + payment + delivery task |
| Contract | Pact | API agreements between services | Order Service → Payment Service |
| E2E | Playwright | Full user journey via UI | Customer registers → searches → orders → tracks → rates |
| Load | k6 | SLO validation, spike handling | 500 concurrent orders/min for 10 min |
| Security | OWASP ZAP, manual | Vulnerabilities, injection, auth bypass | SQL injection, XSS, CSRF, rate limiting |

### 11.3 Test Scenarios (MVP Focus)

**MVP Critical Paths:**
1. **Customer Order Flow** → register → search → order → pay → track → rate
2. **Restaurant Accept** → receive order notification → accept → prepare → mark ready
3. **Driver Delivery** → online → receive task → pick up → deliver → confirm
4. **Refund on Cancellation** → cancel order → refund processed → payment reversed
5. **Payment Failure Recovery** → payment fails → retry → success

**Load Test (k6):**
```javascript
// Place 500 orders in 1 minute (spike scenario)
// Measure: p95 latency < 500ms, error rate < 0.1%
```

---

## 12. SECURITY REQUIREMENTS

### 12.1 Authentication & Authorization

- **JWT:** HS256, TTL 24h, include user_id, role, city_id in payload
- **Refresh Token:** Rotate on use, stored in secure HTTP-only cookie
- **MFA (Phase 2):** OTP via SMS/email for sensitive operations
- **RBAC:** Enforce role checks on API endpoints; row-level filters on sensitive queries

### 12.2 Data Protection

- **TLS 1.3** for all traffic (in-flight)
- **AES-256** encryption for PII (at-rest in DB)
- **PCI-DSS:** Never store raw card data; use payment gateway tokenization
- **GDPR:** Data export, deletion, consent management per user request

### 12.3 Input Validation & Injection Prevention

- **Server-side validation** for all inputs; never trust client
- **Parameterized queries** (sqlc, prepared statements)
- **Sanitization:** Escape HTML in user-generated content (reviews, notes)
- **Rate limiting:** 100 req/min/user, 1000 req/min/IP, 5 login/min/IP

### 12.4 Audit & Compliance

- **Audit logging:** All sensitive ops (login, payment, admin action), retention ≥ 6 months
- **Incident response:** RCA ≤ 24h, post-mortem ≤ 1 week
- **Vulnerability management:** Quarterly pentest, bug bounty program, OWASP Top 10 compliance

---

## 13. DEPLOYMENT & OPERATIONS

### 13.1 Infrastructure (Kubernetes)

- **Service mesh (optional):** Istio for canary, circuit breaker
- **Ingress:** Nginx or Envoy for API gateway
- **Pod management:** 2–5 replicas per service, HPA (CPU-based, request-rate-based)
- **StatefulSets:** PostgreSQL (single master + read replicas), Redis

### 13.2 Deployment Strategy

- **Blue-Green or Canary:** Route % traffic to new version; auto-rollback if SLO breached
- **Image registry:** Docker Hub or ECR
- **GitOps:** ArgoCD syncs Kubernetes manifests from Git

### 13.3 Monitoring & Alerting

- **On-call rotation:** Weekly, 24/7 on-call for P0/P1 incidents
- **Alert escalation:** Slack → SMS → phone call (P0)
- **Incident response:** War room within 15 min for P0

---

## 14. ROADMAP & PHASE PLANNING

### Phase 1 (MVP) – 3–4 months
- User auth, profile, addresses
- Restaurant menu management, onboarding simple
- Order placement, cart, simple checkout
- Payment: COD + 1 gateway
- Delivery: simple assignment, GPS tracking
- Notifications: push, SMS basic
- Admin: dashboard, user management
- Search: geo-search + basic filter (no Elasticsearch)
- Deploy single city (HCM)

### Phase 2 – Months 5–8
- Elasticsearch integration, advanced search, discovery, ranking
- Personalized recommendations
- Advanced promotion: segment targeting, multi-method payment
- Multi-city expansion (Hà Nội, Biên Hòa)
- Driver analytics, loyalty points
- Service mesh (Istio), advanced tracing

### Phase 3 – Months 12+
- Grocery/Pharmacy vertical
- B2B ordering (corporate)
- White-label solution
- Route optimization
- Advanced SLA automation
- Real-time inventory sync

---

## 15. RISK & MITIGATION

| Risk | Likelihood | Impact | Mitigation |
|:-----|:----------:|:------:|:----------:|
| Payment gateway downtime | Medium | Critical | Multiple gateways, fallback COD, circuit breaker |
| DB corruption | Low | Critical | Daily backups, DR test quarterly, point-in-time recovery |
| Double-charge | Low | High | Idempotency key, outbox pattern, daily reconciliation |
| Traffic spike (promotion) | Medium | High | Load test, auto-scale, queue checkout during spike |
| Driver shortage | High | High | Incentive, surge pricing, partner with logistics |
| Security breach | Low | Critical | Pentest quarterly, bug bounty, strict RBAC, audit logs |
| Regulatory change | Medium | Medium | Legal review, feature flags for compliance, versioning |

---

## 16. KPIs & SUCCESS METRICS

### 16.1 Technical KPIs

| KPI | Target |
|:----|:------:|
| Uptime | ≥ 99.5% (MVP), ≥ 99.9% (Phase 2+) |
| p95 API latency | < 500ms (core APIs) |
| Error rate (5xx) | < 0.1% |
| Payment success rate | > 99.9% |
| Unit test coverage | ≥ 80% |
| Integration test coverage | ≥ 60% |
| Mean Time to Recovery (MTTR) | < 30 min for P1 |
| Deployment frequency | 1–2x per week |

### 16.2 Business KPIs

| KPI | Target (Year 1) |
|:----|:---------------:|
| DAU (Daily Active Users) | 50k–100k (MVP end) |
| MAU (Monthly Active Users) | 200k–300k |
| GMV (Gross Merchandise Value) | 500M–1B VND/month |
| AOV (Average Order Value) | 300k VND |
| Customer acquisition cost (CAC) | < 50k VND |
| Retention (Day 30) | ≥ 40% |
| On-time delivery rate | ≥ 95% |
| NPS (Net Promoter Score) | > 50 |
| Restaurant sign-up rate | 100+/month |

---

## APPENDIX: Requirement Traceability Matrix (RTM)

| Business Objective | Epic | User Story | FR-ID | NFR-ID | SLO-ID | Test Scenario |
|:--|:--|:--|:--|:--|:--|:--|
| Fast order placement | Order Management | Customer searches restaurant | FR-SEARCH-01 | NFR-PERF-01 | SLI-2 | Search returns <500ms |
| | | Customer adds items to cart | FR-ORD-02 | NFR-PERF-01 | - | Cart update instant |
| | | Customer applies coupon | FR-COUPON-02 | - | - | Coupon validation correct |
| | | Customer checkout & pays | FR-PAY-02,04 | NFR-SEC-05 | SLI-1,4 | Payment idempotent, no double-charge |
| Reliable delivery | Delivery Mgmt | Driver accepts delivery task | FR-DEL-04 | - | - | Assignment within 2 min |
| | | Customer tracks order realtime | FR-DEL-06 | NFR-PERF-04 | SLI-2 | GPS update <200ms p95 |
| | | Delivery completed on-time | FR-DEL-09 | - | SLI-4 | ≥95% on-time |
| Data integrity | Payment & Ops | Payment processing | FR-PAY-01,07,08 | NFR-SEC-02,05 | SLI-4 | 0 double-charge, 100% reconcile |
| | | Refund on cancellation | FR-ORD-07, FR-PAY-06 | NFR-AVAIL-03 | - | Refund <24h |

---

## END OF SRS v2.0

**Document Status:** Ready for Development Team Review

**Next Steps:**
1. Team review & sign-off (1 week)
2. Kick-off with dev & QA teams (week 1–2 of sprint)
3. Database schema finalization & migration scripts (week 1)
4. API contract testing setup (week 2)
5. Unit test templates & coverage framework (week 1)
6. E2E test scaffold (week 2–3)
7. Sprint planning & task breakdown (week 2)

**Contact:** [BA Name] | [Email] | [Phone]

## Bảng phân chia công việc
| Mục                                                 | Hạng mục công việc                                                                        | Phụ trách chính                        |
| --------------------------------------------------- | ----------------------------------------------------------------------------------------- | -------------------------------------- |
| 1. Executive Summary                                |                                                                                           | BA                                     |
| 1.1                                                 | Project Overview                                                                          | BA                                     |
| 1.2                                                 | Business Objectives                                                                       | BA                                     |
| 1.3                                                 | Target Market & Scale                                                                     | BA                                     |
| 2. Business Requirements & Objectives               |                                                                                           | BA                                     |
| 2.1                                                 | Capability Map (theo role)                                                                | BA                                     |
| 2.2                                                 | User Roles & Primary Use Cases (Customer / Restaurant / Driver / Admin)                   | BA                                     |
| 2.3                                                 | Business Process Flows (Place Order, Cancel, Dispute…)                                    | BA                                     |
| 3. Scope Definition: MVP vs Phase 2+                |                                                                                           | Both                                   |
| 3.1                                                 | MVP (Phase 1) – BA (value/KPI) + SA (feasibility)                                         | Both                                   |
| 3.2                                                 | Phase 2 – Scale & Personalization                                                         | Both                                   |
| 3.3                                                 | Phase 3+ – Expansion                                                                      | Both                                   |
| 4. Business Rules                                   |                                                                                           | Both                                   |
| 4.1                                                 | Pricing & Fee Rules                                                                       | BA, review bởi SA                      |
| 4.2                                                 | Coupon & Promotion Rules                                                                  | BA, review SA                          |
| 4.3                                                 | Cancellation & Refund Policy                                                              | BA                                     |
| 4.4                                                 | Payment & Reconciliation Rules                                                            | Both                                   |
| 4.5                                                 | Order Lifecycle & State Machine                                                           | Both                                   |
| 4.6                                                 | Driver Assignment & SLA                                                                   | Both                                   |
| 4.7                                                 | Restaurant Onboarding & Suspension                                                        | BA                                     |
| 5. Functional Requirements (FR)                     |                                                                                           | BA (Priority/MVP) / SA (Effort) → Both |
| 5.1                                                 | User Service                                                                              | BA                                     |
| 5.2                                                 | Catalog Service                                                                           | BA                                     |
| 5.3                                                 | Order Service                                                                             | BA                                     |
| 5.4                                                 | Payment Service                                                                           | BA                                     |
| 5.5                                                 | Delivery Service                                                                          | BA                                     |
| 5.6                                                 | Search & Discovery                                                                        | BA                                     |
| 5.7                                                 | Notification                                                                              | BA                                     |
| 5.8                                                 | Rating & Review                                                                           | BA                                     |
| 5.9                                                 | Coupon & Promotion                                                                        | BA                                     |
| 5.10                                                | Admin & Reporting                                                                         | BA                                     |
| 6. Non-Functional Requirements (NFR)                |                                                                                           | Both                                   |
| 6.1                                                 | Performance                                                                               | SA (target kỹ thuật) + input từ BA     |
| 6.2                                                 | Availability & Reliability                                                                | SA                                     |
| 6.3                                                 | Security (high-level)                                                                     | Both                                   |
| 6.4                                                 | Scalability                                                                               | SA                                     |
| 6.5                                                 | Maintainability & Observability                                                           | SA                                     |
| 6.6                                                 | Compatibility                                                                             | SA                                     |
| 7. SLO/SLI & Error Budget                           |                                                                                           | SA (lead, BA góp ý business metric)    |
| 7.1                                                 | Core SLIs & SLOs per service                                                              | SA                                     |
| 7.2                                                 | Alert Thresholds & Escalation                                                             | Both                                   |
| 8. System Architecture                              |                                                                                           | SA                                     |
| 8.1                                                 | Architecture Overview (C4 Level 2)                                                        | SA                                     |
| 8.2                                                 | Bounded Context & Service Responsibility                                                  | SA                                     |
| 8.3                                                 | Event-Driven Architecture & Saga Pattern                                                  | SA                                     |
| 9. Data Model & Database Schema                     |                                                                                           | Both                                   |
| 9.1                                                 | ER Overview                                                                               | Both                                   |
| 9.2                                                 | Key Tables & Schema (PostgreSQL)                                                          | SA                                     |
| 9.3                                                 | Indexing Strategy                                                                         | SA                                     |
| 10. API Contracts                                   |                                                                                           | Both                                   |
| 10.x                                                | User / Catalog / Order / Payment / Delivery / Search / Notification / Rating / Admin APIs | SA (lead), BA review                   |
| 11. Testing Strategy                                |                                                                                           | Both                                   |
| 11.1                                                | Test Pyramid & Coverage                                                                   | SA                                     |
| 11.2                                                | Test Levels & Tools                                                                       | SA                                     |
| 11.3                                                | Business/UAT Critical Journeys                                                            | BA                                     |
| 12. Security Requirements                           |                                                                                           | SA (lead)                              |
| 12.1                                                | Auth & Authz (JWT, RBAC, MFA)                                                             | SA                                     |
| 12.2                                                | Data Protection (TLS, encryption, PCI)                                                    | SA                                     |
| 12.3                                                | Input Validation & Rate Limiting                                                          | SA                                     |
| 12.4                                                | Audit & Compliance (log hành vi, retention)                                               | Both                                   |
| 13. Deployment & Operations                         |                                                                                           | SA                                     |
| 13.1                                                | Infra (Kubernetes, CI/CD)                                                                 | SA                                     |
| 13.2                                                | Deployment Strategy (blue-green, canary)                                                  | SA                                     |
| 13.3                                                | Monitoring & Alerting (tooling, on-call)                                                  | SA                                     |
| 14. Roadmap & Phase Planning                        |                                                                                           | Both (BA lead)                         |
| 14.x                                                | Phase 1 (MVP), Phase 2, Phase 3+                                                          | Both                                   |
| 15. Risk & Mitigation                               |                                                                                           | Both (BA lead)                         |
| 15.1                                                | Risk business (driver shortage, promotion spike)                                          | BA                                     |
| 15.2                                                | Risk technical (DB corruption, security breach)                                           | SA                                     |
| 16. KPIs & Success Metrics                          |                                                                                           | Both                                   |
| 16.1                                                | Technical KPIs (latency, uptime, error rate, coverage)                                    | SA                                     |
| 16.2                                                | Business KPIs (DAU, MAU, GMV, AOV, retention, on-time delivery, NPS)                      | BA                                     |
| 17. Appendix: RTM (Requirement Traceability Matrix) |                                                                                           | Both (BA lead)                         |
| 17.x                                                | Mapping Business Objective → Epic → FR → NFR → SLO → Test                                 | Both                                   |