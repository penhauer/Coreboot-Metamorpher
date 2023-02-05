import re
from patcher import SIGN_HEADER_PATTERN, SIGN_FOOTER_PATTERN


ANYTHING_WITH_NO_COMMENT = r"(?:[^\/]|\/[^*])*"

class PatchCleaner:

    def __init__(self) -> None:
        pass

    def wipe_existing_patches(self, code: str) -> str:
        p = rf"\n\s*{SIGN_HEADER_PATTERN}{ANYTHING_WITH_NO_COMMENT}{SIGN_FOOTER_PATTERN}\n"
        return re.sub(p, "", code, flags=re.MULTILINE + re.DOTALL)
