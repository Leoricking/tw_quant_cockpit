"""
quality/ - Data Quality Gate & Production Readiness Score (v0.3.20).

Provides:
  DataQualityGate        : main gate, computes all scores and gate decisions
  ReadinessScoreCalculator : shared score utilities and classification
  MockContaminationChecker : scans for mock data contamination

[!] Research Only. Simulation Only. No Real Orders.
[!] PRODUCTION_BLOCKED is always True in v1.
[!] REAL_ORDER_READY is never allowed.
"""
