FROM rust:1.82-bookworm as builder
WORKDIR /usr/src/app
RUN curl -Lo saturn.tar.gz https://github.com/luka0x12/saturn/archive/refs/heads/main.tar.gz && \
    tar -xvf saturn.tar.gz
WORKDIR /usr/src/app/saturn-main
RUN --mount=type=cache,target=/usr/local/cargo/registry --mount=type=cache,target=/usr/src/app/saturn-main/target cargo build --release && \
    cp target/release/saturn /usr/local/bin/app
FROM debian:bookworm-slim as runtime
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN useradd appuser
USER appuser
COPY --from=builder /usr/local/bin/app /usr/local/bin/app
ENV RUST_LOG=info
ENV SATURN_COLOR=truecolor
ENTRYPOINT ["/usr/local/bin/app"]
