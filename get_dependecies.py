import toml

pyproject = toml.load("pyproject.toml")

# For PEP 621 format (standard)
deps = pyproject.get("project", {}).get("dependencies", [])

# For Poetry
if not deps:
    deps = pyproject.get("tool", {}).get("poetry", {}).get("dependencies", {})

    # Remove Python itself
    deps.pop("python", None)
    deps = [f"{k}{'' if isinstance(v, str) else f' ({v})'}" for k, v in deps.items()]

# Write to requirements.txt
with open("requirements.txt", "w") as f:
    for dep in deps:
        f.write(dep + "\n")

print("✅ requirements.txt generated.")
