from sql.schemas import Player


def test_player_schema():
    data = {
        "id": 1,
        "user_id": 1,
        "game_id": 2,
        "description": "tests that i build"
    }
    player = Player(**data)
    assert player.description == data["description"]
