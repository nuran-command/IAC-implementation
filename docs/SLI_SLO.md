# Service Level Indicators (SLI) & Service Level Objectives (SLO)

This document defines the reliability targets for the SRE Microservices Infrastructure.

## 1. Service Level Indicators (SLI)

We track the following metrics as indicators of our system health:

| Indicator | Definition | Source |
|-----------|------------|--------|
| **Availability** | The percentage of successful requests (non-5xx) over total requests. | Prometheus (`http_requests_total`) |
| **Latency** | The time it takes to process a request (95th percentile). | Prometheus (`http_request_duration_seconds`) |
| **Error Rate** | The percentage of requests that result in a 500-range error. | Prometheus (`http_requests_total{status=~"5.."} / http_requests_total`) |
| **Success Rate**| The percentage of orders successfully completed in the Order Service. | Application Logs / Custom Metrics |

## 2. Service Level Objectives (SLO)

Based on the SLIs above, we have set the following targets for our production environment:

| Objective | Target | Measurement Period |
|-----------|--------|-------------------|
| **Availability** | ≥ 99.9% | Monthly |
| **Latency** | ≤ 200ms (p95) | Rolling 7 Days |
| **Error Rate** | ≤ 0.1% | Rolling 24 Hours |
| **Success Rate**| ≥ 98% | Monthly |

## 3. Error Budget

The Error Budget is the allowed amount of "unreliability" before SREs must stop feature development and focus on reliability.

- **Monthly Availability Budget (99.9%)**: ~43 minutes of downtime allowed per month.
- **Consumption**: If the budget is consumed faster than expected (burn rate > 1), automated alerts will trigger an incident response.

---

## 4. Monitoring Strategy

- **Prometheus**: Scrapes metrics from `/metrics` endpoints of all services every 15 seconds.
- **Grafana**: Visualizes SLO compliance and error budget burn rates.
- **Alertmanager**: Sends alerts when SLO thresholds are breached for more than 5 minutes.
