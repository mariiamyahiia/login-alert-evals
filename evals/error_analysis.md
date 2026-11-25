# Error analysis (16 outputs)

## Notes (one line per output)
| ID | Label given | Note |
|---|---|---|
| A01 | benign | matches truth, consistent device, location, and MFA over 8 months |
| A02 | suspicious | matches truth, high-volume failed logins from new IP/Lagos, no MFA, then success  |
| A03 | suspicious | matches truth, impossible travel (Cairo to Frankfurt in 18 min) with no VPN/travel record. |
| A04 | benign | matches truth, scheduled maintenance window with MFA and approved change ticket |
| A05 | suspicious | matches truth, MFA push fatigue approved from a new country |
| A06 | benign | matches truth, recurring nightly backup login from expected server IP with no failures |
| A07 | benign | matches truth, new phone in usual city with MFA and registered onboarding ticke |
| A08 | suspicious | matches truth, password spraying across 9 accounts from one IP ending in a success |
| A09 | benign | matches truth, brief lockout on usual Cairo laptop followed quickly by valid login |
| A10 | suspicious | matches truth, external mail forwarding rule plus bulk download of 2,300 files in 5 min |
| A11 | benign | matches truth, normal hours login via approved company VPN exit node with MFA |
| A12 | benign | matches truth, off-hours login from cairo residential IP with MFA and no other anomalies |
| A13 | suspicious | matches truth, unrotated 2-year-old API token used off-hours from new hosting IP to list users |
| A14 | benign | matches truth, gradual home-IP failures followed by success alongside a password-reset ticket |
| A15 | suspicious | matches truth, tor exit node login representing first-ever access outside Egypt |
| A16 | benign | matches truth, contractor login from approved client site IP scoped to ticketing system |

## Categories (2 to 4 failure categories, plus No problem)
| Category | Count |
|---|---|
| Off-hours / context-heavy benign edge cases (e.g., A04, A09, A12, A14) | 0 |
| Anonymized / new-location access with valid MFA (e.g., A05, A15) | 0 |
| Post-auth / token abuse signals (e.g., A10, A13) | 0 |
| No problem | 16 |
| **Total** | **16** |