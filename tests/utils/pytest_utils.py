import inspect

import pytest


def pytest_collection_modifyitems(items):
    for item in items:
        if "model" in item.name:
            item.add_marker(pytest.mark.model)
        if "model_structure" in item.name:
            item.add_marker(pytest.mark.model_structure)
        if "unit" in item.name:
            item.add_marker(pytest.mark.unit)
        if "unit_schema" in item.name:
            item.add_marker(pytest.mark.unit_schema)
        if "integration" in item.name:
            item.add_marker(pytest.mark.integration)
        # Checking for async tests
        if inspect.iscoroutinefunction(item.obj):
            item.add_marker(pytest.mark.asyncio)
