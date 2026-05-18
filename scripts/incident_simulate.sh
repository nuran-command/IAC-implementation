#!/usr/bin/env bash
# ============================================================
# SRE Incident Simulation & Recovery Script
# Simulates a failure in the Order Service by injecting an
# incorrect DB host, and restores it back to health.
# Usage: bash scripts/incident_simulate.sh [inject|recover] [compose|swarm|k8s]
# ============================================================
set -euo pipefail

# ANSI color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

ACTION="${1:-inject}"
PLATFORM="${2:-}"

log()  { echo -e "${BLUE}[INCIDENT]${NC} $1"; }
ok()   { echo -e "${GREEN}[  OK  ]${NC} $1"; }
warn() { echo -e "${YELLOW}[ WARN ]${NC} $1"; }
fail() { echo -e "${RED}[ FAIL ]${NC} $1"; exit 1; }

# Auto-detect platform if not specified
detect_platform() {
  if [ -n "$PLATFORM" ]; then
    ok "Using specified platform override: $PLATFORM"
    return
  fi

  log "Auto-detecting active platform..."
  
  # Prioritize Docker Compose (Local Dev) first
  if docker compose ps 2>/dev/null | grep -q "order-service"; then
    PLATFORM="compose"
    ok "Active platform: Docker Compose (Local Dev)"
  elif docker service ls 2>/dev/null | grep -q "sre_app_order-service"; then
    PLATFORM="swarm"
    ok "Active platform: Docker Swarm"
  elif kubectl get ns sre-app &>/dev/null; then
    PLATFORM="k8s"
    ok "Active platform: Kubernetes (K8s)"
  else
    PLATFORM="compose"
    warn "No active orchestration containers found. Defaulting to Docker Compose."
  fi
}

inject_compose() {
  log "Injecting Order Service failure in Docker Compose..."
  if [ -f .env ]; then
    log "Modifying .env file..."
    sed -i.bak 's/DB_HOST=.*/DB_HOST=db_wrong/g' .env || sed -i '' 's/DB_HOST=.*/DB_HOST=db_wrong/g' .env
    log "Recreating Order Service containers with broken configuration..."
    docker compose up -d order-service order-service-2
    ok "Incident injected! Order Service is now unhealthy."
  else
    fail "No .env file found. Please run local setup first."
  fi
}

recover_compose() {
  log "Recovering Order Service in Docker Compose..."
  if [ -f .env ]; then
    log "Restoring .env file..."
    sed -i.bak 's/DB_HOST=.*/DB_HOST=db/g' .env || sed -i '' 's/DB_HOST=.*/DB_HOST=db/g' .env
    log "Recreating Order Service containers with primary configuration..."
    docker compose up -d order-service order-service-2
    ok "Recovery process completed! Order Service is back to healthy."
  else
    fail "No .env file found. Re-run local setup."
  fi
}

inject_swarm() {
  log "Injecting Order Service failure in Docker Swarm..."
  log "Updating service env variables..."
  docker service update --env-add DB_HOST=db_wrong sre_app_order-service
  ok "Incident injected! Swarm service 'sre_app_order-service' is rolling out a crash state."
}

recover_swarm() {
  log "Recovering Order Service in Docker Swarm..."
  log "Removing overriding environment variable..."
  docker service update --env-rm DB_HOST sre_app_order-service
  ok "Recovery completed! Docker Swarm is rolling out the primary, healthy state."
}

inject_k8s() {
  log "Injecting Order Service failure in Kubernetes..."
  log "Updating deployment env var 'DB_HOST=db_wrong' in namespace 'sre-app'..."
  kubectl set env deployment/order-service DB_HOST=db_wrong -n sre-app
  ok "Incident injected! Kubernetes is deploying unhealthy order-service pods."
}

recover_k8s() {
  log "Recovering Order Service in Kubernetes..."
  log "Updating deployment env var 'DB_HOST=db' in namespace 'sre-app'..."
  kubectl set env deployment/order-service DB_HOST=db -n sre-app
  ok "Recovery completed! Kubernetes is deploying healthy order-service pods."
}

# ── Main Execution ─────────────────────────────────────────
detect_platform

case "$ACTION" in
  inject)
    log "Injecting simulated failure state..."
    case "$PLATFORM" in
      compose) inject_compose ;;
      swarm)   inject_swarm ;;
      k8s)     inject_k8s ;;
    esac
    ;;
  recover)
    log "Restoring services to healthy state..."
    case "$PLATFORM" in
      compose) recover_compose ;;
      swarm)   recover_swarm ;;
      k8s)     recover_k8s ;;
    esac
    ;;
  *)
    fail "Unknown action '$ACTION'. Use 'inject' or 'recover'"
    ;;
esac
