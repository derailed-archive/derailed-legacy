FROM rust:latest

WORKDIR /

COPY . .

RUN cargo build --release

EXPOSE 9090

CMD [ "cargo", "run", "--release" ]