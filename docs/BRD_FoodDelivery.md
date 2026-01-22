# Business Requirements Document (BRD)
## Food Delivery Platform

**Version:** 1.0  
**Date:** 20 January 2026  
**Location:** Ho Chi Minh City, Vietnam  
**Status:** Ready for Discussion

---

## TABLE OF CONTENTS

1. Executive Summary
2. Business Objectives
3. Target Market & Scale
4. User Roles & Capabilities
5. Business Process Flows
6. Business Rules
7. Scope & Roadmap
8. KPIs & Success Metrics
9. Risk & Mitigation

---

## 1. EXECUTIVE SUMMARY

### 1.1 Project Overview

Phát triển nền tảng gọi đồ ăn trực tuyến (food delivery platform) phục vụ ba nhóm người dùng chính:
- **Khách hàng (Customer):** Đặt hàng từ nhà hàng yêu thích
- **Nhà hàng (Restaurant Partner):** Kinh doanh trực tuyến, quản lý menu
- **Tài xế giao hàng (Delivery Driver):** Thu nhập từ việc giao hàng

### 1.2 Core Value Propositions

| Stakeholder | Value Proposition |
|:---|:---|
| **Customer** | Đặt hàng nhanh, trải nghiệm mượt mà, theo dõi realtime, tiết kiệm với khuyến mãi |
| **Merchant** | Mở rộng kênh bán hàng, quản lý đơn dễ, thống kê doanh số, tăng lợi nhuận |
| **Driver** | Việc làm linh hoạt, kiếm thêm thu nhập, công cụ quản lý thu nhập rõ ràng |
| **Platform** | Giữa vai trò trung gian, mở rộng sang đa dạng vertical (grocery, pharmacy) |

### 1.3 Business Hypothesis

> "Khách hàng TP.HCM sẵn sàng trả phí giao hàng để nhận tiện ích mua sắm nhanh chóng, an toàn; nhà hàng muốn mở rộng khách hàng qua nền tảng; và có đủ lao động muốn làm tài xế giao hàng theo thời gian linh hoạt."

---

## 2. BUSINESS OBJECTIVES

### 2.1 Strategic Objectives (3-5 năm)

1. **Trở thành nền tảng food delivery #1 TP.HCM**
   - Mục tiêu: Chiếm 30% market share trong năm 2 + 3
   - Chỉ tiêu: 500k+ customers, 5k+ restaurants

2. **Mở rộng đa dạng vertical (multi-vertical expansion)**
   - Năm 1: Food delivery (TP.HCM)
   - Năm 2: Expansion Hà Nội, Bình Dương
   - Năm 3: Grocery, Pharmacy, B2B ordering

3. **Tăng trưởng bền vững**
   - Chỉ tiêu: GMV 500M - 1B VND/tháng (end Year 1)
   - Chỉ tiêu: CAC < 50k VND, Retention Day 30 ≥ 40%

### 2.2 Near-term Objectives (Year 1)

| Objective | Target | Timeline |
|:---|:---|:---|
| MVP Launch | Single city (HCM) | Month 4 |
| User Base | 50k-100k customers, 1k-2k restaurants, 500-1k drivers | Month 6-8 |
| GMV | 100M - 200M VND/month | Month 6-8 |
| Platform Maturity | 99.5% uptime, <500ms latency | Month 4-6 |
| Phase 2 Prep | Elasticsearch, personalization, expansion infra | Month 5-8 |

### 2.3 Business Goals

| Goal ID | Goal | Owner | Success Metric |
|:---|:---|:---|:---|
| BG-01 | Cung cấp trải nghiệm gọi đồ ăn nhanh, đơn giản | Product | Response time <500ms, DAU ≥50k |
| BG-02 | Tối ưu hóa khám phá nhà hàng/món ăn | Product | CTR >15%, conversion >3% |
| BG-03 | Đảm bảo tính toàn vẹn payment (0 double-charge) | Finance + Tech | Double-charge rate = 0 |
| BG-04 | Xây dựng nền tảng dễ mở rộng (scalable) | Tech | Support 10k+ concurrent users (Phase 2) |
| BG-05 | Giữ chất lượng dịch vụ, on-time delivery ≥95% | Operations | On-time rate ≥95% |

---

## 3. TARGET MARKET & SCALE

### 3.1 Market Sizing

