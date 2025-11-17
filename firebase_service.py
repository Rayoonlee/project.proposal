from supabase import create_client
import os


class SupabaseService:
    def __init__(self, user_id):
        self.user_id = user_id
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

        if not self.supabase_url or not self.supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set")

        self.client = create_client(self.supabase_url, self.supabase_key)

    def load_baseline_config(self):
        try:
            response = self.client.table('network_configs').select('*').eq('user_id', self.user_id).execute()

            if response.data and len(response.data) > 0:
                config = response.data[0]
                return {
                    'traffic_threshold': config.get('traffic_threshold', 1000),
                    'connection_rate': config.get('connection_rate', 100),
                    'protocol_blacklist': config.get('protocol_blacklist', 'ICMP,IGMP')
                }
            else:
                default_config = {
                    'traffic_threshold': 1000,
                    'connection_rate': 100,
                    'protocol_blacklist': 'ICMP,IGMP',
                    'user_id': self.user_id
                }
                self.client.table('network_configs').insert(default_config).execute()
                return {
                    'traffic_threshold': default_config['traffic_threshold'],
                    'connection_rate': default_config['connection_rate'],
                    'protocol_blacklist': default_config['protocol_blacklist']
                }
        except Exception as e:
            print(f"Error loading baseline config: {e}")
            return {
                'traffic_threshold': 1000,
                'connection_rate': 100,
                'protocol_blacklist': 'ICMP,IGMP'
            }

    def save_baseline_config(self, config):
        try:
            response = self.client.table('network_configs').select('id').eq('user_id', self.user_id).execute()

            if response.data and len(response.data) > 0:
                config_id = response.data[0]['id']
                self.client.table('network_configs').update(config).eq('id', config_id).execute()
            else:
                config['user_id'] = self.user_id
                self.client.table('network_configs').insert(config).execute()

            return True
        except Exception as e:
            print(f"Error saving baseline config: {e}")
            return False

    def save_anomaly_alert(self, alert_data):
        try:
            alert_doc = {
                'alert_type': alert_data.get('type', 'unknown'),
                'severity': alert_data.get('severity', 'medium'),
                'source_ip': alert_data.get('source_ip', 'unknown'),
                'description': alert_data.get('details', ''),
                'user_id': self.user_id,
                'is_resolved': False
            }

            self.client.table('network_alerts').insert(alert_doc).execute()
            return True
        except Exception as e:
            print(f"Error saving anomaly alert: {e}")
            return False

    def save_metrics(self, metrics):
        try:
            metrics_doc = {
                'total_packets': metrics.get('total_packets', 0),
                'active_hosts': metrics.get('active_hosts', 0),
                'connection_rate': metrics.get('connection_rate', 0),
                'anomaly_count': metrics.get('anomaly_count', 0),
                'user_id': self.user_id
            }

            self.client.table('network_metrics').insert(metrics_doc).execute()
            return True
        except Exception as e:
            print(f"Error saving metrics: {e}")
            return False

    def get_recent_alerts(self, limit=50):
        try:
            response = self.client.table('network_alerts').select('*').eq(
                'user_id', self.user_id
            ).order('timestamp', desc=True).limit(limit).execute()

            return response.data if response.data else []
        except Exception as e:
            print(f"Error getting recent alerts: {e}")
            return []
