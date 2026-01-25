# Max/MSP Integration

How to integrate On-Body Haptics with Max/MSP for audio-haptic installations.

## Coming Soon

This integration guide is under development.

## Quick Example

Max/MSP can send OSC messages directly to the haptic server:

```
udpsend 3333
/haptic/motor/0 1.0 500
```

See [OSC Protocol](../api/osc-protocol.md) for complete message format documentation.

## Resources

- Max/MSP OSC documentation: https://docs.cycling74.com/max8/refpages/osc
- [OSC Protocol Specification](../api/osc-protocol.md)

## Contributing

Have a Max/MSP integration example? Share it! See [CONTRIBUTING.md](../../CONTRIBUTING.md).
