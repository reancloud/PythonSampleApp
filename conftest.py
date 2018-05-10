"""Configuration class file."""
import pytest


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Get report function."""
    outcome = yield
    report = outcome.get_result()
    if report.when == 'call':
        report.stage_metadata = {
            'severity': item.config.cache.get("sev_key", 'MAJOR'),
            'weight': item.config.cache.get("weight_key", 'weight'),
            'description': item.config.cache.get("desc_key", 'description'),
            'possibleSolutions': item.config.cache.get("soln_key",
                                                       'possibleSolutions'),
            'cis_number': item.config.cache.get("cis_number", 'cis_number')
        }
