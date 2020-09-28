"""Define GraphQL server."""
import os
from fastapi import FastAPI
from ariadne import load_schema_from_path, make_executable_schema, snake_case_fallback_resolvers, upload_scalar

from ariadne.asgi import GraphQL
import uvicorn

from api.resolvers.query import query
from api.resolvers.mutation import mutation


app = FastAPI()

schema = load_schema_from_path("api/graphql")
schema = make_executable_schema(schema, [query, mutation] + [snake_case_fallback_resolvers, upload_scalar])


@app.get("/")
async def root():
    return {"msg": "Hello World!"}


app.add_route("/graphql", GraphQL(schema=schema, debug=True))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT")))
