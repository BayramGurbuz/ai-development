from main import append_user_message

def test_append_user_message_adds_correct_role_and_content():
    contents = [{"role": "model", "parts": [{"text": "Merhaba!"}]}]
    result = append_user_message(contents, "Selam")

    assert len(result) == 2
    assert result[-1] == {"role": "user", "parts": [{"text": "Selam"}]}

def test_append_user_message_does_not_mutate_original_list():
    contents = [{"role": "model", "parts": [{"text": "Merhaba!"}]}]
    append_user_message(contents, "Selam")

    assert len(contents) == 1  # orijinal liste değişmemiş olmalı