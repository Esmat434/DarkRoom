from django.shortcuts import redirect
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import CustomUser,Users,ChatData,PersonalToken,GroupData,UserGroup,GroupToken
from asgiref.sync import sync_to_async,async_to_sync
class ChatApp(AsyncWebsocketConsumer):
    async def connect(self):
        self.client_id = self.scope['url_route']['kwargs']['id']
        self.username = self.scope['url_route']['kwargs']['username']
        data = await sync_to_async(list)(Users.objects.filter(username=self.username))
        try:
            self.group_b = await sync_to_async(PersonalToken.objects.get)(receiver=self.username)
        except PersonalToken.DoesNotExist:
            self.group_b = None
        self.group = f"chat_{self.client_id}"
        await self.accept()

        await self.channel_layer.group_add(
            self.group,
            self.channel_name
        )

        for u in data:
            user_data = {'username':u.uuid_name,'user_id':u.uuid_id}
            await self.channel_layer.group_send(
                self.group,
                {
                    'type':'client_chat',
                    'message':user_data
                }
            )
    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group,
            self.channel_name
        )
    
    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            text_data_json = json.loads(text_data)    
            action = text_data_json['action']
            if action == 'message':
                message = text_data_json['message']
                user = await sync_to_async(CustomUser.objects.get)(uuid=message)
                try:
                    old_data = await sync_to_async(Users.objects.get)(uuid_name=user.username)
                except:
                    old_data=None

                if user and old_data is None:
                    await sync_to_async(Users.objects.create)(
                        username=self.username,
                        uuid_name = user.username,
                        uuid_id = user.id,
                        uuid = user.uuid
                    )
                    username = user.username
                    user_id = user.id
                    user_data = {'username':username,'user_id':user_id}
                    await self.channel_layer.group_send(
                        self.group,
                        {
                            'type':'client_chat',
                            'message':user_data
                        }
                    )
            elif action == 'delete':
                if self.group_b:
                    await sync_to_async(self.group_b.delete)()
                delete_id = text_data_json['delete']
                user_dlete = await sync_to_async(Users.objects.get)(uuid_id=delete_id)
                await sync_to_async(user_dlete.delete)()

    async def client_chat(self,event):
        message = event['message']
        await self.send(text_data=json.dumps({'message':message}))
        
class ChatSender(AsyncWebsocketConsumer):
    async def connect(self):
        self.username1 = self.scope['url_route']['kwargs']['username1']
        self.username2 = self.scope['url_route']['kwargs']['username2']
        data = await sync_to_async(list)(ChatData.objects.filter(sender=self.username1,receiver=self.username2,hidden=False))
        her_data = await sync_to_async(list)(ChatData.objects.filter(sender=self.username2,receiver=self.username1,hidden=False))
        try:
            uuid_a = await sync_to_async(PersonalToken.objects.get)(sender=self.username1,receiver=self.username2)
        except PersonalToken.DoesNotExist:
            uuid_a=None
        try:
            uuid_b = await sync_to_async(PersonalToken.objects.get)(sender=self.username2,receiver=self.username1)
        except PersonalToken.DoesNotExist:
            uuid_b=None
        if uuid_a:
            self.group_name = f'chat_{uuid_a.Token}'
        elif uuid_b:
            self.group_name = f'chat_{uuid_b.Token}'


        await self.accept()

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        for d in data:
            n = f'{d.created_time}'
            await self.send(text_data=json.dumps({'kind':'mine','message':d.message,'time':n}))
        
        for i in her_data:
            m = f"{i.created_time}"
            await self.send(text_data=json.dumps({'kind':'your','message':i.message,'time':m}))
    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
    
    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            text_data_json = json.loads(text_data)
            action = text_data_json['action']
            if action == 'message':
                message = text_data_json['message']
                await sync_to_async(ChatData.objects.create)(
                    sender=self.username1,
                    receiver = self.username2,
                    message = message
                )
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        'type':'message_send',
                        'message':message
                    }
                )

            elif action == 'delete':
                delete_message = text_data_json['message']
                sender_message = text_data_json['sender']
                receiver_message = text_data_json['receiver']
                message_time = text_data_json['date_time']
                try:
                    delete_data = await sync_to_async(ChatData.objects.get)(sender=sender_message,receiver=receiver_message,message=delete_message,created_time=message_time)
                except ChatData.DoesNotExist:
                    delete_data=None
                try:
                    delete_data2 = await sync_to_async(ChatData.objects.get)(sender=receiver_message,receiver=sender_message,message=delete_message,created_time=message_time)
                except ChatData.DoesNotExist:
                    delete_data2=None
                if delete_data:
                    await sync_to_async(delete_data.delete)()
                elif delete_data2:
                    await sync_to_async(delete_data2.delete)()
    async def message_send(self,event):
        message = event['message']
        await self.send(text_data=json.dumps({'kind':'your','message':message}))

