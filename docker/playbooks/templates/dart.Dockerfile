FROM dart AS build

WORKDIR /build

COPY pubspec.* /build
RUN dart pub get --no-precompile

COPY . .
RUN dart compile exe app.dart -o run

FROM debian:bullseye-slim

WORKDIR /build

COPY --from=build /build/run /app/run
CMD ["/app/run"]
