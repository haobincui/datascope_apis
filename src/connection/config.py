from src.connection.shared.settings import DataScopeSettings, get_settings

Config = DataScopeSettings


def get_config(f: str = 'application.ini') -> DataScopeSettings:
    """Return config.

    Args:
        f (str): Function to evaluate in the finite-difference formula.

    Returns:
        DataScopeSettings: Requested value for the lookup.
    """
    return get_settings(f)
