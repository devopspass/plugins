FROM mcr.microsoft.com/dotnet/sdk:8.0-alpine AS build

WORKDIR /build

# copy csproj and restore as distinct layers
COPY *.csproj .
RUN dotnet restore

# copy and publish app and libraries
COPY . .
RUN dotnet publish --no-restore -o app

FROM mcr.microsoft.com/dotnet/aspnet:8.0-alpine

WORKDIR /app

COPY --from=build /build/app .

ENTRYPOINT ["./aspnetapp"]
