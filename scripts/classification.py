"""Classification policy for registered synthetic TS-001 comments."""
KNOWN_SYNTHETIC_COMMENT_IDS = frozenset({6623176386})
EXPECTED_TEST_AUTHOR = "jasonlagee-creator"

def classify_comment(comment):
    if (comment.get("id") in KNOWN_SYNTHETIC_COMMENT_IDS
            and (comment.get("user") or {}).get("login") == EXPECTED_TEST_AUTHOR):
        return "synthetic_test"
    return "unverified_submission"
