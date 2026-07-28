from pathlib import Path


def _bullet(items: list) -> str:
    return "\n".join(f"- {item}" for item in items)


def generate_project_vision(state: dict, root: Path) -> None:
    """
    Generate PROJECT_VISION.md
    """

    vision = state["vision"]
    roadmap = state["roadmap"]

    roadmap_text = ""

    for phase in roadmap["phases"]:
        roadmap_text += (
            f"## Phase {phase['phase']} - {phase['name']}\n\n"
            f"{phase['goal']}\n\n"
        )

    content = f"""# EnterpriseBrain - Project Vision

---

# Product

**Name:** {vision["product_name"]}

---

# Current Goal

{vision["current_goal"]}

---

# Final Goal

{vision["final_goal"]}

---

# Current Scope

{_bullet(vision["current_scope"])}

---

# Future Scope

{_bullet(vision["future_scope"])}

---

# Non Goals

{_bullet(vision["non_goals"])}

---

# Development Roadmap

Current Active Phase: **Phase {roadmap["current_phase"]}**

{roadmap_text}

---

# Development Principles

- Build for today's roadmap.
- Design for tomorrow.
- Avoid premature optimization.
- Prefer modular architecture.
- Keep documentation synchronized.
- Verify every milestone before moving forward.
- Enterprise quality over quick hacks.

---

# Learning & Mentoring Principles

{_bullet(state["user_learning_preferences"]["mentoring_style"])}

---

Last Updated: {state["last_updated"]}
"""

    (root / "PROJECT_VISION.md").write_text(
        content,
        encoding="utf-8",
    )