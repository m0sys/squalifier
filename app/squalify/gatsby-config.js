/**
 * Configure your Gatsby site with this file.
 *
 * See: https://www.gatsbyjs.org/docs/gatsby-config/
 */

const path = require(`path`);

module.exports = {
  /* Your site config here */
  plugins: [
    {
      resolve: `gatsby-source-filesystem`,
      options: {
        name: `images`,
        path: path.join(__dirname, `src`, `images`),
      },
    },
    {
      resolve: "gatsby-source-graphql",
      options: {
        // Arbitrary name for the remote schema Query type
        typeName: "SQUALIFY",
        // Field under which the remote schema will be accessible. You'll use this in your Gatsby query
        fieldName: "squalify",
        // Url to query from
        url: "https://squalify-vnr63p7z2a-nn.a.run.app/graphql",
      },
    },
    `gatsby-plugin-sass`,
    `gatsby-transformer-sharp`,
    `gatsby-plugin-sharp`,
  ],

  proxy: {
    prefix: "/api",
    url: "https://squalify-vnr63p7z2a-nn.a.run.app/graphql",
  },
};
