![Derailedeon](./assets/derailedeon.png)

Welcome to the free text & voice platform for open and speedy distributed communication.

This is the publicly available source code of Derailed and is used for issue tracking, 
general project management, and more.

If you want to contribute, you can! Contributions are always open, and we try to make them as friendly as possible, 
even if our stack isn't the easiest to deploy.

## Deploying

Derailed at the current moment cannot fully be deployed using Docker. We provide a single dockerfile, and that is only
for fast and easy deployment of our **Gateway**. Our API, Auth Service (soon to be removed,) App, etc. All don't.

So you'll have to install on bare metal and conform to those special standards.

In the future, we plan to completely allow the deployment of the entire Derailed stack with Docker
to make deployment, testing, and other such categories easier to do.

### Auth

The authentication portion of our API (only.)

- Install [Rust](https://rust-lang.org)
- Run `cargo run --release` to directly run, or just `cargo build --release` to build

### API

The API by far is the simplist.

- Install [Python](https://python.org)
- Create a venv (optional)
- Install requirements (i.e. `pip install -r requirements.txt`)

Now this separates into two parts. For windows (or for general development):

- Run `python development.py`

For Unix-based systems:

- Run `gunicorn`

### Gateway

With our Gateway, you have two options instead of one. *Bare metal* or *docker*.

With bare metal, you have to setup your own machine and install dependencies manually,
which could add room for customizations and speedups.

But with Docker, you can deploy a fully setup Gateway (excluding DB of course) in little time.

#### Metal

- [Install Elixir](https://elixir-lang.org)
- [Install Rust](https://rust-lang.org)
- Install Dependencies (`mix deps.get` & `mix deps.compile`)
- Run! (`mix run --no-halt`)

#### Docker

Just simply build the image, and run it. For more information, just check the [Docker Docs](https://docs.docker.com).

