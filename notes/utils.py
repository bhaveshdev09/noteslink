import difflib


def calculate_changes(current_content, previous_content):
    has_changed, changes = False, []

    # Compute the differences between the previous and current content
    diff = difflib.unified_diff(
        previous_content.splitlines(keepends=True),
        current_content.splitlines(keepends=True),
        "previous",
        "current",
        lineterm="",
    )

    # print(list(diff))
    # Convert the differences to a list of dictionaries
    result = {"previous": previous_content, "current": current_content}

    for line in diff:
        if line.startswith(("+++", "---")) or (
            line.startswith("@") and line.endswith("@")
        ):
            continue
        if line.startswith("+"):
            changes.append({"type": "added", "content": line[1:]})
        elif line.startswith("-"):
            changes.append({"type": "removed", "content": line[1:]})
        else:
            changes.append({"type": "unchanged", "content": line[1:]})

    if changes:
        has_changed = True

    result["changes"] = changes

    return has_changed, result
