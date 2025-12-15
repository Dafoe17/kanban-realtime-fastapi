from tests.data.cards import CARD_PREFIX


async def test_create_checklist(test_checklist):
    assert test_checklist["title"].startswith(f"checklist_title_for_{CARD_PREFIX}")


async def test_create_checklist_item(test_checklist_item):
    assert test_checklist_item["task"].startswith(f"checklist_task_for_{CARD_PREFIX}")