**TP.HCM - Thị trường truyền thống:**
- Dân số: 9M+
- Urban density: Cao (Quận 1, 3, 7, BT, Thủ Đức)
- Smartphone penetration: 70%+
- Food delivery adoption: Tăng 40% YoY

**Addressable Market (TAM):**
- Total serviceable addressable market (TSAM): ~3M users (urban, có smartphone, 18-55 tuổi)
- Serviceable obtainable market (SOM): ~500k users (Year 2-3)

### 3.2 MVP Scale (Phase 1 - Months 1-4)

| Metric | Target |
|:---|:---|
| **Cities** | 1 (TP.HCM) |
| **Customers** | 50k-100k |
| **Restaurants** | 1k-2k |
| **Drivers** | 500-1k |
| **Concurrent Users (Peak)** | 3k-5k |
| **Orders/Second (Peak)** | 10-20 |
| **Avg Orders/Day** | 5k-10k |

### 3.3 Phase 2 Scale (Months 5-8)

| Metric | Target |
|:---|:---|
| **Cities** | 2-3 (HCM expanded, Hà Nội, Bình Dương) |
| **Customers** | 300k-500k |
| **Restaurants** | 5k-10k |
| **Drivers** | 2k-5k |
| **Concurrent Users (Peak)** | 10k+ |
| **Orders/Second (Peak)** | 50+ |
| **Avg Orders/Day** | 50k-100k |

---

## 4. USER ROLES & CAPABILITIES

### 4.1 Customer (Khách hàng)

**Primary Needs:**
- Tìm nhà hàng, xem menu, đặt hàng nhanh
- Thanh toán an toàn, nhanh chóng
- Theo dõi đơn realtime
- Nhận khuyến mãi, discount

**Key Capabilities (MVP):**
1. ✓ Đăng ký/đăng nhập (email, phone, OTP)
2. ✓ Quản lý profile + 2 địa chỉ giao hàng
3. ✓ Tìm kiếm nhà hàng (geo-based, filter cơ bản)
4. ✓ Xem menu, thêm vào giỏ, áp dụng coupon
5. ✓ Đặt hàng (COD + 1 payment gateway)
6. ✓ Theo dõi trạng thái order realtime
7. ✓ Đánh giá & review (sau khi nhận hàng)
8. ✓ Lịch sử đơn, tái đặt (reorder)

**Phase 2+:**
- Personalized recommendations
- Loyalty points, subscription
- Multi-method payment (Momo, Zalo Pay, Bank transfer)
- Chat customer support

### 4.2 Restaurant Partner (Nhà hàng)

**Primary Needs:**
- Đăng ký bán trên nền tảng
- Quản lý menu, giá, hình ảnh
- Nhận + xử lý đơn hàng
- Theo dõi doanh số, lợi nhuận

**Key Capabilities (MVP):**
1. ✓ Onboarding: thông tin cơ bản, địa chỉ, khu vực phục vụ
2. ✓ Menu CRUD: thêm/sửa/xóa món, variants (size, topping)
3. ✓ Update trạng thái: bật/tắt nhận đơn
4. ✓ Nhận thông báo + xử lý order (accept/reject)
5. ✓ Báo "Ready for pickup" khi chuẩn bị xong
6. ✓ Dashboard: số đơn, doanh thu, rating, feedback
7. ✓ Khuyến mãi cơ bản: % off, fixed discount

**Phase 2+:**
- Bulk upload menu (CSV)
- Advanced promotion targeting
- Item-level analytics
- Multi-branch support
- Integration với POS

### 4.3 Delivery Driver (Tài xế giao hàng)

**Primary Needs:**
- Đăng ký, xác minh tài xế
- Nhận đơn giao hàng
- Kiếm thu nhập, rút tiền
- Quản lý lịch làm việc

**Key Capabilities (MVP):**
1. ✓ Onboarding: thông tin cá nhân, phương tiện, bằng lái
2. ✓ Online/offline status
3. ✓ Xem danh sách đơn được gán
4. ✓ Navigate GPS, update trạng thái (picked-up, in-transit, delivered)
5. ✓ Liên hệ customer
6. ✓ Dashboard: doanh thu, lịch giao hàng, rating

**Phase 2+:**
- Route optimization
- Performance analytics
- Surge pricing
- Advanced earning breakdown (per trip, per day, per week)

