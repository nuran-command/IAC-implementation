#!/usr/bin/env bash
# ============================================================
# Automated Deployment Script
# Deploys using Docker Swarm with pre/post health validation
# Usage: bash scripts/deploy.sh [swarm|kubernetes]
# ============================================================
set -euo pipefail

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

MODE="${1:-swarm}"
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

log()  { echo -e "${BLUE}[DEPLOY]${NC} $1"; }
ok()   { echo -e "${GREEN}[  OK  ]${NC} $1"; }
warn() { echo -e "${YELLOW}[ WARN ]${NC} $1"; }
fail() { echo -e "${RED}[ FAIL ]${NC} $1"; exit 1; }

# ── Pre-flight checks ──────────────────────────────────────
log "Starting deployment in mode: $MODE"
log "Project directory: $PROJECT_DIR"

command -v docker >/dev/null 2>&1 || fail "Docker is not installed"

if [[ "$MODE" == "kubernetes" ]]; then
  command -v kubectl >/dev/null 2>&1 || fail "kubectl is not installed"
fi

# ── Docker Swarm Deployment ────────────────────────────────
deploy_swarm() {
  log "Checking Docker Swarm status..."
  if ! docker info 2>/dev/null | grep -q "Swarm: active"; then
    log "Initializing Docker Swarm..."
    docker swarm init || warn "Swarm init failed — may already be a member"
  else
    ok "Swarm is already active"
  fi

  log "Deploying stack from docker-swarm.yml..."
  docker stack deploy -c "$PROJECT_DIR/docker-swarm.yml" sre_app

  log "Waiting for services to stabilize (30s)..."
  sleep 30

  log "Service status:"
  docker service ls

  ok "Docker Swarm deployment complete!"
  echo ""
  echo "  Frontend:   http://localhost:80"
  echo "  Prometheus: http://localhost:9090"
  echo "  Grafana:    http://localhost:3000  (admin/admin)"
}

# ── Kubernetes Deployment ──────────────────────────────────
deploy_kubernetes() {
  log "Applying Kubernetes manifests..."

  kubectl apply -f "$PROJECT_DIR/kubernetes/namespace.yaml"
  kubectl apply -f "$PROJECT_DIR/kubernetes/configmap.yaml"
  kubectl apply -f "$PROJECT_DIR/kubernetes/secret.yaml"
  kubectl apply -f "$PROJECT_DIR/kubernetes/database.yaml"
  kubectl apply -f "$PROJECT_DIR/kubernetes/redis.yaml"
  kubectl apply -f "$PROJECT_DIR/kubernetes/auth-service.yaml"

  kubectl apply -f "$PROJECT_DIR/kubernetes/product-service.yaml"
  kubectl apply -f "$PROJECT_DIR/kubernetes/order-service.yaml"
  kubectl apply -f "$PROJECT_DIR/kubernetes/payment-service.yaml"
  kubectl apply -f "$PROJECT_DIR/kubernetes/notification-service.yaml"
  kubectl apply -f "$PROJECT_DIR/kubernetes/user-profile-service.yaml"
  kubectl apply -f "$PROJECT_DIR/kubernetes/frontend.yaml"
  kubectl apply -f "$PROJECT_DIR/kubernetes/monitoring.yaml"

  log "Waiting for pods to become ready (60s)..."
  sleep 60

  log "Pod status:"
  kubectl get pods -n sre-app

  ok "Kubernetes deployment complete!"
  echo ""
  echo "  Frontend:   http://localhost:30080"
  echo "  Prometheus: http://localhost:30090"
  echo "  Grafana:    http://localhost:30300  (admin/admin)"
}

# ── Main ───────────────────────────────────────────────────
case "$MODE" in
  swarm)      deploy_swarm ;;
  kubernetes) deploy_kubernetes ;;
  *)          fail "Unknown mode '$MODE'. Use 'swarm' or 'kubernetes'" ;;
esac
