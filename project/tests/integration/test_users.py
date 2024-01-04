# import json

# import pytest

# TODO: tests for UUID incorrect value type, dealing with unique emails

# def test_create_user(test_app_with_db):
#     response = test_app_with_db.post(
#         "/api/users/", data=json.dumps({"email": "test@gmail.com"})
#     )

#     print(response.json())

#     assert response.status_code == 201
#     assert response.json()["email"] == "test@gmail.com"


# def test_create_user_invalid_json(test_app):
#     response = test_app.post("/api/users/", data=json.dumps({}))
#     assert response.status_code == 422
#     assert response.json() == {
#         "detail": [
#             {
#                 "loc": ["body", "email"],
#                 "msg": "field required",
#                 "type": "value_error.missing",
#             }
#         ]
#     }

#     response = test_app.post("/api/users/", data=json.dumps({"email": "invalidemail.com"}))
#     assert response.status_code == 422
#     assert response.json()["detail"][0]["msg"] == "value is not a email address"


# def test_get_user(test_app_with_db):
#     response = test_app_with_db.post(
#         "/api/users/", data=json.dumps({"email": "test1@gmail.com"})
#     )
#     print(response.json())
#     user_id = response.json()["id"]

#     response = test_app_with_db.get(f"/api/users/{user_id}/")
#     assert response.status_code == 200

#     response_dict = response.json()
#     assert response_dict["id"] == user_id
#     assert response_dict["email"] == "test1@gmail.com"
#     assert response_dict["credits"] == 0
#     assert response_dict["created_at"]


# def test_get_all_users(test_app_with_db):
#     response = test_app_with_db.post(
#         "/api/users/", data=json.dumps({"email": "test3@gmail.com"})
#     )
#     user_id = response.json()["id"]

#     response = test_app_with_db.get("/api/users/")
#     assert response.status_code == 200

#     response_list = response.json()
#     assert len(list(filter(lambda d: d["id"] == user_id, response_list))) == 1


# def test_remove_user(test_app_with_db):
#     response = test_app_with_db.post(
#         "/api/users/", data=json.dumps({"email": "test4@gmail.com"})
#     )
#     user_id = response.json()["id"]

#     response = test_app_with_db.delete(f"/api/users/{user_id}/")
#     assert response.status_code == 200
#     assert response.json() == {"id": user_id, "email": "test4@gmail.com"}


# def test_update_user(test_app_with_db):
#     response = test_app_with_db.post(
#         "/api/users/", data=json.dumps({"email": "test5@gmail.com"})
#     )
#     user_id = response.json()["id"]

#     response = test_app_with_db.put(
#         f"/api/users/{user_id}/",
#         data=json.dumps({"email": "test5@gmail.com", "credits": 4}),
#     )
#     assert response.status_code == 200

#     response_dict = response.json()
#     assert response_dict["id"] == user_id
#     assert response_dict["email"] == "test5@gmail.com"
#     assert response_dict["credits"] == 4
#     assert response_dict["created_at"]


# @pytest.mark.parametrize(
#     "user_id, payload, status_code, detail",
#     [
#         [
#             999,
#             {"email": "https://foo.bar", "description": "updated!"},
#             404,
#             "User not found",
#         ],
#         [
#             0,
#             {"email": "https://foo.bar", "description": "updated!"},
#             422,
#             [
#                 {
#                     "loc": ["path", "id"],
#                     "msg": "ensure this value is greater than 0",
#                     "type": "value_error.number.not_gt",
#                     "ctx": {"limit_value": 0},
#                 }
#             ],
#         ],
#         [
#             1,
#             {},
#             422,
#             [
#                 {
#                     "loc": ["body", "email"],
#                     "msg": "field required",
#                     "type": "value_error.missing",
#                 },
#                 {
#                     "loc": ["body", "description"],
#                     "msg": "field required",
#                     "type": "value_error.missing",
#                 },
#             ],
#         ],
#         [
#             1,
#             {"email": "https://foo.bar"},
#             422,
#             [
#                 {
#                     "loc": ["body", "description"],
#                     "msg": "field required",
#                     "type": "value_error.missing",
#                 }
#             ],
#         ],
#     ],
# )
# def test_update_user_invalid(test_app_with_db, user_id, payload, status_code, detail):
#     response = test_app_with_db.put(f"/api/users/{user_id}/", data=json.dumps(payload))
#     assert response.status_code == status_code
#     assert response.json()["detail"] == detail


# def test_update_user_invalid_email(test_app_with_db):
#     response = test_app_with_db.put(
#         "/api/users/1/",
#         data=json.dumps({"email": "invalid://email", "description": "updated!"}),
#     )
#     assert response.status_code == 422
#     assert response.json()["detail"][0]["msg"] == "email scheme not permitted"