### 4.4 Admin / Super Admin

**Primary Needs:**
- Quản lý hệ thống (users, restaurants, drivers)
- Duyệt onboarding, suspend account
- Xem báo cáo, metrics, SLA
- Xử lý dispute, complaint

**Key Capabilities (MVP):**
1. ✓ Quản lý users: view, suspend, xóa
2. ✓ Duyệt onboarding merchant/driver
3. ✓ Dashboard KPI: orders, revenue, users, SLA metrics
4. ✓ Quản lý coupon/promotion cơ bản
5. ✓ Xem logs, incident, alert
6. ✓ Báo cáo hàng ngày, tuần, tháng

**Phase 2+:**
- Advanced reporting engine
- Automated campaign management
- Incident automation
- Predictive analytics

---

## 5. BUSINESS PROCESS FLOWS

### 5.1 Primary Flow: Place Order (Happy Path)

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

**Thời gian dự kiến (Estimated):** 30-50 phút từ order → delivery

### 5.2 Exception Flows

**Flow A: Customer Cancels (Before Restaurant Accepts)**
```
Order (CREATED/CONFIRMED) → Customer initiates cancel
→ Check: if restaurant not yet accepted → cancel immediately
→ Refund: 100% full amount + notify restaurant
→ Order status: CANCELLED
```

**Flow B: Restaurant Rejects**
```
Order (CONFIRMED) → Restaurant rejects
→ Refund: 100% immediately
→ Notify: Customer + system
→ Offer: Discount code 50k for next order
```

**Flow C: Payment Failure**
```
Order (CREATED) → Payment processing fails
→ Retry: 1-2 times automatically (with backoff)
→ If still fail → Order status: PAYMENT_FAILED
→ Notify: Customer + allow retry or cancel
```

**Flow D: Delivery SLA Miss**
```
Order (ON_THE_WAY, estimated_delivery_time passed)
→ If delivery takes 3+ hours → auto-cancel + full refund + incident
```

**Flow E: Driver Cannot Contact Customer**
```
Driver arrives at delivery location → attempts to call customer (3 attempts)
→ No response after 3 calls → wait 5 minutes at location
→ Driver marks order as "Contact Failed"
→ System notifies customer support team
→ Support attempts to reach customer (phone/app notification)
→ Options:
   (a) Customer responds within 10 min → Driver re-attempts delivery
   (b) No response → Order marked as UNDELIVERABLE
   (c) Reschedule delivery (if customer requests)
→ Outcome:
   - If undeliverable: Partial refund (order value - delivery fee - restaurant prep cost)
   - Driver compensated for attempted delivery (50% of delivery fee)
   - Restaurant compensated for food preparation
```

**Flow F: Incorrect Delivery Address**
```
Driver arrives at location → address does not match/customer not found
→ Driver contacts customer via app call/message
→ Customer clarifies correct address
→ System calculates new address distance:
   (a) Within 2km: Driver proceeds, no additional charge
   (b) Beyond 2km: Customer charged additional distance fee or cancel option
   (c) Customer confirms/updates delivery address
→ System recalculates:
   - Estimated delivery time (ETA updated)
   - Additional delivery fee (if applicable)
→ Driver navigates to correct address
→ Order status remains ON_THE_WAY with updated ETA
→ If customer cancels due to address error: 
   - Charge 50% cancellation fee (food prepared + partial delivery)
```

**Flow G: Food Quality Issue Reported**
```
Order (DELIVERED) → Customer reports food quality issue within 1 hour
→ Customer submits complaint with:
   - Issue type (wrong item, missing item, quality problem, temperature)
   - Photo evidence (required for quality issues)
   - Description
→ System creates dispute ticket
→ Automated assessment:
   (a) Missing item (verified from order): Immediate refund for item + 10k compensation
   (b) Wrong item: Full item refund + 20k compensation or replacement offer
   (c) Quality issue (with photo): Admin review required
→ Admin review (within 2 hours):
   - Verify evidence
   - Check restaurant history
   - Contact restaurant if needed
→ Resolution options:
   (a) Valid complaint: 50-100% order refund + discount code
   (b) Partial issue: Proportional refund + 30k compensation
   (c) Invalid complaint: No refund, customer warned
→ Restaurant notified of outcome
→ Incident logged for restaurant quality score
```

