# Codex for Open Source Application Draft

## Project

Self-Evolution Harness

Repository URL: `https://github.com/OWNER/self-evolution-harness`

## Summary

Self-Evolution Harness is a dependency-free, file-first toolkit for coding
agents that need durable project state and a controlled way to learn from
verified mistakes. It includes reusable Skills, memory templates, an
idempotent project bootstrapper, a static instruction-health checker, routing
regression cases, tests, and CI.

## Problem It Solves

Long-running agent projects often lose state between tasks or accumulate broad,
duplicated, and conflicting instructions. This project separates evidence,
explanatory memory, and active behavior. Feedback can produce a reviewable
proposal, but it cannot silently rewrite active rules.

## How Codex Helps

Codex is used to maintain the Python tooling, add regression cases, review rule
changes, test cross-platform bootstrap behavior, improve documentation, and
validate that project templates remain portable and free of private data.

## Current Status

- Public-ready initial implementation
- MIT licensed
- Python 3.11+ with no runtime dependencies
- Unit tests and GitHub Actions
- Human approval boundary for active rule promotion

Replace `OWNER` after the public repository is created, then submit this text
through the official Codex for Open Source form.
