![Derailedeon](./assets/derailedeon.png)

**Your smart communications platform.**


Hang out with your friends, have a business meeting, or form a new clan in the newest game. Limitless possibilities while being open, free, and secure.

The new easy-to-use open source platform for secure communications.
Welcome Derailed: the newest edition of open source communication software.

## Deploying with Docker

Derailed can be easily deployed publicly using Docker and Docker Compose.
For starters, Docker Compose will be easier, but for Docker it should be as
straightforward as modifying your environment variables, building, and running.

For Docker Compose it's much simpler and sets up the entire Derailed backend stack.
This currently includes our Gateway and API, but will also include January and February in the future.

For the frontend though, you'll have to build and deploy that yourself.

### Docker Compose

To deploy with Docker Compose, all you have to do is use our `docker-compose.yml` file provided in the root.
Firstly, install [Docker](https://docker.com).

Once you've done that, you simple run `docker compose up --build` in the root directory and it'll automagically
deploy Derailed's backend!
