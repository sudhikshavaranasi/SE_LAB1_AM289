# Use-Case Flow Specification

## Use Case: Reserve Food Batch

### Use Case ID
UC-001

### Primary Actor
Shelter Coordinator

### Goal
Reserve an available surplus food batch and select a suitable pickup window before the food expires.

### Preconditions
1. The Shelter Coordinator is registered and verified on the platform.
2. At least one valid food batch is available for reservation.
3. The selected food batch has not expired.
4. The Shelter Coordinator has access to the platform.

### Postconditions
1. The selected food batch is reserved for the Shelter Coordinator.
2. The selected pickup window is recorded.
3. The reserved batch is no longer available for other shelters.
4. The reservation confirmation is provided to the Shelter Coordinator.

### Main Success Scenario
1. The Shelter Coordinator logs into the platform.
2. The system displays available surplus food batches.
3. The Shelter Coordinator selects an available food batch.
4. The system displays the food batch details, including quantity, dietary information, and expiry time.
5. The Shelter Coordinator chooses the desired food batch.
6. The system displays available pickup windows.
7. The Shelter Coordinator selects a pickup window.
8. The system validates that the food batch is still available and has not expired.
9. The system confirms the reservation.
10. The system marks the food batch as reserved and records the selected pickup window.
11. The system displays the reservation confirmation to the Shelter Coordinator.

### Alternate Flow
**A1. Food batch expires before reservation is completed**

1. The Shelter Coordinator attempts to reserve the selected food batch.
2. The system detects that the food batch has expired.
3. The system prevents the reservation.
4. The system removes the expired food batch from the active claim board.
5. The system asks the Shelter Coordinator to select another available food batch.
