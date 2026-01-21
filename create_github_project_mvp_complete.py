#!/usr/bin/env python3
"""
Create EPICs, User Stories, and Tasks for the Online Food Ordering System MVP GitHub Project.

This script:
1. Creates labels (Epic, User Story, Task, Sprint, Backend, Frontend, Priority)
2. Creates Sprint issues (Sprint 0-8)
3. Creates EPICs (11 total)
4. Creates User Stories (48 total) and links them to EPICs
5. Creates Tasks (195 total) and links them to Sprint issues
6. Adds all issues to GitHub Project #14

Requirements:
- GITHUB_TOKEN environment variable
- Repository owner and name (configurable)
- GitHub Project #14 must exist
"""

import os
import sys
import json
import time
import re
import subprocess
import requests
from typing import Dict, List, Optional, Tuple

# Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    print("ERROR: GITHUB_TOKEN environment variable is required")
    sys.exit(1)

# Get repository info from git remote or environment variables
def get_repo_info():
    """Try to get repository owner and name from git remote."""
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            check=True,
        )
        remote_url = result.stdout.strip()
        
        # Match GitHub URLs: https://github.com/owner/repo.git or git@github.com:owner/repo.git
        patterns = [
            r"github\.com[:/]([^/]+)/([^/]+?)(?:\.git)?$",
            r"git@github\.com:([^/]+)/([^/]+?)(?:\.git)?$",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, remote_url)
            if match:
                return match.group(1), match.group(2)
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    # Fallback to environment variables or defaults
    owner = os.getenv("GITHUB_REPO_OWNER", "your-username")
    repo = os.getenv("GITHUB_REPO_NAME", "online-food-ordering-system")
    return owner, repo

REPO_OWNER, REPO_NAME = get_repo_info()
PROJECT_NUMBER = int(os.getenv("GITHUB_PROJECT_NUMBER", "14"))

# GitHub API endpoints
GITHUB_API = "https://api.github.com"
GITHUB_GRAPHQL = "https://api.github.com/graphql"

# Headers for REST API
REST_HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

# Headers for GraphQL API (with sub-issues preview feature)
GRAPHQL_HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json",
    "GraphQL-Features": "sub_issues",
}

# Rate limiting
REQUEST_DELAY = 0.5  # seconds between requests


