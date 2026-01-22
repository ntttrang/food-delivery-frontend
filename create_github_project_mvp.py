#!/usr/bin/env python3
"""
Create GitHub Project MVP with EPICs, User Stories, Sprints, and Tasks
Uses GitHub CLI (gh) and GraphQL API to create issues with proper parent-child relationships.
"""

import subprocess
import json
import time
import sys
from typing import Dict, List, Optional

# Color codes for output
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'


def run_command(cmd: List[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=check)
        return result
    except subprocess.CalledProcessError as e:
        print(f"{RED}Error running command: {' '.join(cmd)}{RESET}")
        print(f"{RED}Error: {e.stderr}{RESET}")
        raise


def get_repo_info() -> Dict[str, str]:
    """Get repository owner and name."""
    result = run_command(["gh", "repo", "view", "--json", "owner,name"])
    repo_data = json.loads(result.stdout)
    return {
        "owner": repo_data["owner"]["login"],
        "name": repo_data["name"]
    }


def create_github_project(title: str, template: str = "scrum") -> str:
    """Create a GitHub project and return its ID."""
    print(f"{BLUE}Creating GitHub project: {title}...{RESET}")
    
    repo_info = get_repo_info()
    
    # Try using gh project create (for Projects v2)
    try:
        result = run_command(
            ["gh", "project", "create", title, "--format", "json"],
            check=False
        )
        if result.returncode == 0:
            try:
                project_data = json.loads(result.stdout)
                project_id = project_data.get("id") or project_data.get("number")
                if project_id:
                    print(f"{GREEN}✓ Created project: {title} (ID: {project_id}){RESET}")
                    return str(project_id)
            except json.JSONDecodeError:
                pass
    except:
        pass
    
    # Fallback: Use GraphQL API
    print(f"{YELLOW}Using GraphQL API to create project...{RESET}")
    # Note: This requires getting the owner's node ID first
    # For simplicity, we'll just create issues and link them manually
    print(f"{YELLOW}Project creation skipped. Issues will be created without project assignment.{RESET}")
    return ""


def create_issue(title: str, body: str, labels: Optional[List[str]] = None) -> str:
    """Create a GitHub issue and return its node ID."""
    repo_info = get_repo_info()
    
    # Create issue using gh CLI
    cmd = ["gh", "issue", "create", "--title", title, "--body", body]
    if labels:
        # Create labels if they don't exist (ignore errors)
        for label in labels:
            try:
                run_command(["gh", "label", "create", label, "--force"], check=False)
            except:
                pass
        cmd.extend(["--label", ",".join(labels)])
    
    result = run_command(cmd)
    
    # Extract issue number from output
    output = result.stdout.strip()
    issue_number = None
    
    # Try different patterns to extract issue number
    if "#" in output:
        parts = output.split("#")
        for part in parts:
            if part.strip().isdigit():
                issue_number = part.strip()
                break
    
    if not issue_number:
        # Try parsing from stderr or different format
        if "created" in output.lower():
            words = output.split()
            for word in words:
                if word.startswith("#") and word[1:].isdigit():
                    issue_number = word[1:]
                    break
    
    if not issue_number:
        print(f"{RED}Failed to extract issue number from: {output}{RESET}")
        print(f"{YELLOW}Issue may have been created. Check manually.{RESET}")
        return ""
    
    # Get issue node ID using GraphQL
    query = """
    query GetIssue($owner: String!, $repo: String!, $number: Int!) {
      repository(owner: $owner, name: $repo) {
        issue(number: $number) {
          id
          number
        }
      }
    }
    """
    
    variables = {
        "owner": repo_info["owner"],
        "repo": repo_info["name"],
        "number": int(issue_number)
    }
    
    try:
        cmd = [
            "gh", "api", "graphql",
            "-f", f"query={query}",
            "-f", f"variables={json.dumps(variables)}"
        ]
        
        result = run_command(cmd)
        data = json.loads(result.stdout)
        issue_id = data.get("data", {}).get("repository", {}).get("issue", {}).get("id", "")
        
        if issue_id:
            print(f"{GREEN}✓ Created issue #{issue_number}: {title[:50]}...{RESET}")
            return issue_id
        else:
            print(f"{YELLOW}⚠ Created issue #{issue_number} but couldn't get node ID: {title[:50]}...{RESET}")
            return f"ISSUE_{issue_number}"  # Fallback identifier
    except Exception as e:
        print(f"{YELLOW}⚠ Created issue #{issue_number} but error getting node ID: {e}{RESET}")
        return f"ISSUE_{issue_number}"  # Fallback identifier


def add_sub_issue(parent_id: str, child_id: str) -> bool:
    """Link a child issue to a parent issue using GitHub's sub-issue feature."""
    # Skip if IDs are not valid node IDs
    if not parent_id or not child_id or parent_id.startswith("ISSUE_") or child_id.startswith("ISSUE_"):
        return False
    
    # Try using updateIssue mutation with parentId
    mutation = """
    mutation UpdateIssue($input: UpdateIssueInput!) {
      updateIssue(input: $input) {
        issue {
          id
        }
      }
    }
    """
    
    variables = {
        "input": {
            "id": child_id,
            "parentId": parent_id
        }
    }
    
    cmd = [
        "gh", "api", "graphql",
        "-f", f"query={mutation}",
        "-f", f"variables={json.dumps(variables)}"
    ]
    
    try:
        result = run_command(cmd, check=False)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if data.get("data", {}).get("updateIssue", {}).get("issue"):
                return True
        
        # Try alternative: use addSubIssue mutation (if available)
        mutation = """
        mutation AddSubIssue($input: AddSubIssueInput!) {
          addSubIssue(input: $input) {
            issue {
              id
            }
          }
        }
        """
        variables = {
            "input": {
                "parentId": parent_id,
                "childId": child_id
            }
        }
        cmd = [
            "gh", "api", "graphql",
            "-f", f"query={mutation}",
            "-f", f"variables={json.dumps(variables)}"
        ]
        result = run_command(cmd, check=False)
        if result.returncode == 0:
            return True
        
        return False
    except Exception as e:
        # Silently fail - sub-issues might not be supported in this GitHub plan
        return False


# EPICs Data
EPICS = [
    {
        "title": "Epic 1: Identity & Access Management",
        "body": """## Priority: P0

Complete identity and access management system for users, restaurants, and drivers.

### Scope
- User registration and authentication
- Profile management
- Delivery address management
- Payment method management
""",
        "user_stories": [
            {
                "id": "US-AUTH-01",
                "title": "As a user, I can register with email/phone + OTP",
                "priority": "P0",
                "dependencies": "None"
            },
            {
                "id": "US-AUTH-02",
                "title": "As a user, I can login and receive JWT tokens",
                "priority": "P0",
                "dependencies": "US-AUTH-01"
            },
            {
                "id": "US-AUTH-03",
                "title": "As a user, I can reset my password",
                "priority": "P1",
                "dependencies": "US-AUTH-01"
            },
            {
                "id": "US-AUTH-04",
                "title": "As a user, I can manage my profile",
                "priority": "P1",
                "dependencies": "US-AUTH-02"
            },
            {
                "id": "US-AUTH-05",
                "title": "As a user, I can manage delivery addresses",
                "priority": "P0",
                "dependencies": "US-AUTH-02"
            },
            {
                "id": "US-AUTH-06",
                "title": "As a user, I can add payment methods",
                "priority": "P0",
                "dependencies": "US-AUTH-02"
            }
        ]
    },
    {
        "title": "Epic 2: Restaurant & Menu Catalog",
        "body": """## Priority: P0

Restaurant registration and menu management system.

### Scope
- Restaurant registration
- Menu category management
- Menu item management with variants
- Restaurant status management
""",
        "user_stories": [
            {
                "id": "US-CAT-01",
                "title": "As a restaurant owner, I can register my restaurant",
                "priority": "P0",
                "dependencies": "US-AUTH-01"
            },
            {
                "id": "US-CAT-02",
                "title": "As a restaurant owner, I can manage menu categories",
                "priority": "P0",
                "dependencies": "US-CAT-01"
            },
            {
                "id": "US-CAT-03",
                "title": "As a restaurant owner, I can manage menu items with variants",
                "priority": "P0",
                "dependencies": "US-CAT-02"
            },
            {
                "id": "US-CAT-04",
                "title": "As a restaurant owner, I can toggle accepting orders",
                "priority": "P0",
                "dependencies": "US-CAT-01"
            },
            {
                "id": "US-CAT-05",
                "title": "As a customer, I can view restaurant details and menu",
                "priority": "P0",
                "dependencies": "US-CAT-03"
            }
        ]
    },
    {
        "title": "Epic 3: Search & Discovery",
        "body": """## Priority: P0

Restaurant search and discovery features.

### Scope
- Geo-based restaurant search
- Filtering and sorting
- Search result pagination
""",
        "user_stories": [
            {
                "id": "US-SEARCH-01",
                "title": "As a customer, I can search restaurants by location",
                "priority": "P0",
                "dependencies": "US-CAT-01"
            },
            {
                "id": "US-SEARCH-02",
                "title": "As a customer, I can filter by rating, distance, open status",
                "priority": "P0",
                "dependencies": "US-SEARCH-01"
            },
            {
                "id": "US-SEARCH-03",
                "title": "As a customer, I can see search results with pagination",
                "priority": "P1",
                "dependencies": "US-SEARCH-01"
            }
        ]
    },
    {
        "title": "Epic 4: Order Management",
        "body": """## Priority: P0

Complete order management system for customers and restaurants.

### Scope
- Cart management
- Order placement
- Order status management
- Order history
- Order cancellation
""",
        "user_stories": [
            {
                "id": "US-ORD-01",
                "title": "As a customer, I can add items to cart",
                "priority": "P0",
                "dependencies": "US-CAT-05"
            },
            {
                "id": "US-ORD-02",
                "title": "As a customer, I can apply coupon codes",
                "priority": "P0",
                "dependencies": "US-ORD-01"
            },
            {
                "id": "US-ORD-03",
                "title": "As a customer, I can place an order",
                "priority": "P0",
                "dependencies": "US-ORD-01, US-AUTH-05"
            },
            {
                "id": "US-ORD-04",
                "title": "As a customer, I can view order history",
                "priority": "P1",
                "dependencies": "US-ORD-03"
            },
            {
                "id": "US-ORD-05",
                "title": "As a customer, I can cancel order before restaurant accepts",
                "priority": "P0",
                "dependencies": "US-ORD-03"
            },
            {
                "id": "US-ORD-06",
                "title": "As a customer, I can reorder from history",
                "priority": "P1",
                "dependencies": "US-ORD-04"
            },
            {
                "id": "US-ORD-07",
                "title": "As a restaurant, I can view and accept/reject orders",
                "priority": "P0",
                "dependencies": "US-ORD-03"
            },
            {
                "id": "US-ORD-08",
                "title": "As a restaurant, I can update order status (preparing, ready)",
                "priority": "P0",
                "dependencies": "US-ORD-07"
            }
        ]
    },
    {
        "title": "Epic 5: Payment Processing",
        "body": """## Priority: P0

Secure payment processing system.

### Scope
- COD payment
- Card payment integration
- Refund handling
- Idempotency
""",
        "user_stories": [
            {
                "id": "US-PAY-01",
                "title": "As a customer, I can pay with COD",
                "priority": "P0",
                "dependencies": "US-ORD-03"
            },
            {
                "id": "US-PAY-02",
                "title": "As a customer, I can pay with card (Stripe/VNPay)",
                "priority": "P0",
                "dependencies": "US-ORD-03, US-AUTH-06"
            },
            {
                "id": "US-PAY-03",
                "title": "As a system, I handle refunds on cancellation",
                "priority": "P0",
                "dependencies": "US-ORD-05"
            },
            {
                "id": "US-PAY-04",
                "title": "As a system, I prevent double-charges with idempotency",
                "priority": "P0",
                "dependencies": "US-PAY-02"
            }
        ]
    },
    {
        "title": "Epic 6: Delivery & Tracking",
        "body": """## Priority: P0

Driver management and real-time order tracking.

### Scope
- Driver registration
- Driver status management
- Delivery task assignment
- Real-time tracking
""",
        "user_stories": [
            {
                "id": "US-DEL-01",
                "title": "As a driver, I can register with documents",
                "priority": "P0",
                "dependencies": "US-AUTH-01"
            },
            {
                "id": "US-DEL-02",
                "title": "As a driver, I can go online/offline",
                "priority": "P0",
                "dependencies": "US-DEL-01"
            },
            {
                "id": "US-DEL-03",
                "title": "As a driver, I can receive and accept delivery tasks",
                "priority": "P0",
                "dependencies": "US-DEL-02"
            },
            {
                "id": "US-DEL-04",
                "title": "As a driver, I can update delivery status",
                "priority": "P0",
                "dependencies": "US-DEL-03"
            },
            {
                "id": "US-DEL-05",
                "title": "As a customer, I can track order status in real-time",
                "priority": "P0",
                "dependencies": "US-DEL-04"
            },
            {
                "id": "US-DEL-06",
                "title": "As a customer, I can see driver location on map",
                "priority": "P0",
                "dependencies": "US-DEL-05"
            },
            {
                "id": "US-DEL-07",
                "title": "As a driver, I can view my earnings",
                "priority": "P1",
                "dependencies": "US-DEL-04"
            }
        ]
    },
    {
        "title": "Epic 7: Notifications",
        "body": """## Priority: P0

Notification system for all user types.

### Scope
- Push notifications
- SMS notifications
- Notification preferences
""",
        "user_stories": [
            {
                "id": "US-NOTIF-01",
                "title": "As a user, I receive push notifications on status changes",
                "priority": "P0",
                "dependencies": "US-ORD-03"
            },
            {
                "id": "US-NOTIF-02",
                "title": "As a user, I receive SMS for critical events",
                "priority": "P1",
                "dependencies": "US-NOTIF-01"
            }
        ]
    },
    {
        "title": "Epic 8: Rating & Review",
        "body": """## Priority: P1

Rating and review system for restaurants and drivers.

### Scope
- Restaurant ratings
- Driver ratings
- Review display
""",
        "user_stories": [
            {
                "id": "US-RATE-01",
                "title": "As a customer, I can rate restaurant after delivery",
                "priority": "P1",
                "dependencies": "US-ORD-03"
            },
            {
                "id": "US-RATE-02",
                "title": "As a customer, I can rate driver after delivery",
                "priority": "P1",
                "dependencies": "US-DEL-04"
            }
        ]
    },
    {
        "title": "Epic 9: Admin Portal",
        "body": """## Priority: P1

Admin dashboard and management features.

### Scope
- Dashboard KPIs
- Restaurant approval
- Driver approval
- Coupon management
""",
        "user_stories": [
            {
                "id": "US-ADM-01",
                "title": "As an admin, I can view dashboard KPIs",
                "priority": "P1",
                "dependencies": "All services"
            },
            {
                "id": "US-ADM-02",
                "title": "As an admin, I can approve/reject restaurants",
                "priority": "P0",
                "dependencies": "US-CAT-01"
            },
            {
                "id": "US-ADM-03",
                "title": "As an admin, I can approve/reject drivers",
                "priority": "P0",
                "dependencies": "US-DEL-01"
            },
            {
                "id": "US-ADM-04",
                "title": "As an admin, I can manage coupons",
                "priority": "P1",
                "dependencies": "US-ORD-02"
            }
        ]
    },
    {
        "title": "Epic 10: Dispute Management",
        "body": """## Priority: P0

Dispute handling system for order issues.

### Scope
- Dispute creation
- Photo evidence upload
- Admin dispute resolution
""",
        "user_stories": [
            {
                "id": "US-DISPUTE-01",
                "title": "As a customer, I can create a dispute ticket within 24h of delivery",
                "priority": "P0",
                "dependencies": "US-ORD-03"
            },
            {
                "id": "US-DISPUTE-02",
                "title": "As a customer, I can upload photo evidence for disputes",
                "priority": "P0",
                "dependencies": "US-DISPUTE-01"
            },
            {
                "id": "US-DISPUTE-03",
                "title": "As an admin, I can review and resolve disputes",
                "priority": "P0",
                "dependencies": "US-DISPUTE-01"
            }
        ]
    },
    {
        "title": "Epic 11: Exception Flows",
        "body": """## Priority: P0

Exception handling for edge cases in delivery flow.

### Scope
- Customer unreachable handling
- Address mismatch handling
- SLA miss auto-cancellation
- Emergency reassignment
""",
        "user_stories": [
            {
                "id": "US-EXC-01",
                "title": "As a driver, I can mark customer unreachable after 3 call attempts",
                "priority": "P0",
                "dependencies": "US-DEL-04"
            },
            {
                "id": "US-EXC-02",
                "title": "As a driver, I can report address mismatch and request correction",
                "priority": "P0",
                "dependencies": "US-DEL-04"
            },
            {
                "id": "US-EXC-03",
                "title": "As a system, I auto-cancel orders when SLA miss >60min",
                "priority": "P0",
                "dependencies": "US-ORD-03"
            },
            {
                "id": "US-EXC-04",
                "title": "As a driver, I can report emergency and trigger reassignment",
                "priority": "P1",
                "dependencies": "US-DEL-03"
            }
        ]
    }
]


# Sprints Data
SPRINTS = [
    {
        "number": 0,
        "title": "Sprint 0: Foundation",
        "goal": "Setup infrastructure and development environment",
        "tasks": [
            {"id": "INFRA-001", "title": "Setup Git repository with branching strategy", "est": "2h"},
            {"id": "INFRA-002", "title": "Setup Docker Compose for local development (PostgreSQL, Redis, Kafka)", "est": "4h"},
            {"id": "INFRA-003", "title": "Create Kubernetes manifests (Helm charts)", "est": "8h"},
            {"id": "INFRA-004", "title": "Setup CI/CD pipeline (GitHub Actions → Docker Hub → AWS)", "est": "8h"},
            {"id": "INFRA-005", "title": "Database migration framework setup (golang-migrate)", "est": "4h"},
            {"id": "INFRA-006", "title": "Create base project structure for microservices", "est": "6h"},
            {"id": "INFRA-007", "title": "Setup API Gateway (Nginx/Envoy) with basic routing", "est": "6h"},
            {"id": "INFRA-008", "title": "Configure observability stack (Prometheus, Grafana, ELK)", "est": "8h"},
            {"id": "INFRA-009", "title": "Create shared Go libraries (logging, errors, middleware)", "est": "8h"},
            {"id": "INFRA-010", "title": "Setup JWKS endpoint for JWT RS256 verification", "est": "4h"},
            {"id": "SEC-001", "title": "Security headers middleware (X-Content-Type-Options, HSTS, CSP)", "est": "4h"},
            {"id": "INFRA-011", "title": "Audit logging infrastructure setup", "est": "4h"},
            {"id": "INFRA-012", "title": "Redis Pub/Sub verification for WebSocket scaling", "est": "4h"},
            {"id": "DB-000", "title": "Create `cities` and `audit_logs` base tables", "est": "3h"},
            {"id": "[Front]-001", "title": "Setup React Native monorepo (Customer, Restaurant, Driver apps)", "est": "8h"},
            {"id": "[Front]-002", "title": "Setup React Admin Dashboard project with Vite", "est": "4h"},
            {"id": "[Front]-003", "title": "Configure shared component library (design tokens, themes)", "est": "6h"},
            {"id": "[Front]-004", "title": "Setup navigation structure for all mobile apps", "est": "6h"},
            {"id": "[Front]-005", "title": "Configure API client with Axios/React Query + interceptors", "est": "4h"},
            {"id": "[Front]-006", "title": "Setup CI/CD for mobile builds (EAS Build / Fastlane)", "est": "8h"},
            {"id": "[Front]-007", "title": "Create base UI components (Button, Input, Card, Badge)", "est": "8h"},
        ]
    },
    {
        "number": 1,
        "title": "Sprint 1: User Service",
        "goal": "Complete identity and access management",
        "tasks": [
            {"id": "DB-001", "title": "Create `users`, `user_addresses`, `user_payment_methods`, `refresh_tokens` tables", "est": "4h"},
            {"id": "API-001", "title": "POST `/api/v1/auth/register` - Email/phone registration", "est": "8h"},
            {"id": "API-002", "title": "POST `/api/v1/auth/login` - JWT RS256 token generation", "est": "8h"},
            {"id": "API-003", "title": "POST `/api/v1/auth/refresh` - Refresh token rotation", "est": "4h"},
            {"id": "API-004", "title": "CRUD `/api/v1/users/addresses` - Delivery addresses", "est": "6h"},
            {"id": "API-005", "title": "CRUD `/api/v1/users/payment-methods` - Tokenized payment", "est": "6h"},
            {"id": "API-006", "title": "POST `/api/v1/auth/password-reset` - Password reset with OTP", "est": "4h"},
            {"id": "INT-001", "title": "OTP service integration (Twilio SMS)", "est": "4h"},
            {"id": "INT-002", "title": "Redis integration for JWT blacklist", "est": "4h"},
            {"id": "TEST-001", "title": "Unit tests for auth logic (80% coverage)", "est": "8h"},
            {"id": "TEST-002", "title": "Integration tests for auth flow", "est": "4h"},
            {"id": "[Front]-008", "title": "Customer: Splash + Onboarding screens (4 screens)", "est": "6h"},
            {"id": "[Front]-009", "title": "Customer: Login screen with form validation", "est": "4h"},
            {"id": "[Front]-010", "title": "Customer: Registration screen with OTP verification", "est": "6h"},
            {"id": "[Front]-011", "title": "Customer: Profile screen", "est": "4h"},
            {"id": "[Front]-012", "title": "Customer: Saved Addresses screen (CRUD)", "est": "6h"},
            {"id": "[Front]-013", "title": "Customer: Payment Methods screen (tokenized cards)", "est": "6h"},
            {"id": "[Front]-014", "title": "Restaurant: Login/Registration screens", "est": "4h"},
            {"id": "[Front]-015", "title": "Driver: Login/Registration screens", "est": "4h"},
            {"id": "[Front]-016", "title": "Shared: Auth state management (Zustand/Redux)", "est": "4h"},
            {"id": "[Front]-017", "title": "Shared: Secure token storage (AsyncStorage/SecureStore)", "est": "4h"},
        ]
    },
    {
        "number": 2,
        "title": "Sprint 2: Catalog Service",
        "goal": "Restaurant registration and menu management",
        "tasks": [
            {"id": "DB-002", "title": "Create `restaurants`, `menu_categories`, `menu_items`, `menu_item_variants` tables", "est": "4h"},
            {"id": "API-007", "title": "POST `/api/v1/restaurants` - Restaurant registration", "est": "6h"},
            {"id": "API-008", "title": "GET `/api/v1/restaurants/{id}` - Restaurant detail", "est": "4h"},
            {"id": "API-009", "title": "CRUD `/api/v1/restaurants/{id}/menu-categories`", "est": "6h"},
            {"id": "API-010", "title": "CRUD `/api/v1/restaurants/{id}/menu-items` with variants", "est": "8h"},
            {"id": "API-011", "title": "PUT `/api/v1/restaurants/{id}/status` - Toggle accepting orders", "est": "3h"},
            {"id": "API-012", "title": "GET `/api/v1/restaurants/{id}/menu` - Full menu view", "est": "4h"},
            {"id": "API-013", "title": "Admin restaurant approval endpoints (PENDING → APPROVED/REJECTED)", "est": "6h"},
            {"id": "INT-003", "title": "S3/MinIO integration for image upload", "est": "6h"},
            {"id": "CACHE-001", "title": "Redis cache for restaurant/menu data", "est": "4h"},
            {"id": "TEST-003", "title": "Unit + integration tests", "est": "8h"},
            {"id": "[Front]-018", "title": "Customer: Home screen with featured restaurants", "est": "8h"},
            {"id": "[Front]-019", "title": "Customer: Restaurant Detail screen with tabs", "est": "8h"},
            {"id": "[Front]-020", "title": "Customer: Food Item Detail modal/bottom sheet", "est": "4h"},
            {"id": "[Front]-021", "title": "Restaurant: Dashboard screen", "est": "6h"},
            {"id": "[Front]-022", "title": "Restaurant: Menu List screen", "est": "6h"},
            {"id": "[Front]-023", "title": "Restaurant: Add/Edit Menu Item modal with variants", "est": "8h"},
            {"id": "[Front]-024", "title": "Restaurant: Category Management modal", "est": "4h"},
            {"id": "[Front]-025", "title": "Restaurant: Settings screen (toggle accepting orders)", "est": "4h"},
            {"id": "[Front]-026", "title": "Admin: Restaurant Management screen (approve/reject)", "est": "8h"},
            {"id": "[Front]-027", "title": "Shared: Image upload component with S3", "est": "4h"},
        ]
    },
    {
        "number": 3,
        "title": "Sprint 3: Search Service + Order Part 1",
        "goal": "Search restaurants and cart management",
        "tasks": [
            {"id": "DB-003", "title": "Create `coupons`, `coupon_usages` tables", "est": "3h"},
            {"id": "API-014", "title": "GET `/api/v1/restaurants` - Geo-search with filters", "est": "10h"},
            {"id": "API-015", "title": "GET `/api/v1/search` - Full-text search", "est": "6h"},
            {"id": "CACHE-002", "title": "Redis caching for search results", "est": "4h"},
            {"id": "API-016", "title": "Cart management (in-memory/Redis per user)", "est": "8h"},
            {"id": "API-017", "title": "POST `/api/v1/coupons/validate` - Coupon validation", "est": "6h"},
            {"id": "API-018", "title": "Pricing engine (subtotal + tax + delivery fee - discount)", "est": "6h"},
            {"id": "INDEX-001", "title": "PostgreSQL GiST index for geo-queries", "est": "4h"},
            {"id": "TEST-004", "title": "Unit + integration tests", "est": "8h"},
            {"id": "[Front]-028", "title": "Customer: Search screen with autocomplete", "est": "6h"},
            {"id": "[Front]-029", "title": "Customer: Search Results with filters (distance, rating, open)", "est": "8h"},
            {"id": "[Front]-030", "title": "Customer: Filter Modal", "est": "4h"},
            {"id": "[Front]-031", "title": "Customer: Category View screen", "est": "4h"},
            {"id": "[Front]-032", "title": "Customer: Cart screen with item management", "est": "8h"},
            {"id": "[Front]-033", "title": "Customer: Coupon input + validation UI", "est": "4h"},
            {"id": "[Front]-034", "title": "Customer: Pricing breakdown component", "est": "3h"},
            {"id": "[Front]-035", "title": "Shared: Map integration (Google Maps / Mapbox)", "est": "8h"},
        ]
    },
    {
        "number": 4,
        "title": "Sprint 4: Order Part 2 + Payment Service",
        "goal": "Complete order placement and payment processing",
        "tasks": [
            {"id": "DB-004", "title": "Create `orders`, `order_items`, `order_item_variants`, `payments`, `payment_refunds` tables", "est": "6h"},
            {"id": "API-019", "title": "POST `/api/v1/orders` - Create order with validation", "est": "12h"},
            {"id": "API-020", "title": "Order state machine implementation", "est": "8h"},
            {"id": "API-021", "title": "PUT `/api/v1/orders/{id}/cancel` - Cancellation with refund", "est": "6h"},
            {"id": "API-022", "title": "POST `/api/v1/payments/authorize` - Payment authorization", "est": "8h"},
            {"id": "API-023", "title": "POST `/api/v1/payments/{id}/capture` - Payment capture", "est": "6h"},
            {"id": "API-024", "title": "POST `/api/v1/payments/{id}/refund` - Refund processing", "est": "6h"},
            {"id": "INT-004", "title": "Stripe/VNPay gateway integration", "est": "12h"},
            {"id": "INT-005", "title": "Idempotency key implementation", "est": "4h"},
            {"id": "KAFKA-001", "title": "Kafka producer for order events", "est": "6h"},
            {"id": "KAFKA-002", "title": "Kafka consumer stubs for notification events", "est": "4h"},
            {"id": "TEST-005", "title": "Payment idempotency tests (critical)", "est": "8h"},
            {"id": "[Front]-036", "title": "Customer: Checkout Step 1 - Delivery address selection", "est": "6h"},
            {"id": "[Front]-037", "title": "Customer: Checkout Step 2 - Payment method selection", "est": "6h"},
            {"id": "[Front]-038", "title": "Customer: Checkout Step 3 - Order review + place order", "est": "6h"},
            {"id": "[Front]-039", "title": "Customer: Order Confirmation screen", "est": "4h"},
            {"id": "[Front]-040", "title": "Customer: Order History screen", "est": "6h"},
            {"id": "[Front]-041", "title": "Customer: Order Detail screen", "est": "4h"},
            {"id": "[Front]-042", "title": "Restaurant: Incoming Orders screen with accept/reject", "est": "8h"},
            {"id": "[Front]-043", "title": "Restaurant: Order Detail (restaurant view)", "est": "4h"},
            {"id": "[Front]-044", "title": "Restaurant: Preparing Orders screen with status updates", "est": "6h"},
            {"id": "[Front]-045", "title": "Shared: Stripe/VNPay payment integration", "est": "8h"},
        ]
    },
    {
        "number": 5,
        "title": "Sprint 5: Delivery Service + WebSocket",
        "goal": "Driver management and real-time tracking",
        "tasks": [
            {"id": "DB-005", "title": "Create `drivers`, `delivery_tasks`, `delivery_task_events`, `driver_location_history` tables", "est": "6h"},
            {"id": "DB-006", "title": "Configure `driver_location_history` table partitioning for performance", "est": "4h"},
            {"id": "API-025", "title": "POST `/api/v1/drivers/register` - Driver registration", "est": "6h"},
            {"id": "API-026", "title": "PUT `/api/v1/drivers/{id}/status` - Online/offline toggle", "est": "4h"},
            {"id": "API-027", "title": "Driver assignment algorithm (nearest available)", "est": "10h"},
            {"id": "API-028", "title": "PUT `/api/v1/delivery-tasks/{id}/status` - Status updates", "est": "6h"},
            {"id": "API-029", "title": "PUT `/api/v1/drivers/{id}/location` - GPS location updates (every 5s)", "est": "4h"},
            {"id": "API-030", "title": "Admin driver approval endpoints (PENDING → APPROVED/REJECTED)", "est": "6h"},
            {"id": "WS-001", "title": "WebSocket gateway setup (gorilla/websocket)", "est": "10h"},
            {"id": "WS-002", "title": "Order status subscription (order:{id} channel)", "est": "6h"},
            {"id": "WS-003", "title": "Driver location subscription (driver:location:{id})", "est": "6h"},
            {"id": "INT-006", "title": "Redis Pub/Sub for WebSocket scaling", "est": "6h"},
            {"id": "API-031", "title": "Restaurant order management (accept/reject, status update)", "est": "8h"},
            {"id": "TEST-006", "title": "WebSocket integration tests", "est": "6h"},
            {"id": "[Front]-046", "title": "Customer: Order Tracking - Live Map screen", "est": "10h"},
            {"id": "[Front]-047", "title": "Customer: WebSocket integration for real-time updates", "est": "6h"},
            {"id": "[Front]-048", "title": "Driver: Home screen (Online/Offline toggle)", "est": "6h"},
            {"id": "[Front]-049", "title": "Driver: Available Deliveries list", "est": "4h"},
            {"id": "[Front]-050", "title": "Driver: Active Delivery - Pickup screen with navigation", "est": "8h"},
            {"id": "[Front]-051", "title": "Driver: Active Delivery - Dropoff screen", "est": "6h"},
            {"id": "[Front]-052", "title": "Driver: Delivery Complete screen", "est": "3h"},
            {"id": "[Front]-053", "title": "Driver: GPS location tracking service (background)", "est": "8h"},
            {"id": "[Front]-054", "title": "Driver: WebSocket integration for task assignment", "est": "6h"},
            {"id": "[Front]-055", "title": "Admin: Driver Management screen (approve/reject)", "est": "6h"},
        ]
    },
    {
        "number": 6,
        "title": "Sprint 6: Notifications + Saga + Exception Flows",
        "goal": "Push notifications, distributed transaction handling, and exception flows",
        "tasks": [
            {"id": "DB-007", "title": "Create `disputes` table", "est": "3h"},
            {"id": "API-032", "title": "Notification service setup", "est": "6h"},
            {"id": "API-033", "title": "Notification preference APIs", "est": "4h"},
            {"id": "INT-007", "title": "FCM integration for push notifications", "est": "8h"},
            {"id": "INT-008", "title": "Twilio SMS integration", "est": "4h"},
            {"id": "KAFKA-003", "title": "Kafka consumers for notification events", "est": "8h"},
            {"id": "SAGA-001", "title": "Order creation saga implementation", "est": "12h"},
            {"id": "SAGA-002", "title": "Compensation handlers for each saga step", "est": "10h"},
            {"id": "EXC-001", "title": "FR-ORD-11: Customer unreachable flow (mark after 3 attempts)", "est": "6h"},
            {"id": "EXC-002", "title": "FR-ORD-12: Address correction flow (driver reports mismatch)", "est": "6h"},
            {"id": "EXC-003", "title": "FR-ORD-14: SLA miss auto-cancellation scheduler (>60min)", "est": "6h"},
            {"id": "EXC-004", "title": "FR-DEL-10: Driver emergency and reassignment flow", "est": "6h"},
            {"id": "API-034", "title": "POST `/api/v1/disputes` - Create dispute ticket", "est": "6h"},
            {"id": "API-035", "title": "GET `/api/v1/disputes` - List user disputes", "est": "4h"},
            {"id": "TEST-007", "title": "Saga compensation tests", "est": "8h"},
            {"id": "[Front]-056", "title": "Customer: Push notification integration (FCM)", "est": "6h"},
            {"id": "[Front]-057", "title": "Customer: Notification Settings screen", "est": "3h"},
            {"id": "[Front]-058", "title": "Customer: Create Dispute screen with photo upload", "est": "6h"},
            {"id": "[Front]-059", "title": "Driver: Push notification for new delivery tasks", "est": "4h"},
            {"id": "[Front]-060", "title": "Driver: Customer unreachable flow UI (3 call attempts)", "est": "4h"},
            {"id": "[Front]-061", "title": "Driver: Address mismatch report modal", "est": "3h"},
            {"id": "[Front]-062", "title": "Driver: Emergency report flow", "est": "3h"},
            {"id": "[Front]-063", "title": "Restaurant: Push notification for new orders", "est": "4h"},
            {"id": "[Front]-064", "title": "Admin: Dispute Management screen", "est": "6h"},
        ]
    },
    {
        "number": 7,
        "title": "Sprint 7: Rating + Admin + Disputes + Polish",
        "goal": "Rating system, admin dashboard, dispute resolution, bug fixes",
        "tasks": [
            {"id": "DB-008", "title": "Create `ratings` table", "est": "3h"},
            {"id": "API-036", "title": "POST `/api/v1/restaurants/{id}/ratings`", "est": "4h"},
            {"id": "API-037", "title": "POST `/api/v1/drivers/{id}/ratings`", "est": "4h"},
            {"id": "API-038", "title": "Aggregate rating calculation", "est": "4h"},
            {"id": "API-039", "title": "GET `/api/v1/admin/dashboard` - KPI metrics", "est": "8h"},
            {"id": "API-040", "title": "PUT `/api/v1/disputes/{id}/resolve` - Admin resolution", "est": "6h"},
            {"id": "API-041", "title": "Admin coupon management APIs", "est": "6h"},
            {"id": "API-042", "title": "Dispute metrics in admin dashboard", "est": "4h"},
            {"id": "SEC-002", "title": "Security headers implementation verification", "est": "4h"},
            {"id": "SEC-003", "title": "Rate limiting configuration", "est": "4h"},
            {"id": "OPS-001", "title": "Monitoring dashboards (Grafana)", "est": "8h"},
            {"id": "OPS-002", "title": "Alerting rules (P0 incidents)", "est": "4h"},
            {"id": "BUG-XXX", "title": "Bug fixes and performance optimization", "est": "16h"},
            {"id": "TEST-008", "title": "E2E tests for critical paths", "est": "12h"},
            {"id": "[Front]-065", "title": "Customer: Rate Order modal (restaurant + driver)", "est": "6h"},
            {"id": "[Front]-066", "title": "Customer: Restaurant Reviews Tab", "est": "4h"},
            {"id": "[Front]-067", "title": "Driver: Driver Profile screen", "est": "4h"},
            {"id": "[Front]-068", "title": "Driver: Delivery History + Earnings screen", "est": "6h"},
            {"id": "[Front]-069", "title": "Restaurant: Analytics View screen", "est": "6h"},
            {"id": "[Front]-070", "title": "Restaurant: Order History screen", "est": "4h"},
            {"id": "[Front]-071", "title": "Admin: Dashboard screen with KPIs", "est": "8h"},
            {"id": "[Front]-072", "title": "Admin: User Management screen", "est": "6h"},
            {"id": "[Front]-073", "title": "Admin: Order Management screen", "est": "6h"},
            {"id": "[Front]-074", "title": "Admin: Payment Management screen", "est": "4h"},
            {"id": "[Front]-075", "title": "Admin: Coupon Management screen", "est": "6h"},
            {"id": "[Front]-076", "title": "All Apps: Bug fixes and UI polish", "est": "16h"},
        ]
    },
    {
        "number": 8,
        "title": "Sprint 8: Integration Testing + UAT + Launch Prep",
        "goal": "Final testing, security audit, production deployment",
        "tasks": [
            {"id": "TEST-009", "title": "Full E2E testing of all user journeys", "est": "16h"},
            {"id": "TEST-010", "title": "Load testing (target: 5k concurrent users)", "est": "12h"},
            {"id": "SEC-004", "title": "Security penetration testing", "est": "12h"},
            {"id": "PERF-001", "title": "Performance optimization based on test results", "est": "12h"},
            {"id": "OPS-003", "title": "Production environment setup (AWS EKS)", "est": "8h"},
            {"id": "OPS-004", "title": "Database migration to production", "est": "4h"},
            {"id": "OPS-005", "title": "SSL/TLS certificate setup", "est": "2h"},
            {"id": "OPS-006", "title": "DNS configuration", "est": "2h"},
            {"id": "OPS-007", "title": "Monitoring and alerting verification", "est": "4h"},
            {"id": "DOC-001", "title": "Runbook documentation", "est": "8h"},
            {"id": "OPS-008", "title": "On-call rotation setup", "est": "2h"},
            {"id": "LAUNCH-01", "title": "Go-live checklist completion", "est": "4h"},
            {"id": "[Front]-077", "title": "Admin: Revenue Reports screen", "est": "6h"},
            {"id": "[Front]-078", "title": "Admin: Performance Reports screen", "est": "4h"},
            {"id": "[Front]-079", "title": "Admin: User Analytics screen", "est": "4h"},
            {"id": "[Front]-080", "title": "All Apps: E2E testing with Detox (mobile) / Cypress (web)", "est": "16h"},
            {"id": "[Front]-081", "title": "All Apps: Accessibility audit and fixes", "est": "8h"},
            {"id": "[Front]-082", "title": "Mobile: App Store / Play Store submission preparation", "est": "8h"},
            {"id": "[Front]-083", "title": "Admin: Production deployment (Vercel/AWS)", "est": "4h"},
            {"id": "[Front]-084", "title": "All Apps: Performance optimization", "est": "8h"},
        ]
    }
]


def main():
    """Main function to create GitHub project structure."""
    print(f"{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}GitHub Project MVP Creation Script{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    # Check if gh CLI is installed
    try:
        run_command(["gh", "--version"])
    except:
        print(f"{RED}Error: GitHub CLI (gh) is not installed or not in PATH{RESET}")
        print(f"{YELLOW}Please install it from: https://cli.github.com/{RESET}")
        sys.exit(1)
    
    # Check authentication
    try:
        run_command(["gh", "auth", "status"])
    except:
        print(f"{RED}Error: Not authenticated with GitHub{RESET}")
        print(f"{YELLOW}Please run: gh auth login{RESET}")
        sys.exit(1)
    
    # Create project
    project_title = "Online Food Ordering System MVP"
    print(f"\n{BLUE}Step 1: Creating GitHub Project...{RESET}")
    project_id = create_github_project(project_title, "scrum")
    
    # Store issue IDs
    epic_ids = {}
    us_ids = {}
    sprint_ids = {}
    task_ids = {}
    
    # Create EPICs
    print(f"\n{BLUE}Step 2: Creating EPICs ({len(EPICS)} total)...{RESET}")
    for i, epic in enumerate(EPICS, 1):
        print(f"{BLUE}[{i}/{len(EPICS)}] Creating EPIC: {epic['title']}{RESET}")
        epic_id = create_issue(
            title=epic["title"],
            body=epic["body"],
            labels=["epic", "P0" if "P0" in epic["body"] else "P1"]
        )
        epic_ids[epic["title"]] = epic_id
        time.sleep(1)  # Rate limiting
    
    # Create User Stories
    total_us = sum(len(epic["user_stories"]) for epic in EPICS)
    print(f"\n{BLUE}Step 3: Creating User Stories ({total_us} total)...{RESET}")
    us_count = 0
    for epic in EPICS:
        epic_id = epic_ids[epic["title"]]
        for us in epic["user_stories"]:
            us_count += 1
            print(f"{BLUE}[{us_count}/{total_us}] Creating US: {us['id']}{RESET}")
            us_body = f"""## {us['id']}

**Priority:** {us['priority']}
**Dependencies:** {us['dependencies']}

{us['title']}
"""
            us_id = create_issue(
                title=f"{us['id']}: {us['title']}",
                body=us_body,
                labels=["user-story", us['priority']]
            )
            us_ids[us['id']] = us_id
            
            # Link to EPIC
            if epic_id and us_id:
                add_sub_issue(epic_id, us_id)
            
            time.sleep(1)
    
    # Create Sprints
    print(f"\n{BLUE}Step 4: Creating Sprint Issues ({len(SPRINTS)} total)...{RESET}")
    for sprint in SPRINTS:
        print(f"{BLUE}Creating Sprint {sprint['number']}: {sprint['title'].split(': ')[1]}{RESET}")
        sprint_body = f"""## Sprint {sprint['number']}: {sprint['title'].split(': ')[1]}

**Goal:** {sprint['goal']}

### Tasks
This sprint contains {len(sprint['tasks'])} development tasks.
"""
        sprint_id = create_issue(
            title=sprint['title'],
            body=sprint_body,
            labels=["sprint"]
        )
        sprint_ids[sprint['number']] = sprint_id
        time.sleep(1)
    
    # Create Tasks
    total_tasks = sum(len(sprint['tasks']) for sprint in SPRINTS)
    print(f"\n{BLUE}Step 5: Creating Tasks ({total_tasks} total)...{RESET}")
    task_count = 0
    for sprint in SPRINTS:
        sprint_id = sprint_ids[sprint['number']]
        for task in sprint['tasks']:
            task_count += 1
            if task_count % 10 == 0:
                print(f"{BLUE}[{task_count}/{total_tasks}] Creating tasks...{RESET}")
            task_body = f"""## {task['id']}

**Estimate:** {task['est']}

{task['title']}
"""
            task_id = create_issue(
                title=f"{task['id']}: {task['title']}",
                body=task_body,
                labels=["task"]
            )
            task_ids[task['id']] = task_id
            
            # Link to Sprint
            if sprint_id and task_id:
                add_sub_issue(sprint_id, task_id)
            
            time.sleep(1)
    
    # Summary
    print(f"\n{GREEN}{'='*60}{RESET}")
    print(f"{GREEN}✓ Creation Complete!{RESET}")
    print(f"{GREEN}{'='*60}{RESET}")
    print(f"{GREEN}Summary:{RESET}")
    print(f"  {GREEN}✓ EPICs created: {len(epic_ids)}/{len(EPICS)}{RESET}")
    print(f"  {GREEN}✓ User Stories created: {len(us_ids)}/{sum(len(e['user_stories']) for e in EPICS)}{RESET}")
    print(f"  {GREEN}✓ Sprints created: {len(sprint_ids)}/{len(SPRINTS)}{RESET}")
    print(f"  {GREEN}✓ Tasks created: {len(task_ids)}/{sum(len(s['tasks']) for s in SPRINTS)}{RESET}")
    print(f"{GREEN}{'='*60}{RESET}\n")
    
    print(f"{YELLOW}Note: Parent-child relationships (sub-issues) may need to be set up manually{RESET}")
    print(f"{YELLOW}if your GitHub plan doesn't support the sub-issue API feature.{RESET}")
    print(f"{YELLOW}You can link them manually in the GitHub UI by editing issues.{RESET}\n")


if __name__ == "__main__":
    main()
