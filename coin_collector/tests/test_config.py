import pytest
import json
from coin_collector.config import load_level

def test_invalid_radius(tmp_path):
    # Erstellt eine temporäre JSON mit ungültigem Radius (r=1)
    bad_data = {
        "coins": [{"x": 10, "y": 10, "r": 1}],
        "walls": []
    }
    p = tmp_path / "bad.json"
    p.write_text(json.dumps(bad_data))
    
    with pytest.raises(Exception):
        load_level(str(p))