export $(grep -v '^#' .env | xargs)

terraform validate

terraform apply \
    -var="tenant_id="$ARM_TENANT_ID \
    -var="object_id="$OBJECT_ID
