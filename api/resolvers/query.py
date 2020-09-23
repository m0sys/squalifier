"""Root GraphQL query for all types."""
from ariadne import QueryType

query = QueryType()


@query.field("info")
async def resolve_info(*_):
    return "This is the Squalify API used to make predictions"
