from downConnection.DatabaseConnector import DatabaseConnector
from functions.Event import Event, Meta, Content
import hashlib  # Comes with python
import secrets  # Comes with python
from nacl.signing import SigningKey
from testfixtures import LogCapture
import os
from database.EventHandler import EventHandler



def test_get_current_event():
    try:
        with LogCapture() as l:
            private_key = secrets.token_bytes(32)
            signing_key = SigningKey(private_key)
            public_key_feed_id = signing_key.verify_key.encode()

            content = Content('whateverapp/whateveraction', {'somekey': 'somevalue', 'someotherkey': 1})
            hash_of_content = hashlib.sha256(content.get_as_cbor()).hexdigest()
            hash_of_prev = None
            meta = Meta(public_key_feed_id, 0, hash_of_prev, 'ed25519', ('sha256', hash_of_content))
            signature = signing_key.sign(meta.get_as_cbor())._signature
            event = Event(meta, signature, content).get_as_cbor()

            connector = DatabaseConnector()
            connector.add_event(event)
            result = connector.get_current_event(public_key_feed_id)
            print(public_key_feed_id)
            result = Event.from_cbor(result)
        assert result.meta.hash_of_content[1] == meta.hash_of_content[1]
        print(l)
    finally:
        try:
            if os.path.exists('cborDatabase.sqlite'):
                os.remove('cborDatabase.sqlite')
            else:
                assert False
        except PermissionError:
            print('Database is still in use')


def test_get_current_seq_no():
    try:
        with LogCapture() as l:
            private_key = secrets.token_bytes(32)
            signing_key = SigningKey(private_key)
            public_key_feed_id = signing_key.verify_key.encode()

            content = Content('whateverapp/whateveraction', {'somekey': 'somevalue', 'someotherkey': 2})
            hash_of_content = hashlib.sha256(content.get_as_cbor()).hexdigest()
            hash_of_prev = None
            meta = Meta(public_key_feed_id, 0, hash_of_prev, 'ed25519', ('sha256', hash_of_content))
            signature = signing_key.sign(meta.get_as_cbor())._signature
            event = Event(meta, signature, content).get_as_cbor()

            connector = DatabaseConnector()
            connector.add_event(event)
            meta = Meta(public_key_feed_id, 1, hash_of_prev, 'ed25519', ('sha256', hash_of_content))
            signature = signing_key.sign(meta.get_as_cbor())._signature
            event = Event(meta, signature, content).get_as_cbor()
            connector.add_event(event)
            meta = Meta(public_key_feed_id, 2, hash_of_prev, 'ed25519', ('sha256', hash_of_content))
            signature = signing_key.sign(meta.get_as_cbor())._signature
            event = Event(meta, signature, content).get_as_cbor()
            connector.add_event(event)
            res = connector.get_current_seq_no(public_key_feed_id)
        assert res == 2
        print(l)
    finally:
        try:
            if os.path.exists('cborDatabase.sqlite'):
                os.remove('cborDatabase.sqlite')
            else:
                assert False
        except PermissionError:
            print('Database is still in use')


def test_get_event():
    try:
        with LogCapture() as l:
            private_key = secrets.token_bytes(32)
            signing_key = SigningKey(private_key)
            public_key_feed_id = signing_key.verify_key.encode()

            content0 = Content('whateverapp/whateveraction', {'firstkey': 'somevalue', 'someotherkey': 3})
            hash_of_content = hashlib.sha256(content0.get_as_cbor()).hexdigest()
            hash_of_prev = None
            meta = Meta(public_key_feed_id, 0, hash_of_prev, 'ed25519', ('sha256', hash_of_content))
            signature = signing_key.sign(meta.get_as_cbor())._signature
            event = Event(meta, signature, content0).get_as_cbor()

            connector = DatabaseConnector()
            connector.add_event(event)
            meta = Meta(public_key_feed_id, 1, hash_of_prev, 'ed25519', ('sha256', hash_of_content))
            content1 = Content('whateverapp/whateveraction', {'secondkey': 'somevalue', 'someotherkey': 4})
            signature = signing_key.sign(meta.get_as_cbor())._signature
            event = Event(meta, signature, content1).get_as_cbor()
            connector.add_event(event)
            content2 = Content('whateverapp/whateveraction', {'thirdkey': 'somevalue', 'someotherkey': 5})
            meta = Meta(public_key_feed_id, 2, hash_of_prev, 'ed25519', ('sha256', hash_of_content))
            signature = signing_key.sign(meta.get_as_cbor())._signature
            event = Event(meta, signature, content2).get_as_cbor()
            connector.add_event(event)
            res0 = connector.get_event(public_key_feed_id, 0)
            res1 = connector.get_event(public_key_feed_id, 1)
            res2 = connector.get_event(public_key_feed_id, 2)
            result0 = Event.from_cbor(res0)
            result1 = Event.from_cbor(res1)
            result2 = Event.from_cbor(res2)
        assert result0.content.content == content0.content
        assert result1.content.content == content1.content
        assert result2.content.content == content2.content
        print(l)
    finally:
        try:
            if os.path.exists('cborDatabase.sqlite'):
                os.remove('cborDatabase.sqlite')
            else:
                assert False
        except PermissionError:
            print('Database is still in use')


