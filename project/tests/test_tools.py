import json

import pytest


def test_create_tool(test_app_with_db):
    response = test_app_with_db.post(
        "/tools/", data=json.dumps({"url": "https://foo.bar"})
    )

    assert response.status_code == 201
    assert response.json()["url"] == "https://foo.bar"


def test_create_tools_invalid_json(test_app):
    response = test_app.post("/tools/", data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "url"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }

    response = test_app.post("/tools/", data=json.dumps({"url": "invalid://url"}))
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "URL scheme not permitted"


def test_get_tool(test_app_with_db):
    response = test_app_with_db.post(
        "/tools/", data=json.dumps({"url": "https://foo.bar"})
    )
    tool_id = response.json()["id"]

    response = test_app_with_db.get(f"/tools/{tool_id}/")
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == tool_id
    assert response_dict["url"] == "https://foo.bar"
    assert response_dict["description"]
    assert response_dict["created_at"]


def test_get_tool_incorrect_id(test_app_with_db):
    response = test_app_with_db.get("/tools/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Tool not found"

    response = test_app_with_db.get("/tools/0/")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["path", "id"],
                "msg": "ensure this value is greater than 0",
                "type": "value_error.number.not_gt",
                "ctx": {"limit_value": 0},
            }
        ]
    }


def test_get_all_tools(test_app_with_db):
    response = test_app_with_db.post(
        "/tools/", data=json.dumps({"url": "https://foo.bar"})
    )
    tool_id = response.json()["id"]

    response = test_app_with_db.get("/tools/")
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda d: d["id"] == tool_id, response_list))) == 1


def test_remove_tool(test_app_with_db):
    response = test_app_with_db.post(
        "/tools/", data=json.dumps({"url": "https://foo.bar"})
    )
    tool_id = response.json()["id"]

    response = test_app_with_db.delete(f"/tools/{tool_id}/")
    assert response.status_code == 200
    assert response.json() == {"id": tool_id, "url": "https://foo.bar"}


def test_remove_tool_incorrect_id(test_app_with_db):
    response = test_app_with_db.delete("/tools/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Tool not found"

    response = test_app_with_db.delete("/tools/0/")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["path", "id"],
                "msg": "ensure this value is greater than 0",
                "type": "value_error.number.not_gt",
                "ctx": {"limit_value": 0},
            }
        ]
    }


def test_update_tool(test_app_with_db):
    response = test_app_with_db.post(
        "/tools/", data=json.dumps({"url": "https://foo.bar"})
    )
    tool_id = response.json()["id"]

    response = test_app_with_db.put(
        f"/tools/{tool_id}/",
        data=json.dumps({"url": "https://foo.bar", "description": "updated!"}),
    )
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == tool_id
    assert response_dict["url"] == "https://foo.bar"
    assert response_dict["description"] == "updated!"
    assert response_dict["created_at"]


@pytest.mark.parametrize(
    "tool_id, payload, status_code, detail",
    [
        [
            999,
            {"url": "https://foo.bar", "description": "updated!"},
            404,
            "Tool not found",
        ],
        [
            0,
            {"url": "https://foo.bar", "description": "updated!"},
            422,
            [
                {
                    "loc": ["path", "id"],
                    "msg": "ensure this value is greater than 0",
                    "type": "value_error.number.not_gt",
                    "ctx": {"limit_value": 0},
                }
            ],
        ],
        [
            1,
            {},
            422,
            [
                {
                    "loc": ["body", "url"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
                {
                    "loc": ["body", "description"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
            ],
        ],
        [
            1,
            {"url": "https://foo.bar"},
            422,
            [
                {
                    "loc": ["body", "description"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ],
        ],
    ],
)
def test_update_tool_invalid(test_app_with_db, tool_id, payload, status_code, detail):
    response = test_app_with_db.put(f"/tools/{tool_id}/", data=json.dumps(payload))
    assert response.status_code == status_code
    assert response.json()["detail"] == detail


def test_update_tool_invalid_url(test_app_with_db):
    response = test_app_with_db.put(
        "/tools/1/",
        data=json.dumps({"url": "invalid://url", "description": "updated!"}),
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "URL scheme not permitted"
