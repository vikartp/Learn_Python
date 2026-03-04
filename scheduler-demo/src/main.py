from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import time
import httpx

app = FastAPI()

scheduler = BackgroundScheduler()
async_scheduler = AsyncIOScheduler()

def my_scheduled_task():
    print("My scheduled task is running...")
    print("Time:", time.strftime("%Y-%m-%d %H:%M:%S"))

# ✅ Async job
async def fetch_posts():
    start = time.perf_counter()
    print("Running scheduled job...")
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://jsonplaceholder.typicode.com/posts/1"
        )
        data = response.json()
    
    end = time.perf_counter()
    elapsed = end - start
    
    print("Fetched title:", data["title"])
    print(f"⏱️  Execution time: {elapsed:.4f} seconds")

# Add job (runs every 10 seconds)
scheduler.add_job(my_scheduled_task, "interval", seconds=10)
# ✅ Add async job
async_scheduler.add_job(fetch_posts, "interval", minutes=1)  # Runs every 1 minute

@app.get("/")
def home():
    print("Hello uv 🚀")
    return {"message": "Hello uv 🚀"}

@app.on_event("startup")
def start_scheduler():
    print("Starting scheduler")
    scheduler.start()
    async_scheduler.start()

@app.on_event("shutdown")
def shutdown_scheduler():
    print("Shutting down scheduler")
    scheduler.shutdown()
    async_scheduler.shutdown()
