# In case You're using Poetry, uncomment
#
# FROM python:3.9-slim-bullseye as builder
# RUN pip install poetry
#
# WORKDIR /app
# COPY poetry.lock pyproject.toml ./
# RUN poetry install
# COPY poetry.lock pyproject.toml ./
# RUN poetry install

FROM python:3.9-slim-bullseye as base

WORKDIR /app
# In case You're using Poetry, uncomment
#
# COPY --from=builder /app /app
# ENV PATH="/app/.venv/bin:$PATH"

# In case of Poetry, comment next two liness
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# EXPOSE 8000/tcp

# For Poetry
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
