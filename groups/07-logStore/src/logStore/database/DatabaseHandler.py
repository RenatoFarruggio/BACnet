from .ByteArrayHandler import ByteArrayHandler
from .EventHandler import EventHandler
from functions.log import create_logger
from functions.Event import Event

logger = create_logger('DatabaseHandler')


class DatabaseHandler:

    def __init__(self):
        self.__byteArrayHandler = ByteArrayHandler()
        self.__eventHandler = EventHandler()

    # Mixed operations

    def add_to_db(self, event_as_cbor):
        self.__byteArrayHandler.insert_byte_array(event_as_cbor)
        self.__eventHandler.add_event(event_as_cbor)

    #  byte array operations:

    def get_current_seq_no(self, feed_id):
        return self.__byteArrayHandler.get_current_seq_no(feed_id)

    def get_event(self, feed_id, seq_no):
        return self.__byteArrayHandler.get_event(feed_id, seq_no)

    def get_current_event_as_cbor(self, feed_id):
        return self.__byteArrayHandler.get_current_event_as_cbor(feed_id)

    def get_all_feed_ids(self):
        return self.__byteArrayHandler.get_all_feed_ids()

    # Event operations:

    def get_event_since(self, application, timestamp, feed_id, chat_id):
        return self.__eventHandler.get_event_since(application, timestamp, feed_id, chat_id)

    def get_all_from_application(self, application, feed_Id, chat_id):
        return self.__eventHandler.get_all_events(application, feed_Id, chat_id)

    def get_usernames_and_publickey(self):
        return self.__eventHandler.get_Kotlin_usernames()

    def get_all_entries_by_publickey(self, publicKey):
        return self.__eventHandler.get_all_entries_by_publickey(publicKey)
