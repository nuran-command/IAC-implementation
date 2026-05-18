#!/usr/bin/env bash
# ============================================================
# SRE Health Check Script
# Validates status of all microservices via Nginx API Gateway
# Usage: bash scripts/health_check.sh [base_url]
# ============================================================
set -euo pipefail

# ANSI color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default base URL is localhost:8080 (Compose)
BASE_URL="${1:-http://localhost:8080}"

echo -e "${BLUE}===================================================${NC}"
echo -e "${BLUE}        SRE Microservices Health Validation        ${NC}"
echo -e "${BLUE}===================================================${NC}"
echo -e "Target Gateway: ${YELLOW}${BASE_URL}${NC}"
echo ""

# List of microservices to check
services=(
  "auth"
  "users"
  "products"
  "orders"
  "payment"
  "notification"
)

errors=0

for service in "${services[@]}"; do
  url="${BASE_URL}/api/${service}/health"
  
  # Resolve names using standard bash case block for maximum compatibility
  case "$service" in
    "auth")          name="Authentication Service  " ;;
    "users")         name="User Profile Service    " ;;
    "products")      name="Product Catalog Service " ;;
    "orders")        name="Order Processing Service" ;;
    "payment")       name="Payment Handling Service" ;;
    "notification")  name="Notification Service    " ;;
    *)               name="Unknown Service         " ;;
  esac

  # Check with curl, capture response and status code
  set +e
  response=$(curl -s -f -w "\n%{http_code}" --connect-timeout 3 "$url" 2>/dev/null)
  exit_code=$?
  set -e

  if [ $exit_code -ne 0 ]; then
    echo -e "[ ${RED}FAIL${NC} ] ${name} -> Unreachable (curl error ${exit_code})"
    errors=$((errors + 1))
    continue
  fi

  # Extract body and HTTP code
  body=$(echo "$response" | sed '$d')
  http_code=$(echo "$response" | tail -n1)

  if [ "$http_code" -eq 200 ]; then
    # Check if body contains 'healthy'
    if echo "$body" | grep -q '"status":"healthy"' || echo "$body" | grep -q '"status": "healthy"'; then
      echo -e "[  ${GREEN}OK${NC}  ] ${name} -> Healthy (HTTP ${http_code})"
    else
      echo -e "[ ${YELLOW}WARN${NC} ] ${name} -> Status not 'healthy': ${body}"
      errors=$((errors + 1))
    fi
  else
    echo -e "[ ${RED}FAIL${NC} ] ${name} -> Error (HTTP ${http_code}): ${body}"
    errors=$((errors + 1))
  fi
done

echo ""
echo -e "${BLUE}===================================================${NC}"
if [ $errors -eq 0 ]; then
  echo -e "${GREEN}SUCCESS: All microservices are healthy and reachable!${NC}"
  exit 0
else
  echo -e "${RED}FAILURE: ${errors} service health check(s) failed.${NC}"
  exit 1
fi
