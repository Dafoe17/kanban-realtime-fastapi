from uuid import uuid4

from src.schemas import (
    CardCreate,
    ChecklistCreate,
    ChecklistItemCreate,
    CommentCreate,
    TagCreate,
)

from .prefixes import CARD_PREFIX


def generate_test_card(card_prefix=CARD_PREFIX):
    return CardCreate(
        title=f"{card_prefix}_{uuid4().hex[:6]}", description="description_for_card"
    )


def generate_test_comment(comment_prefix=CARD_PREFIX):
    return CommentCreate(text=f"comm_text_for_{comment_prefix}")


def generate_test_tag(tag_prefix=CARD_PREFIX):
    return TagCreate(
        title=f"tag_title_for_{tag_prefix}_{uuid4().hex[:6]}", color="#2424CCFF"
    )


def generate_test_checklist(ch_prefix=CARD_PREFIX):
    return ChecklistCreate(title=f"checklist_title_for_{ch_prefix}")


def generate_test_checklist_item(ch_item_prefix=CARD_PREFIX):
    return ChecklistItemCreate(task=f"checklist_task_for_{ch_item_prefix}")
