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



# 🧠 Approach & Design Write-Up

## ✅ **Approach**

The goal was to build a lightweight, scalable HTTP API that returns the nearest SEPTA Regional Rail station in GeoJSON format, using a provided dataset.

1. **FastAPI** was chosen as the web framework due to its speed, ease of development, and built-in OpenAPI support.
2. The dataset (`doc.geojson`) was preloaded and parsed at application startup to enable fast access without querying a large database each time.
3. A **nearest-neighbor search** is performed by calculating geospatial distances between the input coordinates and each station.
4. MongoDB Atlas was used for cloud database storage, with potential caching or logging use in mind.
5. The application was containerized with **Docker** to support consistent deployments and future scalability.

---

## ⚠️ **Challenges Faced**

- **GeoJSON Parsing:** Ensuring proper handling of GeoJSON format and consistent return of valid GeoJSON required testing and validation.
- **Distance Calculations:** Handling accurate distance comparisons (using Haversine formula or geopy) without relying on heavyweight GIS libraries.
- **Cost Management:** Striving for low resource usage while still allowing future scalability.
- **Docker Setup:** Structuring the project for clean Docker image builds without hardcoding environment-specific settings.

---

## 🧱 **Design Decisions**

- **Cloud MongoDB Atlas** was selected for flexibility, free tier availability, and the ability to scale later if needed.
- **Local GeoJSON File Loading** was preferred over storing all records in MongoDB to reduce read costs and minimize API latency.
- **Docker & Compose** were used to isolate the service, simplifying future deployment to cloud infrastructure or orchestration platforms like Kubernetes.
- **No External APIs** were used for directions to ensure offline support and zero reliance on costly third-party services.
