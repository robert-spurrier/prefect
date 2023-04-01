import json
import os
import shutil
from pathlib import Path

import pytest
import yaml

import prefect
from prefect.projects.base import (
    configure_project_by_recipe,
    find_prefect_directory,
    initialize_project,
    register_flow,
)

TEST_PROJECTS_DIR = prefect.__root_path__ / "tests" / "test-projects"


@pytest.fixture(autouse=True)
def project_dir():
    original_dir = os.getcwd()
    os.chdir(TEST_PROJECTS_DIR)
    (TEST_PROJECTS_DIR / ".prefect").mkdir(exist_ok=True)
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


class TestFindProject:
    async def test_find_project_works_in_root(self, tmp_path):
        # make hidden .prefect/ directory in tmp_path
        (tmp_path / ".prefect").mkdir()
        assert find_prefect_directory(tmp_path) == tmp_path / ".prefect"

    async def test_find_project_works_in_subdir(self, tmp_path):
        # make hidden .prefect/ directory in tmp_path
        (tmp_path / ".prefect").mkdir()
        (tmp_path / "subdir" / "subsubdir").mkdir(parents=True)
        assert (
            find_prefect_directory(tmp_path / "subdir" / "subsubdir")
            == tmp_path / ".prefect"
        )


class TestRecipes:
    async def test_configure_project_by_recipe_raises(self):
        with pytest.raises(ValueError, match="Unknown recipe"):
            configure_project_by_recipe("not-a-recipe")

    @pytest.mark.parametrize(
        "recipe",
        [
            d.absolute().name
            for d in Path(
                prefect.__root_path__ / "src" / "prefect" / "projects" / "recipes"
            ).iterdir()
            if d.is_dir()
        ],
    )
    async def test_configure_project_by_recipe_doesnt_raise(self, recipe):
        recipe_config = configure_project_by_recipe(recipe)
        for key in ["name", "prefect-version", "build", "push", "pull"]:
            assert key in recipe_config

    @pytest.mark.parametrize(
        "recipe",
        [
            d.absolute().name
            for d in Path(
                prefect.__root_path__ / "src" / "prefect" / "projects" / "recipes"
            ).iterdir()
            if d.is_dir() and "git" in d.absolute().name
        ],
    )
    async def test_configure_project_handles_templates_on_git_recipes(self, recipe):
        recipe_config = configure_project_by_recipe(
            recipe, repository="test-org/test-repo"
        )
        clone_step = recipe_config["pull"][0][
            "prefect.projects.steps.git_clone_project"
        ]
        assert clone_step["repository"] == "test-org/test-repo"
        assert clone_step["branch"] == "{{ branch }}"

    async def test_configure_project_replaces_templates_on_docker(self):
        recipe_config = configure_project_by_recipe("docker", name="test-dir")
        clone_step = recipe_config["pull"][0][
            "prefect.projects.steps.set_working_directory"
        ]
        assert clone_step["directory"] == "/opt/prefect/test-dir"


class TestInitProject:
    async def test_initialize_project_works(self, tmp_path):
        files = initialize_project()
        assert len(files) == 3

        for file in files:
            assert Path(file).exists()

        # test defaults
        with open("prefect.yaml", "r") as f:
            contents = yaml.safe_load(f)

        assert contents["name"] == "PrefectHQ/prefect"
        assert contents["prefect-version"] == prefect.__version__

    async def test_initialize_project_with_name(self, tmp_path):
        files = initialize_project(name="my-test-its-a-test")
        assert len(files) == 3

        with open("prefect.yaml", "r") as f:
            contents = yaml.safe_load(f)

        assert contents["name"] == "my-test-its-a-test"

    async def test_initialize_project_with_recipe(self, tmp_path):
        files = initialize_project(recipe="docker-git")
        assert len(files) == 3

        with open("prefect.yaml", "r") as f:
            contents = yaml.safe_load(f)

        assert "prefect.projects.steps.git_clone_project" in contents["pull"]


class TestRegisterFlow:
    async def test_register_flow_works_in_root(self):
        f = await register_flow(
            str(TEST_PROJECTS_DIR / "import-project" / "my_module" / "flow.py")
            + ":test_flow"
        )
        assert f.name == "test"

        with open(TEST_PROJECTS_DIR / ".prefect" / "flows.json", "r") as f:
            flows = json.load(f)

        assert flows["test"] == "import-project/my_module/flow.py:test_flow"

    async def test_register_flow_allows_identical_calls(self):
        f = await register_flow(
            str(TEST_PROJECTS_DIR / "import-project" / "my_module" / "flow.py")
            + ":test_flow"
        )
        assert f.name == "test"

        f = await register_flow(
            str(TEST_PROJECTS_DIR / "import-project" / "my_module" / "flow.py")
            + ":test_flow"
        )
        assert f.name == "test"

    async def test_register_flow_disallows_overwrites(self):
        f = await register_flow(
            str(TEST_PROJECTS_DIR / "import-project" / "my_module" / "flow.py")
            + ":test_flow"
        )
        assert f.name == "test"

        with pytest.raises(ValueError, match="Conflicting entry found"):
            await register_flow(
                str(TEST_PROJECTS_DIR / "import-project" / "my_module" / "flow.py")
                + ":prod_flow"
            )

        f = await register_flow(
            str(TEST_PROJECTS_DIR / "import-project" / "my_module" / "flow.py")
            + ":prod_flow",
            force=True,
        )
        assert f.name == "test"
