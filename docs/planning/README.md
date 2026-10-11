# Planning documents

This directory holds the project's planning artifacts. Three document types, one job each. A large change flows spec then plan; ADRs are recorded whenever a qualifying decision is made, independent of that flow.

## Specs (specs/)

The behavior contract for a change: what the system must do, the decisions made, and the scenarios that define done. A spec states targets in its own voice. Verified facts about the current system are tagged [confirmed], unapproved decisions are tagged [proposed], and labeled guesses are tagged [inferred]. Read a spec to know what a change is supposed to do.

A spec records what was built at the time of building; it does not necessarily reflect the current state of the system. Later change is documented in a new spec that supersedes the old one, never by rewriting the old spec. To learn the current behavior, read the source.

## Plans (plans/)

The execution order for a change: tasks in dependency order, with checkpoints between phases. A plan may be lightweight (overview, task list, one checkpoint) for targeted work. Plans are updated as tasks complete, so they double as the progress record. Read a plan to know what is done and what remains.

## ADRs (adrs/)

Records of decisions that are hard to reverse, surprising without context, and the result of real trade-offs. Not every decision earns one; the obvious and the easily reversible do not. Each records the decision, the context, and why. Read an ADR before changing something that looks wrong on purpose.

## Numbering

All three types use left-padded sequential numbering (0001-slug.md) with kebab case slugs.
