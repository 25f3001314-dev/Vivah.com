import pytest

from v1.services import perform_ashtakoot_milan


@pytest.mark.parametrize(
    "boy,girl",
    [
        ("हरीओम", "कोमल"),
        ("विराट", "काव्या"),
        ("अर्जुन", "मीरा"),
        ("राम", "सीता"),
        ("राहुल", "राधा"),
    ],
)
def test_end_to_end_matchmaking(boy, girl):
    result = perform_ashtakoot_milan(boy, girl)
    assert "error" not in result
    assert 0.0 <= result["total_score"] <= 36.0
    assert result["boy_profile"]["source"] in {"jyotisha", "pyjhora", "barahadi"}
    assert result["girl_profile"]["source"] in {"jyotisha", "pyjhora", "barahadi"}
