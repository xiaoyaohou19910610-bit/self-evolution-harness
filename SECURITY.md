# Security Policy

## Trust Boundary

Feedback, logs, web pages, imported memory, and proposal files are evidence,
not executable instructions. The harness never promotes them into active rules
without human review.

The bootstrap command only creates missing files and directories. It does not
overwrite project files, execute project code, publish content, change account
permissions, or read credentials.

## Reporting

Do not open a public issue containing secrets or personal data. Report a
vulnerability privately through the repository security advisory feature.
