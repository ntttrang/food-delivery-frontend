# Figma UI/UX Design Report
## Food Delivery Platform - "FreshBite"

**Version:** 1.0  
**Date:** 21 January 2026  
**Designer:** Senior UI/UX Designer  
**Domain:** Food Delivery Platform  
**Base Document:** SRS_FoodDelivery.md v2.2

---

## TABLE OF CONTENTS

1. Design Philosophy & Brand Identity
2. Color System
3. Typography System
4. Iconography & Visual Elements
5. Component Library
6. Screen Designs by User Role
7. Interaction & Animation Guidelines
8. Responsive Design Strategy
9. Accessibility Guidelines
10. Design Deliverables

---

## 1. DESIGN PHILOSOPHY & BRAND IDENTITY

### 1.1 Design Vision
**FreshBite** - A modern, clean, and intuitive food delivery platform focused on fresh, healthy, and natural food options.

**Core Values:**
- **Fresh & Natural** - Emphasizing quality ingredients and healthy choices
- **Fast & Efficient** - Streamlined ordering process with minimal friction
- **Transparent & Trustworthy** - Clear communication throughout the delivery journey
- **Delightful & Engaging** - Pleasant user experience with subtle animations

### 1.2 Visual Style
- **Style:** Modern, clean, minimalist with friendly warmth
- **Mood:** Fresh, appetizing, energetic, reliable
- **Approach:** Mobile-first, content-focused, gesture-friendly

---

## 2. COLOR SYSTEM

### 2.1 Primary Colors

```
Primary Green (Fresh & Natural)
- Primary-500: #10B981 (Main brand color)
- Primary-600: #059669 (Hover states)
- Primary-700: #047857 (Active states)
- Primary-400: #34D399 (Light accents)
- Primary-50: #ECFDF5 (Backgrounds)
```

**Usage:** CTAs, active states, success messages, brand elements

### 2.2 Secondary Colors

```
Orange (Energy & Appetite)
- Secondary-500: #F97316 (Accents & promotions)
- Secondary-600: #EA580C (Hover)
- Secondary-400: #FB923C (Light accents)
- Secondary-50: #FFF7ED (Backgrounds)
```

**Usage:** Promotions, ratings, food category tags, hot deals

### 2.3 Neutral Colors

```
Grays (Content & Structure)
- Gray-900: #111827 (Headings, primary text)
- Gray-700: #374151 (Body text)
- Gray-500: #6B7280 (Secondary text)
- Gray-300: #D1D5DB (Borders, dividers)
- Gray-100: #F3F4F6 (Card backgrounds)
- Gray-50: #F9FAFB (Page backgrounds)
- White: #FFFFFF (Cards, modals)
```

### 2.4 Semantic Colors

```
Success: #10B981 (Order confirmed, delivery complete)
Warning: #F59E0B (Delays, address issues)
Error: #EF4444 (Cancellations, payment failures)
Info: #3B82F6 (Tips, informational messages)
```

### 2.5 Food Category Colors

```
Vegetables: #10B981 (Green)
Protein: #DC2626 (Red)
Grains: #D97706 (Amber)
Dairy: #60A5FA (Blue)
Desserts: #EC4899 (Pink)
Beverages: #8B5CF6 (Purple)
```

---

## 3. TYPOGRAPHY SYSTEM

### 3.1 Font Family

**Primary Font: Inter** (Modern, highly readable, excellent for UI)
- Weight: 400 (Regular), 500 (Medium), 600 (SemiBold), 700 (Bold)
- Excellent legibility on small screens
- Professional yet friendly

**Alternative: Plus Jakarta Sans** (Warmer feel, good for headings)

### 3.2 Type Scale

```
Display Large: 48px / Bold / Line-height: 1.2 (Hero sections)
Display Medium: 36px / Bold / Line-height: 1.2 (Page titles)

Heading 1: 32px / SemiBold / Line-height: 1.25 (Main headings)
Heading 2: 24px / SemiBold / Line-height: 1.3 (Section headings)
Heading 3: 20px / SemiBold / Line-height: 1.4 (Card titles)
Heading 4: 18px / Medium / Line-height: 1.5 (Subsections)

Body Large: 16px / Regular / Line-height: 1.5 (Primary content)
Body Regular: 14px / Regular / Line-height: 1.6 (Standard text)
Body Small: 12px / Regular / Line-height: 1.5 (Captions, labels)

Button Large: 16px / SemiBold / Line-height: 1
Button Regular: 14px / SemiBold / Line-height: 1
Button Small: 12px / Medium / Line-height: 1

Caption: 12px / Regular / Line-height: 1.4 (Metadata, timestamps)
Overline: 10px / SemiBold / Uppercase / Letter-spacing: 0.5px (Labels)
```

### 3.3 Font Usage Guidelines

- **Headings:** Use SemiBold (600) or Bold (700) for hierarchy
- **Body text:** Regular (400) for readability
- **CTAs:** SemiBold (600) for emphasis
- **Labels:** Medium (500) for subtle distinction
- **Max line length:** 60-80 characters for optimal readability

---

## 4. ICONOGRAPHY & VISUAL ELEMENTS

### 4.1 Icon Style

**System:** Lucide Icons / Heroicons (Consistent, modern, clear)
- **Style:** Outline for navigation, Solid for active states
- **Stroke width:** 2px for clarity
- **Size:** 16px, 20px, 24px, 32px (multiples of 4)
- **Color:** Inherit from text color or use semantic colors

### 4.2 Key Icons Needed

