# 🚉 SEPTA Regional Rail Station Finder API

This project is a FastAPI-based microservice that provides the nearest SEPTA Regional Rail station in **GeoJSON** format based on a given geographic location.

## ✅ Features Implemented

- ✅ Accepts a latitude and longitude as input
- ✅ Finds the nearest SEPTA Regional Rail station using provided GeoJSON dataset
- ✅ Returns the result as valid GeoJSON
- ✅ HTTP API built with FastAPI
- ✅ Dockerized for container-based deployment
- ✅ Uses MongoDB Atlas as a hosted cloud database
- ✅ Designed for cost-effective operation and scalability

## 📂 Project Structure

```
.
├── app/
│   └── main.py                # FastAPI application code
│
├── data/
│   └── doc.geojson            # Source data for SEPTA Regional Rail stations
│
├── Dockerfile                 # Container setup for FastAPI
├── docker-compose.yml         # Service definition for local deployment
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

## ⚙️ Tech Stack

- Python 3
- FastAPI
- Uvicorn
- MongoDB Atlas
- Docker & Docker Compose


## 🗂️ Dataset

The train station data is loaded from a local GeoJSON file:  
[SEPTA Regional Rail Stations](https://drive.google.com/file/d/11ZfHYz3w77-aM4ZQnQIxSSdxcGnWcFjA/view?usp=drive_link)

## 🧾 Requirements

Python dependencies (in `requirements.txt`):

```
fastapi
uvicorn
pymongo[srv]
```

## 🧼 Clean Code & Best Practices

- Code is modular and separated by responsibility
- Uses environment variables for sensitive configuration
- Dockerized for easy deployment and reproducibility

## 🔒 Security Considerations

- Avoids redundant searches using MongoDB uniqueness constraints
- MongoDB credentials are kept out of the codebase
- The project is designed with production isolation in mind

## 💰 Cost Efficiency

- Lightweight FastAPI application
- Deployed with Docker for resource-efficient hosting
- Uses a single optimized endpoint to reduce overhead

## 🌍 Global Support

- Accepts any valid lat/lon input
- Returns GeoJSON, a standardized format supported globally