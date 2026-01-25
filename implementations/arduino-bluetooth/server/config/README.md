# Configuration

## Quick Start

1. Copy the example configuration:
   ```bash
   cp example.json local.json
   ```

2. Edit `local.json` with your Bluetooth device MAC addresses
3. **Never commit `local.json`** (it's in .gitignore)

## Finding Bluetooth MAC Addresses

### Linux

```bash
# Scan for Bluetooth devices
bluetoothctl
> scan on
# Wait for devices to appear
> devices
# Look for HC-05 or HC-06 devices
# MAC address format: 00:11:22:33:44:55
```

### Windows

```bash
# PowerShell
Get-PnpDevice -Class Bluetooth

# Or use Bluetooth settings in Control Panel
```

### macOS

```bash
# System Preferences > Bluetooth
# Option-click Bluetooth icon in menu bar for advanced info
```

## Configuration Files

- `default.json` - Template with all options (do not modify)
- `example.json` - Example configuration with sample values
- `local.json` - **Your configuration** (create this, not tracked by git)
- `production.json` - Production configuration (not tracked by git)

## Configuration Options

### Bluetooth

```json
{
  "bluetooth": {
    "enabled": true,           // Enable/disable Bluetooth
    "devices": [               // Array of Bluetooth devices
      {
        "id": 1,              // Belt ID (used in OSC addressing)
        "mac": "AA:BB:CC:DD:EE:FF",  // Bluetooth MAC address
        "name": "HC-05-Belt-1",      // Friendly name
        "autoReconnect": true        // Auto-reconnect on disconnect
      }
    ],
    "scanTimeout": 10000,     // Scan timeout in milliseconds
    "connectionRetries": 3    // Number of connection attempts
  }
}
```

### OSC

```json
{
  "osc": {
    "receivePort": 9999,      // Port to receive OSC messages
    "sendPort": 3333,         // Port to send OSC messages
    "address": "0.0.0.0"      // Bind address (0.0.0.0 = all interfaces)
  }
}
```

### WebSocket

```json
{
  "websocket": {
    "enabled": true,          // Enable/disable WebSocket server
    "port": 8080,            // WebSocket port
    "address": "0.0.0.0"     // Bind address
  }
}
```

### Serial

```json
{
  "serial": {
    "baudRate": 57600,        // Must match Arduino firmware
    "dataBits": 8,
    "parity": "none",
    "stopBits": 1
  }
}
```

### Logging

```json
{
  "logging": {
    "level": "info",          // debug, info, warn, error
    "console": true,          // Log to console
    "file": false,           // Log to file
    "filepath": "./logs/haptics.log"
  }
}
```

## Environment Variables

You can override configuration with environment variables:

```bash
# Override OSC receive port
export OSC_RECEIVE_PORT=9998

# Override WebSocket port
export WEBSOCKET_PORT=8081

# Run server
npm start
```

## Multiple Configurations

### Development

```bash
cp example.json local.json
# Edit local.json for development
npm start
```

### Production

```bash
cp example.json production.json
# Edit production.json for production settings
NODE_ENV=production npm start
```

## Security Notes

- **Never commit files with real MAC addresses or credentials**
- `local.json` and `production.json` are in `.gitignore`
- Use environment variables for sensitive data in production
- Consider using a secrets manager for production deployments

## Troubleshooting

### Configuration not loading

```bash
# Check JSON syntax
node -c config/local.json

# Or use jq
jq . config/local.json
```

### Bluetooth MAC address format

- Must be colon-separated: `00:11:22:33:44:55`
- Case insensitive
- 6 pairs of hexadecimal digits

### Port conflicts

If ports are already in use:

```bash
# Check what's using port 9999
lsof -i :9999

# Or on Windows
netstat -ano | findstr :9999
```

Change ports in configuration if needed.
