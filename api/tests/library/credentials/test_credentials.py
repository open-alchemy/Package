# """Tests for credentials."""

# import json

# from open_alchemy import package_database
# from open_alchemy import package_security

# from library import credentials


# def test_get_credentials_not_exist():
#     """
#     GIVEN empty database
#     WHEN get is called
#     THEN credentials are created in the database and returned.
#     """
#     user = "user 1"

#     response = credentials.get(user)

#     stored_credentials = package_database.get().get_credentials(
# sub=user, id_="default")
#     assert stored_credentials is not None

#     assert response.status_code == 200
#     assert response.mimetype == "application/json"
#     returned_credentials = json.loads(response.data.decode())

#     assert "public_key" in returned_credentials
#     assert returned_credentials["public_key"] == stored_credentials["public_key"]
#     assert "secret_key" in returned_credentials


# def test_get_credentials_exist():
#     """
#     GIVEN database with credentials
#     WHEN get is called
#     THEN the credentials are returned.
#     """
#     user = "user 1"
#     credentials = package_security.create(sub=user)
#     package_database.get().create_update_credentials(
#         sub=user,
#         id_="default",
#         public_key=credentials.public_key,
#         secret_key_hash=credentials.secret_key_hash,
#         salt=credentials.salt,
#     )

#     response = credentials.get(user)

#     assert response.status_code == 200
#     assert response.mimetype == "application/json"
#     returned_credentials = json.loads(response.data.decode())

#     assert "public_key" in returned_credentials
#     assert returned_credentials["public_key"] == credentials.public_key
#     assert "secret_key" in returned_credentials
#     assert returned_credentials["secret_key"] == credentials.secret_key
