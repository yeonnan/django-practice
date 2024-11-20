from channels.generic.websocket import JsonWebsocketConsumer


class RolePlayingRoomConsumer(JsonWebsocketConsumer):
    
    def receive_json(self, content, **kwargs):
        print('received : ', content)
        self.send_json(content)