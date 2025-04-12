# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'chat_room'  # Static room name
        self.room_group_name = f'chat_{self.room_name}'

        # Join the chat room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group when disconnected
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = self.scope['user'].username  # Get the current user's username

        # Broadcast the message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username  # Send username along with the message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']  # Get the username from the event

        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username  # Include username in the sent data
        }))
