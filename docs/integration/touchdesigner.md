# TouchDesigner Integration

How to integrate On-Body Haptics with TouchDesigner for interactive installations.

## Coming Soon

This integration guide is under development.

## Quick Example

TouchDesigner can send OSC messages using the OSC Out CHOP:

1. Add OSC Out CHOP
2. Set Network Address to haptic server IP
3. Set Network Port to 3333
4. Send messages like `/haptic/motor/0 1.0 500`

See [OSC Protocol](../api/osc-protocol.md) for complete message format documentation.

## Resources

- TouchDesigner OSC documentation: https://docs.derivative.ca/OSC_Out_CHOP
- [OSC Protocol Specification](../api/osc-protocol.md)

## Contributing

Have a TouchDesigner integration example? Share it! See [CONTRIBUTING.md](../../CONTRIBUTING.md).
