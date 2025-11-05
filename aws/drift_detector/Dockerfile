# -------- Stage 1: Download Terraform binary --------
FROM alpine:3.20 AS terraform
ARG TERRAFORM_VERSION=1.9.0

RUN apk add --no-cache curl unzip \
 && curl -Lo /tmp/terraform.zip https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
 && unzip /tmp/terraform.zip -d /usr/local/bin \
 && rm -f /tmp/terraform.zip

# -------- Stage 2: Minimal runtime --------
FROM alpine:3.20
RUN apk add --no-cache bash jq curl ca-certificates aws-cli \
 && update-ca-certificates \
 && mkdir -p /tmp/plugin-cache \
 && rm -rf /var/cache/apk/*

# Copy Terraform binary from previous stage
COPY --from=terraform /usr/local/bin/terraform /usr/local/bin/terraform

WORKDIR /app
COPY ./terraform /app/
COPY detect_drift.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/detect_drift.sh

# Environment variables
ENV TF_PLUGIN_CACHE_DIR=/tmp/plugin-cache
ENV CHECKPOINT_DISABLE=1
ENV PATH="/usr/local/bin:$PATH"

ENTRYPOINT ["/usr/local/bin/detect_drift.sh"]
