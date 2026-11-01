import json
from datetime import datetime
from pathlib import Path

from app.schemas.api import FeedbackRecord

from app.utils.logger import get_logger

logger = get_logger()


class FeedbackService:

    def __init__(self):

        self.file_path = Path("data/feedback.json")

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not self.file_path.exists():

            self.file_path.write_text(
                "[]",
                encoding="utf-8",
            )

    # --------------------------------------------------

    def save_feedback(
        self,
        record: FeedbackRecord,
    ):

        with open(
            self.file_path,
            "r",
            encoding="utf-8",
        ) as f:

            data = json.load(f)

        data.append(
            record.model_dump(
                mode="json"
            )
        )

        with open(
            self.file_path,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
            )

        logger.success(
            "Feedback saved."
        )

        return {
            "success": True,
            "message": "Feedback recorded successfully.",
        }

    # --------------------------------------------------

    def get_feedback(self):

        with open(
            self.file_path,
            "r",
            encoding="utf-8",
        ) as f:

            return json.load(f)


feedback_service = FeedbackService()