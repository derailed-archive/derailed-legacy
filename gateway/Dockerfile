FROM elixir:alpine as release

WORKDIR /
COPY . .

apk add curl

# required for mix release deps
RUN mix local.hex --force
RUN mix local.rebar --force
# required for auth module
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
# release a production version
ENV MIX_ENV=prod
RUN mix deps.get
RUN mix deps.compile
RUN mix release stack

# recopy to open new build files
FROM elixir:alpine

COPY --from=release /_build/prod/rel/stack .

CMD [ "/bin/stack", "start" ]
