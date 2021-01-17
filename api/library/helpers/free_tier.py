"""Helper for managing the free tier."""

# from open_alchemy import package_database

# from .. import types


# def check_would_exceed(
#     *, user: types.TUser, spec_name: types.TSpecName,
# model_count: types.TSpecModelCount
# ) -> bool:
#     """
#     Check whether adding a spec would exceed the free tier limit.

#     Algorithm:
#         1. retrieve the information for the spec,
#         2. retrieve the model count for the user and
#         3. return whether the user model count plus the new model count minus the
#             existing model count would exceed the free tier.
#     """
#     user_model_count = package_database.get().count_customer_models(sub=user)
#     spec_info = package_database.get().get
