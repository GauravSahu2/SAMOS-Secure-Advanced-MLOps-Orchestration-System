import pytest

def test_openapi_schema_stable():
    """Regression: API contract must not break between versions."""
    from src.sre.serve import app
    schema = app.openapi()
    
    # Core endpoints must exist
    assert "/predict" in schema["paths"], "/predict endpoint missing from contract"
    assert "/health" in schema["paths"], "/health endpoint missing from contract"
    assert "/feedback" in schema["paths"], "/feedback endpoint missing from contract"
    
    # Required schemas must be defined
    assert "Query" in schema["components"]["schemas"], "Query schema missing"
    assert "Feedback" in schema["components"]["schemas"], "Feedback schema missing"
    
    # Predict must require the Query schema in body
    predict_post = schema["paths"]["/predict"]["post"]
    assert "requestBody" in predict_post, "/predict must accept a request body"
