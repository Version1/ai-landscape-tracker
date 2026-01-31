# Documentation Index

## Project: Agentic AI Landscape Tracker

A curated portal tracking developments in the Agentic AI space from major players.

---

## Artifact Status

| Phase | Artifact | Status | Last Updated |
|-------|----------|--------|--------------|
| Phase 1 | [Business Problem Statement](Phase1_Strategy_Planning/business_problem_statement.md) | ✅ Complete | 2026-01-31 |
| Phase 2 | [Solution Design](Phase2_Requirements_Design/solution_design.md) | ✅ Complete | 2026-01-31 |
| Phase 4 | Implementation (crawler/, site/) | ✅ Complete | 2026-01-31 |
| - | [SDLC Adherence Record](sdlc_adherence_record.md) | ✅ Complete | 2026-01-31 |

---

## Phase Progression

```
[Phase 1: Strategy] ──▶ [Phase 2: Design] ──▶ [Phase 4: Build] ──▶ [Deploy]
       ✅                      ✅                    ✅              ⏳
```

**Current Status:** Ready for deployment to GitHub Pages

---

## Reading Guide

### For New Team Members
1. Start with [Business Problem Statement](Phase1_Strategy_Planning/business_problem_statement.md) - understand the why
2. Review [Solution Design](Phase2_Requirements_Design/solution_design.md) - understand the how
3. Check project `README.md` for local development setup

### For Technical Review
1. [Solution Design](Phase2_Requirements_Design/solution_design.md) - architecture decisions
2. `crawler/README.md` - crawler implementation details
3. `.github/workflows/crawl-and-deploy.yml` - automation setup

### For Compliance/Governance
1. [SDLC Adherence Record](sdlc_adherence_record.md) - adherence level and deviations

---

## Directory Structure

```
Documentation/
├── README.md                          # This file
├── sdlc_adherence_record.md          # SDLC compliance documentation
├── Initial Docs/                      # Pre-existing context
│   └── Additional Context from Us/
│       └── Version 1 detailed brand guidelines 2024.md
├── Phase1_Strategy_Planning/
│   └── business_problem_statement.md
└── Phase2_Requirements_Design/
    └── solution_design.md
```

---

## Skipped Phases (Flexible Adherence)

Given the project context (internal tool, low risk, immediate timeline), the following phases were streamlined:

| Phase | Status | Rationale |
|-------|--------|-----------|
| Phase 3: Architecture | Merged into Phase 2 | Simple architecture, no complex decisions |
| Phase 5: Integration | N/A | GitHub Actions handles integration |
| Phase 6: Test | Deferred | Manual testing for MVP |
| Phase 7-9: Ops/Improve/Maintain | Post-deployment | Will establish after initial release |

See [SDLC Adherence Record](sdlc_adherence_record.md) for full details.
