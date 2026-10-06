"""GUIDE Phần 1 - Định nghĩa subagent (tác tử con).   >>> SINH VIÊN CÀI ĐẶT <<<

Pseudo-code: guides/pseudocode/02_subagents.md
Kiểm tra:    pytest tests/test_02_agent.py
"""


def get_subagents() -> list[dict]:
    """Trả về danh sách subagent (ít nhất 2, tên khác nhau).

    Mỗi phần tử là một dict có các khóa bắt buộc:
      "name":          tên duy nhất (chữ thường, có thể có dấu gạch ngang)
      "description":   khi nào tác tử chính nên giao việc cho subagent này (viết như một hướng dẫn hành động)
      "system_prompt": chỉ dẫn cho subagent
    Gợi ý vai trò: explorer (đọc và báo cáo), implementer (thực hiện), reviewer (kiểm tra độc lập).
    """
    return [
        {
            "name": "explorer",
            "description": (
                "Use when you need to inspect project structure, read README, specifications, "
                "docstrings, sample data, or logs before making changes. Reports factual observations "
                "without modifying any files."
            ),
            "system_prompt": (
                "You are an exploratory subagent. Your role is to explore the workspace, inspect files, "
                "read documentation, docstrings, logs, or dataset samples, and report precise factual "
                "observations back to the coordinator. Do NOT modify or create any files."
            ),
        },
        {
            "name": "implementer",
            "description": (
                "Use when you need to execute multi-step changes, write or edit code/files, "
                "run scripts or tests via shell, and report execution results."
            ),
            "system_prompt": (
                "You are an implementation subagent. Your role is to carry out requested code or data "
                "modifications, run validation commands or tests using the shell, and report the detailed "
                "results back to the coordinator."
            ),
        },
        {
            "name": "reviewer",
            "description": (
                "Use when you need an independent audit of the current solution against instructions, "
                "edge cases, formatting rules, and test requirements before finalizing."
            ),
            "system_prompt": (
                "You are a review subagent. Your role is to independently verify that all requirements, "
                "formatting conventions, edge cases, and regression tests are satisfied. Report any gaps "
                "or failures back to the coordinator. Do NOT modify any files."
            ),
        },
    ]
