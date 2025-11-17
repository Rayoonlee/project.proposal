import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os
import json


class FirebaseService:
    def __init__(self, app_id, user_id):
        self.app_id = app_id
        self.user_id = user_id

        if not firebase_admin._apps:
            service_account_path = os.getenv('FIREBASE_SERVICE_ACCOUNT_PATH', 'service-account.json')

            if os.path.exists(service_account_path):
                cred = credentials.Certificate(service_account_path)
            else:
                service_account_json = os.getenv('FIREBASE_SERVICE_ACCOUNT_JSON')
                if service_account_json:
                    cred = credentials.Certificate(json.loads(service_account_json))
                else:
                    cred = credentials.Certificate({
                        "type": "service_account",
                        "project_id": "YOUR_PROJECT_ID",
                        "private_key_id": "YOUR_PRIVATE_KEY_ID",
                        "private_key": "YOUR_PRIVATE_KEY",
                        "client_email": "YOUR_CLIENT_EMAIL",
                        "client_id": "YOUR_CLIENT_ID",
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                        "client_x509_cert_url": "YOUR_CERT_URL"
                    })

            firebase_admin.initialize_app(cred)

        self.db = firestore.client()
        self.config_path = f'artifacts/{self.app_id}/users/{self.user_id}/config'
        self.alerts_path = f'artifacts/{self.app_id}/users/{self.user_id}/alerts'

    def load_baseline_config(self):
        try:
            doc_ref = self.db.collection(self.config_path).document('baseline')
            doc = doc_ref.get()

            if doc.exists:
                config_data = doc.to_dict()
                return {
                    'trafficThreshold': config_data.get('trafficThreshold', 1000),
                    'connectionRate': config_data.get('connectionRate', 100),
                    'protocolBlacklist': config_data.get('protocolBlacklist', 'ICMP,IGMP')
                }
            else:
                default_config = {
                    'trafficThreshold': 1000,
                    'connectionRate': 100,
                    'protocolBlacklist': 'ICMP,IGMP'
                }
                doc_ref.set(default_config)
                return default_config
        except Exception as e:
            print(f"Error loading baseline config: {e}")
            return {
                'trafficThreshold': 1000,
                'connectionRate': 100,
                'protocolBlacklist': 'ICMP,IGMP'
            }

    def save_baseline_config(self, config):
        try:
            doc_ref = self.db.collection(self.config_path).document('baseline')
            doc_ref.set(config)
            return True
        except Exception as e:
            print(f"Error saving baseline config: {e}")
            return False

    def save_anomaly_alert(self, alert_data):
        try:
            alert_doc = {
                'timestamp': firestore.SERVER_TIMESTAMP,
                'type': alert_data.get('type', 'unknown'),
                'severity': alert_data.get('severity', 'medium'),
                'source_ip': alert_data.get('source_ip', 'unknown'),
                'details': alert_data.get('details', '')
            }

            self.db.collection(self.alerts_path).add(alert_doc)
            return True
        except Exception as e:
            print(f"Error saving anomaly alert: {e}")
            return False

    def get_recent_alerts(self, limit=50):
        try:
            alerts_ref = self.db.collection(self.alerts_path).order_by(
                'timestamp', direction=firestore.Query.DESCENDING
            ).limit(limit)

            alerts = []
            for doc in alerts_ref.stream():
                alert = doc.to_dict()
                alert['id'] = doc.id
                alerts.append(alert)

            return alerts
        except Exception as e:
            print(f"Error getting recent alerts: {e}")
            return []
