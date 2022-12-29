import json
# channels
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

# local
# serializers
from chat.api.serializers import (
    CommunityChatRoomMessageSerializer as MessageSerializer,
)
# model
from chat.models import (
    CommunityChatRoomMessage as Message,
    CommunityChatRoomMember as Member,
    CommunityChatRoom as Room,
)


def is_authenticated(scope):
    return scope['user'].is_authenticated


class ChatConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def save_message(self, data):
        room = Room.objects.get(slug=data['room'])
        serializer = MessageSerializer(data={
            'chat_room': room.id,
            'owner': self.scope['user'].id,
            'message': data['message']
        })

        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

        return serializer.data

    @database_sync_to_async
    def get_room_messages(self, room_slug):
        room = Room.objects.get(slug=room_slug)
        messages = Message.objects.filter(room=room)
        serializer = MessageSerializer(messages, many=True)
        return serializer.data

    @database_sync_to_async
    def mark_user_online(self, room_slug):
        room = Room.objects.get(slug=room_slug)
        member = Member.objects.get(member=self.scope['user'], chat_room=room)
        member.is_online = True
        member.save()

    @database_sync_to_async
    def mark_user_offline(self, room_slug):
        room = Room.objects.get(slug=room_slug)
        member = Member.objects.get(member=self.scope['user'], chat_room=room)
        member.is_online = False
        member.save()

    @database_sync_to_async
    def mark_user_typing(self, room_slug):
        room = Room.objects.get(slug=room_slug)
        member = Member.objects.get(member=self.scope['user'], chat_room=room)
        member.is_typing = True
        member.save()

    @database_sync_to_async
    def mark_user_not_typing(self, room_slug):
        room = Room.objects.get(slug=room_slug)
        member = Member.objects.get(member=self.scope['user'], chat_room=room)
        member.is_typing = False
        member.save()

    @database_sync_to_async
    def get_room_details(self, room_slug):
        room = Room.objects.get(slug=room_slug)
        members = Member.objects.filter(chat_room=room)
        return room, members

    async def connect(self):
        if not is_authenticated(self.scope):
            await self.close()
            return

        self.room_slug = self.scope['url_route']['kwargs']['room_slug']

        room, members = await self.get_room_details(self.room_slug)

        chat_room = f'chat_{room.slug}'

        self.channel_name = chat_room

        # Join room group
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )

        await self.accept()

        await self.mark_user_online(self.room_slug)

    async def disconnect(self, close_code):
        chat_room = f'chat_{self.room_slug}'

        await self.channel_layer.group_discard(
            chat_room,
            self.channel_name
        )

        await self.mark_user_offline(self.room_slug)

    async def chat_message(self, event):

        if event['user'] == self.scope['user']:
            return

        await self.send(text_data=json.dumps({
            'type': 'user_typing',
            'user': event['user']
        }))

    async def receive(self, text_data):
        await self.mark_user_not_typing(self.room_slug)

        text_data_json = json.loads(text_data)

        message = text_data_json['message']

        # get room orm object
        room, members = await self.get_room_details(self.room_slug)

        response = await self.save_message({
            'room': room.slug,
            'message': message
        })

        self.send(text_data=json.dumps({
            'message': response['message'],
            'room': room.slug,
        }))

        # Send message to room group
        await self.channel_layer.group_send(
            self.channel_name,
            {
                'type': 'chat_message',
                'message': response['message']
            }
        )