**Flow H: Driver Accident or Emergency**
```
Order (ON_THE_WAY) → Driver encounters accident/emergency
→ Driver marks status as "EMERGENCY" in app
→ System immediately:
   - Notifies customer of delay
   - Alerts operations team
   - Triggers driver support protocol
→ Operations team contacts driver to assess situation
→ Order reassignment decision:
   (a) Minor delay (<15 min): Wait for driver to resume
   (b) Moderate delay (15-30 min): Offer customer reschedule or cancel
   (c) Major incident (30+ min): Reassign to new driver immediately
→ If reassignment:
   - Find nearest available driver
   - Transfer pickup location (restaurant or current driver location)
   - Update customer with new ETA
→ Compensation:
   - Original driver: Full delivery fee (insurance covers)
   - Customer: Discount code (50k) for inconvenience
   - New driver: Standard delivery fee
→ Incident report filed for insurance claim
```

**Flow I: Payment Dispute (After Delivery)**
```
Order (DELIVERED, payment CAPTURED) → Customer disputes charge within 7 days
→ Customer submits dispute reason:
   - Unauthorized transaction
   - Service not received as described
   - Duplicate charge
   - Quality issue
→ System checks:
   (a) Duplicate charge: Auto-refund immediately if detected
   (b) Other issues: Create dispute ticket
→ Admin investigation:
   - Review order history, delivery proof, payment logs
   - Contact customer for additional info
   - Check restaurant/driver records
→ Resolution (within 48 hours):
   (a) Valid dispute: Full/partial refund + apology
   (b) Service failure: Refund + 100k discount for next order
   (c) Invalid dispute: No refund, evidence shared with customer
   (d) Chargeback (card payment): Follow gateway chargeback process
→ If refund approved:
   - Process refund via original payment method
   - Settlement adjustment with restaurant (deduct commission refund)
   - Driver payment unaffected (unless driver error proven)
```

---

## 6. BUSINESS RULES

### 6.1 Pricing & Delivery Fee

**BR-PRI-001: Order Total**
- Total = Subtotal + Tax + Delivery Fee - Coupon Discount

**BR-PRI-002: Delivery Fee (MVP)**
- Base: 15,000 VND for distance ≤ 3km
- Additional: 3,000/km for distance > 3km
- Free delivery: for orders > 200,000 VND

**BR-PRI-003: Minimum Order Value**
- Default: 50,000 VND (configurable per restaurant)

### 6.2 Cancellation & Refund

**BR-CANCEL-001: Customer Cancellation**
- Before restaurant accepts: Full refund, no penalty
- After restaurant accepts: Allow with 10% penalty (MVP; Phase 2: time-based)

**BR-CANCEL-002: Restaurant Cancellation**
- Full refund + 50,000 VND discount code to customer

**BR-CANCEL-003: System Auto-Cancel (SLA Miss)**
- If delivery > estimated_delivery_time + 60min → auto-cancel + full refund + 25k discount

### 6.3 Payment & Reconciliation

**BR-PAY-001: Idempotency & Double-Charge Prevention**
- Every order has unique idempotency_key
- Zero tolerance for double-charge
- Daily reconciliation job to verify accuracy

**BR-PAY-002: Payment Status**
- COD: marked CAPTURED only after driver confirms delivery
- Card/Gateway: AUTHORIZED → CAPTURED after verification

**BR-PAY-003: Refund Timeline**
- Initiated immediately upon cancellation/dispute
- Appears in customer account within 1-2 business days

### 6.4 Driver Assignment & SLA

**BR-DRIVER-001: Assignment Algorithm (MVP – Simple)**
- Get drivers: status=APPROVED, is_online=true, distance ≤ 10km
- Rank by: distance ASC, rating DESC
- Send offer to top 3 drivers; first to accept gets delivery
- Timeout: if no acceptance within 2min → expand radius

**BR-DRIVER-002: SLA & Performance**
- On-time delivery target: ≥ 95% of orders
- Quality metric: average rating ≥ 4.5 stars
- Acceptance rate: ≥ 70% (if < 50% → lower priority)

### 6.5 Restaurant Onboarding & Suspension

**BR-REST-001: Onboarding**
- Register → submit info → admin review → approve/reject
- Once approved: start upload menu

