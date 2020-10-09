import fetch from "cross-fetch";
import { ApolloClient, InMemoryCache, HttpLink } from "@apollo/client";
import { createUploadLink } from "apollo-upload-client";

export const client = new ApolloClient({
  link: createUploadLink({
    uri: "https://squalify-vnr63p7z2a-nn.a.run.app/graphql",
    fetch,
  }),
  cache: new InMemoryCache(),
});
