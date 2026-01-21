# Food Delivery Platform

A comprehensive food delivery platform connecting customers, restaurants, and drivers in Ho Chi Minh City, Vietnam.

## 📋 Overview

This platform is a SaaS solution that enables:
- **Customers** to order food online with real-time tracking
- **Restaurants** to manage orders and menus through a dashboard
- **Drivers** to accept and deliver orders efficiently
- **Admins** to oversee platform operations

## 🏗️ Architecture

### System Architecture
- **Pattern:** Hexagonal Architecture (Ports & Adapters) with Event-Driven Microservices
- **Repository Structure:** Monorepo containing 10 microservices
- **Language:** Go 1.25+
- **Communication:** REST/gRPC (synchronous) + Kafka (asynchronous events)

### Microservices

1. **User Service** - Authentication, user management, profiles
2. **Catalog Service** - Restaurant and menu management
3. **Order Service** - Order lifecycle management
4. **Payment Service** - Payment processing and transactions
5. **Delivery Service** - Delivery assignment and tracking
6. **Search Service** - Restaurant and menu search
7. **Promotion Service** - Discounts and promotional campaigns
8. **Notification Service** - Push notifications and alerts
9. **Rating Service** - Reviews and ratings management
10. **Admin Service** - Administrative operations and analytics

## 🛠️ Technology Stack

### Backend
- **Language:** Go 1.25+
- **Framework:** Gin/Echo
- **Database:** PostgreSQL 14+
- **Cache:** Redis 7+
- **Message Broker:** Kafka 3+
- **WebSocket:** gorilla/websocket
- **Container:** Docker
- **Orchestration:** Kubernetes

### Frontend
- **Web:** React 18+ / Next.js with Vite
- **Mobile:** React Native 0.73+ (TypeScript) with Expo
- **State Management:** Zustand + React Query
- **UI Components:** React Native Paper / shadcn/ui
- **Maps:** React Native Maps / Google Maps API
- **Real-time:** socket.io-client

### DevOps
- **CI/CD:** GitHub Actions → Docker Hub → AWS EKS
- **Monitoring:** Prometheus + Grafana
- **Logging:** ELK Stack (Elasticsearch, Logstash, Kibana)
- **Tracing:** Jaeger
- **Error Tracking:** Sentry

## 📁 Project Structure

```
online_food_ordering_system/
├── docs/                    # Documentation
│   └── MVP_Sprint_Plan_with_Review.md
├── mockups/                 # UI/UX mockups
├── .cursor/                 # Cursor IDE commands
├── BRD_FoodDelivery.md     # Business Requirements Document
├── PRD_FoodDelivery.md     # Product Requirements Document
├── SRS_FoodDelivery.md     # Software Requirements Specification
├── SDD_FoodDelivery.md     # Software Design Document
├── ERD_FoodDelivery.md     # Entity Relationship Diagram
├── Figma_Design_Report_FoodDelivery.md
└── swagger.yaml            # API specification
```

## 🚀 Getting Started

### Prerequisites

- Go 1.25 or higher
- Docker and Docker Compose
- PostgreSQL 14+
- Redis 7+
- Kafka 3+
- Node.js 18+ (for frontend development)
- React Native development environment (for mobile)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd online_food_ordering_system
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start infrastructure services**
   ```bash
   docker-compose up -d postgres redis kafka
   ```

4. **Run database migrations**
   ```bash
   # TBD: Add migration commands
   ```

5. **Start microservices**
   ```bash
   # TBD: Add service startup commands
   ```

## 📚 Documentation

- [Business Requirements Document](BRD_FoodDelivery.md)
- [Product Requirements Document](PRD_FoodDelivery.md)
- [Software Requirements Specification](SRS_FoodDelivery.md)
- [Software Design Document](SDD_FoodDelivery.md)
- [Entity Relationship Diagram](ERD_FoodDelivery.md)
- [API Specification](swagger.yaml)
- [MVP Sprint Plan](docs/MVP_Sprint_Plan_with_Review.md)

## 🧪 Testing

```bash
# Run unit tests
go test ./...

# Run integration tests
# TBD: Add integration test commands

# Run frontend tests
cd frontend && npm test
```

## 🚢 Deployment

The platform is designed for deployment on AWS using:
- **Container Registry:** Docker Hub
- **Orchestration:** AWS EKS (Elastic Kubernetes Service)
- **CI/CD:** GitHub Actions

See [SDD_FoodDelivery.md](SDD_FoodDelivery.md) Section 6 for detailed deployment architecture.

## 🔒 Security

- JWT RS256 authentication
- Security headers implementation
- GDPR compliance measures
- Rate limiting and API gateway protection

See [SDD_FoodDelivery.md](SDD_FoodDelivery.md) Section 7 for detailed security design.

## 📊 Features

### MVP Features
- User registration and authentication
- Restaurant browsing and search
- Order placement and management
- Real-time order tracking
- Payment processing
- Rating and review system
- Restaurant dashboard
- Driver delivery management
- Admin dashboard

## 🤝 Contributing

1. Create a feature branch from `main`
2. Make your changes
3. Write/update tests
4. Ensure all tests pass
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

For questions or support, please refer to the project documentation or contact the development team.

---

**Version:** 3.0  
**Last Updated:** January 2026  
**Location:** Ho Chi Minh City, Vietnam
