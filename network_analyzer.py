from scapy.all import sniff, IP, TCP, UDP, ICMP
from threading import Thread, Lock
from collections import defaultdict
import time


class NetworkAnalyzer:
    def __init__(self, config):
        self.config = config
        self.is_running = False
        self.sniffer_thread = None

        self.total_packets = 0
        self.active_hosts = set()
        self.connection_count = 0
        self.host_packet_count = defaultdict(int)
        self.last_reset_time = time.time()

        self.metrics_lock = Lock()
        self.callback = None

        self.protocol_map = {
            1: 'ICMP',
            2: 'IGMP',
            6: 'TCP',
            17: 'UDP'
        }

    def update_config(self, config):
        with self.metrics_lock:
            self.config = config
            print(f"Configuration updated: {config}")

    def start_sniffing(self, callback):
        if self.is_running:
            print("Sniffer is already running")
            return

        self.callback = callback
        self.is_running = True

        self.sniffer_thread = Thread(target=self._sniff_packets, daemon=True)
        self.sniffer_thread.start()
        print("Network sniffer started")

    def stop_sniffing(self):
        self.is_running = False
        if self.sniffer_thread:
            self.sniffer_thread.join(timeout=2)
        print("Network sniffer stopped")

    def _sniff_packets(self):
        try:
            sniff(prn=self.process_packet, store=False, stop_filter=lambda x: not self.is_running)
        except Exception as e:
            print(f"Error in packet sniffing: {e}")
            self.is_running = False

    def process_packet(self, packet):
        try:
            if not packet.haslayer(IP):
                return

            with self.metrics_lock:
                self.total_packets += 1

                src_ip = packet[IP].src
                dst_ip = packet[IP].dst

                self.active_hosts.add(src_ip)
                self.active_hosts.add(dst_ip)

                self.host_packet_count[src_ip] += 1

                if packet.haslayer(TCP) or packet.haslayer(UDP):
                    self.connection_count += 1

                protocol_num = packet[IP].proto
                protocol_name = self.protocol_map.get(protocol_num, f'UNKNOWN_{protocol_num}')

                blacklist = [p.strip().upper() for p in self.config.get('protocolBlacklist', '').split(',') if p.strip()]

                if protocol_name in blacklist:
                    alert_data = {
                        'type': 'blacklisted_protocol',
                        'severity': 'high',
                        'source_ip': src_ip,
                        'details': f'Blacklisted protocol detected: {protocol_name}'
                    }
                    if self.callback:
                        self.callback(alert_data)

                traffic_threshold = self.config.get('trafficThreshold', 1000)
                if self.host_packet_count[src_ip] > traffic_threshold:
                    alert_data = {
                        'type': 'traffic_threshold_exceeded',
                        'severity': 'medium',
                        'source_ip': src_ip,
                        'details': f'Host exceeded traffic threshold: {self.host_packet_count[src_ip]} packets'
                    }
                    if self.callback:
                        self.callback(alert_data)
                    self.host_packet_count[src_ip] = 0

                connection_rate = self.config.get('connectionRate', 100)
                current_time = time.time()
                time_elapsed = current_time - self.last_reset_time

                if time_elapsed >= 60:
                    if self.connection_count > connection_rate:
                        alert_data = {
                            'type': 'connection_rate_exceeded',
                            'severity': 'medium',
                            'source_ip': 'multiple',
                            'details': f'Connection rate exceeded: {self.connection_count} connections per minute'
                        }
                        if self.callback:
                            self.callback(alert_data)

                    self.connection_count = 0
                    self.last_reset_time = current_time

        except Exception as e:
            print(f"Error processing packet: {e}")

    def get_realtime_metrics(self):
        with self.metrics_lock:
            return {
                'total_packets': self.total_packets,
                'active_hosts': len(self.active_hosts),
                'connection_rate': self.connection_count,
                'is_running': self.is_running
            }

    def reset_metrics(self):
        with self.metrics_lock:
            self.total_packets = 0
            self.active_hosts.clear()
            self.connection_count = 0
            self.host_packet_count.clear()
            self.last_reset_time = time.time()