**BR-REST-002: Auto-Suspension**
- Closure rate > 30% → 7-day suspension
- Average rating < 3.0 → warning + review required
- Multiple customer complaints → manual review

---

## 7. SCOPE & ROADMAP

### 7.1 MVP (Phase 1) – Go-Live

**Scope Table:**

| Component | MVP Include | Details |
|:---|:---:|:---|
| **Auth** | YES | Email/phone/OTP, JWT, basic RBAC |
| **Customer** | YES | Profile, 2 addresses, 1-2 payment methods |
| **Search** | MINIMAL | Geo-search, basic filter (open, rating) |
| **Order** | YES | Cart, apply coupon, checkout, state machine |
| **Payment** | YES | COD + 1 gateway (Stripe/VNPay) |
| **Delivery** | YES | Driver assignment simple, GPS tracking |
| **Notification** | YES | Push (FCM), SMS, basic retry |
| **Rating** | YES | Star + comment (no moderation yet) |
| **Admin** | YES | Dashboard KPI, onboarding approval |

**Timeline:** 3-4 months

### 7.2 Phase 2 (Expansion) – Months 5-8

- Elasticsearch + advanced search
- Personalization engine
- Multi-city expansion (Hà Nội, Bình Dương)
- Advanced promotion, multi-method payment
- Service mesh, advanced tracing

### 7.3 Phase 3+ (Ecosystem)

- Grocery/Pharmacy vertical
- B2B ordering (corporate)
- Route optimization
- White-label solution

---

## 8. KPIs & SUCCESS METRICS

### 8.1 Business KPIs (Targets Year 1)

| KPI | Target |
|:---|:---|
| **DAU (Daily Active Users)** | 50k-100k (end Year 1) |
| **MAU (Monthly Active Users)** | 200k-300k (end Year 1) |
| **GMV** | 500M-1B VND/month (end Year 1) |
| **AOV (Avg Order Value)** | 300k VND |
| **CAC (Customer Acquisition Cost)** | < 50k VND |
| **Retention (Day 30)** | ≥ 40% |
| **On-time Delivery Rate** | ≥ 95% |
| **NPS (Net Promoter Score)** | > 50 |
| **Restaurants Active** | 100+/month new |
| **Repeat Order Rate** | ≥ 25% |

### 8.2 Operational KPIs

| KPI | Target |
|:---|:---|
| **Order Fulfillment Time** | 30-50 min (median) |
| **Customer Support Response Time** | < 2 hours |
| **Dispute Resolution Rate** | 100% within 48 hours |
| **Payment Success Rate** | > 99.9% |
| **Driver Acceptance Rate** | ≥ 70% |
| **Restaurant Approval Rate** | ≥ 80% onboarded restaurants stay active |

---

## 9. RISK & MITIGATION

| Risk | Likelihood | Impact | Mitigation |
|:---|:---:|:---:|:---|
| **Driver Shortage** | HIGH | HIGH | Incentive, surge pricing, partnership logistics |
| **Low Customer Adoption** | MEDIUM | HIGH | Aggressive marketing, referral, promotion |
| **Payment Gateway Downtime** | MEDIUM | CRITICAL | Multiple gateways, fallback COD, circuit breaker |
| **Restaurant Low Quality** | MEDIUM | MEDIUM | Strict onboarding, quality audit, rating system |
| **Competition** | HIGH | MEDIUM | Differentiation (speed, price, UX), exclusive merchants |
| **Regulatory Change** | MEDIUM | MEDIUM | Legal review, compliance team, feature flags |
| **Traffic Spike** | MEDIUM | HIGH | Load test, auto-scale, surge pricing |
| **Security Breach** | LOW | CRITICAL | Pentest quarterly, bug bounty, OWASP Top 10 |

---

## CONCLUSION

Food Delivery Platform target là trở thành nền tảng hàng đầu TP.HCM bằng cách cung cấp trải nghiệm nhanh, an toàn, và tín cậy cho khách hàng; tạo cơ hội kinh doanh cho nhà hàng; và mô hình việc làm linh hoạt cho tài xế.

---

**Document Status:** Ready for Stakeholder Approval

**Next Steps:**
1. Stakeholder review & sign-off (1-2 weeks)
2. Validate market assumptions via interviews (1 week)
3. Product strategy workshop (1 week)
4. Finalize roadmap & timelines with tech team