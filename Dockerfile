# Base image using Python 3.11
FROM python:3.11

# Build arguments for image metadata
ARG NAME
ARG BRANCH
ARG HASH
ARG DOCKERTAG
ARG CREATED

# Set image metadata labels following OCI standards
LABEL org.opencontainers.image.vendor   "AgentScape"
LABEL org.opencontainers.image.title    ${NAME}
LABEL org.opencontainers.image.version  ${DOCKERTAG}
LABEL org.opencontainers.image.created  ${CREATED}
LABEL org.opencontainers.image.revision ${HASH}
LABEL org.opencontainers.image.ref.name ${BRANCH}

# Set environment variables for application versioning and tracking
ENV NAME=${NAME}
ENV BRANCH=${BRANCH}
ENV HASH=${HASH}
ENV DOCKERTAG=${DOCKERTAG}
ENV CREATED=${CREATED}

# Configure timezone settings
ENV TZ=Etc/UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Set up application directory and dependencies
WORKDIR /opt/app
COPY . .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]