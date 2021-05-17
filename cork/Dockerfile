FROM rust
RUN git clone https://github.com/RedDocMD/cork.git
RUN cd cork && cargo build --release
ENTRYPOINT ["cork/target/release/cork"]
