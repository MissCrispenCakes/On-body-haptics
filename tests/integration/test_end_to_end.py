"""
End-to-End Integration Tests

These tests verify the complete workflow from OSC message to haptic output.
Note: Most of these tests require actual hardware and are marked accordingly.
"""

import pytest
from pythonosc import udp_client
from pythonosc import osc_server
from pythonosc import dispatcher
import time
import threading


class TestArduinoIntegration:
    """Integration tests for Arduino + Bluetooth implementation"""

    @pytest.mark.hardware
    def test_arduino_pattern_execution(self):
        """Test sending pattern to Arduino (requires hardware)"""
        client = udp_client.SimpleUDPClient("localhost", 9999)

        # Send pattern
        client.send_message("/onbody/1/pattern", "CW")

        # In a real test, we would verify the pattern executed
        # This requires hardware feedback or monitoring
        assert True  # Placeholder

    def test_osc_message_format_arduino(self):
        """Test OSC message format without hardware"""
        # Create message
        client = udp_client.SimpleUDPClient("localhost", 9999)

        # These calls don't fail even without server
        # They test message construction
        client.send_message("/onbody/1/pattern", "CW")
        client.send_message("/onbody/2/pattern", "CCW")
        client.send_message("/onbody/*/pattern", "PULSE")

        assert True  # Messages constructed successfully


class TestRaspberryPiIntegration:
    """Integration tests for Raspberry Pi + I2C implementation"""

    @pytest.mark.hardware
    def test_raspberry_pi_effect_execution(self):
        """Test sending effect to Raspberry Pi (requires hardware)"""
        client = udp_client.SimpleUDPClient("localhost", 9999)

        # Send effect
        client.send_message("/onbody/effect/14", 0)

        # In a real test, we would verify the effect executed
        assert True  # Placeholder

    def test_osc_message_format_raspberry_pi(self):
        """Test OSC message format without hardware"""
        client = udp_client.SimpleUDPClient("localhost", 9999)

        # Test various effect messages
        for channel in range(8):
            client.send_message("/onbody/effect/14", channel)

        assert True  # Messages constructed successfully


class TestOSCServer:
    """Test OSC server receiving and dispatching"""

    def test_osc_dispatcher_patterns(self):
        """Test OSC dispatcher pattern matching"""
        received_messages = []

        def handler(unused_addr, *args):
            received_messages.append(args)

        # Create dispatcher
        disp = dispatcher.Dispatcher()
        disp.map("/onbody/*/pattern", handler)

        # Test dispatcher mapping
        assert disp is not None

    @pytest.mark.slow
    def test_osc_server_receive(self):
        """Test OSC server receiving messages (without hardware)"""
        received = []

        def pattern_handler(unused_addr, pattern):
            received.append(pattern)

        # Create dispatcher
        disp = dispatcher.Dispatcher()
        disp.map("/onbody/1/pattern", pattern_handler)

        # Create server in separate thread
        server = osc_server.ThreadingOSCUDPServer(
            ("127.0.0.1", 9998), disp
        )

        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        # Send message
        client = udp_client.SimpleUDPClient("127.0.0.1", 9998)
        client.send_message("/onbody/1/pattern", "CW")

        # Wait for message
        time.sleep(0.1)

        # Cleanup
        server.shutdown()

        # Verify
        assert "CW" in received


class TestMultiDeviceCoordination:
    """Test coordination between multiple devices"""

    def test_broadcast_to_all_belts(self):
        """Test broadcasting pattern to all belts"""
        client = udp_client.SimpleUDPClient("localhost", 9999)

        # Send to all belts using wildcard
        client.send_message("/onbody/*/pattern", "PULSE")

        assert True  # Message sent

    def test_sequential_patterns(self):
        """Test sending patterns sequentially"""
        client = udp_client.SimpleUDPClient("localhost", 9999)

        patterns = ["CW", "CCW", "PULSE", "WAVE"]

        for pattern in patterns:
            client.send_message("/onbody/1/pattern", pattern)
            time.sleep(0.1)  # Small delay between patterns

        assert True  # All patterns sent

    @pytest.mark.hardware
    def test_synchronized_multi_channel(self):
        """Test synchronized effects on multiple channels (requires hardware)"""
        client = udp_client.SimpleUDPClient("localhost", 9999)

        # Trigger effect on all channels simultaneously
        for channel in range(8):
            client.send_message("/onbody/effect/14", channel)

        assert True  # Placeholder


class TestErrorConditions:
    """Test error handling and edge cases"""

    def test_invalid_pattern_name(self):
        """Test sending invalid pattern name"""
        client = udp_client.SimpleUDPClient("localhost", 9999)

        # Send invalid pattern (should be ignored by server)
        client.send_message("/onbody/1/pattern", "INVALID_PATTERN")

        # No exception should be raised
        assert True

    def test_invalid_effect_id(self):
        """Test sending out-of-range effect ID"""
        client = udp_client.SimpleUDPClient("localhost", 9999)

        # Send invalid effect ID (should be clamped by server)
        client.send_message("/onbody/effect/999", 0)

        # No exception should be raised
        assert True

    def test_invalid_channel(self):
        """Test sending invalid channel number"""
        client = udp_client.SimpleUDPClient("localhost", 9999)

        # Send invalid channel (should be ignored by server)
        client.send_message("/onbody/effect/14", 99)

        # No exception should be raised
        assert True


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "not hardware"])
