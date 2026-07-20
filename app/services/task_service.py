from pydantic import BaseModel, Field

from app.integrations.interface_bitrix_client import BitrixClientInterface


class FileDataResponse(BaseModel):
    name: str = Field(..., description="File name", alias="NAME")
    url: str = Field(..., description="File URL", alias="DOWNLOAD_URL")


class TaskService:
    def __init__(self, bitrix_client: BitrixClientInterface):
        self.bitrix_client: BitrixClientInterface = bitrix_client

    async def execute_task(self, file_id: int, smart_type_id: int, smart_id: int, task_type: str):
        response = await self.bitrix_client.call("disk.file.get", {"id": file_id})
        if "error" in response:
            print(f"Error fetching file data: {response.get('error')}")
            return {"error": response.get("error"), "message": response}

        file_data = FileDataResponse(**response.get("result", {}))
        
        file_content = await self.bitrix_client.upload_file(file_data.url)
        if not file_content:
            print("Error uploading file content.")
            return {"error": "FileUploadError", "message": "Failed to upload file content."}
        
        response = await self.bitrix_client.call("crm.item.update", {}, {
            "entityTypeId": smart_type_id,
            "id": smart_id,
            "fields": {
                "ufCrm9_1783613402": [
                    file_data.name,
                    file_content
                ]
            }
        })
        if 'error' in response:
            print(f"Error updating CRM item: {response.get('error')}")
            return {"error": response.get("error"), "message": response}
        
        return {'success': True}
