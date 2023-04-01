import os
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

import prefect
from prefect.server.schemas.actions import WorkPoolCreate
from prefect.testing.cli import invoke_and_assert
from prefect.utilities.asyncutils import run_sync_in_worker_thread

TEST_PROJECTS_DIR = prefect.__root_path__ / "tests" / "test-projects"


@pytest.fixture
def project_dir():
    original_dir = os.getcwd()
    os.chdir(TEST_PROJECTS_DIR)
    result = invoke_and_assert("project init --name test_project")
    yield
    os.chdir(original_dir)
    shutil.rmtree((TEST_PROJECTS_DIR / ".prefect"), ignore_errors=True)

    # missing_ok=True is only available in Python 3.8+
    files = [
        TEST_PROJECTS_DIR / ".prefectignore",
        TEST_PROJECTS_DIR / "prefect.yaml",
        TEST_PROJECTS_DIR / "deployment.yaml",
    ]
    for file in files:
        if file.exists():
            file.unlink()


class TestProjectRecipes:
    def test_project_recipe_ls(self):
        result = invoke_and_assert("project recipe ls")
        assert result.exit_code == 0

        lines = result.output.split()
        assert len(lines) > 3
        assert "local" in lines
        assert "docker" in lines
        assert "git" in lines


class TestProjectInit:
    def test_project_init(self):
        with TemporaryDirectory() as tempdir:
            result = invoke_and_assert(
                "project init --name test_project", temp_dir=str(tempdir)
            )
            assert result.exit_code == 0
            for file in ["prefect.yaml", "deployment.yaml", ".prefectignore"]:
                # temp_dir creates a *new* nested temporary directory within tempdir
                assert any(Path(tempdir).rglob(file))

    def test_project_init_with_recipe(self):
        with TemporaryDirectory() as tempdir:
            result = invoke_and_assert(
                "project init --name test_project --recipe local", temp_dir=str(tempdir)
            )
            assert result.exit_code == 0

    def test_project_init_with_unknown_recipe(self):
        result = invoke_and_assert(
            "project init --name test_project --recipe def-not-a-recipe",
            expected_code=1,
        )
        assert result.exit_code == 1
        assert "prefect project recipe ls" in result.output


class TestProjectDeploy:
    async def test_project_deploy(self, project_dir, orion_client):
        await orion_client.create_work_pool(WorkPoolCreate(name="test-pool"))
        result = await run_sync_in_worker_thread(
            invoke_and_assert,
            command="deploy ./flows/hello.py:my_flow -n test-name -p test-pool",
        )
        assert result.exit_code == 0
        assert "An important name/test" in result.output

        deployment = await orion_client.read_deployment_by_name(
            "An important name/test-name"
        )
        assert deployment.name == "test-name"
        assert deployment.work_pool_name == "test-pool"
