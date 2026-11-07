"""Importing the stage modules runs make_cfg(), which copies ~/.claude/.credentials.json
into SP_CFG. Point HOME and SP_CFG at a throwaway directory first, so a test run never
copies real credentials anywhere."""
import os
import tempfile

_sandbox = tempfile.mkdtemp(prefix="sp-tests-")
os.environ["HOME"] = _sandbox
os.environ["SP_CFG"] = os.path.join(_sandbox, "cfg")
