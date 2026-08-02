# Legacy Project State

This directory contains files preserved from the migration from the original
single `project_state.yaml` design to the modular `project_manifest/state/*.yaml`
architecture.

These files are retained only for historical reference and rollback support.

They are not used by the active documentation or project-update workflow.

Active source of truth:

project_manifest/state/

Active update workflow:

project_manifest/updates/pending/
    -> tools/apply_project_update.py
    -> project_manifest/state/
    -> tools/update_docs.py
    -> generated Markdown documents
