import asyncio
import pytest

from pubnub.models.consumer.presence import PNWhereNowResult
from pubnub.pubnub_asyncio import PubNubAsyncio
from tests.helper import pnconf_sub_copy, pnconf_pam_copy
from tests.integrational.vcr_asyncio_sleeper import get_sleeper, VCR599Listener
from tests.integrational.vcr_helper import pn_vcr


@get_sleeper('tests/integrational/fixtures/asyncio/where_now/single_channel.yaml')
@pn_vcr.use_cassette(
    'tests/integrational/fixtures/asyncio/where_now/single_channel.yaml',
    filter_query_parameters=['uuid', 'pnsdk'])
@pytest.mark.asyncio
async def test_single_channel(event_loop, sleeper=asyncio.sleep):
    pubnub = PubNubAsyncio(pnconf_sub_copy(), custom_event_loop=event_loop)
    ch = 'test-where-now-asyncio-ch'
    uuid = 'test-where-now-asyncio-uuid'
    pubnub.config.uuid = uuid

    callback = VCR599Listener(1)
    pubnub.add_listener(callback)
    pubnub.subscribe().channels(ch).execute()

    await callback.wait_for_connect()

    await sleeper(2)

    env = await pubnub.where_now() \
        .uuid(uuid) \
        .future()

    channels = env.result.channels

    assert len(channels) == 1
    assert channels[0] == ch

    pubnub.unsubscribe().channels(ch).execute()
    await callback.wait_for_disconnect()

    await pubnub.stop()


@get_sleeper('tests/integrational/fixtures/asyncio/where_now/multiple_channels.yaml')
@pn_vcr.use_cassette(
    'tests/integrational/fixtures/asyncio/where_now/multiple_channels.yaml',
    filter_query_parameters=['pnsdk'],
    match_on=['method', 'scheme', 'host', 'port', 'string_list_in_path', 'query'],
)
@pytest.mark.asyncio
async def test_multiple_channels(event_loop, sleeper=asyncio.sleep):
    pubnub = PubNubAsyncio(pnconf_sub_copy(), custom_event_loop=event_loop)

    ch1 = 'test-where-now-asyncio-ch1'
    ch2 = 'test-where-now-asyncio-ch2'
    uuid = 'test-where-now-asyncio-uuid'
    pubnub.config.uuid = uuid

    callback = VCR599Listener(1)
    pubnub.add_listener(callback)
    pubnub.subscribe().channels([ch1, ch2]).execute()

    await callback.wait_for_connect()

    await sleeper(7)

    env = await pubnub.where_now() \
        .uuid(uuid) \
        .future()

    channels = env.result.channels

    assert len(channels) == 2
    assert ch1 in channels
    assert ch2 in channels

    pubnub.unsubscribe().channels([ch1, ch2]).execute()
    await callback.wait_for_disconnect()

    await pubnub.stop()


# @pytest.mark.asyncio
@pytest.mark.skip(reason="Needs to be reworked to use VCR")
async def test_where_now_super_admin_call(event_loop):
    pubnub = PubNubAsyncio(pnconf_pam_copy(), custom_event_loop=event_loop)

    uuid = 'test-where-now-asyncio-uuid-.*|@'
    pubnub.config.uuid = uuid

    res = await pubnub.where_now() \
        .uuid(uuid) \
        .result()
    assert isinstance(res, PNWhereNowResult)

    await pubnub.stop()
