export $(grep -v '^#' .env | xargs)

terraform validate

terraform apply \
    -var="tenant_id="$ARM_TENANT_ID \
    -var="object_id="$OBJECT_ID \
    -var="enable_cosmos_db_free_tier="$ENABLE_COSMOS_DB_FREE_TIER
