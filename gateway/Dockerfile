FROM elixir:slim as release

WORKDIR /
COPY . .

RUN apt update && apt upgrade
RUN apt install -y curl

# required for mix release deps
RUN mix local.hex --force
RUN mix local.rebar --force
# required for auth module
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
# release a production version
ENV MIX_ENV=prod
RUN mix deps.get
RUN mix deps.compile
RUN mix release stack

# recopy to open new build files
FROM elixir:slim

COPY --from=release /_build/prod/rel/stack .

CMD [ "/bin/stack", "start" ]