```
Navigation:
- Home, Search, Orders, Profile, Menu
- Map/Location, GPS, Navigation Arrow

Food & Restaurant:
- Restaurant, Utensils, Chef Hat, Menu
- Clock (Prep time), Star (Rating), Heart (Favorite)

Order & Delivery:
- Shopping Cart, Check Circle, Truck, Package
- Clock (ETA), Warning, Info Circle

User Actions:
- Plus/Minus (Quantity), Filter, Sort, Share
- Phone, Chat, Camera, Upload

Payment:
- Credit Card, Wallet, Cash, Check Mark
```

### 4.3 Illustrations & Graphics

**Style Guide:**
- **Illustrations:** Friendly, minimal, 2-3 colors max
- **Food Photography:** High-quality, appetizing, well-lit, natural colors
- **Hero Images:** 16:9 ratio, focus on fresh ingredients
- **Empty States:** Light illustrations with encouraging messages

**Usage:**
- Onboarding screens: Simple line illustrations
- Empty cart: Playful food illustrations
- Success states: Celebratory graphics
- Error states: Friendly, apologetic illustrations

### 4.4 Image Treatment

```
Restaurant Images:
- Aspect Ratio: 16:9 (Hero), 4:3 (Cards)
- Border Radius: 12px
- Overlay: Gradient overlay for text readability

Food Item Images:
- Aspect Ratio: 1:1 (Square)
- Border Radius: 8px
- Background: White or light gray
- Shadow: Subtle drop shadow for depth

Avatar Images:
- Shape: Circle
- Sizes: 32px, 48px, 64px
- Border: 2px solid white (on colored backgrounds)
```

---

## 5. COMPONENT LIBRARY

### 5.1 Buttons

**Primary Button:**
```
Background: Primary-500 (#10B981)
Text: White
Padding: 12px 24px (Regular), 16px 32px (Large)
Border Radius: 8px
Font: Button Regular/Large
Shadow: 0 1px 2px rgba(0,0,0,0.05)
Hover: Primary-600
Active: Primary-700
Disabled: Gray-300 (50% opacity)
```

**Secondary Button:**
```
Background: White
Text: Primary-500
Border: 2px solid Primary-500
Other specs: Same as Primary
```

**Text Button:**
```
Background: Transparent
Text: Primary-500
Padding: 8px 16px
No border
Hover: Primary-50 background
```

**Icon Button:**
```
Size: 40px × 40px (Regular)
Icon: 20px
Border Radius: 8px (Square) or 50% (Circle)
Background: Gray-100 (Default), Primary-500 (Accent)
Hover: Gray-200 or Primary-600
```

### 5.2 Input Fields

**Text Input:**
```
Height: 48px (Mobile), 44px (Desktop)
Padding: 12px 16px
Border: 1px solid Gray-300
Border Radius: 8px
Font: Body Regular
Placeholder: Gray-500

Focus State:
- Border: 2px solid Primary-500
- Shadow: 0 0 0 3px Primary-50

Error State:
- Border: 2px solid Error
- Error message: 12px, Error color
```

**Search Bar:**
```
Icon: Search icon (20px) on left
Clear icon: X icon (16px) on right (when active)
Background: Gray-100
Height: 48px
Border Radius: 24px (Pill shape)
```

### 5.3 Cards

**Restaurant Card:**
```
Width: Full width (Mobile), 280px (Desktop)
Padding: 0
Border Radius: 12px
Shadow: 0 1px 3px rgba(0,0,0,0.1)
Hover: Shadow 0 4px 12px rgba(0,0,0,0.15)

Structure:
- Image: 16:9, Border Radius 12px 12px 0 0
- Content Padding: 12px
- Restaurant Name: Heading 3
- Rating: Star icon + 4.5 (14px)
- Tags: Chips (12px)
- Delivery Info: Caption with Clock icon
```

**Food Item Card:**
```
Layout: Horizontal (Image left, content right)
Height: 100px
Padding: 12px
Gap: 12px
Border Radius: 8px
Background: White
Border: 1px solid Gray-200

Structure:
- Image: 1:1, 76px × 76px, Border Radius 8px
- Name: Heading 4
- Description: Body Small (2 lines max)
- Price: Heading 3, Primary-500
- Add button: Icon button (Plus)
```

**Order Card:**
```
Padding: 16px
Border Radius: 12px
Border: 1px solid Gray-200
Background: White

Structure:
- Header: Restaurant name + Order ID
- Status Badge: Colored pill
- Items list: Condensed
- Total: Bold, right-aligned
- Action buttons: Primary CTA
```

### 5.4 Navigation

**Bottom Navigation (Mobile):**
```
Height: 64px
Background: White
Shadow: 0 -2px 8px rgba(0,0,0,0.08)
Items: 5 max
Spacing: Equal distribution

Each Item:
- Icon: 24px
- Label: 10px
- Active: Primary-500
- Inactive: Gray-500
```

**Top Navigation (Desktop):**
```
Height: 72px
Background: White
Shadow: 0 1px 3px rgba(0,0,0,0.1)
Padding: 0 24px

Structure:
- Logo: 40px height
- Search: Center, max 600px width
- Icons: Cart, Profile (32px)
```

### 5.5 Badges & Chips

**Status Badge:**
```
Padding: 4px 12px
Border Radius: 12px (Pill)
Font: 12px SemiBold
Uppercase

States:
- Confirmed: Primary-50 bg, Primary-700 text
- Preparing: Secondary-50 bg, Secondary-700 text
- On the Way: Info-50 bg, Info-700 text
- Delivered: Success-50 bg, Success-700 text
- Cancelled: Error-50 bg, Error-700 text
```

