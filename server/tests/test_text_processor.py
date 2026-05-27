from server.app.services.text_processor import (
    count_syllables, split_sentences, split_into_chunks,
    compute_flesh_index, compute_keyword_density, detect_section_type
)

def test_count_syllables():
    assert count_syllables("привет") == 2
    assert count_syllables("я") == 1
    assert count_syllables("") == 1

def test_split_sentences():
    text = "Предложение один. Предложение два! И три?"
    assert len(split_sentences(text)) == 3

def test_split_into_chunks():
    text = "Это короткое предложение. А это чуть подлиннее предложение для теста."
    chunks = split_into_chunks(text, min_len=10)
    assert len(chunks) > 0
    assert "hash" in chunks[0]

def test_compute_flesh_index():
    text = "Мама мыла раму. Рама была чистой."
    score = compute_flesh_index(text)
    assert 0 <= score <= 100

def test_compute_keyword_density_empty():
    assert compute_keyword_density("") == 0

def test_compute_keyword_density():
    text = "тест тест тест тест слово слово"
    density = compute_keyword_density(text)
    assert density > 0

def test_detect_section_type():
    assert detect_section_type("Введение") == "введение"
    assert detect_section_type("Заключение") == "заключение"
    assert detect_section_type("Список литературы") == "список литературы"
    assert detect_section_type("Неизвестный заголовок") == "Неизвестный заголовок"
