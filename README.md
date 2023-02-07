# Derailed

# RUST PROTOTYPE

This is the Rust Prototype Repo. This should not be used anywhere except for testing.
This is being used to play around with Rust, and see which tools are best to use for Derailed's use case.


> Derail yourself from Discord and Guilded.

Platform for Gamers. The Derailed monorepo
powered by many tools.

More or less, this is more of a Derailed mono monorepo
because it holds three strict holdings:

- API - The Derailed API, Auth, and it's many other holdings.
- Gateway - The Derailed Gateway incapsulated by an Umbrella project
- Front - Derailed's frontend, using turborepo for better web-based goodies

These three put in place our most important stones:

- The API, our most sacred piece.
- The Gateway, our real-time infrastructure.
- And the frontend, our app, our website, etc.

For anything not in the topic of these, or
necessarily in the topic of a multitude of these,
they will be put in their own directory on the root named according to their function.

## Why Monorepo?

TL;DR: To unify feature development, and other such

This monorepo helps Derailed serve users more cleanly.
When developing a new feature, a dev just has to hop onto one repo and can build everything they need there.
And when it launches all of our services can be deployed simultaneously.

This helps for things like database migrations and the such, where we wouldn't want to break a new or old builds functionality.

As for using a multitude of different strategies, it's mostly because
it's more worthy using multiple.
Our API does not need a monorepo in itself, so we don't have one for that.
The Gateway can be put into an Elixir Umbrella project which does the job for us.
And for the frontend, we can use the modern Turborepo built by Vercel to provide fast builds throughout our entire frontend easily and fast.

The biggest reason overall though is to centralize development.
