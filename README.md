# Event Announcement Service

A web application that allows users to subscribe to an event notification service and create events. The service notifies subscribed users when new events are created.  

---

## Features

- **User Subscription:** Users can subscribe to the service to receive notifications for new events.  
- **Event Creation:** Users can create events which are stored in DynamoDB.  
- **Event Display:** Users can view all previously created events.  
- **Notifications:** Users receive notifications via AWS SNS when new events are created.  
- **Automatic Event Expiry:** Events automatically expire after 2 days using DynamoDB TTL.  
- **CI/CD:** Automated deployment using **AWS CodePipeline**.  
- **Content Delivery:** Frontend delivered via **AWS CloudFront** for fast, global access.  

---

## Tech Stack

- **Frontend:** Hosted on **AWS S3** and delivered through **CloudFront** ([d3lnqu8pzyn695.cloudfront.net](https://d3lnqu8pzyn695.cloudfront.net))  
- **Backend / API:** **AWS REST API** with 3 endpoints:
  1. **Subscribe** – Add a new subscriber  
  2. **Create Event** – Add a new event to DynamoDB  
  3. **Get Events** – Fetch events from DynamoDB  
- **Database:** **AWS DynamoDB** (with TTL of 2 days for events)  
- **Notifications:** **AWS SNS** to notify subscribed users  
- **CI/CD:** **AWS CodePipeline** to automate deployments  

---

## Architecture Overview

1. User visits the frontend delivered via **CloudFront**.  
2. User subscribes to the service or creates an event using the REST API endpoints.  
3. Created events are stored in DynamoDB with a TTL of 2 days.  
4. Subscribed users are notified via SNS when a new event is created.  
5. Expired events are automatically deleted by DynamoDB after TTL.  
6. CodePipeline automates deployment of frontend and backend changes.  

---

## API Endpoints

| Endpoint          | Method | Description                           |
|------------------|--------|---------------------------------------|
| `/subscribe`      | POST   | Add a new subscriber                  |
| `/create-event`   | POST   | Create a new event                    |
| `/get-events`     | GET    | Retrieve all active events            |

---

## Setup Instructions

### Prerequisites
- AWS Account  
- AWS CLI configured  
- Node.js and npm (if frontend requires build)  

### Steps

1. **Frontend Deployment:**
   - Upload your frontend build to the S3 bucket.  
   - Enable static website hosting.  
   - Use CloudFront to deliver the frontend content globally.  
   - Integrate with CodePipeline for automatic deployment on code changes.  

2. **Backend Setup:**
   - Create a REST API using AWS API Gateway.  
   - Configure Lambda functions (or other backend services) for endpoints.  
   - Connect endpoints to DynamoDB tables.  
   - Add backend to CodePipeline for CI/CD automation.  

3. **Database Setup:**
   - Create a DynamoDB table to store events.  
   - Add a TTL attribute to automatically delete events after 2 days.  

4. **Notifications:**
   - Create an SNS topic for subscribers.  
   - Ensure subscribers are added to this topic.  
   - Send notifications when new events are created.  

---

## Notes

- Make sure your API Gateway has CORS enabled to allow requests from the frontend.  
- TTL in DynamoDB is in **epoch time (seconds)**, so ensure your events store the correct expiration timestamp.  
- SNS subscriptions can be email, SMS, or other supported protocols.  
- CodePipeline can automatically deploy frontend and backend changes whenever updates are pushed to your repository.  
- Access your application via **CloudFront URL:** [https://d3lnqu8pzyn695.cloudfront.net](https://d3lnqu8pzyn695.cloudfront.net)  

---

## License

This project is licensed under the MIT License.  

---

## Author

**Sachin Bhatt**  
- GitHub: [your-github-username](https://github.com/your-github-username)  
- Website: [madebysachin.com](https://madebysachin.com)