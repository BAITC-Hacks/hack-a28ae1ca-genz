"""Tests for the request classifier."""

import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from classifier import classify, classify_with_llm, validate_category
from responder import generate_response, generate_response_with_llm, validate_response
from llm_client import parse_json_response
from memory import load_memory, save_memory, append_record
from main import process_message, load_messages


# === Required test cases from AGENTS.md ===

class TestRequiredMessages:
    """Test the 5 required messages with deterministic expected categories."""

    def test_message_1_spravka(self):
        msg = "Как получить справку о месте учёбы?"
        cat, conf = classify(msg)
        assert cat == "справка"
        assert 0.0 <= conf <= 1.0

    def test_message_2_zhaloba(self):
        msg = "В столовой очередь, еда холодная."
        cat, conf = classify(msg)
        assert cat == "жалоба"
        assert 0.0 <= conf <= 1.0

    def test_message_3_other(self):
        msg = "Хочу записаться на консультацию завтра."
        cat, conf = classify(msg)
        assert cat == "другое"
        assert 0.0 <= conf <= 1.0

    def test_message_4_zhaloba(self):
        msg = "Пропал Wi-Fi в корпусе B."
        cat, conf = classify(msg)
        assert cat == "жалоба"
        assert 0.0 <= conf <= 1.0

    def test_message_5_spravka(self):
        msg = "Где парковка для гостей?"
        cat, conf = classify(msg)
        assert cat == "справка"
        assert 0.0 <= conf <= 1.0


# === Fallback and safety tests ===

class TestFallback:
    """Test fallback behavior for edge cases."""

    def test_irrelevant_input_fallback(self):
        msg = "asdfghjkl random words"
        cat, conf = classify(msg)
        assert cat == "другое"

    def test_empty_input_safe(self):
        result = process_message("")
        assert result["category"] == "другое"
        assert result["valid"] is False

    def test_none_like_input_safe(self):
        result = process_message("   ")
        assert result["category"] == "другое"
        assert result["valid"] is False

    def test_invalid_llm_output_fallback(self):
        """Simulate invalid output by testing validate_category."""
        assert not validate_category("invalid_category")
        assert not validate_category("")
        assert not validate_category(None)  # type: ignore[arg-type]

    def test_low_confidence_falls_back(self):
        """Messages with very weak matches should fall to другое."""
        msg = "abc def ghi"
        cat, conf = classify(msg)
        assert cat == "другое"


# === Validation tests ===

class TestValidation:
    """Test output validation rules."""

    def test_category_in_valid_set(self):
        for msg in ["Где выход?", "Проблема с светом", "Привет"]:
            cat, _ = classify(msg)
            assert validate_category(cat)

    def test_response_non_empty_russian(self):
        for cat in ["справка", "жалоба", "другое"]:
            resp = generate_response(cat, "test")
            assert resp
            assert validate_response(resp)

    def test_confidence_in_range(self):
        messages = ["Где парковка?", "Пропал интернет", "Хочу есть"]
        for msg in messages:
            _, conf = classify(msg)
            assert 0.0 <= conf <= 1.0

    def test_no_none_in_output(self):
        result = process_message("Где парковка?")
        assert result["category"] is not None
        assert result["response"] is not None
        assert result["confidence"] is not None


# === Memory tests ===

class TestMemory:
    """Test memory persistence."""

    def test_load_missing_file(self):
        records = load_memory("nonexistent_memory.json")
        assert records == []

    def test_save_and_load(self, tmp_path):
        filepath = str(tmp_path / "test_memory.json")
        records = [{"message": "test", "category": "справка"}]
        save_memory(records, filepath)
        loaded = load_memory(filepath)
        assert loaded == records

    def test_corrupted_file_recovery(self, tmp_path):
        filepath = str(tmp_path / "corrupted.json")
        with open(filepath, "w") as f:
            f.write("not valid json {{{")
        records = load_memory(filepath)
        assert records == []

    def test_append_record(self, tmp_path):
        filepath = str(tmp_path / "append_test.json")
        append_record("test msg", "справка", "test response", 0.8, filepath)
        records = load_memory(filepath)
        assert len(records) == 1
        assert records[0]["message"] == "test msg"
        assert records[0]["category"] == "справка"


# === Pipeline integration test ===

class TestPipeline:
    """Test the full pipeline integration."""

    def test_process_message_full(self):
        result = process_message("Где парковка для гостей?")
        assert result["category"] == "справка"
        assert result["valid"] is True
        assert validate_response(result["response"])

    def test_load_messages_from_file(self):
        messages = load_messages("messages.txt")
        assert len(messages) == 5

    def test_process_all_messages(self):
        messages = load_messages("messages.txt")
        results = [process_message(msg) for msg in messages]
        categories = [r["category"] for r in results]
        assert categories == ["справка", "жалоба", "другое", "жалоба", "справка"]
        assert all(r["valid"] for r in results)


