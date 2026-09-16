"""Validate an asset-sheet plan and compile one inspectable prompt per sheet."""
import argparse
import json
import re
from pathlib import Path


SAFE_ID = re.compile(r"^[A-Za-z0-9_-]+$")


def load_plan(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(plan: dict) -> None:
    if plan.get("schema_version") != 1:
        raise ValueError("schema_version must be 1")
    for key in ("reference", "style", "assets", "sheets"):
        if not plan.get(key):
            raise ValueError(f"Missing required field: {key}")

    assets = plan["assets"]
    asset_ids = [item.get("id") for item in assets]
    if any(not isinstance(aid, str) or not SAFE_ID.fullmatch(aid) for aid in asset_ids):
        raise ValueError("Asset IDs must use letters, digits, hyphens, or underscores")
    if len(set(asset_ids)) != len(asset_ids):
        raise ValueError("Duplicate asset IDs")
    if any(not isinstance(item.get("description"), str) or not item["description"].strip() for item in assets):
        raise ValueError("Every asset needs a non-empty description")

    defaults = plan.get("sheet_defaults", {})
    maximum = defaults.get("max_assets_per_sheet", 6)
    if not isinstance(maximum, int) or maximum < 1:
        raise ValueError("max_assets_per_sheet must be a positive integer")

    sheet_ids = []
    assigned = []
    known = set(asset_ids)
    for sheet in plan["sheets"]:
        sid = sheet.get("id")
        if not isinstance(sid, str) or not SAFE_ID.fullmatch(sid):
            raise ValueError("Sheet IDs must use letters, digits, hyphens, or underscores")
        sheet_ids.append(sid)
        cols, rows = sheet.get("columns"), sheet.get("rows")
        ids = sheet.get("asset_ids")
        if not isinstance(cols, int) or not isinstance(rows, int) or cols < 1 or rows < 1:
            raise ValueError(f"Invalid grid for sheet {sid}")
        if not isinstance(ids, list) or not ids:
            raise ValueError(f"Sheet {sid} has no assets")
        if len(ids) > cols * rows or len(ids) > maximum:
            raise ValueError(f"Sheet {sid} exceeds its grid or max-assets limit")
        unknown = [aid for aid in ids if aid not in known]
        if unknown:
            raise ValueError(f"Sheet {sid} uses unknown assets: {unknown}")
        for field in ("prompt_file", "output_file"):
            if not isinstance(sheet.get(field), str) or not sheet[field].strip():
                raise ValueError(f"Sheet {sid} needs {field}")
        assigned.extend(ids)

    if len(set(sheet_ids)) != len(sheet_ids):
        raise ValueError("Duplicate sheet IDs")
    duplicates = sorted(aid for aid in set(assigned) if assigned.count(aid) > 1)
    missing = sorted(known - set(assigned))
    if duplicates:
        raise ValueError(f"Assets assigned more than once: {duplicates}")
    if missing:
        raise ValueError(f"Assets not assigned to a sheet: {missing}")


def compile_prompt(plan: dict, sheet: dict) -> str:
    by_id = {item["id"]: item["description"].strip() for item in plan["assets"]}
    defaults = plan.get("sheet_defaults", {})
    margin = defaults.get("margin_percent", 12)
    background = defaults.get("background_instruction", "真实透明背景，不画棋盘格或白底")
    common = defaults.get("common_instruction", "每格一个完整视觉单元，元素互不接触，不画格线、编号或新增文字")
    items = "；".join(f"{index}. [{aid}] {by_id[aid]}" for index, aid in enumerate(sheet["asset_ids"], 1))
    return (
        f"参考输入整图的画风，重新画一张独立素材板，{sheet['columns']}列×{sheet['rows']}行。\n"
        f"从左到右、从上到下分别是：{items}。\n"
        f"共同画风：{plan['style'].strip()}。\n"
        f"每格保留约{margin}%空白。{common.strip()}。\n"
        f"背景要求：{background.strip()}。\n"
        "只画清单中的元素，不画参考图的整体背景或其他元素。"
    )


def compile_files(plan_path: Path) -> list[Path]:
    plan_path = plan_path.resolve()
    plan = load_plan(plan_path)
    validate(plan)
    created = []
    for sheet in plan["sheets"]:
        target = (plan_path.parent / sheet["prompt_file"]).resolve()
        try:
            target.relative_to(plan_path.parent)
        except ValueError as exc:
            raise ValueError(f"prompt_file escapes task directory: {sheet['prompt_file']}") from exc
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(compile_prompt(plan, sheet) + "\n", encoding="utf-8")
        created.append(target)
    return created


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path)
    args = parser.parse_args()
    created = compile_files(args.plan)
    print(json.dumps({"prompts": [str(path) for path in created]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
