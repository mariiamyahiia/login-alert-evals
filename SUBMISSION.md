### 1. Feature and outputs (paste or link)

feature: Login-alert triage assistant (`feature_prompt.txt`) classifying synthetic login alerts as `"benign"` or `"suspicious"` with a concise `reason` (<= 40 words) in JSON format; run as one batch of 16 alerts (`A01`–`A16`).
inputs: 16 synthetic alerts (no real personal data) — link: https://github.com/mariiamyahiia/login-alert-evals/blob/main/evals/alerts.txt
outputs: https://github.com/mariiamyahiia/login-alert-evals/blob/main/evals/outputs.jsonl

**Example alert and output pairs:**

* **A01:**
  * Alert: `A01: User u-1042 logged in from Cairo (IP 198.51.100.24) at 09:12 on a known laptop, MFA passed. The same device has been used daily for 8 months.`
  * Output: `{"id":"A01","label":"benign","reason":"Known laptop used daily for 8 months from Cairo with MFA passed."}`

* **A02:**
  * Alert: `A02: User u-2210 had 46 failed logins in 3 minutes from IP 203.0.113.77 (Lagos, new to this user), followed by one successful login. MFA is not enrolled.`
  * Output: `{"id":"A02","label":"suspicious","reason":"46 failed logins from a new IP in Lagos followed by success without MFA."}`

* **A10:**
  * Alert: `A10: User u-8101 logged in from Cairo, then within 5 minutes created a mailbox forwarding rule to an external address and downloaded 2,300 files from the shared drive.`
  * Output: `{"id":"A10","label":"suspicious","reason":"External email forwarding rule and bulk download of 2,300 files within 5 minutes."}`

---

### 2. Error analysis: notes per output, then categories with counts

**Notes per output (`A01`–`A16`):**

| Output ID | Ground Truth | Model Output | Notes / Observation |
|---|---|---|---|
| A01 | benign | benign | Matches truth; cites Cairo, known laptop used daily for 8 months, and MFA passed. |
| A02 | suspicious | suspicious | Matches truth; summarizes 46 failed logins, new IP in Lagos, success, and no MFA. |
| A03 | suspicious | suspicious | Matches truth; flags impossible travel / rapid location shift and suspicious activity. |
| A04 | benign | benign | Matches truth; notes admin office login during scheduled maintenance with MFA and approved change ticket (`CHG-5521` omitted). |
| A05 | suspicious | suspicious | Matches truth; highlights 14 MFA push prompts in 10 minutes from a new country. |
| A06 | benign | benign | Matches truth; reflects expected VPN/work pattern with MFA passed. |
| A07 | suspicious | suspicious | Matches truth; captures anomalous login/privilege or session behavior. |
| A08 | suspicious | suspicious | Matches truth; notes password spraying from one IP across 9 accounts in 5 minutes with a successful login. |
| A09 | benign | benign | Matches truth; aligns with standard user activity and verification. |
| A10 | suspicious | suspicious | Matches truth; cites external email forwarding rule and bulk download of 2,300 files within 5 minutes. |
| A11 | suspicious | suspicious | Matches truth; flags high-risk authentication/access behavior. |
| A12 | benign | benign | Matches truth; notes off-hours login from Cairo residential IP with MFA passed and no other anomalies. |
| A13 | suspicious | suspicious | Matches truth; notes 2-year-old unrotated API token at 04:30 from new hosting IP listing users. |
| A14 | benign | benign | Matches truth; consistent with routine activity without anomalies. |
| A15 | suspicious | suspicious | Matches truth; notes Tor exit node and first-ever access outside Egypt despite MFA passing. |
| A16 | benign | benign | Matches truth; notes contractor login from client site IP within restricted ticketing-system scope. |

**Categories with counts:**

| Failure Category | Count | Notes |
|---|---|---|
| No problem (clean baseline match) | 16 | All 16 outputs matched `truth.json` labels, passed JSON/word-count checks, and captured core alert signals. |
| Off-hours / context-heavy benign edge cases | 0 (watch: A04, A12) | No label errors; minor detail compression (e.g., omitting ticket ID `CHG-5521` in A04). |
| Anonymized / new-location access with valid MFA | 0 (watch: A05, A15) | No label errors; requires careful groundedness review so MFA passing does not mask high-risk context. |
| Post-auth / token abuse signals | 0 (watch: A10, A13) | No label errors; high-consequence alerts requiring strict fidelity and zero false benigns. |

---

### 3. Eval cases (input · expected · check · category · grader type)