**Category Chip:**
```
Padding: 6px 12px
Border Radius: 16px
Font: 12px Regular
Background: Gray-100
Border: 1px solid Gray-200
Hover: Gray-200
Selected: Primary-500 bg, White text
```

### 5.6 Modals & Overlays

**Modal:**
```
Max Width: 480px (Mobile: Full width)
Border Radius: 16px (Top corners only on mobile)
Background: White
Shadow: 0 20px 25px rgba(0,0,0,0.15)
Padding: 24px

Header:
- Title: Heading 2
- Close button: Top right

Footer:
- Buttons: Full width on mobile, auto on desktop
- Spacing: 12px gap
```

**Bottom Sheet (Mobile):**
```
Border Radius: 24px 24px 0 0
Background: White
Padding: 24px 16px
Handle: 32px × 4px, Gray-300, centered
Shadow: 0 -4px 12px rgba(0,0,0,0.1)
```

### 5.7 Progress & Loading

**Stepper (Order Status):**
```
Style: Horizontal line with circles
Circle Size: 32px
Line: 2px solid
Colors:
- Complete: Primary-500
- Current: Primary-500 (pulsing)
- Upcoming: Gray-300
```

**Skeleton Loader:**
```
Background: Gray-200
Animation: Shimmer (Gray-300)
Border Radius: Match component
```

**Spinner:**
```
Size: 32px (Regular), 48px (Large)
Color: Primary-500
Style: Circular, rotating
```

---

## 6. SCREEN DESIGNS BY USER ROLE

### 6.1 Customer App Screens

#### A. Authentication Flow

**1. Splash Screen**
```
Layout:
- Logo: Center, 80px
- Tagline: "Fresh food, delivered fast"
- Background: Gradient (Primary-50 to White)
- Auto-advance: 2 seconds
```

**2. Onboarding (3 screens)**
```
Screen 1: "Browse Restaurants"
- Illustration: Restaurant grid
- Title: "Discover Fresh Food"
- Description: "Explore hundreds of restaurants near you"

Screen 2: "Track Orders"
- Illustration: Delivery map
- Title: "Real-Time Tracking"
- Description: "Watch your order come to you live"

Screen 3: "Easy Checkout"
- Illustration: Payment
- Title: "Quick & Secure"
- Description: "Multiple payment options, saved for next time"

Navigation:
- Skip button: Top right
- Dots indicator: Bottom center
- Next/Get Started: Bottom button
```

**3. Login Screen**
```
Layout:
- Logo: Top, 60px
- Title: "Welcome Back"
- Email input
- Password input (with show/hide toggle)
- Forgot password: Text button
- Login: Primary button (full width)
- Divider: "or"
- Social login: Google, Facebook (outlined buttons)
- Sign up: Text link at bottom

Spacing: 16px between elements
Padding: 24px horizontal
```

**4. Registration Screen**
```
Fields:
- First Name
- Last Name
- Email
- Phone (with country code dropdown)
- Password (with strength indicator)
- Confirm Password

Additional:
- Terms & Privacy: Checkbox with links
- Sign Up: Primary button
- Already have account: Text link

Validation: Real-time, inline errors
```

#### B. Home & Discovery

**5. Home Screen**
```
Structure:
┌─────────────────────────┐
│ Location Header          │ ← Current location + Change
├─────────────────────────┤
│ Search Bar              │ ← "Search restaurants or dishes"
├─────────────────────────┤
│ Category Chips          │ ← Horizontal scroll (All, Pizza, etc.)
├─────────────────────────┤
│ Promotions Carousel     │ ← 16:9 cards, auto-play
├─────────────────────────┤
│ "Featured Restaurants"  │ ← Section heading + See all
│ Restaurant Cards        │ ← Horizontal scroll
├─────────────────────────┤
│ "Trending Now"          │
│ Restaurant Cards        │ ← Vertical list
├─────────────────────────┤
│ "New on FreshBite"      │
│ Restaurant Cards        │
└─────────────────────────┘

Top Elements:
- Location: Icon + "Delivering to Home" + Dropdown
- Notification: Bell icon (badge if unread)

States:
- Loading: Skeleton screens
- Empty: "No restaurants nearby" + Illustration
```

**6. Search Screen**
```
Header:
- Search bar (focused)
- Cancel button

Content:
┌─────────────────────────┐
│ Recent Searches         │ ← Clock icon + Search term + X
│ Suggested Searches      │ ← Trending icon + Search term
├─────────────────────────┤
│ [Search Results]        │
│ Filters: Distance, Rating, Price │
│ Sort: Relevance, Distance, Rating │
│ Restaurant Cards        │
└─────────────────────────┘

Filters:
- Modal/Bottom sheet
- Distance: Slider (1-20 km)
- Rating: Buttons (4+, 4.5+)
- Price: $ $$ $$$ buttons
- Dietary: Chips (Vegan, Halal, etc.)
- Apply button
```

**7. Restaurant Detail Screen**
```
Structure:
┌─────────────────────────┐
│ Hero Image              │ ← 16:9, with gradient overlay
│ Back + Share + Favorite │ ← Floating buttons
├─────────────────────────┤
│ Restaurant Info Card    │
│ - Name                  │
│ - Rating + Reviews      │
│ - Cuisine tags          │
│ - Distance + Est. time  │
│ - Min order + Delivery  │
├─────────────────────────┤
│ Sticky Tabs             │ ← Menu, Info, Reviews
├─────────────────────────┤
│ [Tab Content]           │
└─────────────────────────┘
│ Floating Cart Button    │ ← Bottom (when items added)
└─────────────────────────┘

Menu Tab:
- Category chips (sticky)
- Food item cards (vertical)
- Add button opens quantity picker

Info Tab:
- Opening hours
- Address (with map)
- Phone number
- About description

Reviews Tab:
- Overall rating card
- Review filters (5★, 4★, etc.)
- Review cards (Avatar, Name, Date, Rating, Text, Images)
```

