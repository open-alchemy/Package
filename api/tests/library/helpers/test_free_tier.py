"""Tests for the free tier helper."""

# import pytest
# from library import config
# from library.helpers import free_tier
# from open_alchemy import package_database

# CHECK_WOULD_EXCEED_TESTS = [
#     pytest.param([], "user 1", "name 1", 0, False, id="empty database no additional"),
#     pytest.param([], "user 1", "name 1", 1, False,
# id="empty database some additional"),
#     pytest.param(
#         [], "user 1", "name 1", 10, False, id="empty database equal additional"
#     ),
#     pytest.param(
#         [],
#         "user 1",
#         "name 1",
#         11,
#         True,
#         id="empty database more than additional",
#     ),
#     pytest.param(
#         [],
#         "user 1",
#         "name 1",
#         15,
#         True,
#         id="empty database much more than additional",
#     ),
#     pytest.param(
#         [{"sub": "user 1", "name": "name 1", "version": "version 1",
# "model_count": 0}],
#         "user 1",
#         "name 2",
#         0,
#         False,
#         id="single item no model database no additional",
#     ),
#     pytest.param(
#         [{"sub": "user 1", "name": "name 1",
# "version": "version 1", "model_count": 5}],
#         "user 1",
#         "name 2",
#         0,
#         False,
#         id="single item some model database no additional",
#     ),
#     pytest.param(
#         [
#             {
#                 "sub": "user 1",
#                 "name": "name 1",
#                 "version": "version 1",
#                 "model_count": 10,
#             }
#         ],
#         "user 1",
#         "name 2",
#         0,
#         False,
#         id="single item equal model database no additional",
#     ),
#     pytest.param(
#         [
#             {
#                 "sub": "user 1",
#                 "name": "name 1",
#                 "version": "version 1",
#                 "model_count": 11,
#             }
#         ],
#         "user 1",
#         "name 2",
#         0,
#         True,
#         id="single item more than model database no additional",
#     ),
#     pytest.param(
#         [
#             {
#                 "sub": "user 1",
#                 "name": "name 1",
#                 "version": "version 1",
#                 "model_count": 15,
#             }
#         ],
#         "user 1",
#         "name 2",
#         0,
#         True,
#         id="single item much more than model database no additional",
#     ),
#     pytest.param(
#         [
#             {
#                 "sub": "user 1",
#                 "name": "name 1",
#                 "version": "version 1",
#                 "model_count": 1,
#             }
#         ],
#         "user 1",
#         "name 2",
#         1,
#         False,
#         id="single less than model database less than additional total less",
#     ),
#     pytest.param(
#         [
#             {
#                 "sub": "user 1",
#                 "name": "name 1",
#                 "version": "version 1",
#                 "model_count": 5,
#             }
#         ],
#         "user 1",
#         "name 2",
#         5,
#         False,
#         id="single less than model database less than additional total equal",
#     ),
#     pytest.param(
#         [
#             {
#                 "sub": "user 1",
#                 "name": "name 1",
#                 "version": "version 1",
#                 "model_count": 5,
#             }
#         ],
#         "user 1",
#         "name 2",
#         6,
#         True,
#         id="single less than model database less than additional total more than",
#     ),
#     pytest.param(
#         [
#             {
#                 "sub": "user 1",
#                 "name": "name 1",
#                 "version": "version 1",
#                 "model_count": 5,
#             }
#         ],
#         "user 1",
#         "name 1",
#         6,
#         False,
#         id=(
#             "single less than model database less than additional same model "
#             "total more than"
#         ),
#     ),
#     pytest.param(
#         [
#             {
#                 "sub": "user 1",
#                 "name": "name 1",
#                 "version": "version 1",
#                 "model_count": 5,
#             }
#         ],
#         "user 2",
#         "name 2",
#         6,
#         False,
#         id=(
#             "single less than model database less than additional different user "
#             "total more than"
#         ),
#     ),
# ]


# @pytest.mark.parametrize(
#     "initial_items, user, spec_name, model_count, expected_result",
#     CHECK_WOULD_EXCEED_TESTS,
# )
# @pytest.mark.helpers
# def test_check_would_exceed(
#     initial_items, user, spec_name, model_count, expected_result, _clean_specs_table
# ):
#     """
#     GIVE database with initial items, a user, the name of a spec and a model count
#     WHEN check_would_exceed is called with the user, spec name and model count
#     THEN the expected result is returned.
#     """
#     config.get().free_tier_model_count = 10
#     for item in initial_items:
#         package_database.get().create_update_spec(**item)

#     returned_result = free_tier.check_would_exceed(
#         user=user, spec_name=spec_name, model_count=model_count
#     )

#     assert returned_result == expected_result
