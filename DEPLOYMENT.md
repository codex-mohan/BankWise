# BankWise AI Banking Support API - Deployment Guide

## Overview

This guide provides step-by-step instructions for deploying the BankWise AI Banking Support API on Render.com with Neon DB integration.

## Prerequisites

- **Render.com Account**: Create a free account at [render.com](https://render.com)
- **Neon DB Account**: Create a free account at [neon.tech](https://neon.tech)
- **Git Repository**: Push your code to a Git repository (GitHub, GitLab, etc.)

## Step 1: Set up Neon Database

### 1.1 Create Neon Project

1. Log in to your Neon account
2. Click "New Project"
3. Choose a project name (e.g., `bankwise-ai-banking-db`)
4. Select a region close to your target users
5. Click "Create Project"

### 1.2 Get Database Connection String

1. Once the project is created, navigate to the "Dashboard"
2. Find your project and click on it
3. Go to the "Connection Details" tab
4. Copy the **Connection String** (starts with `postgresql://`)

### 1.3 Create Environment File

1. Create a `.env` file in your project root
2. Add your Neon connection string:

```bash
DATABASE_URL=postgresql://username:password@hostname:5432/database_name
```

3. Add other environment variables:

```bash
ENVIRONMENT=production
PYTHON_VERSION=3.11
PORT=10000
LOG_LEVEL=INFO
```

## Step 2: Configure Render.com

### 2.1 Create Render Service

1. Log in to your Render account
2. Click "New +" → "Web Service"
3. Select your Git repository
4. Configure the service:
   - **Name**: `bankwise-ai-banking-api`
   - **Runtime**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`
   - **Region**: Choose the same region as your Neon DB

### 2.2 Add Environment Variables

1. In the service configuration, go to "Environment"
2. Add the following environment variables:
   ```
   PYTHON_VERSION: "3.11"
   PORT: "10000"
   ENVIRONMENT: "production"
   LOG_LEVEL: "INFO"
   DATABASE_URL: [Your Neon connection string]
   ```

### 2.3 Configure Health Check

1. Go to "Health Check" section
2. Set:
   - **Health Check Path**: `/health`
   - **Health Check Interval**: 30s
   - **Health Check Timeout**: 5s
   - **Health Check Retries**: 3

### 2.4 Configure Resources

1. Go to "Resources" section
2. Set appropriate resources for free tier:
   - **Instance Count**: 1
   - **CPU**: 1
   - **Memory**: 512MB
   - **Disk**: 1GB

## Step 3: Deploy and Test

### 3.1 Deploy the Application

1. Click "Save and Deploy"
2. Wait for the deployment to complete (this may take 5-10 minutes)
3. Once deployed, you'll get a URL like `https://bankwise-ai-banking-api.onrender.com`

### 3.2 Test the API

1. Access the API documentation at: `https://bankwise-ai-banking-api.onrender.com/docs`
2. Test the health endpoint: `https://bankwise-ai-banking-api.onrender.com/health`
3. Test a sample API endpoint like balance check

### 3.3 Verify Database Integration

1. Check the logs to see if database initialization was successful
2. Look for messages like "Database initialized successfully" or "Database initialization failed, using mock data only"
3. If database initialization failed, the API will automatically use mock data as fallback

## Step 4: Database Management

### 4.1 Database Schema

The application automatically creates the following tables:

- `accounts` - Customer account information
- `cards` - Credit/debit card details
- `transactions` - Transaction history
- `branches` - Bank branch locations
- `atms` - ATM locations
- `complaints` - Customer complaints
- `disputes` - Transaction disputes
- `loans` - Loan information
- `fd_rates` - Fixed deposit rates

### 4.2 Data Population

- On first run, the application populates tables with mock data
- Data is generated using Faker library for realistic test data
- Subsequent runs use existing data from the database

### 4.3 Database Maintenance

- For production use, consider setting up regular backups
- Monitor database performance and storage usage
- Update connection string if you need to migrate to a different database

## Step 5: Monitoring and Logging

### 5.1 Application Logs

- Logs are written to `banking_api.log` file
- Logs include timestamps, request details, and error information
- In production, consider using a centralized logging service

### 5.2 Health Monitoring

- Use the `/health` endpoint for basic health checks
- Monitor the database connection status in the health response
- Set up alerts for deployment failures or health check failures

### 5.3 Performance Monitoring

- Monitor response times for API endpoints
- Track database query performance
- Monitor memory and CPU usage in Render dashboard

## Step 6: Scaling and Optimization

### 6.1 Horizontal Scaling

- Increase instance count in Render dashboard for higher traffic
- Use load balancing for multiple instances
- Consider using Redis for session management if scaling beyond free tier

### 6.2 Database Scaling

- Neon DB automatically scales storage
- For higher performance, consider upgrading Neon plan
- Implement connection pooling for better database performance

### 6.3 Cost Optimization

- Monitor Render.com usage to stay within free tier limits
- Use auto-scaling to handle traffic spikes
- Consider using spot instances for cost savings

## Troubleshooting

### Common Issues

#### Database Connection Failed

1. Verify the DATABASE_URL is correct
2. Check that Neon DB is accessible from Render
3. Ensure proper network configuration
4. The application will fall back to mock data if database is unavailable

#### Deployment Failed

1. Check Git repository access
2. Verify requirements.txt includes all dependencies
3. Check for syntax errors in main.py
4. Review Render deployment logs for specific error messages

#### API Performance Issues

1. Check database query performance
2. Monitor memory usage
3. Consider adding caching for frequently accessed data
4. Optimize API response times

### Debug Commands

```bash
# Local testing
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Check database connection
python -c "from database import db_manager; print(db_manager.initialize())"

# Test specific endpoints
curl -X POST "http://localhost:8000/api/account/balance" -H "Content-Type: application/json" -d '{"account_number": "123456789012"}'
```

## Support

For issues and questions:

- **Email**: codexmohan@gmail.com
- **Project Repository**: [GitHub Repository Link]
- **Render Support**: [Render.com Support](https://render.com/support)
- **Neon Support**: [Neon.tech Support](https://neon.tech/support)

---

**Note**: This deployment guide is for the AetherOps Banking Support API project by Mohana Krishna (University ID: 23BAI10630).
