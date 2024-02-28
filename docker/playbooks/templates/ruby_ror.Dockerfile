FROM ruby:3.2-slim-bullseye

# Install system dependencies required both at runtime and build time
RUN apt-get update && apt-get install -y \
    build-essential \
    # example system dependencies that need for "gem install pg"
    libpq-dev

COPY Gemfile Gemfile.lock ./

# Install (excluding development/test dependencies)
RUN gem install bundler && \
  bundle config set without "development test" && \
  bundle install

COPY . .

CMD ["rails", "server", "-b", "0.0.0.0"]
