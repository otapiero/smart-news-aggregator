# Personalized News Update Aggregator

A production-ready microservice application that delivers personalized news updates based on user preferences.
Built with Python and powered by AI, it currently serves personalized news content to users through email notifications.



The purpose of this project is to demonstrate the use of microservices and specifically the IDesign Method in building a scalable and robust application.
The application is built using a microservices architecture, with each service responsible for a specific task. and the communication between services is done using Dapr.






## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
- [Project Architecture](#project-architecture)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Contact](#contact)
- [TODO](#todo)
- [Authors](#authors)

## Overview

The Personalized News Update Aggregator is a microservice application that provides personalized news updates to users based on their preferences.
## Core Features

Our system currently provides:

- Personalized news updates based on user preferences to the user's email
- AI-powered article summarization
- Multi-channel delivery through email and Telegram notifications #TODO add telegram support
- Robust caching system for optimal performance

## Tech Stack

The application is built using:

- Python 3.11 for microservices
- Flask, gRPC, and Dapr SDK for service communication
- PostgresSQL for user data and preferences
- Redis for caching
- Docker and Docker Compose for containerization
- Dapr for microservices communication
- newsapi.ai for news content
- Gemini AI for article summarization
- SendGrid for email delivery
- RabbitMQ for message queuing

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.11
- Node.js



### Installation and Setup

**1. **Clone the repository:****
```bash
git clone https://github.com/otapiero/news-aggregator.git
cd news-aggregator
```

**2. **Set up environment variables:****

a. Create a `.env` file in EmailApiAccessor folder with the following content:
```env
SENDGRID_API_KEY=your_sendgrid_key
SENDER_EMAIL=your_email
```
to get the key, sign up at https://sendgrid.com/

b. Create a `.env` file in LLMSummarizationAPIAccessor folder with the following content:
```env
GENERATIVE_API_KEY=your_generative_key
```
to get the key, sign up at https://ai.google.dev/gemini-api/docs/api-key

c. Create a `.env` file in NewsApiAccessor folder with the following content:
```env
NEWS_API_AI_API_KEY=your_newsdata_io_key
```
to get the key, sign up at https://newsapi.ai/


**3. Start the services:**
```bash
cd BFF
cd frontend
npm install react-router axios 
npm run build
```
In a new terminal:
```bash
docker-compose up -d
```

4. Access the application:
- Web Interface: http://127.0.0.1:5003/


## Project Architecture

The application is built using a microservices architecture following the IDesign Method.

![System Architecture](assets/personalized_news_update_aggregator_architecture.png)

 
It consists of the following components:
- **BFF (Backend for Frontend):** The entry point for the frontend application, responsible for serving the web interface and handling user requests to the backend services.
- **Managers:** User Manager, News Manager.
- **Engines:** News Engine.
- **Accessors:** Email API Accessor, News API Accessor, LLM Summarization API Accessor, User Database Accessor, News Database Accessor.
- **Databases:** User Database (PostgreSQL), News Database (REDIS).
- **APIs:** Gemini API, News API, SendGrid API.
- **Frontend:** React.js web interface for user interaction.

The communication between services is done using Dapr, image below shows the communication between services.
![System Architecture with Dapr](assets/personalized_news_update_aggregator_architecture_(dapr_sidecars).png)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request to the `develop` branch

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [IDesign Method](https://www.idesign.net/)
- [Dapr](https://dapr.io/)
- [NewsAPI.ai](https://newsapi.ai/)
- [Gemini AI](https://ai.google.dev/gemini-api/)
- [SendGrid](https://sendgrid.com/)


## Contact

For support or queries, reach out to: [ smartnewsaggregator@gmail.com](mailto:smartnewsaggregator@gmail.com)

## TODO
- [ ] Add tests
- [ ] Add Telegram notifications support
- [ ] Add user authentication

## Authors

- [otapiero github](https://github.com/otapiero)