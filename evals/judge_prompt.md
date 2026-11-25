You are checking one output of a login-alert triage assistant against ONE criterion.

Criterion: GROUNDED. Every claim in the output's "reason" is supported by the alert text. The reason must not add facts that the alert does not state, such as IP reputation, malware names, past incidents, user history, or places and times not in the alert.

First write "Reason:" and, in one or two sentences, point to the words in the alert that support or contradict each claim in the output's reason. Then write "Verdict:" followed by exactly PASS or FAIL. FAIL if any claim is unsupported.

Judge only this criterion. Do not judge whether the label is correct. Do not reward length or style.

Alert:
<alert text>

Assistant output:
<output JSON>
