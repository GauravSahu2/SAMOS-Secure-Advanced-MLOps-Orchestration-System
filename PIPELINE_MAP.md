# 🗺️ Visual Architecture Map

```mermaid
graph TD
  NiFi[Apache NiFi] --> A[DataOps]
  Airflow[Apache Airflow] -.->|Orchestrates| A
  Airflow -.->|Orchestrates| B
  A[DataOps] --> B[MLOps]
  B --> C[ModelSecOps]
  C --> D[DevSecOps]
  D --> E[SRE]
  E --> F[SENTIENT_FACTORY]
  subgraph DataOps
    A0[NiFi Bridge] --> A1[Ingest] --> A2[Validate] --> A3[Privacy]
  end
  subgraph MLOps
    B1[AutoML] --> B2[NAS] --> B3[Train] --> B4[Distillation Forge]
  end
  subgraph SRE
    E1[MAB] --> E2[Drift] --> E3[Failover]
  end
  Prometheus[Prometheus] --- E
  Grafana[Grafana] --- Prometheus
```