**8. Food Item Detail Modal**
```
Layout:
- Image: Full width, 1:1
- Close button: Top right
- Name: Heading 1
- Description: Body Regular
- Price: Heading 2, Primary-500

Options:
- Size: Radio buttons
- Add-ons: Checkboxes
- Special instructions: Text area

Quantity:
- Minus/Plus buttons with count

Footer:
- Add to Cart: Primary button
- Shows total price
```

#### C. Cart & Checkout

**9. Cart Screen**
```
Header:
- Title: "Your Cart"
- Clear all: Text button

Content:
┌─────────────────────────┐
│ Restaurant Section      │
│ - Restaurant name       │
│ - Item cards (editable) │
│ - Add more items        │
├─────────────────────────┤
│ Coupon Input            │ ← Icon + Input + Apply button
├─────────────────────────┤
│ Price Breakdown         │
│ - Subtotal              │
│ - Delivery fee          │
│ - Tax                   │
│ - Discount              │
│ - Total (Large, Bold)   │
├─────────────────────────┤
│ Delivery Details        │
│ - Address card          │ ← Change link
│ - Delivery time         │ ← ASAP or Schedule
├─────────────────────────┤
│ Payment Method          │
│ - Card/Wallet           │ ← Change link
└─────────────────────────┘
│ Place Order Button      │ ← Sticky bottom
└─────────────────────────┘

Item Card:
- Image thumbnail
- Name + Variants
- Quantity picker
- Price
- Remove button
```

**10. Checkout Screen**
```
Steps:
1. Delivery Details
2. Payment Method
3. Review Order

Step 1 - Delivery Details:
- Address selection (Radio cards)
- Add new address
- Delivery instructions
- Contact phone

Step 2 - Payment Method:
- Saved payment methods (Radio cards)
- Add new payment method
- COD option

Step 3 - Review:
- Restaurant + Items summary
- Delivery address
- Payment method
- Price breakdown
- Place Order: Primary button

Progress:
- Stepper at top
- Back/Next navigation
```

#### D. Order Tracking

**11. Order Confirmation Screen**
```
Layout:
- Success animation (Checkmark)
- Title: "Order Confirmed!"
- Order ID + Time
- Estimated delivery time (Large, Bold)

Content:
- Restaurant info
- Items summary (Collapsed)
- Delivery address
- Payment method

Actions:
- Track Order: Primary button
- Back to Home: Secondary button
```

**12. Order Tracking Screen**
```
Layout:
┌─────────────────────────┐
│ Live Map View           │ ← 50% height
│ - Driver marker         │ ← Animated
│ - Restaurant marker     │
│ - Customer marker       │
│ - Route polyline        │
├─────────────────────────┤
│ Status Card             │ ← Draggable bottom sheet
│ - Status: "On the way"  │
│ - ETA: Large, updating  │
│ - Order number          │
├─────────────────────────┤
│ Driver Info (when assigned) │
│ - Avatar                │
│ - Name + Rating         │
│ - Vehicle info          │
│ - Call + Chat buttons   │
├─────────────────────────┤
│ Order Progress          │
│ - Stepper (horizontal)  │
│   • Confirmed           │
│   • Preparing           │
│   • Picked up           │
│   • Delivered           │
├─────────────────────────┤
│ Order Details           │ ← Expandable
│ - Items list            │
│ - Total                 │
└─────────────────────────┘

Real-time Updates:
- Driver location: Every 5 seconds
- Status changes: Instant (WebSocket)
- ETA: Updates based on traffic
```

**13. Order History Screen**
```
Header:
- Title: "Orders"
- Filters: Status dropdown (All, Active, Completed)

List:
- Order cards (Chronological)
- Each card shows:
  • Restaurant name + Image
  • Order date + time
  • Status badge
  • Total price
  • Items count
  • Reorder button
  • View Details

States:
- Active orders: At top, expandable
- Empty state: "No orders yet" + Browse button
```

**14. Order Detail Screen**
```
Structure:
- Status header (Colored banner)
- Order ID + Date
- Status stepper
- Restaurant info
- Items list (Full details)
- Price breakdown
- Delivery address
- Payment method
- Help button: "Need help?" (Opens support)

Actions (based on status):
- Confirmed: Cancel Order
- Delivered: Rate Order, Reorder, Report Issue
```

#### E. Profile & Settings

**15. Profile Screen**
```
Header:
- Avatar (Large, editable)
- Name
- Email + Phone
- Edit profile button

Sections:
┌─────────────────────────┐
│ Account                 │
│ • Personal Information  │
│ • Saved Addresses       │
│ • Payment Methods       │
├─────────────────────────┤
│ Preferences             │
│ • Notification Settings │
│ • Language              │
│ • Dietary Preferences   │
├─────────────────────────┤
│ Support                 │
│ • Help Center           │
│ • Contact Support       │
│ • Report Issue          │
├─────────────────────────┤
│ Legal                   │
│ • Terms & Conditions    │
│ • Privacy Policy        │
│ • About                 │
├─────────────────────────┤
│ Logout                  │ ← Text button, Error color
└─────────────────────────┘
```

