from app.services.task_service import TaskService
from app.integrations.bitrix_client import BitrixClient
from app.config.config import settings


def get_task_service() -> TaskService:
    webhook_url = settings.bitrix_webhook
    if not webhook_url:
        raise ValueError("Bitrix webhook URL is not configured.")
    bitrix_client = BitrixClient(webhook_url=webhook_url)
    return TaskService(bitrix_client=bitrix_client)
