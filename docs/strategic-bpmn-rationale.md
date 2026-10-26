# Strategic BPMN – Design Rationale

**Author:** Campbell Clark · **Model:** v3 – Complete message flows, message start events, layout and annotations (Campbell).bpmn /
**Versions:** v1 initial draft (Patryk) → v2 + v3 (Campbell)

## Structure
- **1 pool, 3 lanes:** Bristol Regional Food Network – Marketplace Platform, Finance, Network Administration (lanes show responsibility)
- **4 external black-box pools:** Customer, Producer, Certification Verification Service (use case 1), Payment Provider – we model only our interactions with them
- **Collapsed sub-processes:** strategic level; detail added in Sprint 2

## Key decisions
- Message start events where an external message triggers a process (order, product submission, stock update)
- Timer start event for weekly producer settlement (case study)
- Process customer orders → Manage inventory, because orders reduce stock (use case 1 out-of-stock rule)
- No gateways – decisions are operational detail for Sprint 2

## Traceability
| Use case 1 | Functionality | Strategic BPMN | Sprint 2 |
|---|---|---|---|
| List, validate, verify organic, publish | F1: Adding a new product | Validate and publish product listings | Operational BPMN 1 |
| Update stock/season, auto unavailable at 0 | F2: Updating stock and availability | Manage inventory and availability | Operational BPMN 2 |
