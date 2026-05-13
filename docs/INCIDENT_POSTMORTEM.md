# Incident Postmortem: Order Service Failure

## Incident Summary
**Date:** 2026-05-06
**Status:** Resolved
**Impact:** Order creation was unavailable for approximately 15 minutes. Partial service degradation.

## Root Cause Analysis
**Scenario:** Order Service failed due to incorrect database configuration.
**Details:** The `DB_HOST` environment variable for the `order-service` was pointing to a non-existent database replica instead of the primary PostgreSQL database container. This caused the application to crash on startup, repeatedly failing the Docker Swarm health checks.

## Detection and Response
1. **Detection:** Prometheus generated an alert (`InstanceDown`) which was visualized on the Grafana dashboard. The `order_service_status` metric dropped to 0.
2. **Log Analysis:** Investigated logs using `docker service logs sre_app_order-service`. The logs indicated `psycopg2.OperationalError: could not translate host name "db-replica" to address`.
3. **Configuration Fix:** Updated the `docker-compose.yml` and Kubernetes ConfigMap to correct `DB_HOST` back to `db`.
4. **Service Restart:** Executed `docker stack deploy -c docker-compose.yml sre_app` to apply the fix and restart the service.

## Resolution and Outcome
- **System Restored:** The order service successfully connected to the database.
- **Metrics Normalized:** Prometheus showed the `order_service_status` metric returned to 1, and the error rate dropped back to 0%.

## Action Items
1. Implement stricter validation for environment variables during CI/CD pipelines.
2. Introduce a configuration management tool (Ansible) to handle sensitive environment variable deployments consistently.
3. Set up a staging environment that perfectly mirrors production database topologies.
