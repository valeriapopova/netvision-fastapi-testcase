import uvicorn

from fastapi import FastAPI

from routers import router

# models.Base.metadata.create_all(bind=database.PGDB(**config.PG_CONF).engine)
app = FastAPI(title='Entry CRUD API',
              description='Service to create, retrieve and delete entries')

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app)
