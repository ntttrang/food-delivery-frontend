# Product Requirements Document (PRD)
## Food Delivery Platform

**Version:** 2.0  
**Date:** 21 January 2026  
**Location:** Ho Chi Minh City, Vietnam  
**Status:** Ready for Product Development  
**Related Documents:** BRD_FoodDelivery.md, SRS_FoodDelivery.md

---

## TABLE OF CONTENTS

1. [Overview](#1-overview)
   - 1.1 Product Definition
   - 1.2 Product Positioning
   - 1.3 Market Sizing
   - 1.4 Customer Personas
   - 1.5 Product Goals
2. [Product Vision & Strategy](#2-product-vision--strategy)
3. [User Stories & Epics](#3-user-stories--epics)
   - 3.1-3.7 Core Epics (Search, Order, Tracking, Rating, Restaurant, Driver, Admin)
   - 3.8 Order Cancellation & Dispute
   - 3.9 Quick Reorder
4. [Feature Specifications (MVP)](#4-feature-specifications-mvp)
5. [User Flows & Wireframes](#5-user-flows--wireframes-description)
   - 5.1-5.3 Happy Paths (Customer, Restaurant, Driver)
   - 5.4 Exception Flows
6. [Business Rules](#6-business-rules)
7. [Product Roadmap](#7-product-roadmap)
8. [Success Metrics & Analytics](#8-success-metrics--analytics)
9. [Risk Analysis & Mitigation](#9-risk-analysis--mitigation)
10. [Constraints & Dependencies](#10-constraints--dependencies)

---

## 1. OVERVIEW

### 1.1 Product Definition

Food Delivery Platform là một nền tảng SaaS kết nối ba nhóm người dùng chính:
- **Customers:** Đặt hàng ăn trực tuyến
- **Restaurants:** Bán hàng qua nền tảng
- **Drivers:** Giao hàng

Nền tảng cung cấp real-time tracking, payment gateway integration, và analytics cho các bên liên quan.

### 1.2 Product Positioning

- **Target Market:** Urban customers (TP.HCM), age 18-45, có smartphone, regular food delivery users
- **Differentiation:** Fast UX, reliable delivery (on-time > 95%), competitive pricing, diverse restaurant selection
- **Competition:** Grab, Now, Baemin, Loship (direct), Lazada Food, Shopee Food (indirect)

### 1.3 Market Sizing (TP.HCM)

| Metric | Value |
|:---|:---|
| **TAM (Total Addressable Market)** | ~15M người dùng tiềm năng (VN) |
| **SAM (Serviceable Available Market)** | ~3M người dùng urban, có smartphone (TP.HCM) |
| **SOM (Year 1)** | 50k-100k active users = 1-2% market penetration |

**Market Characteristics:**
- Dân số TP.HCM: 9M+
- Smartphone penetration: 70%+
- Food delivery adoption: Tăng 40% YoY
- Urban density cao: Q1, Q3, Q7, Bình Thạnh, Thủ Đức

### 1.4 Customer Personas

| Persona | Age | Order Time | AOV | Frequency | Key Needs |
|:--------|:----|:-----------|:----|:----------|:----------|
| **Office Worker** | 25-35 | Lunch (11-13h) | 80-120k | 3-5x/week | Speed, variety, easy payment |
| **Young Family** | 28-40 | Dinner (18-20h) | 200-400k | 2-3x/week | Family meals, promotions, quality |
| **Student** | 18-24 | Late night (20-23h) | 50-80k | 1-2x/week | Budget-friendly, fast delivery |
| **Busy Professional** | 30-45 | Varied | 150-250k | 4-5x/week | Reliability, premium options |

### 1.5 Product Goals (Year 1)

| Goal | Success Metric |
|:---|:---|
| Capture market share | 50k-100k active customers by end Year 1 |
| High user engagement | ≥25% repeat order rate |
| Reliable service | ≥95% on-time delivery |
| Sustainable unit economics | CAC < 50k VND, AOV 300k VND |
| Platform reliability | 99.5% uptime, <500ms API latency |
| Customer retention | Churn rate < 5%/month |
| Customer satisfaction | NPS > 50 |
| Sustainable growth | LTV:CAC ratio ≥ 10:1 |

---

## 2. PRODUCT VISION & STRATEGY

### 2.1 Long-term Vision

> "Become the most convenient, reliable, and affordable food delivery platform in Southeast Asia."

### 2.2 Product Strategy

**MVP Focus (Phase 1 - Months 1-4):**
- Single city launch (TP.HCM)
- Core user journeys: search → order → pay → track → rate
- Basic features, high reliability, great UX
- Target: 50k-100k customers, break-even on unit economics

**Growth Phase (Phase 2 - Months 5-8):**
- Multi-city expansion
- Advanced features (personalization, recommendations, loyalty)
- 300k-500k customers, revenue scale

**Scale Phase (Phase 3+):**
- Multi-vertical platform (grocery, pharmacy, B2B)
- 1M+ customers, 5k+ restaurants
- Profitability target

---

## 3. USER STORIES & EPICS

### 3.1 Epic: Customer Order Management

**EP-CUS-01: Search & Browse Restaurants**

```
US-CUS-01.1: As a customer, I want to search for restaurants by location 
so that I can find nearby options quickly.

Acceptance Criteria:
- Search returns restaurants within 5km radius (default)
- Results sorted by distance + rating
- Display: name, rating, distance, est delivery time, min order
- Geo-location permission request on first use
- Cache results for 5 minutes

MVP: ✓ Geo-based search only
Phase 2: + Full-text search (restaurant name, cuisine type)
```

**US-CUS-01.2: Filter & Sort Restaurants**

```
As a customer, I want to filter restaurants (open status, rating, cuisine type)
so that I can refine my search quickly.

Acceptance Criteria:
- Filter options: Open now, Rating (4+/5+), Cuisine type
- Sort by: Distance, Rating, Delivery time, Popularity
- Apply multiple filters simultaneously
- Clear filters button

MVP: ✓ Basic filters (Open, Rating, Distance)
Phase 2: + Cuisine type, Price range
```

**US-CUS-01.3: View Restaurant Details**

```
As a customer, I want to see restaurant details (hours, menu, reviews)
so that I can decide whether to order.

Acceptance Criteria:
- Display: name, image, hours, address, phone, description
- Menu preview (featured items)
- Customer reviews with ratings (3-5 recent)
- Restaurant info tab, menu tab, reviews tab

MVP: ✓ Basic details + menu + reviews
Phase 2: + Restaurant video, promotions, loyalty program
```

### 3.2 Epic: Order Placement & Checkout

**EP-ORD-01: Add Items to Cart**

```
US-ORD-01.1: As a customer, I want to add items to my cart with variants
so that I can customize my order.

Acceptance Criteria:
- Select item → choose size/topping → set quantity
- Add to cart button shows current cart total
- Cart persisted in session/local storage
- Can edit quantity/variants before checkout

MVP: ✓ Basic variants (size, topping)
Phase 2: + Recipe customization, notes per item
```

**US-ORD-01.2: Apply Coupon Code**

```
As a customer, I want to apply discount codes at checkout
so that I can save money on my order.

Acceptance Criteria:
- Enter coupon code field at checkout
- Validate code: correct format, active, within limit
- Display: discount amount, final total
- Error message if invalid
- Remove coupon option

MVP: ✓ Basic percentage/fixed coupon
Phase 2: + Stacking, segment-based coupons
```

**US-ORD-01.3: Select Delivery Address**

```
As a customer, I want to select or add delivery address
so that I know where my order will be delivered.

Acceptance Criteria:
- Show saved addresses from profile
- Option to add new address
- Map preview of delivery location
- Use current location button

MVP: ✓ Saved addresses + add new
Phase 2: + Address suggestions, landmark-based
```

**US-ORD-01.4: Select Payment Method**

```
As a customer, I want to choose payment method at checkout
so that I can pay using my preferred option.

Acceptance Criteria:
- Show saved payment methods
- Option to add new card
- COD option always available
- Clear display of which payment is default

MVP: ✓ COD + 1 card/e-wallet
Phase 2: + Momo, Zalo Pay, Bank transfer
```

**US-ORD-01.5: Place Order**

```
As a customer, I want to confirm and place my order
so that the restaurant can start preparing it.

Acceptance Criteria:
- Show order summary (items, fees, total)
- Confirm button at bottom
- Order confirmation screen with order ID
- Notification sent immediately
- Order appears in "My Orders" section

MVP: ✓ Basic order confirmation
Phase 2: + Receipt PDF download, email receipt
```

### 3.3 Epic: Order Tracking & Notifications

**EP-TRK-01: Real-time Order Tracking**

```
US-TRK-01.1: As a customer, I want to track my order status in real-time
so that I know when my food will arrive.

Acceptance Criteria:
- Order status: CREATED → CONFIRMED → PREPARING → READY → ON_THE_WAY → DELIVERED
- ETA updates every minute
- Show driver location on map (anonymized)
- Status notifications (push + SMS)

MVP: ✓ Basic status updates + ETA
Phase 2: + Driver live location, chat support
```

### 3.4 Epic: Rating & Reviews

**EP-RAT-01: Submit Rating**

```
US-RAT-01.1: As a customer, I want to rate and review my order
so that I can share feedback and help other customers.

Acceptance Criteria:
- Prompt after delivery completed (30 min later)
- Rate restaurant (1-5 stars) + optional comment
- Rate driver (1-5 stars) + optional comment
- Can rate individually or together
- Submit button submits both

MVP: ✓ Basic star rating + text comment
Phase 2: + Photo upload, rating moderation, merchant reply
```

### 3.5 Epic: Restaurant Order Management

**EP-REST-01: Receive & Accept Orders**

```
US-REST-01.1: As a restaurant owner, I want to receive notifications
when a customer places an order so that I can prepare it.

Acceptance Criteria:
- Push notification on order placed (realtime)
- In-app notification center showing all orders
- Notification shows: customer name, items, delivery address, ETA
- Sound/vibration alert configurable

MVP: ✓ Push + in-app notification
Phase 2: + SMS alert, Telegram bot
```

**US-REST-01.2: Accept or Reject Order**

```
As a restaurant owner, I want to accept or reject orders
so that I can manage my capacity.

Acceptance Criteria:
- Accept button → order status → PREPARING
- Reject button → reason dropdown, full refund triggered
- Auto-accept option (for high volume)
- Confirm action dialog

MVP: ✓ Manual accept/reject
Phase 2: + Auto-accept, smart queue
```

**US-REST-01.3: Update Order Status**

```
As a restaurant owner, I want to update order status as I prepare it
so that customer knows when it's ready.

Acceptance Criteria:
- Mark as PREPARING when started
- Mark as READY_FOR_PICKUP when ready
- Driver can see when ready (triggers assignment)
- Timestamp recorded for each transition

MVP: ✓ Two-click status update (preparing, ready)
Phase 2: + Detailed prep tracking
```

### 3.6 Epic: Driver Delivery Management

**EP-DRV-01: Receive Delivery Tasks**

```
US-DRV-01.1: As a driver, I want to receive delivery offers
so that I can choose which deliveries to accept.

Acceptance Criteria:
- Offer notification with: restaurant, customer address, distance, payout
- Accept/Decline buttons (3 sec timeout then offer goes to next driver)
- Accepted task shows: pickup address, delivery address, contact info
- Direction to restaurant provided (Google Maps link)

MVP: ✓ Simple FIFO assignment, driver accepts
Phase 2: + Batch offers, route planning
```

**US-DRV-01.2: Update Delivery Status**

```
As a driver, I want to mark status as I deliver
so that customer can track progress.

Acceptance Criteria:
- Picked up: tap button at restaurant
- Delivered: tap button at customer location
- Option to take photo proof of delivery
- Customer receives notification at each step

MVP: ✓ Two-step confirmation (picked, delivered)
Phase 2: + Photo proof, signature capture
```

**US-DRV-01.3: View Earnings**

```
As a driver, I want to see my earnings breakdown
so that I can track how much I'm making.

Acceptance Criteria:
- Dashboard showing: today's earnings, total trips
- Weekly and monthly breakdown
- Per-trip details (amount, payout)
- Payout schedule information

MVP: ✓ Simple summary (total today, pending payout)
Phase 2: + Detailed breakdown, tax reports
```

### 3.7 Epic: Admin System Management

**EP-ADM-01: Dashboard & Analytics**

```
US-ADM-01.1: As an admin, I want to see platform KPIs on dashboard
so that I can monitor system health and business metrics.

Acceptance Criteria:
- Real-time metrics: total orders (today, week, month)
- Revenue (today, week, month)
- Active users (customers, restaurants, drivers)
- On-time delivery rate
- Avg order value, payment success rate
- Charts for trend analysis

MVP: ✓ Basic dashboard with key metrics
Phase 2: + Detailed drill-down, custom reports
```

### 3.8 Epic: Order Cancellation & Dispute

**EP-CANCEL-01: Order Cancellation**

```
US-CANCEL-01.1: As a customer, I want to cancel my order before restaurant accepts
so that I can change my mind without penalty.

Acceptance Criteria:
- Cancel button visible when order status = CREATED/CONFIRMED
- Full refund if before restaurant accepts
- 10% penalty if after restaurant accepts (PREPARING)
- Clear cancellation reason dropdown (required)
- Confirmation dialog before cancel
- Order status → CANCELLED
- Notification sent to restaurant + driver (if assigned)

MVP: ✓ Basic cancellation with simple refund
Phase 2: + Time-based penalty (0-5min: free, 5-15min: 5%, 15+min: 10%)
```

**EP-DISPUTE-01: Dispute Resolution**

```
US-DISPUTE-01.1: As a customer, I want to report issues with my order within 24h
so that I can get refund/compensation for problems.

Acceptance Criteria:
- Report button available within 24h of delivery
- Issue categories: Late delivery, Wrong items, Missing items, Quality issue
- Photo upload option (required for quality issues)
- Description field (max 500 chars)
- Create dispute ticket automatically
- Admin review within 24h
- Resolution options: full refund, partial refund, discount code
- Notification when dispute resolved

MVP: ✓ Basic dispute with manual admin review
Phase 2: + Automated assessment for simple cases (missing item, wrong item)
```

### 3.9 Epic: Quick Reorder

**EP-REORDER-01: Reorder Previous Orders**

```
US-REORDER-01.1: As a customer, I want to quickly reorder my previous orders
so that I can save time on frequent orders.

Acceptance Criteria:
- Show recent orders (last 30 days) in "Order History"
- One-click "Reorder" button on each past order
- Check item availability before adding to cart
- If items unavailable: show warning, allow partial reorder
- Option to modify cart before checkout
- Same delivery address pre-selected (can change)
- Same payment method pre-selected (can change)

MVP: ✓ Basic reorder with availability check
Phase 2: + Scheduled reorder, favorite orders
```

---

## 4. FEATURE SPECIFICATIONS (MVP)

### 4.1 Customer Features

**Customer Authentication & Profile**
- Email/phone registration with OTP verification
- JWT-based login, 24-hour token TTL
- Profile: name, avatar, email, phone, default address, default payment method
- Forgot password via OTP

**Search & Browse**
- Geo-based restaurant search (nearby 5km default, expandable)
- Basic filters: open now, rating ≥3.5, distance
- Sort: distance, rating, delivery time
- Result pagination (10 per page)
- Redis caching for search results (5 min TTL)

**Order Placement**
- Add items with size/topping variants
- Modify quantity before checkout
- Apply single coupon code
- Calculate total: subtotal + tax + delivery fee - discount
- Minimum order validation
- Free delivery threshold (200k+)

**Checkout & Payment**
- Save up to 2 payment methods
- COD + 1 gateway (Stripe or VNPay, to be decided)
- Order confirmation with order ID
- Payment status tracking

**Order Tracking**
- Real-time order status updates
- ETA countdown
- Driver location on map (after pickup)
- Push notifications at key milestones
- SMS for critical events (delivery, issue)

**Rating & Reviews**
- Star rating (1-5) for restaurant + driver
- Optional text comment (max 500 chars)
- Prompt after delivery completed

### 4.2 Restaurant Features

**Restaurant Onboarding**
- Register: email, phone, restaurant name, address, service radius
- Admin manual verification (simple checks)
- Once approved: can upload menu

**Menu Management**
- Add/edit/delete menu categories
- Add/edit/delete items with name, description, price, image
- Item variants: size (S/M/L), topping (X/Y/Z)
- Mark item as unavailable (temp disable)
- Bulk category/item toggle

**Order Management**
- In-app notification on new order
- View order details: customer name, items, address, special notes
- Accept/Reject with reason (if reject)
- Mark as PREPARING
- Mark as READY_FOR_PICKUP
- View all orders (today, past 7 days, all)

**Analytics (Basic)**
- Dashboard: orders/day, revenue/day, avg order value
- Top items, cuisine breakdown
- Average rating, review count
- Payout summary (weekly)

### 4.3 Driver Features

**Driver Onboarding & Verification**
- Register: personal info, phone, email
- Upload: ID card, driver's license, vehicle info
- Admin verification (simple manual check)
- Once approved: can go online

**Delivery Management**
- Toggle online/offline status
- GPS permission required
- Receive delivery offers (push notification)
- Accept/decline delivery (3 sec auto-decline)
- Navigate to restaurant (Google Maps link)
- Mark pickup + delivery (with optional photo)

**Earnings Tracking**
- Dashboard: today's earnings, pending payout
- Weekly breakdown (last 7 days)
- Per-trip details
- Payout scheduled weekly (Monday)
- Bank account on file for transfer

### 4.4 Admin Features

**Dashboard**
- KPI cards: orders (today/week/month), revenue, active users
- Charts: daily order trend, revenue trend, delivery success rate
- Real-time alert: system status, critical errors

**User Management**
- View all users (filter by role: customer, restaurant, driver)
- View user details: profile, orders, status
- Suspend/unsuspend user account
- Disable individual payment method

**Restaurant Management**
- View pending onboarding applications
- Approve/reject with notes
- View all restaurants (active, inactive, suspended)
- Suspend/unsuspend restaurant

**Driver Management**
- View pending driver applications
- Approve/reject with notes
- View all drivers (active, inactive, suspended)

**Coupon Management**
- Create coupon: code, % off or fixed amount, min cart, max discount, per-user limit, date range
- View/edit/deactivate coupon
- View coupon usage stats

**Payment Reconciliation** (Admin only)
- Daily reconciliation report: total orders vs total payments captured
- Flag discrepancies
- Manual refund trigger

---

## 5. USER FLOWS & WIREFRAMES (Description)

### 5.1 Customer Happy Path

```
1. Mobile App / Web opens
   → Check if logged in? YES → goto Home Screen / NO → goto Login

2. Login Screen
   → Email/phone input
   → OTP verification
   → [Logged in] → Home

3. Home Screen
   → Auto-detect location (geo-location)
   → Show "Restaurants near you"
   → Search bar (text input) or filter button
   → Featured restaurants carousel

4. Search Results
   → List of restaurants
   → Each card: name, rating, delivery time, distance, min order
   → Tap to open restaurant detail

5. Restaurant Detail
   → Hero image
   → Menu tabs: "All", categories (pho, bun, etc)
   → Each menu item: image, name, price, [Add] button
   → Tap [Add] → Item detail sheet

6. Item Detail Sheet (Bottom Sheet)
   → Item image, name, description
   → Size selector (S/M/L dropdown)
   → Topping selector (checkboxes: multiple select)
   → Quantity adjuster (-, 1, +)
   → Price shows dynamic (base + variants)
   → [Add to Cart] button

7. Back to Restaurant → Add more items → [Proceed to Checkout]

8. Checkout Screen
   → Cart items list (name, qty, price per item)
   → Subtotal
   → Coupon code field (optional)
   → Tax calculation
   → Delivery fee
   → [Apply Coupon] → recalculate total
   → Delivery address selector (dropdown, default selected)
   → Payment method selector (COD / card)
   → Order notes field (optional)
   → Total price
   → [Place Order] button

9. Payment Processing (if not COD)
   → If card: redirect to gateway → confirm → back to app
   → If COD: proceed immediately

10. Order Confirmation Screen
    → Order ID (big, copyable)
    → "Your order is confirmed!"
    → Estimated delivery time (e.g., 40 minutes)
    → [Track Order] button
    → [Back to Home] button

11. Order Tracking Screen (realtime)
    → Order status card (CONFIRMED, PREPARING, READY, PICKED_UP, ON_THE_WAY, DELIVERED)
    → Timeline showing completed steps
    → ETA countdown (XX min remaining)
    → Map with driver location (after pickup)
    → Tap to expand: restaurant details, driver info, delivery address
    → Chat/call buttons

12. Post-Delivery
    → [Rate] button appears after delivery
    → Rating dialog: star rating + optional comment (restaurant + driver)
    → [Submit] → thank you message
    → [Order Again] button (quick reorder)
```

### 5.2 Restaurant Happy Path

```
1. Restaurant Admin App opens
   → Login
   → Dashboard

2. Restaurant Dashboard
   → Active orders count
   → Today's revenue
   → Next pending order notification (alert badge)

3. New Order Notification (Real-time)
   → Push notification (sound + vibration)
   → [Tap] → Open order detail

4. Order Detail Screen
   → Order #ID
   → Customer name, phone
   → Items list: name, qty, variants
   → Delivery address
   → Special notes
   → [ACCEPT] / [REJECT] buttons

5. If ACCEPT
   → Status → PREPARING
   → Order moves to "Active Orders" tab
   → Kitchen staff starts preparing

6. While Preparing
   → Status visible to customer (PREPARING)
   → Restaurant can view status anytime

7. Order Ready
   → [Mark as Ready for Pickup] button
   → Status → READY_FOR_PICKUP
   → Notification to driver (auto-assign)
   → Customer sees driver assigned

8. Driver Pickup
   → Restaurant: status updates to ON_THE_WAY automatically (from driver app)

9. All Orders Tab
   → View today's orders, past orders, filter by status
   → Search by order ID or customer
   → Export option (future)
```

### 5.3 Driver Happy Path

```
1. Driver App opens
   → Login
   → Dashboard

2. Driver Dashboard
   → Toggle "Online" / "Offline" (default offline)
   → Toggle to Online → await delivery offers

3. Delivery Offer Notification (Real-time)
   → Push notification (sound + vibration)
   → Offer card: restaurant name, customer address, distance, payout (e.g., 25k)
   → [ACCEPT] / [DECLINE] buttons
   → Auto-decline after 3 seconds if no action

4. If ACCEPT
   → Order assigned
   → Map opens: navigation to restaurant (Google Maps)
   → "Go to: [Restaurant Address]"
   → Arrival confirmation: [Arrived at Restaurant] button

5. At Restaurant
   → [Confirm Pickup] button + optional photo
   → Status: ON_THE_WAY
   → Map opens: navigation to customer (Google Maps)

6. At Customer Location
   → [Confirm Delivery] button
   → Optional photo/signature
   → Status: DELIVERED
   → Payout recorded

7. Post-Delivery
   → Earnings updated on dashboard
   → Rate customer (optional, 1-5 stars)
   → [Accept next delivery] or [Go offline]

8. Earnings Dashboard
   → Today's earnings
   → Trip count
   → Rating
   → Weekly breakdown
   → Payout schedule info
```

### 5.4 Exception Flows

#### Flow A: Customer Cancels Order

```
Order (CREATED/CONFIRMED) → Customer taps [Cancel Order]
→ System checks: has restaurant accepted?
   → NO (status = CREATED/CONFIRMED): 
      - Cancel immediately
      - Full refund (100%)
      - Notification to restaurant
   → YES (status = PREPARING+):
      - Show penalty notice: "10% cancellation fee will apply"
      - Customer confirms or goes back
      - If confirmed: Cancel with 90% refund
→ Order status: CANCELLED
→ Refund processed within 24h
→ Optional: Offer 25k discount code for next order
```

#### Flow B: Restaurant Rejects Order

```
Order (CONFIRMED) → Restaurant taps [Reject Order]
→ Restaurant selects reason:
   - Out of stock
   - Too busy
   - Closing soon
   - Other (require description)
→ Order status: CANCELLED_BY_RESTAURANT
→ Refund: 100% immediately
→ Notification to customer: "Order cancelled by restaurant"
→ Compensation: 50k discount code sent to customer
→ If driver assigned: Cancel delivery task, no penalty to driver
```

#### Flow C: Payment Failure

```
Checkout → Customer taps [Place Order]
→ Payment gateway processing...
→ FAILURE: gateway returns error
→ Retry automatically (1-2 times with 2s backoff)
→ If still fail:
   → Show error message: "Payment failed. Please try again."
   → Options for customer:
      (a) Retry with same method
      (b) Try another payment method
      (c) Switch to COD
      (d) Cancel order
→ Order status: PAYMENT_FAILED (if cancelled)
→ No charge to customer
```

#### Flow D: Delivery SLA Miss

```
Order (ON_THE_WAY) → Current time > estimated_delivery_time + 60 min
→ System triggers alert to support team
→ Notification to customer: "Your delivery is delayed. We apologize."
→ Support contacts driver for status update
→ If delivery time > 3 hours from order:
   → Auto-cancel order
   → Full refund (100%)
   → Compensation: 25k discount code
   → Generate incident report
   → Flag driver for review
→ Driver assignment adjusted in future (lower priority)
```

#### Flow E: Driver Cannot Contact Customer

```
Driver arrives at delivery location
→ Driver calls customer (attempt 1) → no answer
→ Driver waits 2 min → calls again (attempt 2) → no answer
→ Driver waits 2 min → calls again (attempt 3) → no answer
→ Driver marks status: "Customer Unreachable"
→ System sends push notification + SMS to customer
→ Wait timer: 5 minutes at location
→ If customer responds within 5 min:
   → Driver proceeds with delivery
→ If no response:
   → Order status: UNDELIVERABLE
   → Customer charged: order value - 50% (for food prep cost)
   → Driver compensated: 50% of delivery fee
   → Restaurant compensated: food preparation cost
```

#### Flow F: Food Quality Issue Reported

```
Order (DELIVERED) → Customer reports issue within 1 hour
→ Customer selects issue type:
   - Missing item
   - Wrong item
   - Quality problem (requires photo)
   - Temperature issue
→ System creates dispute ticket
→ Automated assessment:
   (a) Missing item: Immediate refund for item + 10k compensation
   (b) Wrong item: Full item refund + 20k compensation
   (c) Quality/Temperature: Requires admin review with photo
→ Admin review within 2 hours:
   - Verify evidence
   - Check restaurant history
   - Contact restaurant if needed
→ Resolution:
   - Valid: 50-100% refund + discount code
   - Invalid: No refund, feedback to customer
→ Restaurant notified, incident logged for quality score
```

---

## 6. BUSINESS RULES

### 6.1 Pricing & Fee Rules

**BR-PRI-001: Order Total Calculation**
```
Total = Subtotal + Tax + Delivery Fee - Coupon Discount
Where:
- Subtotal = SUM(item_price × quantity + variant_price_delta × quantity)
- Tax = Subtotal × 10% (VAT)
- Delivery Fee = calculated per BR-PRI-002
- Coupon Discount = cannot exceed (Subtotal + Delivery Fee)
```

**BR-PRI-002: Delivery Fee Structure (MVP)**

| Distance | Fee |
|:---------|:----|
| 0-3 km | 15,000 VND (base) |
| >3 km | 15,000 + (distance - 3) × 3,000 VND/km |
| Orders > 200,000 VND | FREE delivery |

**BR-PRI-003: Minimum Order Value**
- Default: 50,000 VND
- Configurable per restaurant
- System validates at checkout; if cart < minimum, show error

### 6.2 Coupon & Promotion Rules

**BR-COUPON-001: Coupon Eligibility**
A coupon is valid only if ALL conditions are met:
- `current_time` is within coupon `[start_time, end_time]`
- Order `subtotal ≥ coupon.min_order_value`
- Customer usage < `coupon.per_user_usage_limit`
- Global usage < `coupon.global_usage_limit`
- `coupon.target_restaurant_id` is NULL or matches `order.restaurant_id`

**BR-COUPON-002: Discount Calculation**
- If type = "PERCENT": `discount = subtotal × (value/100)`, capped at `max_discount`
- If type = "FLAT": `discount = value`

**BR-COUPON-003: Stacking Policy (MVP)**
- Only 1 coupon per order (no stacking in MVP)
- Phase 2: Platform coupon + Merchant coupon stacking allowed

### 6.3 Cancellation & Refund Policy

**BR-CANCEL-001: Customer Cancellation**

| Order Status | Cancellation | Refund |
|:-------------|:-------------|:-------|
| CREATED / CONFIRMED | Allowed | 100% |
| PREPARING | Allowed with penalty | 90% (10% penalty) |
| READY_FOR_PICKUP | Not recommended | 80% (20% penalty) |
| ON_THE_WAY / DELIVERED | Not allowed | N/A (use dispute) |

**BR-CANCEL-002: Restaurant Cancellation**
- Allowed only when order status = CONFIRMED
- Customer receives: 100% refund + 50,000 VND discount code
- Notification sent via push + SMS

**BR-CANCEL-003: System Auto-Cancel (SLA Miss)**
- Trigger: `delivery_time > estimated_delivery_time + 60 min`
- Action: Auto-cancel + 100% refund + 25,000 VND discount code
- Incident report generated for review

### 6.4 Payment & Reconciliation

**BR-PAY-001: Idempotency & Double-Charge Prevention**
- Every order has unique `idempotency_key = hash(customer_id, restaurant_id, created_at, nonce)`
- Zero tolerance for double-charge incidents
- Daily reconciliation job to verify 100% accuracy

**BR-PAY-002: Payment Status Flow**
- **COD:** `PENDING → CAPTURED` (only after driver confirms delivery)
- **Card/Gateway:** `PENDING → AUTHORIZED → CAPTURED` (after verification)
- Timeout: If capture not confirmed within 30 min → mark FAILED, refund authorized amount

**BR-PAY-003: Refund Timeline**
- Initiated: Immediately upon cancellation/dispute approval
- Customer account: Within 1-2 business days (gateway dependent)
- All refunds must link to original `payment_id`

### 6.5 Driver Assignment & SLA

**BR-DRIVER-001: Assignment Algorithm (MVP - Simple)**
```
1. Get all drivers: status=APPROVED, is_online=true
2. Filter: distance ≤ 10km from restaurant, acceptance_rate ≥ 50%
3. Rank by: distance ASC, rating DESC
4. Send delivery offer to top 3 drivers (in order)
5. First to accept gets delivery (3 sec timeout per driver)
6. If no acceptance within 2 min: expand radius to 15km, retry
7. If no driver found after 5 min: queue order, notify restaurant/customer
```

**BR-DRIVER-002: Performance Metrics & SLA**

| Metric | Target | Action if Below |
|:-------|:-------|:----------------|
| On-time delivery | ≥ 95% | Review + warning |
| Average rating | ≥ 4.5 stars | If < 4.0: review, if < 3.5: suspend |
| Acceptance rate | ≥ 70% | If < 50%: lower priority, if < 20%: suspend |
| Incident rate | < 5%/month | Review required |

### 6.6 Restaurant Onboarding & Suspension

**BR-REST-001: Onboarding Workflow**
1. Restaurant owner registers with basic info
2. Admin reviews (manual in MVP, auto-verify in Phase 2)
3. If approved: Restaurant can upload menu
4. First order expected within 48h of approval

**BR-REST-002: Auto-Suspension Triggers**

| Condition | Action |
|:----------|:-------|
| Closure rate > 30%/month | 7-day suspension + warning |
| Average rating < 3.0 | Email warning, review required |
| Multiple customer complaints (quality, hygiene) | Manual review by admin |
| Regulatory/compliance violation | Immediate suspension |

---

## 7. PRODUCT ROADMAP

### 7.1 Phase 1 (MVP) – Months 1-4

**Priority Features:**
- ✓ User auth (customer, restaurant, driver)
- ✓ Search & browse restaurants
- ✓ Order placement & checkout
- ✓ Payment (COD + 1 gateway)
- ✓ Order tracking (realtime)
- ✓ Rating & reviews
- ✓ Restaurant order management
- ✓ Driver delivery management
- ✓ Admin dashboard (basic KPIs)
- ✓ Notification (push, SMS)

**Launch Targets:**
- 1 city (TP.HCM)
- 50k-100k customers
- 1k-2k restaurants
- 500-1k drivers
- 99.5% uptime SLA

#### MVP Milestones

| Month | Milestone | Deliverables |
|:------|:----------|:-------------|
| **Month 1** | Foundation | Auth service, User service, basic DB schema, CI/CD setup |
| **Month 2** | Core Features | Catalog service, Order service, Payment integration |
| **Month 3** | Delivery & Ops | Driver app, delivery tracking, notifications, admin dashboard |
| **Month 4** | Polish & Launch | Bug fixes, load testing, security audit, soft launch |

#### MVP Exit Criteria

- [ ] 99.5% uptime achieved for 2 consecutive weeks
- [ ] <500ms p95 API latency verified
- [ ] 1,000 test orders processed successfully
- [ ] 50+ restaurants onboarded and active
- [ ] 100+ drivers approved and active
- [ ] Security audit passed (OWASP Top 10)
- [ ] Load test passed (10 orders/second sustained)
- [ ] Payment reconciliation 100% accurate for 7 days

### 7.2 Phase 2 (Months 5-8) – Scale & Personalization

**New Features:**
- Elasticsearch + advanced search
- Personalized recommendations
- Loyalty points & subscription
- Multi-method payment (Momo, Zalo Pay)
- Multi-city support (Hà Nội, Bình Dương)
- Advanced merchant analytics
- Driver route optimization (Phase 2.5)
- In-app messaging/chat

**Growth Targets:**
- 3 cities
- 300k-500k customers
- 5k-10k restaurants
- 2k-5k drivers

#### Feature Flags & A/B Testing Strategy

| Feature | Flag Name | Rollout Strategy |
|:--------|:----------|:-----------------|
| New checkout flow | `ff_checkout_v2` | 10% → 50% → 100% over 2 weeks |
| Recommendation engine | `ff_recommendations` | A/B test 2 weeks, measure CTR |
| Surge pricing | `ff_surge_pricing` | City-based rollout (HCM first) |
| Chat support | `ff_chat_support` | Premium users first, then all |
| Loyalty points | `ff_loyalty` | 20% → 100% over 1 month |

### 7.3 Phase 3 (Months 12+) – Ecosystem

**Vertical Expansion:**
- Grocery delivery
- Pharmacy delivery
- B2B ordering (corporate)

**Platform Improvements:**
- Route optimization engine
- White-label solution
- Advanced SLA automation
- Real-time inventory sync

---

## 8. SUCCESS METRICS & ANALYTICS

### 8.1 Key Success Metrics (North Star Metrics)

| Metric | Target | Tracking |
|:---|:---|:---|
| **DAU** | 50k-100k (MVP end) | Daily dashboard |
| **MAU** | 200k-300k | Monthly cohort analysis |
| **Repeat Order Rate** | ≥25% | 30-day user cohort |
| **On-time Delivery** | ≥95% | Real-time tracking |
| **Payment Success** | >99.9% | Daily reconciliation |
| **Uptime** | ≥99.5% | Prometheus alerting |

### 8.2 Engagement Metrics

| Metric | Target | Tool |
|:---|:---|:---|
| **Conversion Rate** (search → order) | ≥3% | Analytics SDK |
| **AOV** (Average Order Value) | 300k VND | Mixpanel |
| **Order Frequency** | 2-3x/month per user | Amplitude |
| **Session Duration** | >5 min | Google Analytics |
| **Retention (Day 7)** | ≥30% | Cohort analysis |
| **Retention (Day 30)** | ≥40% | Cohort analysis |

### 8.3 Business Metrics

| Metric | Target | Owner |
|:---|:---|:---|
| **GMV** | 500M-1B VND/month (end Year 1) | Finance |
| **CAC** | <50k VND | Marketing |
| **LTV** | >500k VND | Product |
| **Unit Economics** | LTV:CAC ≥ 10:1 | Finance |
| **Churn Rate** | <5% monthly | Product |
| **NPS** | >50 | Product |

### 8.4 Operational Metrics

| Metric | Target | Tracking |
|:---|:---|:---|
| **Order Fulfillment Time** | 30-50 min (median) | Real-time |
| **Customer Support Response** | <2 hours | Zendesk |
| **Dispute Resolution** | 100% within 48 hours | Admin dashboard |
| **Restaurant Rejection Rate** | <5% | Weekly report |
| **Driver Cancellation Rate** | <5% | Weekly report |
| **Cart Abandonment Rate** | <60% | Analytics |
| **App Crash Rate** | <0.1% | Crashlytics |

### 8.5 Analytics Implementation

- **SDK:** Mixpanel / Amplitude (mobile + web)
- **Event Tracking:** Key flows (search, add-to-cart, checkout, order, delivery, rating)
- **Dashboard:** Metabase / Tableau for business reporting
- **Real-time:** Kafka → ClickHouse for real-time analytics

---

## 9. RISK ANALYSIS & MITIGATION

### 9.1 Business Risks

| Risk | Likelihood | Impact | Mitigation |
|:-----|:----------:|:------:|:-----------|
| **Strong competition** (Grab, Now, Baemin) | HIGH | HIGH | Focus on UX, speed, niche segments; exclusive restaurant partnerships |
| **Driver shortage** (peak hours) | HIGH | HIGH | Incentive programs, surge pricing, partner with logistics companies |
| **Low customer adoption** | MEDIUM | HIGH | Aggressive marketing, referral program, first-order promotions |
| **Restaurant quality inconsistent** | MEDIUM | MEDIUM | Strict onboarding, quality audits, rating/suspension system |
| **Regulatory changes** (food delivery license) | MEDIUM | MEDIUM | Legal compliance team, feature flags for quick adaptation |

### 9.2 Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|:-----|:----------:|:------:|:-----------|
| **Payment gateway downtime** | MEDIUM | CRITICAL | Multiple gateways, COD fallback, circuit breaker pattern |
| **Database performance** | MEDIUM | HIGH | Query optimization, read replicas, connection pooling |
| **Double-charge incidents** | LOW | CRITICAL | Idempotency keys, outbox pattern, daily reconciliation |
| **Security breach** | LOW | CRITICAL | Encryption, pentest quarterly, bug bounty, OWASP Top 10 |
| **GPS tracking inaccuracy** | MEDIUM | MEDIUM | Fallback to address-based ETA, Google Maps API |

### 9.3 Contingency Plans

| Scenario | Trigger | Immediate Action |
|:---------|:--------|:-----------------|
| Gateway down | >5 min outage | Switch to backup gateway, enable COD-only mode |
| Traffic spike | >200% normal load | Auto-scale pods, queue checkout requests, show wait time |
| Driver shortage | <50% coverage in zone | Expand search radius, activate incentive notifications |
| Major bug in production | P0 incident | Rollback within 15 min, war room activation |
| Security incident | Data breach detected | Isolate affected systems, notify users within 24h, engage security team |

---

## 10. CONSTRAINTS & DEPENDENCIES

### 10.1 Technical Constraints

- **Platform:** Mobile-first (iOS + Android via React Native TypeScript), web secondary
- **Architecture:** Microservices (Golang backend, React (Web) + React Native TypeScript (Mobile))
- **Database:** PostgreSQL (primary), Redis (cache)
- **Payment Gateway:** Stripe or VNPay (to be decided in Week 1)
- **Hosting:** AWS or GCP
- **Search (MVP):** Redis caching, no Elasticsearch
- **Search (Phase 2):** Elasticsearch for advanced search & discovery

### 10.2 Business Constraints

- **MVP Timeline:** Hard deadline Month 4 for TP.HCM launch
- **Budget:** Defined by finance (not in scope)
- **Regulatory:** Compliance with Vietnamese logistics, payment, data protection laws
- **Market:** Competitor presence (Grab, Now, Baemin already established)
- **Single City Launch:** TP.HCM only for MVP (multi-city in Phase 2)

### 10.3 Dependencies

| Dependency | Status | Owner | Due Date |
|:---|:---|:---|:---|
| Payment gateway integration (Stripe/VNPay) | TBD | Engineering | Month 2 |
| SMS provider (Twilio / local) | TBD | Ops | Month 1 |
| Google Maps API | TBD | Ops | Month 1 |
| Firebase Cloud Messaging (FCM) setup | TBD | Ops | Month 1 |
| Restaurant onboarding process (legal, tax ID) | TBD | Legal + Ops | Month 2 |
| Driver verification process (ID check, license) | TBD | Ops | Month 2 |
| Admin approval workflow | TBD | Ops | Month 3 |
| Security audit vendor | TBD | Engineering | Month 4 |

---

## DOCUMENT TRACEABILITY

| Section | Related BRD Section | Alignment Status |
|:--------|:--------------------|:-----------------|
| 1. Overview | BRD 1. Executive Summary | ✅ Aligned |
| 1.3 Market Sizing | BRD 3. Target Market | ✅ Aligned |
| 1.5 Product Goals | BRD 2. Business Objectives | ✅ Aligned |
| 3. User Stories | BRD 4. User Roles | ✅ Aligned |
| 5. User Flows | BRD 5. Business Process | ✅ Aligned |
| 6. Business Rules | BRD 6. Business Rules | ✅ Aligned |
| 7. Product Roadmap | BRD 7. Scope & Roadmap | ✅ Aligned |
| 8. Success Metrics | BRD 8. KPIs | ✅ Aligned |
| 9. Risk Analysis | BRD 9. Risk & Mitigation | ✅ Aligned |

---

## APPROVAL & NEXT STEPS

**Prepared by:** Product Manager  
**Reviewed by:** Product Lead, Engineering Lead  
**Approved by:** [VP Product / Founder]

**Document Version History:**

| Version | Date | Author | Changes |
|:--------|:-----|:-------|:--------|
| 1.0 | 20 Jan 2026 | PM | Initial PRD |
| 2.0 | 21 Jan 2026 | PM | Added Business Rules, Risk Analysis, Exception Flows, Market Sizing, Customer Personas, aligned with BRD |

**Next Steps:**
1. PRD review + sign-off (1 week)
2. Technical feasibility assessment (1 week)
3. UX/UI design sprint (2 weeks)
4. Engineering sprint planning (1 week)
5. Development start (Month 1, Week 1)