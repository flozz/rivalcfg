import nox


@nox.session
def lint(session):
    session.install("flake8")
    session.run("flake8", "rivalcfg", "test", "noxfile.py")


@nox.session(python=["2.7", "3.5", "3.6", "3.7", "3.8"])
def test(session):
    session.install("pytest")
    session.install(".")
    session.run("pytest", "--doctest-modules", "rivalcfg", env={
        "RIVALCFG_DRY": "1",
        })
    session.run("pytest", "test")
