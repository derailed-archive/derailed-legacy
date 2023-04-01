FROM rust:latest

WORKDIR /

COPY . .

RUN cargo build --release

EXPOSE 8080

CMD [ "cargo", "run", "--release" ]