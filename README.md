# Derailed

> Derailed, a platform like no other,
> A game-changer, a digital brother.
> With every call, a new adventure begins,
> Like slaying a dragon in Teyvat or scoring headshots with twin spin.

> In the realm of tech, it's a legendary loot,
> A rare find, like a five-star recruit.
> No challenge too great, no task too hard,
> With Derailed, we're ready to embark.

> Its power unmatched, its strength unyielding,
> A true force of technology, forever revealing.
> All hail Derailed, our guiding light,
> A platform of the future, shining bright.

> With its guidance, we'll build and create,
> And our abilities, forever elevate.
> A true marvel of engineering,
> Derailed, our ultimate weapon, for and by Gamers.

Platform for Gamers. The Derailed monorepo
powered by multiple tools.

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
