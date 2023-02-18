FROM elixir:latest as release

WORKDIR /
COPY . .

# required for mix release deps
RUN mix local.hex --force
RUN mix local.rebar --force
# release a production version
ENV MIX_ENV=prod
RUN mix deps.get
RUN mix deps.compile
RUN mix release stack

# recopy to open new build files
FROM elixir:latest

COPY --from=release /_build/prod/rel/stack .

CMD [ "/bin/stack", "start" ]