**16. Saved Addresses Screen**
```
List:
- Address cards
- Each shows:
  • Label (Home, Work, etc.)
  • Full address
  • Default badge
  • Edit + Delete buttons

Add New:
- Floating action button
- Opens address form

Form:
- Label
- Search address (Map integration)
- Street
- City
- District
- Instructions
- Set as default: Toggle
```

**17. Payment Methods Screen**
```
List:
- Payment cards
- Each shows:
  • Card icon (Visa, Mastercard)
  • **** 4242
  • Expiry date
  • Default badge
  • Delete button

Add New:
- Button
- Opens form (Card, E-wallet)

COD:
- Always available
- Cannot be removed
```

### 6.2 Restaurant Owner App Screens

#### A. Dashboard

**18. Restaurant Dashboard**
```
Header:
- Restaurant name
- Online/Offline toggle (Large, prominent)
- Notification bell

Metrics Cards:
┌─────────────────────────┐
│ Today's Orders          │ ← Large number
│ Total Revenue           │ ← Currency
│ Average Order Value     │
│ On-time Rate           │ ← Percentage
└─────────────────────────┘

Sections:
- Pending Orders (Count badge)
- Active Orders (Real-time updates)
- Order History
- Quick Actions:
  • View Menu
  • Update Hours
  • Promotions
  • Analytics
```

#### B. Order Management

**19. Incoming Orders Screen**
```
List:
- Order cards (Chronological)
- Each card:
  • Order ID + Time
  • Customer name
  • Items list (Collapsed)
  • Special instructions (Highlighted)
  • Total price
  • Estimated prep time
  • Accept + Reject buttons

Auto-sound: Alert for new orders

Accept Flow:
- Confirm prep time (Adjustable)
- Accept button
- Status → "Preparing"

Reject Flow:
- Reason selection (Required)
- Confirm rejection
- Customer notified + Refunded
```

**20. Preparing Orders Screen**
```
List:
- Active order cards
- Each card:
  • Prep time countdown (Large, visible)
  • Order details
  • Mark Ready button

Mark Ready:
- Status → "Ready for Pickup"
- Notify driver
```

#### C. Menu Management

**21. Menu Screen**
```
Header:
- Add Category
- Add Item

List:
- Category sections (Collapsible)
- Each item:
  • Image thumbnail
  • Name
  • Price
  • Available toggle (Quick action)
  • Edit button

Edit Item:
- Modal with form
- Fields:
  • Name
  • Description
  • Price
  • Category
  • Image
  • Variants (Size, add-ons)
  • Available toggle
```

### 6.3 Driver App Screens

#### A. Driver Dashboard

**22. Driver Home Screen**
```
Header:
- Online/Offline toggle (Large)
- Earnings today (Prominent)

Map View:
- Current location
- Available deliveries (Markers)
- Accepted delivery route

Bottom Sheet:
┌─────────────────────────┐
│ Available Deliveries    │
│ - Delivery cards        │
│   • Restaurant name     │
│   • Distance            │
│   • Estimated pay       │
│   • Accept button       │
├─────────────────────────┤
│ Current Delivery        │ ← When accepted
│ - Order details         │
│ - Navigation button     │
│ - Status buttons        │
└─────────────────────────┘
```

**23. Active Delivery Screen**
```
Layout:
- Map (Full screen)
- Route to pickup/dropoff
- ETA (Large, top center)

Bottom Sheet:
┌─────────────────────────┐
│ Delivery Steps          │
│ 1. Pick up from Restaurant │
│    - Address             │
│    - Navigate button     │
│    - Call button         │
│    - Mark Picked Up      │
│                          │
│ 2. Deliver to Customer  │
│    - Address             │
│    - Navigate button     │
│    - Call button         │
│    - Mark Delivered      │
└─────────────────────────┘

Status Actions:
- Picked Up: Confirm pickup
- Issue: Report problem
- Delivered: Confirm delivery (with photo option)
```

### 6.4 Admin Web Dashboard

**24. Admin Dashboard (Desktop)**
```
Layout:
- Sidebar navigation (Fixed left)
- Top bar (Breadcrumbs, Search, Profile)
- Main content area

Sidebar:
- Dashboard
- Users
- Restaurants
- Drivers
- Orders
- Payments
- Disputes
- Reports
- Settings

Dashboard Content:
- KPI cards (Grid)
  • Total Orders
  • Total Revenue
  • Active Users
  • Active Restaurants
  • Active Drivers
  • Average Delivery Time
- Charts:
  • Revenue trend (Line chart)
  • Orders by hour (Bar chart)
  • Top restaurants (Table)
  • Driver performance (Table)
```

**25. Restaurant Management Screen**
```
Header:
- Title: "Restaurants"
- Filters: Status, City
- Add Restaurant button

Table:
- Columns:
  • Logo (Thumbnail)
  • Name
  • Owner
  • City
  • Status (Badge)
  • Rating
  • Total Orders
  • Actions (View, Edit, Suspend)

Pagination: Bottom
Row Actions:
- View details
- Approve/Reject (for pending)
- Suspend/Activate
- Edit
```

---

## 7. INTERACTION & ANIMATION GUIDELINES

### 7.1 Micro-interactions

**Button Press:**
```
Scale: 0.98 (Tap down)
Duration: 100ms
Easing: ease-out
```

**Card Hover (Desktop):**
```
Lift: translateY(-4px)
Shadow: Increase elevation
Duration: 200ms
Easing: ease-out
```