# === LLM Client tests ===

class TestLLMClient:
    """Test LLM client utilities."""

    def test_parse_json_response_valid(self):
        text = '{"category": "справка", "confidence": 0.9}'
        result = parse_json_response(text)
        assert result == {"category": "справка", "confidence": 0.9}

    def test_parse_json_response_with_markdown(self):
        text = '```json\n{"category": "жалоба", "confidence": 0.8}\n```'
        result = parse_json_response(text)
        assert result == {"category": "жалоба", "confidence": 0.8}

    def test_parse_json_response_invalid(self):
        text = "not json at all"
        result = parse_json_response(text)
        assert result is None

    def test_parse_json_response_empty(self):
        result = parse_json_response("")
        assert result is None

    def test_parse_json_response_none(self):
        result = parse_json_response(None)
        assert result is None


# === LLM Classification tests ===

class TestLLMClassification:
    """Test LLM classification with mocked API calls."""

    @patch("classifier.call_llm")
    def test_classify_with_llm_valid_response(self, mock_call_llm):
        mock_call_llm.return_value = '{"category": "справка", "confidence": 0.95}'
        cat, conf = classify_with_llm("Где парковка?")
        assert cat == "справка"
        assert conf == 0.95

    @patch("classifier.call_llm")
    def test_classify_with_llm_invalid_category(self, mock_call_llm):
        mock_call_llm.return_value = '{"category": "invalid", "confidence": 0.9}'
        cat, conf = classify_with_llm("Где парковка?")
        assert cat == "справка"  # Falls back to rule-based
        assert 0.0 <= conf <= 1.0

    @patch("classifier.call_llm")
    def test_classify_with_llm_api_failure(self, mock_call_llm):
        mock_call_llm.return_value = None
        cat, conf = classify_with_llm("Где парковка?")
        assert cat == "справка"  # Falls back to rule-based
        assert 0.0 <= conf <= 1.0

    @patch("classifier.call_llm")
    def test_classify_with_llm_empty_input(self, mock_call_llm):
        cat, conf = classify_with_llm("")
        assert cat == "другое"
        assert conf == 0.0
        mock_call_llm.assert_not_called()

    @patch("classifier.call_llm")
    def test_classify_with_llm_json_parse_error(self, mock_call_llm):
        mock_call_llm.return_value = "not json"
        cat, conf = classify_with_llm("Где парковка?")
        assert cat == "справка"  # Falls back to rule-based


# === LLM Response Generation tests ===

class TestLLMResponseGeneration:
    """Test LLM response generation with mocked API calls."""

    @patch("responder.call_llm")
    def test_generate_response_with_llm_valid(self, mock_call_llm):
        mock_call_llm.return_value = "Обращение принято к рассмотрению."
        resp = generate_response_with_llm("жалоба", "Еда холодная")
        assert resp == "Обращение принято к рассмотрению."

    @patch("responder.call_llm")
    def test_generate_response_with_llm_empty_response(self, mock_call_llm):
        mock_call_llm.return_value = ""
        resp = generate_response_with_llm("справка", "Где парковка?")
        assert resp == "Для получения информации обратитесь в деканат или справочную службу."

    @patch("responder.call_llm")
    def test_generate_response_with_llm_non_russian(self, mock_call_llm):
        mock_call_llm.return_value = "Response in English"
        resp = generate_response_with_llm("справка", "Где парковка?")
        assert resp == "Для получения информации обратитесь в деканат или справочную службу."

    @patch("responder.call_llm")
    def test_generate_response_with_llm_api_failure(self, mock_call_llm):
        mock_call_llm.side_effect = ValueError("API key not set")
        resp = generate_response_with_llm("жалоба", "Проблема")
        assert resp == "Обращение подготовлено для передачи ответственному сотруднику."


# === Integration with mocked LLM ===

class TestLLMIntegration:
    """Test full pipeline with mocked LLM calls."""

    @patch("responder.call_llm")
    @patch("classifier.call_llm")
    def test_process_message_with_llm(self, mock_classify_llm, mock_respond_llm):
        mock_classify_llm.return_value = '{"category": "справка", "confidence": 0.9}'
        mock_respond_llm.return_value = "Информация доступна в деканате."
        result = process_message("Где парковка?", use_llm=True)
        assert result["category"] == "справка"
        assert result["valid"] is True

    @patch("responder.call_llm")
    @patch("classifier.call_llm")
    def test_process_message_llm_fallback(self, mock_classify_llm, mock_respond_llm):
        mock_classify_llm.return_value = None
        mock_respond_llm.return_value = None
        result = process_message("Где парковка?", use_llm=True)
        assert result["category"] == "справка"  # Falls back to rule-based
        assert result["valid"] is True
