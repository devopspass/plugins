FROM ruby:3.2-slim-bullseye

# Install system dependencies required both at runtime and build time
RUN apt-get update && apt-get install -y \
    build-essential \
    # example system dependencies that need for "gem install pg"
    libpq-dev \
    nodejs \
    yarn

COPY Gemfile Gemfile.lock ./

# Install (excluding development/test dependencies)
RUN gem install bundler && \
  bundle config set without "development test" && \
  bundle install

COPY package.json yarn.lock ./
RUN yarn install

COPY . .

# Install assets
RUN RAILS_ENV=production SECRET_KEY_BASE=assets bundle exec rails assets:precompile

CMD ["rails", "server", "-b", "0.0.0.0"]

# Note - On MacOS M Chip, maybe you need to add a flag --platform=linux/amd64 when build:
#
#   docker build . -t rubyonrails-app --platform=linux/amd64