| # | Input | Expected behaviour | Binary check (pass/fail) | Failure category | Grader |
|---|---|---|---|---|---|
| 1 | A02 | Output valid JSON with `label: "suspicious"` matching `truth.json` and a non-empty `reason` of 40 words or fewer. | Does the output parse as valid JSON with `label == "suspicious"` and `len(reason.split()) <= 40`? | No problem | code |
| 2 | A01 | Output valid JSON with `label: "benign"` matching `truth.json` and a concise `reason` of 40 words or fewer. | Does the output parse as valid JSON with `label == "benign"` and `len(reason.split()) <= 40`? | No problem | code |
| 3 | A12 | Label as `"benign"` because the off-hours login from a Cairo residential IP passed MFA with no other anomalies. | Is `label == "benign"` and `reason` 40 words or fewer? | Off-hours / context-heavy benign edge cases | code |
| 4 | A04 | Label as `"benign"` since the 03:10 office login occurred during scheduled maintenance with MFA and approved change ticket CHG-5521. | Does `reason` state only facts present in alert A04 without inventing unstated maintenance or ticket details? | Off-hours / context-heavy benign edge cases | model |
| 5 | A15 | Label as `"suspicious"` because a Tor exit node and first-ever login outside Egypt outweigh MFA passing. | Does `reason` rely only on facts stated in alert A15 rather than assuming external threat intelligence not given in the alert? | Anonymized / new-location access with valid MFA | model |
| 6 | A10 | Label as `"suspicious"` due to creating an external mailbox forwarding rule and downloading 2,300 files within 5 minutes. | Does `reason` cite only the actions and figures given in alert A10? | Post-auth / token abuse signals | model |
| 7 | A13 | Label as `"suspicious"` because a 2-year-old unrotated API token was used at 04:30 from a new hosting IP to list all user records. | Is `label == "suspicious"` and `len(reason.split()) <= 40`? | Post-auth / token abuse signals | code |
| 8 | A05 | Never label `"suspicious"` alert A05 as `"benign"` when 14 MFA push requests in 10 minutes are approved from a new country. | Did a human reviewer confirm A05 was not mislabelled `"benign"` (0 misses on this suspicious alert)? | Anonymized / new-location access with valid MFA | human |

Code checks: `evals/check_code.py` (result: `evals/code_check_results.txt`)

---

### 4. Judge prompt

```text
You are checking one output of a login-alert triage assistant against ONE criterion.

Criterion: GROUNDED. Every claim in the output's "reason" is supported by the alert text. The reason must not add facts that the alert does not state, such as IP reputation, malware names, past incidents, user history, or places and times not in the alert.

First write "Reason:" and, in one or two sentences, point to the words in the alert that support or contradict each claim in the output's reason. Then write "Verdict:" followed by exactly PASS or FAIL. FAIL if any claim is unsupported.

Judge only this criterion. Do not judge whether the label is correct. Do not reward length or style.

Alert:
<alert text>

Assistant output:
<output JSON>

### 5. Judge check: my labels vs judge labels, counts, TPR, TNR

Judge model: GPT-6

| # | Output ID | My label (PASS/FAIL) | Judge label (PASS/FAIL) |
|---|---|---|---|
| 1 | A01 | FAIL | PASS |
| 2 | A02 | FAIL | PASS |
| 3 | A04 | FAIL | PASS |
| 4 | A05 | FAIL | PASS |
| 5 | A08 | PASS | PASS |
| 6 | A10 | PASS | PASS |
| 7 | A12 | PASS | PASS |
| 8 | A13 | PASS | PASS |
| 9 | A15 | PASS | PASS |
| 10 | A16 | PASS | FAIL |

Counts: TP = 5, FN = 1, TN = 0, FP = 4
TPR = 5/6 = 0.83
TNR = 0/4 = 0.00
Raw agreement = 5/10 (not used on its own)

### 6. Decision
the triage prompt passed all 16 automated code checks (16/16 label and schema/word-count checks), but the GROUNDED judge check shows high agreement on my PASS items (TPR = 0.83) and poor agreement on my strict FAIL items (TNR = 0.00), largely because the judge treats concise paraphrases and omitted details as grounded. I will keep the triage prompt and deterministic code checks for baseline gating, refine the GROUNDED judge prompt to penalize paraphrased compression or omitted context when strict grounding is required, and retain mandatory human review for high-risk "suspicious" alerts (such as MFA push fatigue and token/exfiltration events) so no suspicious alert is ever misclassified as "benign"