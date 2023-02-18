FROM rust:latest

WORKDIR /

COPY . .

RUN cargo build --release

EXPOSE 4600

CMD [ "cargo", "run", "--release" ]
