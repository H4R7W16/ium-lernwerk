import argparse
import json
import os
import tempfile
from pathlib import Path

try:
    from .ium11_publication import (
        IUM11PublicationError,
        PUBLICATION_PATHS,
        compile_publication_contract,
        render_publication_contract_json,
        render_publication_markdown_block,
        replace_publication_block,
    )
    from .validate_ium10 import validate_ium10_repository
    from .validate_ium11 import validate_pilot_protocol
except ImportError:
    from ium11_publication import (
        IUM11PublicationError,
        PUBLICATION_PATHS,
        compile_publication_contract,
        render_publication_contract_json,
        render_publication_markdown_block,
        replace_publication_block,
    )
    from validate_ium10 import validate_ium10_repository
    from validate_ium11 import validate_pilot_protocol


CONTRACT_PATH = "pilot/docs/publication-contract.json"


def _load_json(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def compile_repository_publication_contract(root):
    root = Path(root)
    time_model = _load_json(root / "roadmap/time-model.json")
    protocol = validate_pilot_protocol(
        _load_json(root / "pilot/pilot-protocol.json"), time_model,
    )
    return compile_publication_contract(
        protocol,
        time_model,
        validate_ium10_repository(root),
    )


def expected_publication_outputs(root):
    root = Path(root).resolve()
    contract = compile_repository_publication_contract(root)
    block = render_publication_markdown_block(contract)
    outputs = {root / CONTRACT_PATH: render_publication_contract_json(contract)}
    for relative_path in PUBLICATION_PATHS:
        target = root / relative_path
        source = target.read_text(encoding="utf-8")
        outputs[target] = replace_publication_block(source, block).encode("utf-8")
    return outputs


def _write_replace_atomic(path, payload):
    descriptor, temporary_path = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent,
    )
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
    finally:
        if os.path.exists(temporary_path):
            os.remove(temporary_path)


def build_publication_contract(root, check=False):
    outputs = expected_publication_outputs(root)
    if check:
        drifted = [
            path for path, payload in outputs.items()
            if not path.exists() or path.read_bytes() != payload
        ]
        if drifted:
            raise IUM11PublicationError(
                "publication output drift: "
                + ", ".join(str(path) for path in drifted)
            )
        return outputs
    for path, payload in outputs.items():
        _write_replace_atomic(path, payload)
    return outputs


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Build the deterministic IUM11 publication contract.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root containing the IUM11 publication inputs.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify generated publication outputs without writing files.",
    )
    arguments = parser.parse_args(argv)
    try:
        build_publication_contract(arguments.root, check=arguments.check)
    except (IUM11PublicationError, OSError, json.JSONDecodeError) as error:
        print(f"IUM11 publication build failed: {error}", file=__import__("sys").stderr)
        return 1
    print("IUM11 publication contract is current" if arguments.check else "IUM11 publication contract built")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