def test_get_chat_event():
    try:
        with LogCapture() as l:
            private_key = secrets.token_bytes(32)
            signing_key = SigningKey(private_key)
            public_key_feed_id = signing_key.verify_key.encode()

            content0 = Content('chat/whateveraction',
                               {'messagekey': 'hallo zusammen', 'chat_id': '1', 'timestampkey': 10})
            hash_of_content = hashlib.sha256(content0.get_as_cbor()).hexdigest()
            hash_of_prev = None
            meta = Meta(public_key_feed_id, 0, hash_of_prev, 'ed25519', ('sha256', hash_of_content))
            signature = signing_key.sign(meta.get_as_cbor())._signature
            event = Event(meta, signature, content0).get_as_cbor()

            connector = EventHandler()
            connector.add_event(event)
            meta = Meta(public_key_feed_id, 1, hash_of_prev, 'ed25519', ('sha256', hash_of_content))
            content1 = Content('chat/whateveraction',
                               {'messagekey': 'wie gehts?', 'chat_id': '1', 'timestampkey': 20})
            signature = signing_key.sign(meta.get_as_cbor())._signature
            event = Event(meta, signature, content1).get_as_cbor()
            connector.add_event(event)
            content2 = Content('chat/whateveraction',
                               {'messagekey': 'schönes Wetter heute', 'chat_id': '1', 'timestampkey': 30})
            meta = Meta(public_key_feed_id, 2, hash_of_prev, 'ed25519', ('sha256', hash_of_content))
            signature = signing_key.sign(meta.get_as_cbor())._signature
            event = Event(meta, signature, content2).get_as_cbor()
            connector.add_event(event)

        print('\n#######################################')

        s = connector.get_all_events('chat', public_key_feed_id, '1')
        print(s)
        print('\n#######################################')

        p = connector.get_event_since(application='chat', timestamp=21, feed_id=public_key_feed_id, chat_id='1')
        print(p)
        print(l)
    finally:
        try:
            if os.path.exists('eventDatabase.sqlite'):
                os.remove('eventDatabase.sqlite')
            else:
                assert False
        except PermissionError:
            print('Database is still in use')


def test_get_kotlin_event():
    try:
        with LogCapture() as l:
            private_key = secrets.token_bytes(32)
            signing_key = SigningKey(private_key)
            public_key_feed_id = signing_key.verify_key.encode()
            content0 = Content('KotlinUI/whateveraction',
                               {'text': 'Hi Alice, nice to hear from you', 'username': 'Bob', 'publickey': '11',
                                'timestamp': 11})
            hash_of_content = hashlib.sha256(content0.get_as_cbor()).hexdigest()
            hash_of_prev = None
            meta = Meta(public_key_feed_id, 0, hash_of_prev, 'ed25519', ('sha256', hash_of_content))
            signature = signing_key.sign(meta.get_as_cbor())._signature
            event = Event(meta, signature, content0).get_as_cbor()

            connector = EventHandler()
            connector.add_event(event)
            meta = Meta(public_key_feed_id, 1, hash_of_prev, 'ed25519', ('sha256', hash_of_content))
            content1 = Content('KotlinUI/whateveraction',
                               {'text': 'Hi Bob', 'username': 'Alice', 'publickey': '111', 'timestamp': 15})
            signature = signing_key.sign(meta.get_as_cbor())._signature
            event = Event(meta, signature, content1).get_as_cbor()
            connector.add_event(event)
            content2 = Content('KotlinUI/whateveraction',
                               {'text': 'Hello everyone', 'username': 'Max', 'publickey': '1111',
                                'timestamp': 17})
            meta = Meta(public_key_feed_id, 2, hash_of_prev, 'ed25519', ('sha256', hash_of_content))
            signature = signing_key.sign(meta.get_as_cbor())._signature
            event = Event(meta, signature, content2).get_as_cbor()
            connector.add_event(event)

            s = connector.get_all_kotlin_events(public_key_feed_id)
            print(s)
            p = connector.get_Kotlin_usernames()
            print(p)
            q = connector.get_all_entries_by_publickey('111')
            print(q)
            m = connector.get_last_kotlin_event()
            print(m)

        print(l)
    finally:
        try:
            if os.path.exists('eventDatabase.sqlite'):
                os.remove('eventDatabase.sqlite')
            else:
                assert False
        except PermissionError:
            print('Database is still in use')

def test_get_all_feed_ids():
    try:
        with LogCapture() as l:
            private_key = secrets.token_bytes(32)
            signing_key = SigningKey(private_key)
            public_key_feed_id = signing_key.verify_key.encode()

            content = Content('whateverapp/whateveraction', {'somekey': 'somevalue', 'someotherkey': 1})
            hash_of_content = hashlib.sha256(content.get_as_cbor()).hexdigest()
            hash_of_prev = None
            meta = Meta(public_key_feed_id, 0, hash_of_prev, 'ed25519', ('sha256', hash_of_content))
            signature = signing_key.sign(meta.get_as_cbor())._signature
            event = Event(meta, signature, content).get_as_cbor()

            connector = DatabaseConnector()
            connector.add_event(event)
            result = connector.get_all_feed_ids()
        print(result)
        assert True
    finally:
        try:
            if os.path.exists('cborDatabase.sqlite'):
                os.remove('cborDatabase.sqlite')
            else:
                assert False
        except PermissionError:
            print('Database is still in use')