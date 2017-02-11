import pytest

# see http://doc.pytest.org/en/latest/example/simple.html#control-skipping-of-tests-according-to-command-line-option

def pytest_addoption(parser):
    parser.addoption("--runslow", action="store_true",
        help="run slow tests")
