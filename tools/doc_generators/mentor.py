from pathlib import Path

from doc_generators.constants import PROJECT_MANIFEST_DIR


def generate_mentor_context(state: dict, root: Path) -> None:
    """
    Generate MENTOR_CONTEXT.md
    """

    project = state["project"]
    vision = state["vision"]
    roadmap = state["roadmap"]
    progress = state["progress"]
    architecture = state["application_architecture"]

    architecture_decisions = "\n".join(
        f"- {item['date']} : {item['decision']}"
        for item in state["architecture_decisions"]
    )

    roadmap_text = ""

    for phase in roadmap["phases"]:
        roadmap_text += (
            f"### Phase {phase['phase']} - {phase['name']}\n"
            f"{phase['goal']}\n\n"
        )

    layers = "\n".join(
        f"- {layer}"
        for layer in architecture["layers"]
    )

    pipeline = "\n".join(
        f"- {step}"
        for step in architecture["current_pipeline"]
    )

    instructions = "\n".join(
        f"- {rule}"
        for rule in state["assistant_context"]["working_rules"]
    )

    learning = "\n".join(
        f"- {rule}"
        for rule in state["user_learning_preferences"]["mentoring_style"]
    )

    content = f"""# Mentor Context

---

# Project

**Name:** {project["name"]}

**Version:** {project["version"]}

---

# Vision

## Current Goal

{vision["current_goal"]}

## Final Goal

{vision["final_goal"]}

---

# Current Roadmap

Current Phase : {roadmap["current_phase"]}

{roadmap_text}

---

# Current Progress

Phase : {progress["phase"]}

Step : {progress["current_step"]}

Current Task :

{progress["current_task"]}

Next Task :

{progress["next_task"]}

---

# Current Architecture

## Layers

{layers}

## Current Pipeline

{pipeline}

---

# Architecture Decisions

{architecture_decisions}

---

# Assistant Instructions

{instructions}

---

# User Learning Preferences

{learning}

---

Last Updated : {state["last_updated"]}
"""

    (PROJECT_MANIFEST_DIR / "MENTOR_CONTEXT.md").write_text(
        content,
        encoding="utf-8",
    )