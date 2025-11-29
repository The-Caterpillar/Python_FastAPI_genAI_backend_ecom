FROM python:3.12
RUN apt-get update && apt-get install -y pandoc
RUN apt-get update && apt-get upgrade -y
RUN apt-get install python3 -y \
    curl \
    git \
    libzbar0 \
    mupdf \
    libzbar-dev \
    python3-pip \
    python3-venv -y \
    && apt-get clean
WORKDIR /app
COPY . ./

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PATH="/venv/bin:$PATH"

ARG AZURE_CLIENT_ID
ARG AZURE_CLIENT_SECRET
ARG AZURE_AI_ENDPOINT
ARG AZURE_TENANT_ID
ARG AZURE_DEPLOYMENT_MODEL
ARG AZURE_API_VERSION
ARG RDS_URI


ENV AZURE_CLIENT_ID=$AZURE_CLIENT_ID
ENV AZURE_CLIENT_SECRET=$AZURE_CLIENT_SECRET
ENV AZURE_AI_ENDPOINT=$AZURE_AI_ENDPOINT
ENV AZURE_TENANT_ID=$AZURE_TENANT_ID
ENV AZURE_DEPLOYMENT_MODEL=$AZURE_DEPLOYMENT_MODEL
ENV AZURE_API_VERSION=$AZURE_API_VERSION
ENV RDS_URI=$RDS_URI

COPY requirements.txt .
RUN pip install -r requirements.txt

# Load environment variables from env_var file
COPY env_var .env
RUN cat .env >> /etc/environment

EXPOSE 5051
ENTRYPOINT [ "/bin/bash" ]
CMD ["run.sh"]