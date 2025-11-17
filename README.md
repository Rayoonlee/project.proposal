# PySecureNet Analyzer

A comprehensive network security analysis system for identifying vulnerabilities and anomalous activities within local area networks.

## Overview

PySecureNet Analyzer is a full-stack application combining real-time network packet capture, analysis, and a modern web dashboard for security monitoring. The system detects anomalies, tracks metrics, and provides actionable intelligence for network administrators.

### Key Features

- **Real-Time Packet Capture**: Scapy-based network packet sniffing and analysis
- **Anomaly Detection**: Identifies malicious traffic patterns, blacklisted protocols, and threshold violations
- **Dashboard**: Interactive web interface for monitoring metrics and alerts
- **Configuration Management**: Adjustable security thresholds and protocol blacklisting
- **Alert System**: Real-time anomaly detection with severity classification
- **Persistent Storage**: Supabase integration for all data persistence
- **Authentication**: Secure user authentication with Supabase Auth

## Architecture

### Frontend (React + Vite)
- Modern, responsive UI with real-time data updates
- Dashboard with metrics visualization
- Alert management and configuration panels
- User authentication

### Backend (Flask)
- RESTful API for frontend communication
- Network packet analysis engine
- Supabase integration for data persistence
- Background threading for continuous packet capture

### Database (Supabase PostgreSQL)
- `network_configs`: User baseline security configurations
- `network_packets`: Captured packet data
- `network_alerts`: Detected anomalies and security events
- `network_metrics`: Aggregated metrics snapshots
- Row-Level Security (RLS) for multi-tenant data isolation

## System Requirements

- Python 3.8+
- Node.js 16+
- Linux/macOS (packet sniffing requires Unix-based OS)
- Network interface with promiscuous mode capability

## Installation

### Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Set environment variables
export SUPABASE_URL=your_supabase_url
export SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
export USER_ID=your_user_id
export FLASK_DEBUG=False
```

### Frontend Setup

```bash
# Install Node dependencies
npm install

# Build for production
npm run build

# Run development server (optional)
npm run dev
```

## Running the Application

### Start Backend API

```bash
python app.py
```

The Flask server runs on `http://localhost:5000`

### Access Frontend

- Built files are in `dist/` directory
- Serve with any static server or deploy to CDN
- Access at `http://localhost:5173` (dev) or your deployment URL

## API Endpoints

### Metrics
- `GET /api/metrics` - Get real-time network metrics
- `POST /api/metrics/reset` - Reset metric counters

### Configuration
- `GET /api/config` - Get current security configuration
- `POST /api/config` - Update security configuration

### Alerts
- `GET /api/alerts` - Retrieve recent alerts (limit query parameter)

### System
- `GET /api/status` - Check system status
- `GET /health` - Health check

## Configuration

### Network Thresholds

**Traffic Threshold** (default: 1000 packets)
- Alerts when a single host exceeds packet threshold
- Helps detect data exfiltration or DoS attacks

**Connection Rate** (default: 100 connections/min)
- Monitors total new connections per minute
- Detects connection-based attacks

**Protocol Blacklist** (default: ICMP,IGMP)
- Comma-separated list of protocols to block
- Immediate alerts for blacklisted protocols

## Security Analysis

### Detection Capabilities

1. **Protocol Anomalies**
   - Identifies blacklisted protocol usage
   - Severity: HIGH
   - Source: Protocol analysis in packet header

2. **Traffic Threshold Violations**
   - Detects excessive traffic from single host
   - Severity: MEDIUM
   - Threshold: Configurable per environment

3. **Connection Rate Anomalies**
   - Monitors connection establishment rate
   - Severity: MEDIUM
   - Period: Per-minute analysis

### Alert Severity Levels

- **CRITICAL**: Immediate action required
- **HIGH**: Urgent investigation needed
- **MEDIUM**: Standard monitoring
- **LOW**: Informational alert

## Threat Detection Examples

### 1. ICMP Flood Attack
```
Detection: Blacklisted protocol (ICMP)
Severity: HIGH
Response: Alert user, log source IP, block traffic
```

### 2. Port Scanning
```
Detection: High connection rate
Severity: MEDIUM
Response: Monitor activity, analyze patterns
```

### 3. Data Exfiltration
```
Detection: Traffic threshold exceeded
Severity: HIGH
Response: Alert, capture session data, block if critical
```

## Database Schema

### network_configs
- User-specific security baselines
- Traffic thresholds and connection limits
- Protocol whitelist/blacklist definitions

### network_alerts
- Timestamped anomaly records
- Severity classification
- Source IP and attack description
- Resolution status tracking

### network_metrics
- Periodic metric snapshots
- Total packets, active hosts, connection rates
- Anomaly counters

### network_packets
- Individual packet details
- Source/destination IPs
- Protocol information
- Packet size and timestamps

## Row-Level Security

All tables enforce RLS policies:
- Users can only access their own data
- Authenticated users required
- Service role key for backend operations
- Anon key for frontend authentication

## Performance Considerations

- Packet sniffing runs in background thread
- Metrics aggregate in-memory before database writes
- Alert buffering to reduce database writes
- Configurable alert thresholds to balance detection vs. load

## Troubleshooting

### No Packets Captured
- Verify network interface is in promiscuous mode
- Check Scapy permissions (may require root)
- Verify SUPABASE environment variables

### Database Connection Errors
- Confirm SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are set
- Check network connectivity to Supabase
- Verify service account key is valid

### High CPU Usage
- Adjust traffic thresholds to reduce processing
- Reduce packet buffer size in network_analyzer.py
- Monitor active hosts count

## Future Enhancements

- Machine learning-based anomaly detection
- Real-time traffic visualization
- Integration with SIEM systems
- Automated response actions
- Advanced reporting and analytics
- Mobile app for monitoring
- Multi-interface support

## License

Proprietary - PySecureNet Analyzer