class ChatGroup(AsyncWebsocketConsumer):
    async def connect(self):
        self.username = self.scope['url_route']['kwargs']['username']
        self.chat_name = self.scope['url_route']['kwargs']['groupname']
        self.group_id = f"chat_{self.chat_name}"
        await self.accept()

        await self.channel_layer.group_add(
            self.group_id,
            self.channel_name
        )

        try:
            data = await sync_to_async(list)(GroupData.objects.filter(is_enable=True))
        except:
            data=None
        
        for d in data:
            time = f'{d.created_time}'
            await self.send(text_data=json.dumps({'action':'message','message':d.message,'time':time,'name':d.username}))


    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_id,
            self.channel_name
        )
    
    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            text_data_json = json.loads(text_data)
            action = text_data_json['action']
            if action == 'message':
                message = text_data_json['message']
                await sync_to_async(GroupData.objects.create)(
                    username=self.username,
                    message=message
                )
                await self.channel_layer.group_send(
                    self.group_id,
                    {
                        'type':'group_message',
                        'message':message
                    }
                )
            elif action == 'block':
                try:
                    block_user_token = await sync_to_async(list)(UserGroup.objects.filter(groupname=self.chat_name))
                except UserGroup.DoesNotExist:
                    block_user_token = None

                try:
                    block_group_token = await sync_to_async(GroupToken.objects.get)(admin=self.username,groupname=self.chat_name)
                except GroupToken.DoesNotExist:
                    block_group_token = None
                
                try:
                    block_group_data = await sync_to_async(list)(GroupData.objects.filter(username=self.username))
                except GroupData.DoesNotExist:
                    block_group_data = None
                
                try:
                    admin_name = await sync_to_async(GroupToken.objects.get)(admin=self.username)
                except GroupToken.DoesNotExist:
                    admin_name = None
                
                if admin_name is not None:
                    try:
                        block_group_data = await sync_to_async(list)(GroupData.objects.filter(is_enable=True))
                    except GroupData.DoesNotExist:
                        block_group_data = None

                try:
                    block_user_data = await sync_to_async(list)(GroupData.objects.filter(username=self.username))
                except GroupData.DoesNotExist:
                    block_user_data = None
                
                if block_group_data is not None:
                    for group_data in block_group_data:
                        await sync_to_async(group_data.delete)()
                
                if block_user_data is not None:
                    for user_data in block_user_data:
                        await sync_to_async(user_data.delete)()

                if block_user_token is not None:
                    for block_user in block_user_token:
                        await sync_to_async(block_user.delete)()
                
                if block_group_token is not None:
                    await sync_to_async(block_group_token.delete)()
            elif action == 'clear':
                try:
                    name_admin = await sync_to_async(GroupToken.objects.get)(admin=self.username)
                except GroupToken.DoesNotExist:
                    name_admin = None
                
                if name_admin is not None:  
                    # کل کوئری را به `sync_to_async` می‌دهیم
                    del_g_message = await sync_to_async(lambda: list(GroupData.objects.filter(is_enable=True)))()
                    
                    for del_g in del_g_message:
                        await sync_to_async(del_g.delete)()

                # کل کوئری را به `sync_to_async` می‌دهیم
                del_u_message = await sync_to_async(lambda: list(GroupData.objects.filter(username=self.username)))()
                for del_u in del_u_message:
                    await sync_to_async(del_u.delete)()
            elif action == 'delete':
                del_time = text_data_json['time']
                del_message = text_data_json['message']
                
                try:
                    delete_data = await sync_to_async(GroupData.objects.get)(message=del_message,created_time=del_time)
                except GroupData.DoesNotExist:
                    delete_data=None
                
                if delete_data is not None:
                    await sync_to_async(delete_data.delete)()

    async def group_message(self,event):
        message = event['message']
        await self.send(text_data=json.dumps({'message':message}))
