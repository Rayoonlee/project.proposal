/*
  # PySecureNet Analyzer Database Schema

  1. New Tables
    - `network_configs` - Baseline security configurations per user
      - `id` (uuid, primary key)
      - `user_id` (uuid, references auth.users)
      - `traffic_threshold` (int) - Packet threshold for anomaly detection
      - `connection_rate` (int) - Connections per minute threshold
      - `protocol_blacklist` (text) - Comma-separated protocol names
      - `created_at` (timestamp)
      - `updated_at` (timestamp)
    
    - `network_packets` - Captured network packet data
      - `id` (uuid, primary key)
      - `user_id` (uuid, references auth.users)
      - `source_ip` (text)
      - `destination_ip` (text)
      - `protocol` (text)
      - `packet_size` (int)
      - `timestamp` (timestamp)
    
    - `network_alerts` - Anomaly detection alerts
      - `id` (uuid, primary key)
      - `user_id` (uuid, references auth.users)
      - `alert_type` (text) - Type of anomaly detected
      - `severity` (text) - 'low', 'medium', 'high', 'critical'
      - `source_ip` (text)
      - `description` (text)
      - `is_resolved` (boolean)
      - `timestamp` (timestamp)
    
    - `network_metrics` - Aggregated metrics snapshots
      - `id` (uuid, primary key)
      - `user_id` (uuid, references auth.users)
      - `total_packets` (int)
      - `active_hosts` (int)
      - `connection_rate` (int)
      - `anomaly_count` (int)
      - `timestamp` (timestamp)

  2. Security
    - Enable RLS on all tables
    - Users can only access their own data
    - Authenticated users required for all operations

  3. Indexes
    - Index on user_id for all tables (query performance)
    - Index on timestamp for sorting operations
    - Index on source_ip for packet analysis
*/

CREATE TABLE IF NOT EXISTS network_configs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  traffic_threshold int DEFAULT 1000,
  connection_rate int DEFAULT 100,
  protocol_blacklist text DEFAULT 'ICMP,IGMP',
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  UNIQUE(user_id)
);

CREATE TABLE IF NOT EXISTS network_packets (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  source_ip text NOT NULL,
  destination_ip text NOT NULL,
  protocol text NOT NULL,
  packet_size int DEFAULT 0,
  timestamp timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS network_alerts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  alert_type text NOT NULL,
  severity text CHECK (severity IN ('low', 'medium', 'high', 'critical')) DEFAULT 'medium',
  source_ip text NOT NULL,
  description text,
  is_resolved boolean DEFAULT false,
  timestamp timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS network_metrics (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  total_packets int DEFAULT 0,
  active_hosts int DEFAULT 0,
  connection_rate int DEFAULT 0,
  anomaly_count int DEFAULT 0,
  timestamp timestamptz DEFAULT now()
);

ALTER TABLE network_configs ENABLE ROW LEVEL SECURITY;
ALTER TABLE network_packets ENABLE ROW LEVEL SECURITY;
ALTER TABLE network_alerts ENABLE ROW LEVEL SECURITY;
ALTER TABLE network_metrics ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage own config"
  ON network_configs FOR ALL
  TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view own packets"
  ON network_packets FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own packets"
  ON network_packets FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can manage own alerts"
  ON network_alerts FOR ALL
  TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view own metrics"
  ON network_metrics FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own metrics"
  ON network_metrics FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

CREATE INDEX idx_network_configs_user_id ON network_configs(user_id);
CREATE INDEX idx_network_packets_user_id ON network_packets(user_id);
CREATE INDEX idx_network_packets_timestamp ON network_packets(timestamp DESC);
CREATE INDEX idx_network_packets_source_ip ON network_packets(source_ip);
CREATE INDEX idx_network_alerts_user_id ON network_alerts(user_id);
CREATE INDEX idx_network_alerts_timestamp ON network_alerts(timestamp DESC);
CREATE INDEX idx_network_alerts_severity ON network_alerts(severity);
CREATE INDEX idx_network_metrics_user_id ON network_metrics(user_id);
CREATE INDEX idx_network_metrics_timestamp ON network_metrics(timestamp DESC);