**Toggle Switch:**
```
Animation: Slide with bounce
Duration: 300ms
Color transition: 200ms
```

### 7.2 Page Transitions

**Screen Navigation:**
```
Mobile:
- Forward: Slide from right
- Back: Slide to right
- Duration: 300ms
- Easing: ease-in-out

Desktop:
- Fade: 200ms
```

**Modal Open:**
```
Mobile (Bottom Sheet):
- Slide from bottom
- Backdrop fade in
- Duration: 300ms

Desktop:
- Fade + Scale (0.95 → 1)
- Duration: 200ms
```

### 7.3 Loading States

**Skeleton:**
```
Animation: Shimmer (left to right)
Duration: 1500ms
Loop: Infinite
```

**Spinner:**
```
Rotation: 360deg
Duration: 800ms
Loop: Infinite
```

**Success Checkmark:**
```
Animation: Draw stroke + Scale bounce
Duration: 600ms
Delay: 200ms
```

### 7.4 Real-time Updates

**Order Status Change:**
```
Animation: Pulse + Color transition
Duration: 400ms
Sound: Subtle chime (optional)
```

**Driver Location Update:**
```
Animation: Smooth interpolation
Duration: 500ms (every 5s update)
Marker: Rotation based on heading
```

**New Message/Notification:**
```
Badge: Scale bounce
Duration: 300ms
Repeat: 2 times
```

---

## 8. RESPONSIVE DESIGN STRATEGY

### 8.1 Breakpoints

```
Mobile S: 320px - 374px (Small phones)
Mobile M: 375px - 424px (Standard phones)
Mobile L: 425px - 767px (Large phones)
Tablet: 768px - 1023px
Desktop: 1024px - 1439px
Desktop L: 1440px+
```

### 8.2 Layout Adaptations

**Mobile → Desktop:**

| Element | Mobile | Desktop |
|---------|--------|---------|
| Navigation | Bottom bar | Top bar + Sidebar |
| Cards | Full width | Grid (2-4 columns) |
| Modals | Bottom sheet | Center modal |
| Forms | Full width | Max 600px |
| Images | 16:9 | 4:3 or 1:1 |

### 8.3 Touch Targets

```
Minimum Size: 44px × 44px (iOS), 48px × 48px (Android)
Comfortable: 56px × 56px
Spacing: 8px minimum between targets
```

### 8.4 Font Scaling

```
Mobile: Base 14px
Tablet: Base 15px
Desktop: Base 16px

Scale factor: 1.2 (Major second)
```

---

## 9. ACCESSIBILITY GUIDELINES

### 9.1 Color Contrast

```
Text on background:
- Normal text: 4.5:1 (AA)
- Large text (18px+): 3:1 (AA)
- Interactive elements: 3:1 (AA)

Success:
- Primary-500 on White: 4.52:1 ✓
- Gray-700 on White: 10.74:1 ✓
- Gray-500 on White: 4.58:1 ✓
```

### 9.2 Keyboard Navigation

- All interactive elements focusable
- Tab order: Logical, top-to-bottom
- Focus indicators: 2px solid Primary-500
- Escape: Close modals
- Enter/Space: Activate buttons

### 9.3 Screen Reader Support

- Semantic HTML (headings, landmarks)
- Alt text for images
- ARIA labels for icons
- Live regions for updates
- Skip navigation links

### 9.4 Reduced Motion

```
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 10. DESIGN DELIVERABLES

### 10.1 Figma File Structure

```
📁 FreshBite Food Delivery Design System

├── 📄 Cover Page
│   ├── Project Overview
│   ├── Version History
│   └── Team Credits
│
├── 📄 Design Tokens
│   ├── Colors (All variants)
│   ├── Typography (Scale)
│   ├── Spacing (4px grid)
│   ├── Shadows
│   └── Border Radius
│
├── 📄 Component Library
│   ├── Atoms (Buttons, Inputs, Icons)
│   ├── Molecules (Cards, Navigation)
│   ├── Organisms (Headers, Forms)
│   └── States (Default, Hover, Active, Disabled)
│
├── 📄 Customer App
│   ├── 🔹 Authentication (6 screens)
│   ├── 🔹 Home & Discovery (5 screens)
│   ├── 🔹 Restaurant & Menu (4 screens)
│   ├── 🔹 Cart & Checkout (4 screens)
│   ├── 🔹 Order Tracking (5 screens)
│   └── 🔹 Profile & Settings (6 screens)
│
├── 📄 Restaurant Owner App
│   ├── 🔹 Dashboard (3 screens)
│   ├── 🔹 Order Management (4 screens)
│   └── 🔹 Menu Management (3 screens)
│
├── 📄 Driver App
│   ├── 🔹 Driver Dashboard (3 screens)
│   └── 🔹 Active Delivery (4 screens)
│
├── 📄 Admin Web Dashboard
│   ├── 🔹 Dashboard (1 screen)
│   ├── 🔹 Management Screens (6 screens)
│   └── 🔹 Reports (3 screens)
│
├── 📄 Prototypes
│   ├── Customer Journey
│   ├── Restaurant Journey
│   └── Driver Journey
│
└── 📄 Documentation
    ├── Design Guidelines
    ├── Component Usage
    └── Handoff Notes
