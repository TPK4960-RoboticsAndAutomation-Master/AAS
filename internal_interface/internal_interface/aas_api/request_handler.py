import sys
sys.path.insert(0, "..")
import logging
import asyncio

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async
from opcua import ua, Server, uamethod
from .models import Robot


class RequestMiddleware:
    def __init__(self, get_response):
        self.main()
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
        
        try:
            print(response.data['command'])

            command_splt = response.data['command'].split(":")

            if command_splt[0] == "lbr":
                self.lbrEvgen.event.Message = ua.LocalizedText(command_splt[1])
                self.lbrEvgen.trigger()
                print("LBREvent sent!")
            elif command_splt[0] == "kmp":
                self.kmpEvgen.event.Message = ua.LocalizedText(command_splt[1])
                self.kmpEvgen.trigger()
                print("KMPEvent sent!")

        except (KeyError, AttributeError) as e:
            pass

        return response

    @uamethod
    def update_status(self, parent, msg):
        loop = asyncio.get_running_loop()
        loop.create_task(self.update_database(msg))
        loop.create_task(self.send_async(str("updated")))

    async def update_database(self, msg):
        rid, component, component_status = msg.split(':')
        obj, created = await sync_to_async(Robot.objects.update_or_create)(
            robot_id=rid,
            defaults={component: component_status}
        )

    async def send_async(self, msg):
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            'status_update',
            {
                'type': 'send_to_aas',
                'message': msg
            }
        )     

    def main(self):
        logging.basicConfig(level=logging.WARN)
        logger = logging.getLogger("opcua.server.internal_subscription")
        #logger.setLevel(logging.DEBUG)

        # setup our server with IP of the computer running the internal_interface
        server = Server()
        server.set_endpoint("opc.tcp://10.22.25.161:4840/freeopcua/server/")

        # setup our own namespace, not really necessary but should as spec
        uri = "OPCUA_AAS_COMMUNICATION_SERVER"
        idx = server.register_namespace(uri)

        # get Objects node, this is where we should put our custom stuff
        objects = server.get_objects_node()

        # populating our address space
        myobj = objects.add_object(idx, "MyObject")
        status_node = myobj.add_method(idx, "update_status", self.update_status, [ua.VariantType.String], [ua.VariantType.Int64])
        print(status_node)
        
        lbrEvent = server.create_custom_event_type(idx, 'LBREvent')
        kmpEvent = server.create_custom_event_type(idx, 'KMPEvent')

        self.lbrEvgen = server.get_event_generator(lbrEvent, myobj)
        self.kmpEvgen = server.get_event_generator(kmpEvent, myobj)

        # starting!
        server.start()