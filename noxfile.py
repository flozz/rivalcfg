import nox


@nox.session
def lint(session):
    session.install("flake8")
    session.run("flake8", "rivalcfg", "test", "noxfile.py", "scripts")


@nox.session(python=["2.7", "3.5", "3.6", "3.7", "3.8"])
def test(session):
    session.install("pytest")
    session.install(".")
    # Do not run doctest when using Python 2 as the output of some functions
    # looks deferent from the one of Python 3 and so it cannot be matched
    # properly...
    if session.python == "2.7":
        session.run("pytest", "test", env={"RIVALCFG_DRY": "1"})
    else:
        session.run("pytest", "--doctest-modules", "rivalcfg", "test", env={
            "RIVALCFG_DRY": "1",
            })


@nox.session
def gendoc(session):
    session.install("sphinx", "sphinx-rtd-theme")
    session.install("-e", ".")
    session.run("sphinx-build", "-M", "html", "doc", "build")


@nox.session
def update_ssdb(session):
    session.install("natsort")
    session.run("python", "./scripts/sse3_db_update.py", "ssdb/sse3.db.csv")
