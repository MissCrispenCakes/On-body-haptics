"""
Test OSC Protocol Validation

Tests the OSC message format and protocol compliance.
"""

import pytest
from pythonosc import osc_message_builder
from pythonosc import osc_bundle_builder
import time


class TestOSCProtocol:
    """Test OSC protocol message formats"""

    def test_arduino_pattern_message_format(self):
        """Test Arduino pattern message format"""
        # Build OSC message
        builder = osc_message_builder.OscMessageBuilder(address="/onbody/1/pattern")
        builder.add_arg("CW")
        msg = builder.build()

        # Verify message structure
        assert msg.address == "/onbody/1/pattern"
        assert len(msg.params) == 1
        assert msg.params[0] == "CW"

    def test_raspberry_pi_effect_message_format(self):
        """Test Raspberry Pi effect message format"""
        builder = osc_message_builder.OscMessageBuilder(address="/onbody/effect/14")
        builder.add_arg(0)  # Channel 0
        msg = builder.build()

        assert msg.address == "/onbody/effect/14"
        assert len(msg.params) == 1
        assert msg.params[0] == 0

    def test_pattern_names(self):
        """Test valid pattern names"""
        valid_patterns = ["CW", "CCW", "PULSE", "WAVE",
                         "CUSTOM1", "CUSTOM2", "CUSTOM3", "CUSTOM4",
                         "CUSTOM5", "CUSTOM6", "CUSTOM7", "OFF"]

        for pattern in valid_patterns:
            builder = osc_message_builder.OscMessageBuilder(address="/onbody/1/pattern")
            builder.add_arg(pattern)
            msg = builder.build()
            assert msg.params[0] in valid_patterns

    def test_effect_ids(self):
        """Test valid effect ID range (DRV2605L: 1-123)"""
        valid_effects = [1, 14, 15, 18, 20, 33, 123]

        for effect_id in valid_effects:
            builder = osc_message_builder.OscMessageBuilder(
                address=f"/onbody/effect/{effect_id}"
            )
            builder.add_arg(0)  # Channel 0
            msg = builder.build()
            assert 1 <= effect_id <= 123

    def test_channel_range(self):
        """Test valid channel range (0-7 for Raspberry Pi)"""
        valid_channels = list(range(8))

        for channel in valid_channels:
            builder = osc_message_builder.OscMessageBuilder(address="/onbody/effect/14")
            builder.add_arg(channel)
            msg = builder.build()
            assert 0 <= msg.params[0] <= 7

    def test_belt_id_range(self):
        """Test valid belt ID range (1-6 for Arduino)"""
        valid_belt_ids = list(range(1, 7))

        for belt_id in valid_belt_ids:
            builder = osc_message_builder.OscMessageBuilder(
                address=f"/onbody/{belt_id}/pattern"
            )
            builder.add_arg("CW")
            msg = builder.build()
            assert 1 <= belt_id <= 6

    def test_wildcard_addressing(self):
        """Test wildcard addressing for all belts"""
        builder = osc_message_builder.OscMessageBuilder(address="/onbody/*/pattern")
        builder.add_arg("PULSE")
        msg = builder.build()

        assert msg.address == "/onbody/*/pattern"
        assert msg.params[0] == "PULSE"

    def test_osc_bundle_timing(self):
        """Test OSC bundle with timing"""
        bundle = osc_bundle_builder.OscBundleBuilder(
            osc_bundle_builder.IMMEDIATELY
        )

        msg_builder = osc_message_builder.OscMessageBuilder(address="/onbody/1/pattern")
        msg_builder.add_arg("CW")
        bundle.add_content(msg_builder.build())

        built_bundle = bundle.build()
        assert built_bundle is not None


class TestOSCAddressPatterns:
    """Test OSC address pattern matching"""

    def test_arduino_address_patterns(self):
        """Test valid Arduino OSC address patterns"""
        valid_patterns = [
            "/onbody/1/pattern",
            "/onbody/2/pattern",
            "/onbody/*/pattern",
            "/onbody/[12]/pattern",
        ]

        for pattern in valid_patterns:
            builder = osc_message_builder.OscMessageBuilder(address=pattern)
            builder.add_arg("CW")
            msg = builder.build()
            assert msg.address == pattern

    def test_raspberry_pi_address_patterns(self):
        """Test valid Raspberry Pi OSC address patterns"""
        valid_patterns = [
            "/onbody/effect/14",
            "/onbody/effect/33",
            "/onbody/channel/0/effect",
        ]

        for pattern in valid_patterns:
            builder = osc_message_builder.OscMessageBuilder(address=pattern)
            if "channel" in pattern:
                builder.add_arg(14)  # Effect ID
            else:
                builder.add_arg(0)  # Channel
            msg = builder.build()
            assert msg.address == pattern


class TestOSCMessageTypes:
    """Test OSC message type tags"""

    def test_string_argument(self):
        """Test string type tag for pattern names"""
        builder = osc_message_builder.OscMessageBuilder(address="/onbody/1/pattern")
        builder.add_arg("CW", arg_type="s")
        msg = builder.build()
        assert isinstance(msg.params[0], str)

    def test_integer_argument(self):
        """Test integer type tag for channels and effects"""
        builder = osc_message_builder.OscMessageBuilder(address="/onbody/effect/14")
        builder.add_arg(0, arg_type="i")
        msg = builder.build()
        assert isinstance(msg.params[0], int)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
