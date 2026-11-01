"""
Input validation utilities.
"""

import re
from typing import Optional

def sanitize_search_query(q: Optional[str]) -> Optional[str]:
    """Sanitizes user search strings for safe SQL LIKE pattern matching."""
    if not q:
        return None
    # Strip whitespace and limit length
    cleaned = q.strip()[:100]
    # Escape SQL LIKE wildcards if needed
    cleaned = cleaned.replace("%", "\\%").replace("_", "\\_")
    return cleaned if cleaned else None