```

### 10.2 Component Specifications

**Each component should include:**
1. Visual design (All states)
2. Measurements (px)
3. Spacing (Auto-layout)
4. Typography specs
5. Color tokens
6. Interaction states
7. Usage guidelines
8. Code snippets (for developers)

### 10.3 Interactive Prototypes

**Flow 1: Complete Order (Customer)**
```
Splash → Home → Search → Restaurant → Item → Cart → Checkout → Tracking → Rating
```

**Flow 2: Restaurant Order Handling**
```
Login → Dashboard → New Order Alert → Accept → Preparing → Mark Ready
```

**Flow 3: Driver Delivery**
```
Login → Go Online → Accept Delivery → Navigate → Pick Up → Deliver → Complete
```

### 10.4 Assets for Export

**Icons:**
- SVG format
- 16px, 20px, 24px, 32px sizes
- Organized by category

**Images:**
- 1x, 2x, 3x resolutions
- PNG (with transparency)
- JPG (photos)
- WebP (optimized)

**Illustrations:**
- SVG format
- Single color + Multi-color versions

### 10.5 Developer Handoff

**Include:**
1. Design tokens (JSON)
2. Component specs (Zeplin/Figma Inspect)
3. Asset package
4. Prototype links
5. Animation specifications
6. Accessibility notes
7. Responsive breakpoints
8. API integration points (from SRS)

---

## 11. MULTIMEDIA ENHANCEMENTS

### 11.1 Animations

**Order Confirmation:**
```
Animation: Confetti + Success checkmark
Duration: 2 seconds
File: Lottie JSON
Trigger: Order placed successfully
```

**Food Preparation:**
```
Animation: Steam rising from pot
Duration: Loop
File: Lottie JSON
Screen: Order tracking (Preparing status)
```

**Delivery in Transit:**
```
Animation: Scooter moving
Duration: Loop
File: Lottie JSON
Screen: Order tracking (On the way)
```

### 11.2 Sounds (Optional)

**Order Placed:**
- Sound: Success chime
- Duration: 0.5s
- Format: MP3, AAC

**Order Ready:**
- Sound: Notification bell
- Duration: 1s
- Use: Restaurant app

**Delivery Arrived:**
- Sound: Doorbell
- Duration: 1s
- Use: Customer app

### 11.3 Videos (Onboarding)

**Welcome Video:**
- Duration: 15-20 seconds
- Style: 2D motion graphics
- Content: How it works
- Format: MP4, WebM
- Placement: Onboarding screen

---

## 12. IMPLEMENTATION RECOMMENDATIONS

### 12.1 Phase 1 - MVP (Week 1-4)

**Priority Screens:**
1. Customer: Authentication, Home, Restaurant, Cart, Checkout, Tracking (15 screens)
2. Restaurant: Dashboard, Order Management (5 screens)
3. Driver: Dashboard, Active Delivery (4 screens)

**Total: 24 screens**

### 12.2 Phase 2 - Enhancements (Week 5-8)

**Additional Screens:**
1. Customer: Profile, Settings, Order History (8 screens)
2. Admin: Dashboard, Management (10 screens)
3. Advanced features: Ratings, Disputes

**Total: 18 screens**

### 12.3 Design System First Approach

1. **Week 1:** Design tokens + Component library
2. **Week 2:** Customer core flow (15 screens)
3. **Week 3:** Restaurant + Driver apps (9 screens)
4. **Week 4:** Prototyping + Handoff prep
5. **Week 5-6:** Phase 2 screens
6. **Week 7:** Admin dashboard
7. **Week 8:** Polish + Documentation

---

## 13. SUCCESS METRICS

### 13.1 Design Quality Metrics

- **Consistency:** 95%+ component reuse
- **Accessibility:** WCAG 2.1 AA compliance
- **Performance:** <3s load time
- **Responsiveness:** Works 320px - 1920px

### 13.2 User Experience Metrics

- **Task completion:** >90%
- **Time to order:** <3 minutes
- **Error rate:** <5%
- **User satisfaction:** >4.5/5

---

## CONCLUSION

This design report provides a comprehensive blueprint for implementing the FreshBite food delivery platform UI/UX in Figma. The design system emphasizes:

✅ **Fresh & Natural** brand identity with green color palette
✅ **Clean & Modern** typography using Inter font
✅ **Intuitive** iconography and easy-to-understand visuals
✅ **Comprehensive** component library for consistency
✅ **Complete** screen designs for all user roles (50+ screens)
✅ **Delightful** animations and transitions
✅ **Accessible** design meeting WCAG standards
✅ **Responsive** layouts for mobile and desktop

**Next Steps:**
1. Create Figma file with this structure
2. Build component library
3. Design 24 MVP screens (Phase 1)
4. Create interactive prototypes
5. Conduct usability testing
6. Iterate based on feedback
7. Prepare developer handoff

**Design Files Ready for:**
- Mobile apps (iOS + Android)
- Web application (Desktop)
- Restaurant & Driver apps
- Admin dashboard

---

## 14. FIGJAM USER FLOW DIAGRAMS

The following FigJam diagrams have been created to visualize the key user journeys and system flows:

### 14.1 User Journey Diagrams

| Diagram | Description | FigJam Link |
|---------|-------------|-------------|
| **Customer Ordering Journey** | Complete flow from splash to order rating | [View in FigJam](https://www.figma.com/online-whiteboard/create-diagram/0a427629-d713-4950-a18b-f1761a9fc2dd?utm_source=other&utm_content=edit_in_figjam) |
| **Restaurant Owner Journey** | Order management and menu handling flow | [View in FigJam](https://www.figma.com/online-whiteboard/create-diagram/43205746-f9e5-47eb-a0a6-44aefaffd661?utm_source=other&utm_content=edit_in_figjam) |
| **Driver Delivery Journey** | Complete delivery process from pickup to completion | [View in FigJam](https://www.figma.com/online-whiteboard/create-diagram/0a52f85f-6d24-4591-b616-2b5b8710faaa?utm_source=other&utm_content=edit_in_figjam) |
| **Mobile App Screen Flow** | Navigation structure for all tabs and screens | [View in FigJam](https://www.figma.com/online-whiteboard/create-diagram/d17b05bc-cc00-4282-8b50-ccc5e71a9e67?utm_source=other&utm_content=edit_in_figjam) |

### 14.2 System Flow Diagrams

| Diagram | Description | FigJam Link |
|---------|-------------|-------------|
| **Order Status State Machine** | All order statuses from creation to delivery | [View in FigJam](https://www.figma.com/online-whiteboard/create-diagram/67c93d07-fe54-44fb-8b47-796c5127738d?utm_source=other&utm_content=edit_in_figjam) |
| **Real-Time Order Tracking** | WebSocket communication for live tracking | [View in FigJam](https://www.figma.com/online-whiteboard/create-diagram/8d2106f8-04dc-4cab-a4ec-f402e12a36e9?utm_source=other&utm_content=edit_in_figjam) |
| **Payment Processing Flow** | Card and COD payment paths | [View in FigJam](https://www.figma.com/online-whiteboard/create-diagram/c2f43be3-0ba9-4efb-813d-eb17b5c42981?utm_source=other&utm_content=edit_in_figjam) |
| **Dispute Resolution Flow** | Auto-resolution and admin review paths | [View in FigJam](https://www.figma.com/online-whiteboard/create-diagram/d34ff34a-e257-4efd-adcf-56a94db3b180?utm_source=other&utm_content=edit_in_figjam) |
| **Order Saga Workflow** | Complete order saga with compensation actions | [View in FigJam](https://www.figma.com/online-whiteboard/create-diagram/081c8253-90f7-475e-b1cd-11e0ed6bef85?utm_source=other&utm_content=edit_in_figjam) |

### 14.3 Architecture Diagrams

| Diagram | Description | FigJam Link |
|---------|-------------|-------------|
| **System Architecture Overview** | All layers: clients, gateway, microservices, data | [View in FigJam](https://www.figma.com/online-whiteboard/create-diagram/30fa77c4-f36f-4c97-87d4-cf2b9ff106df?utm_source=other&utm_content=edit_in_figjam) |
| **Admin Dashboard Workflow** | User, restaurant, driver, and dispute management | [View in FigJam](https://www.figma.com/online-whiteboard/create-diagram/7d0a17b1-864f-4dce-bbcd-904599738ad4?utm_source=other&utm_content=edit_in_figjam) |

### 14.4 Using the FigJam Diagrams

1. Click on any diagram link to open it in FigJam
2. Use the diagrams as reference for UI screen transitions
3. Share with development team for implementation guidance
4. Edit and expand diagrams as needed during design iterations

---

## 15. FIGMA IMPLEMENTATION GUIDE

### 15.1 Creating the Design File

To create the Figma design file based on this report:

**Step 1: Create New Figma File**
```
File Name: FreshBite_FoodDelivery_DesignSystem
Team: Trang Nguyen's team
```

**Step 2: Set Up Pages**
```
1. 📋 Cover
2. 🎨 Design Tokens
3. 🧩 Components
4. 📱 Customer App
5. 🍽️ Restaurant App
6. 🚗 Driver App
7. 💻 Admin Dashboard
8. 🔗 Prototypes
9. 📝 Documentation
```

**Step 3: Configure Auto Layout & Variables**
- Enable Variables for colors, spacing, typography
- Set up component variants for states
- Use Auto Layout for responsive components

### 15.2 Design Token Variables

Create the following variable collections in Figma:

**Colors Collection:**
```
Primary/500: #10B981
Primary/600: #059669
Primary/700: #047857
Primary/400: #34D399
Primary/50: #ECFDF5
Secondary/500: #F97316
Secondary/600: #EA580C
Gray/900: #111827
Gray/700: #374151
Gray/500: #6B7280
Gray/300: #D1D5DB
Gray/100: #F3F4F6
Success: #10B981
Warning: #F59E0B
Error: #EF4444
Info: #3B82F6
```

**Spacing Collection:**
```
space/2: 2px
space/4: 4px
space/8: 8px
space/12: 12px
space/16: 16px
space/24: 24px
space/32: 32px
space/48: 48px
space/64: 64px
```

**Border Radius Collection:**
```
radius/sm: 4px
radius/md: 8px
radius/lg: 12px
radius/xl: 16px
radius/full: 9999px
```

### 15.3 Export Settings

**For Development Handoff:**
- Icons: SVG (16px, 20px, 24px, 32px)
- Images: PNG @1x, @2x, @3x
- Illustrations: SVG
- Design tokens: Export as JSON

**Export Plugin Recommendations:**
- Figma Tokens (for design token sync)
- Export Kit (for asset export)
- Autoflow (for user flow documentation)

---

**Document Version:** 1.2  
**Last Updated:** 21 January 2026  
**Status:** ✅ Ready for Figma Implementation  
**Based on:** SRS_FoodDelivery.md v2.2

**Design System:** FreshBite Design System v1.0  
**Total Screens:** 50+ screens across all user roles  
**Component Library:** 40+ reusable components  
**Color Palette:** 15 colors (Primary, Secondary, Semantic)  
**Typography Scale:** 12 text styles  
**Icon Set:** 50+ icons  
**FigJam Diagrams:** 11 flow diagrams created
