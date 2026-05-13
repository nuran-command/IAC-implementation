# SLI/SLO Definitions — End Term SRE Project

## Overview

Service Level Indicators (SLIs) are the quantitative measurements of service behavior.
Service Level Objectives (SLOs) are the target values for each SLI that define reliability goals.

---

## SLIs and SLOs per Service

| Service            | SLI Metric              | Measurement Method                          | SLO Target       |
|--------------------|-------------------------|---------------------------------------------|------------------|
| **All Services**   | **Availability**        | `up` metric from Prometheus                  | ≥ 99.0%          |
| **All Services**   | **Latency (p95)**       | HTTP response time (95th percentile)         | ≤ 200 ms         |
| **All Services**   | **Error Rate**          | `5xx` responses / total requests             | ≤ 1%             |
| **All Services**   | **Request Success Rate**| Successful HTTP responses / total requests   | ≥ 99%            |
| **Order Service**  | **DB Connection Rate**  | `order_service_status` metric                | = 1 (connected)  |
| **Payment Service**| **Payment Success Rate**| Successful payment API calls / total calls   | ≥ 99.5%          |
| **Auth Service**   | **Auth Success Rate**   | Successful logins / total login attempts     | ≥ 99%            |

---

## Detailed SLO Definitions

### 1. Availability SLO
- **SLI**: Percentage of time the service is responding to health-check requests with HTTP 200.
- **SLO**: ≥ 99% availability per rolling 30-day window.
- **Prometheus Expression**: `avg_over_time(up{job="<service>"}[30d]) * 100`
- **Alert**: Fire `ServiceDown` alert if `up == 0` for > 1 minute.

### 2. Latency SLO
- **SLI**: 95th percentile of HTTP request duration in milliseconds.
- **SLO**: p95 latency ≤ 200 ms.
- **Prometheus Expression**: `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) * 1000`
- **Alert**: Fire `HighLatency` alert if p95 > 300 ms for > 5 minutes.

### 3. Error Rate SLO
- **SLI**: Percentage of HTTP requests resulting in 5xx status codes.
- **SLO**: Error rate ≤ 1% over a 5-minute window.
- **Prometheus Expression**: `rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) * 100`
- **Alert**: Fire `HighErrorRate` alert if error rate > 1% for > 2 minutes.

### 4. Request Success Rate SLO
- **SLI**: Percentage of HTTP requests that complete successfully (2xx and 3xx).
- **SLO**: ≥ 99% success rate.
- **Prometheus Expression**: `rate(http_requests_total{status=~"2..|3.."}[5m]) / rate(http_requests_total[5m]) * 100`

---

## Error Budget

| Window    | Allowed Downtime (99% SLO) |
|-----------|---------------------------|
| Daily     | 14.4 minutes              |
| Weekly    | 1 hour 40 minutes         |
| Monthly   | 7 hours 18 minutes        |

If the error budget is exhausted, new feature releases are paused until reliability is restored.

---

## Incident Threshold

Incidents are declared when:
- Any service SLO drops below its target for **> 5 minutes**
- The Order Service database connection metric `order_service_status = 0` for **> 1 minute**
- CPU usage exceeds 80% for **> 2 minutes** (capacity risk)
