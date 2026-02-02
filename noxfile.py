import nox

PYTHON_FILES = [
    "rivalcfg",
    "test",
    "noxfile.py",
    "scripts",
]


@nox.session(reuse_venv=True)
def lint(session):
    session.install("-e", ".[dev]")
    session.run("black", "--check", "--diff", "--color", *PYTHON_FILES)
    session.run("flake8", *PYTHON_FILES)
    session.run("validate-pyproject", "pyproject.toml")


@nox.session(reuse_venv=True)
def black_fix(session):
    session.install("-e", ".[dev]")
    session.run("black", *PYTHON_FILES)


@nox.session(python=["3.10", "3.11", "3.12", "3.13", "3.14"], reuse_venv=True)
def test(session):
    session.install("-e", ".[dev]")
    session.run(
        "pytest",
        "--doctest-modules",
        "rivalcfg",
        "test",
        env={
            "RIVALCFG_DRY": "1",
            "RIVALCFG_DEBUG_NO_COMMAND_DELAY": "1",
        },
    )


@nox.session(reuse_venv=True)
def gendoc(session):
    session.install("-e", ".[dev]")
    session.install("-e", ".")
    session.run("sphinx-build", "-M", "html", "doc", "build")


@nox.session(reuse_venv=True)
def update_ssdb(session):
    session.run("python", "./scripts/sse3_db_update.py", "ssdb/sse3.db.csv")
