import nox


PYTHON_FILES = [
    "rivalcfg",
    "test",
    "noxfile.py",
    "scripts",
]


@nox.session(reuse_venv=True)
def lint(session):
    session.install("flake8", "black")
    session.run("black", "--check", "--diff", "--color", *PYTHON_FILES)
    session.run("flake8", *PYTHON_FILES)


@nox.session(reuse_venv=True)
def black_fix(session):
    session.install("black")
    session.run("black", *PYTHON_FILES)


@nox.session(python=["3.7", "3.8", "3.9", "3.10"], reuse_venv=True)
def test(session):
    session.install("pytest")
    session.install(".")
    session.run(
        "pytest",
        "--doctest-modules",
        "rivalcfg",
        "test",
        env={
            "RIVALCFG_DRY": "1",
        },
    )


@nox.session(reuse_venv=True)
def gendoc(session):
    session.install("sphinx", "sphinx-rtd-theme")
    session.install("-e", ".")
    session.run("sphinx-build", "-M", "html", "doc", "build")


@nox.session(reuse_venv=True)
def update_ssdb(session):
    session.run("python", "./scripts/sse3_db_update.py", "ssdb/sse3.db.csv")
