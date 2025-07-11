import json
from channels.generic.websocket import AsyncWebsocketConsumer
from celery.result import AsyncResult
from async_mysql_project.tasks import generate_excel  # Задача Celery

class ExportConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "some_path"
        self.room_group_name = f"export_{self.room_name}"

        # Присоединяемся к группе
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Подтверждаем подключение (это должно происходить после того, как подключение установлено)
        await self.accept()

    async def disconnect(self, close_code):
        # Отключаемся от группы
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        if data.get("action") == "export_excel":
            sid = self.channel_name  # Идентификатор соединения
            data = [data.get("contract_date"), data.get("end_date")]

            # Запуск задачи Celery
            task = generate_excel.apply_async(args=[sid, data])

            # print('POPAL', task.id)
            # exit()

            # Отправляем task_id клиенту
            await self.send(text_data=json.dumps({
                "type": "export_started",
                "task_id": task.id
            }))

        elif data.get("action") == "check_task_status":
            task_id = data.get("task_id")
            task_result = AsyncResult(task_id)

            # Проверка статуса задачи
            if task_result.state == "PENDING":
                await self.send(text_data=json.dumps({
                    "type": "task_status_pending",
                    "status": 'pending'
                }))
            elif task_result.state == "SUCCESS":
                file_url, filename = task_result.result
                await self.send(text_data=json.dumps({
                    "type": "export_success",
                    "file_url": file_url,
                    "filename": filename
                }))
            elif task_result.state == "FAILURE":
                await self.send(text_data=json.dumps({
                    "type": "task_status_failure",
                    "status": "failure",
                    "error": str(task_result.info)
                }))