def make_rest_request(method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
    """Make a REST API request to GitHub."""
    url = f"{GITHUB_API}{endpoint}"
    response = requests.request(method, url, headers=REST_HEADERS, json=data)
    
    if response.status_code == 429:
        retry_after = int(response.headers.get("Retry-After", 60))
        print(f"Rate limited. Waiting {retry_after} seconds...")
        time.sleep(retry_after)
        return make_rest_request(method, endpoint, data)
    
    response.raise_for_status()
    return response.json() if response.content else {}


def make_graphql_request(query: str, variables: Optional[Dict] = None) -> Dict:
    """Make a GraphQL API request to GitHub."""
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    
    response = requests.post(GITHUB_GRAPHQL, headers=GRAPHQL_HEADERS, json=payload)
    
    if response.status_code == 429:
        retry_after = int(response.headers.get("Retry-After", 60))
        print(f"Rate limited. Waiting {retry_after} seconds...")
        time.sleep(retry_after)
        return make_graphql_request(query, variables)
    
    response.raise_for_status()
    result = response.json()
    
    if "errors" in result:
        raise Exception(f"GraphQL errors: {result['errors']}")
    
    return result.get("data", {})


def get_project_id(project_number: int) -> str:
    """Get the GraphQL node ID for a GitHub Project."""
    query = """
    query($owner: String!, $repo: String!, $number: Int!) {
      repository(owner: $owner, name: $repo) {
        projectV2(number: $number) {
          id
        }
      }
    }
    """
    variables = {
        "owner": REPO_OWNER,
        "repo": REPO_NAME,
        "number": project_number,
    }
    result = make_graphql_request(query, variables)
    project_id = result.get("repository", {}).get("projectV2", {}).get("id")
    if not project_id:
        raise Exception(f"Project #{project_number} not found")
    return project_id


def create_label(name: str, color: str, description: str = "") -> bool:
    """Create a label if it doesn't exist."""
    try:
        endpoint = f"/repos/{REPO_OWNER}/{REPO_NAME}/labels"
        make_rest_request("POST", endpoint, {
            "name": name,
            "color": color,
            "description": description,
        })
        print(f"✓ Created label: {name}")
        time.sleep(REQUEST_DELAY)
        return True
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 422:
            print(f"  Label '{name}' already exists, skipping")
            return False
        raise


def create_labels():
    """Create all required labels."""
    print("\n=== Creating Labels ===")
    labels = [
        ("Epic", "8B5CF6", "Epic-level issue"),
        ("User Story", "0052CC", "User Story issue"),
        ("Task", "4BCE97", "Development task"),
        ("Sprint", "FBCA04", "Sprint container"),
        ("Backend", "1D76DB", "Backend development"),
        ("Frontend", "E99695", "Frontend development"),
        ("Priority: P0", "D73A4A", "Critical priority"),
        ("Priority: P1", "FBCA04", "High priority"),
    ]
    
    for name, color, description in labels:
        create_label(name, color, description)
        time.sleep(REQUEST_DELAY)


def get_issue_node_id(issue_number: int) -> str:
    """Get the GraphQL node ID for an issue."""
    query = """
    query($owner: String!, $repo: String!, $number: Int!) {
      repository(owner: $owner, name: $repo) {
        issue(number: $number) {
          id
        }
      }
    }
    """
    variables = {
        "owner": REPO_OWNER,
        "repo": REPO_NAME,
        "number": issue_number,
    }
    result = make_graphql_request(query, variables)
    issue_id = result.get("repository", {}).get("issue", {}).get("id")
    if not issue_id:
        raise Exception(f"Issue #{issue_number} not found")
    return issue_id


def add_issue_to_project(issue_node_id: str, project_id: str) -> bool:
    """Add an issue to a GitHub Project."""
    query = """
    mutation($projectId: ID!, $contentId: ID!) {
      addProjectV2ItemById(input: { projectId: $projectId, contentId: $contentId }) {
        item {
          id
        }
      }
    }
    """
    variables = {
        "projectId": project_id,
        "contentId": issue_node_id,
    }
    try:
        make_graphql_request(query, variables)
        return True
    except Exception as e:
        print(f"  Warning: Could not add issue to project: {e}")
        return False


def create_issue(title: str, body: str, labels: List[str], project_id: Optional[str] = None) -> int:
    """Create an issue and optionally add it to a project."""
    endpoint = f"/repos/{REPO_OWNER}/{REPO_NAME}/issues"
    data = {
        "title": title,
        "body": body,
        "labels": labels,
    }
    
    result = make_rest_request("POST", endpoint, data)
    issue_number = result["number"]
    print(f"✓ Created issue #{issue_number}: {title}")
    time.sleep(REQUEST_DELAY)
    
    # Add to project if provided
    if project_id:
        issue_node_id = get_issue_node_id(issue_number)
        add_issue_to_project(issue_node_id, project_id)
        time.sleep(REQUEST_DELAY)
    
    return issue_number


def link_sub_issue(parent_issue_number: int, child_issue_number: int) -> bool:
    """Link a child issue to a parent issue using GraphQL addSubIssue mutation."""
    parent_id = get_issue_node_id(parent_issue_number)
    child_id = get_issue_node_id(child_issue_number)
    
    query = """
    mutation($parentId: ID!, $childId: ID!) {
      addSubIssue(input: { issueId: $parentId, subIssueId: $childId }) {
        issue { id title }
        subIssue { id title }
      }
    }
    """
    variables = {
        "parentId": parent_id,
        "childId": child_id,
    }
    
    try:
        result = make_graphql_request(query, variables)
        print(f"  ✓ Linked issue #{child_issue_number} to parent #{parent_issue_number}")
        time.sleep(REQUEST_DELAY)
        return True
    except Exception as e:
        print(f"  ✗ Failed to link issue #{child_issue_number} to parent #{parent_issue_number}: {e}")
        return False


def create_sprint_issues(project_id: str) -> Dict[int, int]:
    """Create Sprint 0-8 issues."""
    print("\n=== Creating Sprint Issues ===")
    sprints = {
        0: "Foundation - Setup infrastructure, CI/CD, base project structure",
        1: "User Service - Auth, registration, addresses, payment methods",
        2: "Catalog Service - Restaurant registration, menu management",
        3: "Search Service + Order Part 1 - Geo-search, cart, coupons",
        4: "Order Part 2 + Payment - Order placement, payment processing",
        5: "Delivery Service + WebSocket - Driver management, real-time tracking",
        6: "Notifications + Saga - Push notifications, distributed transactions",
        7: "Rating + Admin - Rating system, admin dashboard, polish",
        8: "Testing + Launch - E2E testing, security audit, production deployment",
    }
    
    sprint_issues = {}
    for sprint_num, description in sprints.items():
        title = f"Sprint {sprint_num}: {description.split(' - ')[0]}"
        body = f"""## Sprint {sprint_num}

**Goal:** {description}

This sprint container holds all development tasks for Sprint {sprint_num}.
"""
        issue_number = create_issue(
            title=title,
            body=body,
            labels=["Sprint"],
            project_id=project_id,
        )
        sprint_issues[sprint_num] = issue_number
    
    return sprint_issues


def create_epics(project_id: str) -> Dict[str, int]:
    """Create all EPICs."""
    print("\n=== Creating EPICs ===")
    epics = [
        {
            "id": "EPIC-1",
            "title": "Epic 1: Identity & Access Management",
            "priority": "P0",
            "description": "User authentication, registration, profile management, addresses, and payment methods.",
        },
        {
            "id": "EPIC-2",
            "title": "Epic 2: Restaurant & Menu Catalog",
            "priority": "P0",
            "description": "Restaurant registration, menu management, and catalog browsing.",
        },
        {
            "id": "EPIC-3",
            "title": "Epic 3: Search & Discovery",
            "priority": "P0",
            "description": "Geo-based restaurant search, filtering, and discovery features.",
        },
        {
            "id": "EPIC-4",
            "title": "Epic 4: Order Management",
            "priority": "P0",
            "description": "Order placement, cart management, order lifecycle, and restaurant order handling.",
        },
        {
            "id": "EPIC-5",
            "title": "Epic 5: Payment Processing",
            "priority": "P0",
            "description": "Payment processing, refunds, and idempotency handling.",
        },
        {
            "id": "EPIC-6",
            "title": "Epic 6: Delivery & Tracking",
            "priority": "P0",
            "description": "Driver management, delivery assignment, and real-time tracking.",
        },
        {
            "id": "EPIC-7",
            "title": "Epic 7: Notifications",
            "priority": "P0",
            "description": "Push notifications and SMS for status changes and critical events.",
        },
        {
            "id": "EPIC-8",
            "title": "Epic 8: Rating & Review",
            "priority": "P1",
            "description": "Restaurant and driver rating system.",
        },
        {
            "id": "EPIC-9",
            "title": "Epic 9: Admin Portal",
            "priority": "P1",
            "description": "Admin dashboard, KPI metrics, and administrative operations.",
        },
        {
            "id": "EPIC-10",
            "title": "Epic 10: Dispute Management",
            "priority": "P0",
            "description": "Dispute creation, tracking, and resolution workflow.",
        },
        {
            "id": "EPIC-11",
            "title": "Epic 11: Exception Flows",
            "priority": "P0",
            "description": "Exception handling for unreachable customers, address mismatches, SLA misses, and emergencies.",
        },
    ]
    
    epic_issues = {}
    for epic in epics:
        priority_label = f"Priority: {epic['priority']}"
        body = f"""## {epic['title']}

**Priority:** {epic['priority']}

**Description:**
{epic['description']}

This epic contains all related user stories.
"""
        issue_number = create_issue(
            title=epic["title"],
            body=body,
            labels=["Epic", priority_label],
            project_id=project_id,
        )
        epic_issues[epic["id"]] = issue_number
    
    return epic_issues


def create_user_stories(epic_issues: Dict[str, int], project_id: str) -> Dict[str, int]:
    """Create all User Stories and link them to EPICs."""
    print("\n=== Creating User Stories ===")
    
    user_stories = [
        # Epic 1: Identity & Access Management
        {"id": "US-AUTH-01", "epic": "EPIC-1", "title": "As a user, I can register with email/phone + OTP", "priority": "P0"},
        {"id": "US-AUTH-02", "epic": "EPIC-1", "title": "As a user, I can login and receive JWT tokens", "priority": "P0"},
        {"id": "US-AUTH-03", "epic": "EPIC-1", "title": "As a user, I can reset my password", "priority": "P1"},
        {"id": "US-AUTH-04", "epic": "EPIC-1", "title": "As a user, I can manage my profile", "priority": "P1"},
        {"id": "US-AUTH-05", "epic": "EPIC-1", "title": "As a user, I can manage delivery addresses", "priority": "P0"},
        {"id": "US-AUTH-06", "epic": "EPIC-1", "title": "As a user, I can add payment methods", "priority": "P0"},
        
        # Epic 2: Restaurant & Menu Catalog
        {"id": "US-CAT-01", "epic": "EPIC-2", "title": "As a restaurant owner, I can register my restaurant", "priority": "P0"},
        {"id": "US-CAT-02", "epic": "EPIC-2", "title": "As a restaurant owner, I can manage menu categories", "priority": "P0"},
        {"id": "US-CAT-03", "epic": "EPIC-2", "title": "As a restaurant owner, I can manage menu items with variants", "priority": "P0"},
        {"id": "US-CAT-04", "epic": "EPIC-2", "title": "As a restaurant owner, I can toggle accepting orders", "priority": "P0"},
        {"id": "US-CAT-05", "epic": "EPIC-2", "title": "As a customer, I can view restaurant details and menu", "priority": "P0"},
        
        # Epic 3: Search & Discovery
        {"id": "US-SEARCH-01", "epic": "EPIC-3", "title": "As a customer, I can search restaurants by location", "priority": "P0"},
        {"id": "US-SEARCH-02", "epic": "EPIC-3", "title": "As a customer, I can filter by rating, distance, open status", "priority": "P0"},
        {"id": "US-SEARCH-03", "epic": "EPIC-3", "title": "As a customer, I can see search results with pagination", "priority": "P1"},
        
        # Epic 4: Order Management
        {"id": "US-ORD-01", "epic": "EPIC-4", "title": "As a customer, I can add items to cart", "priority": "P0"},
        {"id": "US-ORD-02", "epic": "EPIC-4", "title": "As a customer, I can apply coupon codes", "priority": "P0"},
        {"id": "US-ORD-03", "epic": "EPIC-4", "title": "As a customer, I can place an order", "priority": "P0"},
        {"id": "US-ORD-04", "epic": "EPIC-4", "title": "As a customer, I can view order history", "priority": "P1"},
        {"id": "US-ORD-05", "epic": "EPIC-4", "title": "As a customer, I can cancel order before restaurant accepts", "priority": "P0"},
        {"id": "US-ORD-06", "epic": "EPIC-4", "title": "As a customer, I can reorder from history", "priority": "P1"},
        {"id": "US-ORD-07", "epic": "EPIC-4", "title": "As a restaurant, I can view and accept/reject orders", "priority": "P0"},
        {"id": "US-ORD-08", "epic": "EPIC-4", "title": "As a restaurant, I can update order status (preparing, ready)", "priority": "P0"},
        
        # Epic 5: Payment Processing
        {"id": "US-PAY-01", "epic": "EPIC-5", "title": "As a customer, I can pay with COD", "priority": "P0"},
        {"id": "US-PAY-02", "epic": "EPIC-5", "title": "As a customer, I can pay with card (Stripe/VNPay)", "priority": "P0"},
        {"id": "US-PAY-03", "epic": "EPIC-5", "title": "As a system, I handle refunds on cancellation", "priority": "P0"},
        {"id": "US-PAY-04", "epic": "EPIC-5", "title": "As a system, I prevent double-charges with idempotency", "priority": "P0"},
        
        # Epic 6: Delivery & Tracking
        {"id": "US-DEL-01", "epic": "EPIC-6", "title": "As a driver, I can register with documents", "priority": "P0"},
        {"id": "US-DEL-02", "epic": "EPIC-6", "title": "As a driver, I can go online/offline", "priority": "P0"},
        {"id": "US-DEL-03", "epic": "EPIC-6", "title": "As a driver, I can receive and accept delivery tasks", "priority": "P0"},
        {"id": "US-DEL-04", "epic": "EPIC-6", "title": "As a driver, I can update delivery status", "priority": "P0"},
        {"id": "US-DEL-05", "epic": "EPIC-6", "title": "As a customer, I can track order status in real-time", "priority": "P0"},
        {"id": "US-DEL-06", "epic": "EPIC-6", "title": "As a customer, I can see driver location on map", "priority": "P0"},
        {"id": "US-DEL-07", "epic": "EPIC-6", "title": "As a driver, I can view my earnings", "priority": "P1"},
        
        # Epic 7: Notifications
        {"id": "US-NOTIF-01", "epic": "EPIC-7", "title": "As a user, I receive push notifications on status changes", "priority": "P0"},
        {"id": "US-NOTIF-02", "epic": "EPIC-7", "title": "As a user, I receive SMS for critical events", "priority": "P1"},
        
        # Epic 8: Rating & Review
        {"id": "US-RATE-01", "epic": "EPIC-8", "title": "As a customer, I can rate restaurant after delivery", "priority": "P1"},
        {"id": "US-RATE-02", "epic": "EPIC-8", "title": "As a customer, I can rate driver after delivery", "priority": "P1"},
        
        # Epic 9: Admin Portal
        {"id": "US-ADM-01", "epic": "EPIC-9", "title": "As an admin, I can view dashboard KPIs", "priority": "P1"},
        {"id": "US-ADM-02", "epic": "EPIC-9", "title": "As an admin, I can approve/reject restaurants", "priority": "P0"},
        {"id": "US-ADM-03", "epic": "EPIC-9", "title": "As an admin, I can approve/reject drivers", "priority": "P0"},
        {"id": "US-ADM-04", "epic": "EPIC-9", "title": "As an admin, I can manage coupons", "priority": "P1"},
        
        # Epic 10: Dispute Management
        {"id": "US-DISPUTE-01", "epic": "EPIC-10", "title": "As a customer, I can create a dispute ticket within 24h of delivery", "priority": "P0"},
        {"id": "US-DISPUTE-02", "epic": "EPIC-10", "title": "As a customer, I can upload photo evidence for disputes", "priority": "P0"},
        {"id": "US-DISPUTE-03", "epic": "EPIC-10", "title": "As an admin, I can review and resolve disputes", "priority": "P0"},
        
        # Epic 11: Exception Flows
        {"id": "US-EXC-01", "epic": "EPIC-11", "title": "As a driver, I can mark customer unreachable after 3 call attempts", "priority": "P0"},
        {"id": "US-EXC-02", "epic": "EPIC-11", "title": "As a driver, I can report address mismatch and request correction", "priority": "P0"},
        {"id": "US-EXC-03", "epic": "EPIC-11", "title": "As a system, I auto-cancel orders when SLA miss >60min", "priority": "P0"},
        {"id": "US-EXC-04", "epic": "EPIC-11", "title": "As a driver, I can report emergency and trigger reassignment", "priority": "P1"},
    ]
    
    us_issues = {}
    for us in user_stories:
        priority_label = f"Priority: {us['priority']}"
        body = f"""## {us['id']}: {us['title']}

**Priority:** {us['priority']}

**Epic:** {us['epic']}

**Acceptance Criteria:**
- [ ] TBD

**Dependencies:**
- TBD
"""
        issue_number = create_issue(
            title=f"{us['id']}: {us['title']}",
            body=body,
            labels=["User Story", priority_label],
            project_id=project_id,
        )
        us_issues[us["id"]] = issue_number
        
        # Link to parent EPIC
        parent_issue_number = epic_issues[us["epic"]]
        link_sub_issue(parent_issue_number, issue_number)
    
    return us_issues


def create_tasks(sprint_issues: Dict[int, int], project_id: str) -> Dict[str, int]:
    """Create all Tasks and link them to Sprint issues."""
    print("\n=== Creating Tasks ===")
    
    # Define all tasks by sprint
    tasks_by_sprint = {
        0: [
            {"id": "INFRA-001", "title": "Setup Git repository with branching strategy", "type": "Backend", "est": "2h"},
            {"id": "INFRA-002", "title": "Setup Docker Compose for local development (PostgreSQL, Redis, Kafka)", "type": "Backend", "est": "4h"},
            {"id": "INFRA-003", "title": "Create Kubernetes manifests (Helm charts)", "type": "Backend", "est": "8h"},
            {"id": "INFRA-004", "title": "Setup CI/CD pipeline (GitHub Actions → Docker Hub → AWS)", "type": "Backend", "est": "8h"},
            {"id": "INFRA-005", "title": "Database migration framework setup (golang-migrate)", "type": "Backend", "est": "4h"},
            {"id": "INFRA-006", "title": "Create base project structure for microservices", "type": "Backend", "est": "6h"},
            {"id": "INFRA-007", "title": "Setup API Gateway (Nginx/Envoy) with basic routing", "type": "Backend", "est": "6h"},
            {"id": "INFRA-008", "title": "Configure observability stack (Prometheus, Grafana, ELK)", "type": "Backend", "est": "8h"},
            {"id": "INFRA-009", "title": "Create shared Go libraries (logging, errors, middleware)", "type": "Backend", "est": "8h"},
            {"id": "INFRA-010", "title": "Setup JWKS endpoint for JWT RS256 verification", "type": "Backend", "est": "4h"},
            {"id": "SEC-001", "title": "Security headers middleware (X-Content-Type-Options, HSTS, CSP)", "type": "Backend", "est": "4h"},
            {"id": "INFRA-011", "title": "Audit logging infrastructure setup", "type": "Backend", "est": "4h"},
            {"id": "INFRA-012", "title": "Redis Pub/Sub verification for WebSocket scaling", "type": "Backend", "est": "4h"},
            {"id": "DB-000", "title": "Create `cities` and `audit_logs` base tables", "type": "Backend", "est": "3h"},
            {"id": "[Front]-001", "title": "Setup React Native monorepo (Customer, Restaurant, Driver apps)", "type": "Frontend", "est": "8h"},
            {"id": "[Front]-002", "title": "Setup React Admin Dashboard project with Vite", "type": "Frontend", "est": "4h"},
            {"id": "[Front]-003", "title": "Configure shared component library (design tokens, themes)", "type": "Frontend", "est": "6h"},
            {"id": "[Front]-004", "title": "Setup navigation structure for all mobile apps", "type": "Frontend", "est": "6h"},
            {"id": "[Front]-005", "title": "Configure API client with Axios/React Query + interceptors", "type": "Frontend", "est": "4h"},
            {"id": "[Front]-006", "title": "Setup CI/CD for mobile builds (EAS Build / Fastlane)", "type": "Frontend", "est": "8h"},
            {"id": "[Front]-007", "title": "Create base UI components (Button, Input, Card, Badge)", "type": "Frontend", "est": "8h"},
        ],
        1: [
            {"id": "DB-001", "title": "Create `users`, `user_addresses`, `user_payment_methods`, `refresh_tokens` tables", "type": "Backend", "est": "4h"},
            {"id": "API-001", "title": "POST `/api/v1/auth/register` - Email/phone registration", "type": "Backend", "est": "8h"},
            {"id": "API-002", "title": "POST `/api/v1/auth/login` - JWT RS256 token generation", "type": "Backend", "est": "8h"},
            {"id": "API-003", "title": "POST `/api/v1/auth/refresh` - Refresh token rotation", "type": "Backend", "est": "4h"},
            {"id": "API-004", "title": "CRUD `/api/v1/users/addresses` - Delivery addresses", "type": "Backend", "est": "6h"},
            {"id": "API-005", "title": "CRUD `/api/v1/users/payment-methods` - Tokenized payment", "type": "Backend", "est": "6h"},
            {"id": "API-006", "title": "POST `/api/v1/auth/password-reset` - Password reset with OTP", "type": "Backend", "est": "4h"},
            {"id": "INT-001", "title": "OTP service integration (Twilio SMS)", "type": "Backend", "est": "4h"},
            {"id": "INT-002", "title": "Redis integration for JWT blacklist", "type": "Backend", "est": "4h"},
            {"id": "TEST-001", "title": "Unit tests for auth logic (80% coverage)", "type": "Backend", "est": "8h"},
            {"id": "TEST-002", "title": "Integration tests for auth flow", "type": "Backend", "est": "4h"},
            {"id": "[Front]-008", "title": "Customer: Splash + Onboarding screens (4 screens)", "type": "Frontend", "est": "6h"},
            {"id": "[Front]-009", "title": "Customer: Login screen with form validation", "type": "Frontend", "est": "4h"},
            {"id": "[Front]-010", "title": "Customer: Registration screen with OTP verification", "type": "Frontend", "est": "6h"},
            {"id": "[Front]-011", "title": "Customer: Profile screen", "type": "Frontend", "est": "4h"},
            {"id": "[Front]-012", "title": "Customer: Saved Addresses screen (CRUD)", "type": "Frontend", "est": "6h"},
            {"id": "[Front]-013", "title": "Customer: Payment Methods screen (tokenized cards)", "type": "Frontend", "est": "6h"},
            {"id": "[Front]-014", "title": "Restaurant: Login/Registration screens", "type": "Frontend", "est": "4h"},
            {"id": "[Front]-015", "title": "Driver: Login/Registration screens", "type": "Frontend", "est": "4h"},
            {"id": "[Front]-016", "title": "Shared: Auth state management (Zustand/Redux)", "type": "Frontend", "est": "4h"},
            {"id": "[Front]-017", "title": "Shared: Secure token storage (AsyncStorage/SecureStore)", "type": "Frontend", "est": "4h"},
        ],
        2: [
            {"id": "DB-002", "title": "Create `restaurants`, `menu_categories`, `menu_items`, `menu_item_variants` tables", "type": "Backend", "est": "4h"},
            {"id": "API-007", "title": "POST `/api/v1/restaurants` - Restaurant registration", "type": "Backend", "est": "6h"},
            {"id": "API-008", "title": "GET `/api/v1/restaurants/{id}` - Restaurant detail", "type": "Backend", "est": "4h"},
            {"id": "API-009", "title": "CRUD `/api/v1/restaurants/{id}/menu-categories`", "type": "Backend", "est": "6h"},
            {"id": "API-010", "title": "CRUD `/api/v1/restaurants/{id}/menu-items` with variants", "type": "Backend", "est": "8h"},
            {"id": "API-011", "title": "PUT `/api/v1/restaurants/{id}/status` - Toggle accepting orders", "type": "Backend", "est": "3h"},
            {"id": "API-012", "title": "GET `/api/v1/restaurants/{id}/menu` - Full menu view", "type": "Backend", "est": "4h"},
            {"id": "API-013", "title": "Admin restaurant approval endpoints (PENDING → APPROVED/REJECTED)", "type": "Backend", "est": "6h"},
            {"id": "INT-003", "title": "S3/MinIO integration for image upload", "type": "Backend", "est": "6h"},
            {"id": "CACHE-001", "title": "Redis cache for restaurant/menu data", "type": "Backend", "est": "4h"},
            {"id": "TEST-003", "title": "Unit + integration tests", "type": "Backend", "est": "8h"},
            {"id": "[Front]-018", "title": "Customer: Home screen with featured restaurants", "type": "Frontend", "est": "8h"},
            {"id": "[Front]-019", "title": "Customer: Restaurant Detail screen with tabs", "type": "Frontend", "est": "8h"},
            {"id": "[Front]-020", "title": "Customer: Food Item Detail modal/bottom sheet", "type": "Frontend", "est": "4h"},
            {"id": "[Front]-021", "title": "Restaurant: Dashboard screen", "type": "Frontend", "est": "6h"},
            {"id": "[Front]-022", "title": "Restaurant: Menu List screen", "type": "Frontend", "est": "6h"},
            {"id": "[Front]-023", "title": "Restaurant: Add/Edit Menu Item modal with variants", "type": "Frontend", "est": "8h"},
            {"id": "[Front]-024", "title": "Restaurant: Category Management modal", "type": "Frontend", "est": "4h"},
            {"id": "[Front]-025", "title": "Restaurant: Settings screen (toggle accepting orders)", "type": "Frontend", "est": "4h"},
            {"id": "[Front]-026", "title": "Admin: Restaurant Management screen (approve/reject)", "type": "Frontend", "est": "8h"},
            {"id": "[Front]-027", "title": "Shared: Image upload component with S3", "type": "Frontend", "est": "4h"},
        ],
        3: [
            {"id": "DB-003", "title": "Create `coupons`, `coupon_usages` tables", "type": "Backend", "est": "3h"},
            {"id": "API-014", "title": "GET `/api/v1/restaurants` - Geo-search with filters", "type": "Backend", "est": "10h"},
            {"id": "API-015", "title": "GET `/api/v1/search` - Full-text search", "type": "Backend", "est": "6h"},
            {"id": "CACHE-002", "title": "Redis caching for search results", "type": "Backend", "est": "4h"},
            {"id": "API-016", "title": "Cart management (in-memory/Redis per user)", "type": "Backend", "est": "8h"},
            {"id": "API-017", "title": "POST `/api/v1/coupons/validate` - Coupon validation", "type": "Backend", "est": "6h"},
            {"id": "API-018", "title": "Pricing engine (subtotal + tax + delivery fee - discount)", "type": "Backend", "est": "6h"},
            {"id": "INDEX-001", "title": "PostgreSQL GiST index for geo-queries", "type": "Backend", "est": "4h"},
            {"id": "TEST-004", "title": "Unit + integration tests", "type": "Backend", "est": "8h"},
            {"id": "[Front]-028", "title": "Customer: Search screen with autocomplete", "type": "Frontend", "est": "6h"},
            {"id": "[Front]-029", "title": "Customer: Search Results with filters (distance, rating, open)", "type": "Frontend", "est": "8h"},
            {"id": "[Front]-030", "title": "Customer: Filter Modal", "type": "Frontend", "est": "4h"},
            {"id": "[Front]-031", "title": "Customer: Category View screen", "type": "Frontend", "est": "4h"},
            {"id": "[Front]-032", "title": "Customer: Cart screen with item management", "type": "Frontend", "est": "8h"},
            {"id": "[Front]-033", "title": "Customer: Coupon input + validation UI", "type": "Frontend", "est": "4h"},
            {"id": "[Front]-034", "title": "Customer: Pricing breakdown component", "type": "Frontend", "est": "3h"},
            {"id": "[Front]-035", "title": "Shared: Map integration (Google Maps / Mapbox)", "type": "Frontend", "est": "8h"},
        ],
        4: [
            {"id": "DB-004", "title": "Create `orders`, `order_items`, `order_item_variants`, `payments`, `payment_refunds` tables", "type": "Backend", "est": "6h"},
            {"id": "API-019", "title": "POST `/api/v1/orders` - Create order with validation", "type": "Backend", "est": "12h"},
            {"id": "API-020", "title": "Order state machine implementation", "type": "Backend", "est": "8h"},
            {"id": "API-021", "title": "PUT `/api/v1/orders/{id}/cancel` - Cancellation with refund", "type": "Backend", "est": "6h"},
            {"id": "API-022", "title": "POST `/api/v1/payments/authorize` - Payment authorization", "type": "Backend", "est": "8h"},
            {"id": "API-023", "title": "POST `/api/v1/payments/{id}/capture` - Payment capture", "type": "Backend", "est": "6h"},
            {"id": "API-024", "title": "POST `/api/v1/payments/{id}/refund` - Refund processing", "type": "Backend", "est": "6h"},
            {"id": "INT-004", "title": "Stripe/VNPay gateway integration", "type": "Backend", "est": "12h"},
            {"id": "INT-005", "title": "Idempotency key implementation", "type": "Backend", "est": "4h"},
            {"id": "KAFKA-001", "title": "Kafka producer for order events", "type": "Backend", "est": "6h"},
            {"id": "KAFKA-002", "title": "Kafka consumer stubs for notification events", "type": "Backend", "est": "4h"},
            {"id": "TEST-005", "title": "Payment idempotency tests (critical)", "type": "Backend", "est": "8h"},
            {"id": "[Front]-036", "title": "Customer: Checkout Step 1 - Delivery address selection", "type": "Frontend", "est": "6h"},
            {"id": "[Front]-037", "title": "Customer: Checkout Step 2 - Payment method selection", "type": "Frontend", "est": "6h"},
            {"id": "[Front]-038", "title": "Customer: Checkout Step 3 - Order review + place order", "type": "Frontend", "est": "6h"},
            {"id": "[Front]-039", "title": "Customer: Order Confirmation screen", "type": "Frontend", "est": "4h"},
            {"id": "[Front]-040", "title": "Customer: Order History screen", "type": "Frontend", "est": "6h"},
            {"id": "[Front]-041", "title": "Customer: Order Detail screen", "type": "Frontend", "est": "4h"},
            {"id": "[Front]-042", "title": "Restaurant: Incoming Orders screen with accept/reject", "type": "Frontend", "est": "8h"},
            {"id": "[Front]-043", "title": "Restaurant: Order Detail (restaurant view)", "type": "Frontend", "est": "4h"},
            {"id": "[Front]-044", "title": "Restaurant: Preparing Orders screen with status updates", "type": "Frontend", "est": "6h"},
            {"id": "[Front]-045", "title": "Shared: Stripe/VNPay payment integration", "type": "Frontend", "est": "8h"},
        ],
        5: [
            {"id": "DB-005", "title": "Create `drivers`, `delivery_tasks`, `delivery_task_events`, `driver_location_history` tables", "type": "Backend", "est": "6h"},
            {"id": "DB-006", "title": "Configure `driver_location_history` table partitioning for performance", "type": "Backend", "est": "4h"},
            {"id": "API-025", "title": "POST `/api/v1/drivers/register` - Driver registration", "type": "Backend", "est": "6h"},
            {"id": "API-026", "title": "PUT `/api/v1/drivers/{id}/status` - Online/offline toggle", "type": "Backend", "est": "4h"},
            {"id": "API-027", "title": "Driver assignment algorithm (nearest available)", "type": "Backend", "est": "10h"},
            {"id": "API-028", "title": "PUT `/api/v1/delivery-tasks/{id}/status` - Status updates", "type": "Backend", "est": "6h"},
            {"id": "API-029", "title": "PUT `/api/v1/drivers/{id}/location` - GPS location updates (every 5s)", "type": "Backend", "est": "4h"},
            {"id": "API-030", "title": "Admin driver approval endpoints (PENDING → APPROVED/REJECTED)", "type": "Backend", "est": "6h"},
            {"id": "WS-001", "title": "WebSocket gateway setup (gorilla/websocket)", "type": "Backend", "est": "10h"},
            {"id": "WS-002", "title": "Order status subscription (order:{id} channel)", "type": "Backend", "est": "6h"},
            {"id": "WS-003", "title": "Driver location subscription (driver:location:{id})", "type": "Backend", "est": "6h"},
            {"id": "INT-006", "title": "Redis Pub/Sub for WebSocket scaling", "type": "Backend", "est": "6h"},
            {"id": "API-031", "title": "Restaurant order management (accept/reject, status update)", "type": "Backend", "est": "8h"},
            {"id": "TEST-006", "title": "WebSocket integration tests", "type": "Backend", "est": "6h"},
            {"id": "[Front]-046", "title": "Customer: Order Tracking - Live Map screen", "type": "Frontend", "est": "10h"},
            {"id": "[Front]-047", "title": "Customer: WebSocket integration for real-time updates", "type": "Frontend", "est": "6h"},
            {"id": "[Front]-048", "title": "Driver: Home screen (Online/Offline toggle)", "type": "Frontend", "est": "6h"},
            {"id": "[Front]-049", "title": "Driver: Available Deliveries list", "type": "Frontend", "est": "4h"},
            {"id": "[Front]-050", "title": "Driver: Active Delivery - Pickup screen with navigation", "type": "Frontend", "est": "8h"},
            {"id": "[Front]-051", "title": "Driver: Active Delivery - Dropoff screen", "type": "Frontend", "est": "6h"},
            {"id": "[Front]-052", "title": "Driver: Delivery Complete screen", "type": "Frontend", "est": "3h"},
            {"id": "[Front]-053", "title": "Driver: GPS location tracking service (background)", "type": "Frontend", "est": "8h"},
            {"id": "[Front]-054", "title": "Driver: WebSocket integration for task assignment", "type": "Frontend", "est": "6h"},
            {"id": "[Front]-055", "title": "Admin: Driver Management screen (approve/reject)", "type": "Frontend", "est": "6h"},
        ],
        6: [
            {"id": "DB-007", "title": "Create `disputes` table", "type": "Backend", "est": "3h"},
            {"id": "API-032", "title": "Notification service setup", "type": "Backend", "est": "6h"},
            {"id": "API-033", "title": "Notification preference APIs", "type": "Backend", "est": "4h"},
            {"id": "INT-007", "title": "FCM integration for push notifications", "type": "Backend", "est": "8h"},
            {"id": "INT-008", "title": "Twilio SMS integration", "type": "Backend", "est": "4h"},
            {"id": "KAFKA-003", "title": "Kafka consumers for notification events", "type": "Backend", "est": "8h"},
            {"id": "SAGA-001", "title": "Order creation saga implementation", "type": "Backend", "est": "12h"},
            {"id": "SAGA-002", "title": "Compensation handlers for each saga step", "type": "Backend", "est": "10h"},
            {"id": "EXC-001", "title": "FR-ORD-11: Customer unreachable flow (mark after 3 attempts)", "type": "Backend", "est": "6h"},
            {"id": "EXC-002", "title": "FR-ORD-12: Address correction flow (driver reports mismatch)", "type": "Backend", "est": "6h"},
            {"id": "EXC-003", "title": "FR-ORD-14: SLA miss auto-cancellation scheduler (>60min)", "type": "Backend", "est": "6h"},
            {"id": "EXC-004", "title": "FR-DEL-10: Driver emergency and reassignment flow", "type": "Backend", "est": "6h"},
            {"id": "API-034", "title": "POST `/api/v1/disputes` - Create dispute ticket", "type": "Backend", "est": "6h"},
            {"id": "API-035", "title": "GET `/api/v1/disputes` - List user disputes", "type": "Backend", "est": "4h"},
            {"id": "TEST-007", "title": "Saga compensation tests", "type": "Backend", "est": "8h"},
            {"id": "[Front]-056", "title": "Customer: Push notification integration (FCM)", "type": "Frontend", "est": "6h"},
            {"id": "[Front]-057", "title": "Customer: Notification Settings screen", "type": "Frontend", "est": "3h"},
            {"id": "[Front]-058", "title": "Customer: Create Dispute screen with photo upload", "type": "Frontend", "est": "6h"},
            {"id": "[Front]-059", "title": "Driver: Push notification for new delivery tasks", "type": "Frontend", "est": "4h"},
            {"id": "[Front]-060", "title": "Driver: Customer unreachable flow UI (3 call attempts)", "type": "Frontend", "est": "4h"},
            {"id": "[Front]-061", "title": "Driver: Address mismatch report modal", "type": "Frontend", "est": "3h"},
            {"id": "[Front]-062", "title": "Driver: Emergency report flow", "type": "Frontend", "est": "3h"},
            {"id": "[Front]-063", "title": "Restaurant: Push notification for new orders", "type": "Frontend", "est": "4h"},
            {"id": "[Front]-064", "title": "Admin: Dispute Management screen", "type": "Frontend", "est": "6h"},
        ],
        7: [
            {"id": "DB-008", "title": "Create `ratings` table", "type": "Backend", "est": "3h"},
            {"id": "API-036", "title": "POST `/api/v1/restaurants/{id}/ratings`", "type": "Backend", "est": "4h"},
            {"id": "API-037", "title": "POST `/api/v1/drivers/{id}/ratings`", "type": "Backend", "est": "4h"},
            {"id": "API-038", "title": "Aggregate rating calculation", "type": "Backend", "est": "4h"},
            {"id": "API-039", "title": "GET `/api/v1/admin/dashboard` - KPI metrics", "type": "Backend", "est": "8h"},
            {"id": "API-040", "title": "PUT `/api/v1/disputes/{id}/resolve` - Admin resolution", "type": "Backend", "est": "6h"},
            {"id": "API-041", "title": "Admin coupon management APIs", "type": "Backend", "est": "6h"},
            {"id": "API-042", "title": "Dispute metrics in admin dashboard", "type": "Backend", "est": "4h"},
            {"id": "SEC-002", "title": "Security headers implementation verification", "type": "Backend", "est": "4h"},
            {"id": "SEC-003", "title": "Rate limiting configuration", "type": "Backend", "est": "4h"},
            {"id": "OPS-001", "title": "Monitoring dashboards (Grafana)", "type": "Backend", "est": "8h"},
            {"id": "OPS-002", "title": "Alerting rules (P0 incidents)", "type": "Backend", "est": "4h"},
            {"id": "BUG-XXX", "title": "Bug fixes and performance optimization", "type": "Backend", "est": "16h"},
            {"id": "TEST-008", "title": "E2E tests for critical paths", "type": "Backend", "est": "12h"},
            {"id": "[Front]-065", "title": "Customer: Rate Order modal (restaurant + driver)", "type": "Frontend", "est": "6h"},
            {"id": "[Front]-066", "title": "Customer: Restaurant Reviews Tab", "type": "Frontend", "est": "4h"},
            {"id": "[Front]-067", "title": "Driver: Driver Profile screen", "type": "Frontend", "est": "4h"},
            {"id": "[Front]-068", "title": "Driver: Delivery History + Earnings screen", "type": "Frontend", "est": "6h"},
            {"id": "[Front]-069", "title": "Restaurant: Analytics View screen", "type": "Frontend", "est": "6h"},
            {"id": "[Front]-070", "title": "Restaurant: Order History screen", "type": "Frontend", "est": "4h"},
            {"id": "[Front]-071", "title": "Admin: Dashboard screen with KPIs", "type": "Frontend", "est": "8h"},
            {"id": "[Front]-072", "title": "Admin: User Management screen", "type": "Frontend", "est": "6h"},
            {"id": "[Front]-073", "title": "Admin: Order Management screen", "type": "Frontend", "est": "6h"},
            {"id": "[Front]-074", "title": "Admin: Payment Management screen", "type": "Frontend", "est": "4h"},
            {"id": "[Front]-075", "title": "Admin: Coupon Management screen", "type": "Frontend", "est": "6h"},
            {"id": "[Front]-076", "title": "All Apps: Bug fixes and UI polish", "type": "Frontend", "est": "16h"},
        ],
        8: [
            {"id": "TEST-009", "title": "Full E2E testing of all user journeys", "type": "Backend", "est": "16h"},
            {"id": "TEST-010", "title": "Load testing (target: 5k concurrent users)", "type": "Backend", "est": "12h"},
            {"id": "SEC-004", "title": "Security penetration testing", "type": "Backend", "est": "12h"},
            {"id": "PERF-001", "title": "Performance optimization based on test results", "type": "Backend", "est": "12h"},
            {"id": "OPS-003", "title": "Production environment setup (AWS EKS)", "type": "Backend", "est": "8h"},
            {"id": "OPS-004", "title": "Database migration to production", "type": "Backend", "est": "4h"},
            {"id": "OPS-005", "title": "SSL/TLS certificate setup", "type": "Backend", "est": "2h"},
            {"id": "OPS-006", "title": "DNS configuration", "type": "Backend", "est": "2h"},
            {"id": "OPS-007", "title": "Monitoring and alerting verification", "type": "Backend", "est": "4h"},
            {"id": "DOC-001", "title": "Runbook documentation", "type": "Backend", "est": "8h"},
            {"id": "OPS-008", "title": "On-call rotation setup", "type": "Backend", "est": "2h"},
            {"id": "LAUNCH-01", "title": "Go-live checklist completion", "type": "Backend", "est": "4h"},
            {"id": "[Front]-077", "title": "Admin: Revenue Reports screen", "type": "Frontend", "est": "6h"},
            {"id": "[Front]-078", "title": "Admin: Performance Reports screen", "type": "Frontend", "est": "4h"},
            {"id": "[Front]-079", "title": "Admin: User Analytics screen", "type": "Frontend", "est": "4h"},
            {"id": "[Front]-080", "title": "All Apps: E2E testing with Detox (mobile) / Cypress (web)", "type": "Frontend", "est": "16h"},
            {"id": "[Front]-081", "title": "All Apps: Accessibility audit and fixes", "type": "Frontend", "est": "8h"},
            {"id": "[Front]-082", "title": "Mobile: App Store / Play Store submission preparation", "type": "Frontend", "est": "8h"},
            {"id": "[Front]-083", "title": "Admin: Production deployment (Vercel/AWS)", "type": "Frontend", "est": "4h"},
            {"id": "[Front]-084", "title": "All Apps: Performance optimization", "type": "Frontend", "est": "8h"},
        ],
    }
    
    task_issues = {}
    for sprint_num, tasks in tasks_by_sprint.items():
        sprint_issue_number = sprint_issues[sprint_num]
        print(f"\n  Creating tasks for Sprint {sprint_num}...")
        
        for task in tasks:
            type_label = task["type"]
            body = f"""## {task['id']}: {task['title']}

**Type:** {task['type']}
**Estimate:** {task['est']}
**Sprint:** {sprint_num}

**Description:**
{task['title']}

**Acceptance Criteria:**
- [ ] TBD

**Dependencies:**
- TBD
"""
            issue_number = create_issue(
                title=f"{task['id']}: {task['title']}",
                body=body,
                labels=["Task", type_label],
                project_id=project_id,
            )
            task_issues[task["id"]] = issue_number
            
            # Link to parent Sprint
            link_sub_issue(sprint_issue_number, issue_number)
    
    return task_issues


def main():
    """Main execution function."""
    print("=" * 60)
    print("GitHub MVP Project Creation Script")
    print("=" * 60)
    print(f"Repository: {REPO_OWNER}/{REPO_NAME}")
    print(f"Project: #{PROJECT_NUMBER}")
    print()
    
    # Get project ID
    print("Getting project ID...")
    try:
        project_id = get_project_id(PROJECT_NUMBER)
        print(f"✓ Found project ID: {project_id}")
    except Exception as e:
        print(f"ERROR: Could not get project ID: {e}")
        sys.exit(1)
    
    # Create labels
    create_labels()
    
    # Create Sprint issues
    sprint_issues = create_sprint_issues(project_id)
    print(f"\n✓ Created {len(sprint_issues)} Sprint issues")
    
    # Create EPICs
    epic_issues = create_epics(project_id)
    print(f"\n✓ Created {len(epic_issues)} EPICs")
    
    # Create User Stories
    us_issues = create_user_stories(epic_issues, project_id)
    print(f"\n✓ Created {len(us_issues)} User Stories")
    
    # Create Tasks
    task_issues = create_tasks(sprint_issues, project_id)
    print(f"\n✓ Created {len(task_issues)} Tasks")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"✓ Labels created")
    print(f"✓ {len(sprint_issues)} Sprint issues created")
    print(f"✓ {len(epic_issues)} EPICs created")
    print(f"✓ {len(us_issues)} User Stories created and linked to EPICs")
    print(f"✓ {len(task_issues)} Tasks created and linked to Sprints")
    print(f"✓ All issues added to Project #{PROJECT_NUMBER}")
    print("\nDone! 🎉")


if __name__ == "__main__":
    main()
