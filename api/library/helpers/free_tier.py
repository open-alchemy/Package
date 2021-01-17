"""Helper for managing the free tier."""

import typing

from open_alchemy import package_database

from .. import config, types


def check_within_limit(
    *, user: types.TUser, spec_name: types.TSpecName, model_count: types.TSpecModelCount
) -> types.TResult:
    """
    Check whether adding a spec would exceed the free tier limit.

    Algorithm:
        1. retrieve the information for the spec,
        2. retrieve the model count for the user and
        3. return whether the user model count plus the new model count minus the
            existing model count would exceed the free tier.

    Args:
        user: The user to run the check for
        spec_name: The name of the spec
        model_count: The new model count of the spec

    Returns:
        The result and the reason if the result is true.

    """
    current_spec_model_count = 0
    try:
        spec_info = package_database.get().get_spec(sub=user, name=spec_name)
        current_spec_model_count = spec_info["model_count"]
    except package_database.exceptions.BaseError:
        pass
    user_model_count = package_database.get().count_customer_models(sub=user)

    new_user_model_count = user_model_count + model_count - current_spec_model_count

    result = new_user_model_count <= config.get().free_tier_model_count
    reason: typing.Optional[str] = None
    if not result:
        reason = (
            "with this spec the maximum number of "
            f"{config.get().free_tier_model_count} models for the free "
            f"tier would be exceeded, current models count: {user_model_count}, "
            f"current models in the spec: {current_spec_model_count}, "
            f"models in the new version of th spec: {model_count}, "
            f"new total model count: {new_user_model_count}, "
        )

    return types.TResult(value=result, reason=reason)
