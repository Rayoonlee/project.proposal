from flask import Flask, jsonify, request
from flask_cors import CORS
from firebase_service import SupabaseService
from network_analyzer import NetworkAnalyzer
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

USER_ID = os.getenv('USER_ID', 'default_user')

supabase_service = SupabaseService(USER_ID)

initial_config = supabase_service.load_baseline_config()
print(f"Loaded initial configuration: {initial_config}")

network_analyzer = NetworkAnalyzer(initial_config)


def alert_callback(alert_data):
    print(f"Anomaly detected: {alert_data}")
    supabase_service.save_anomaly_alert(alert_data)


network_analyzer.start_sniffing(alert_callback)


@app.route('/api/status', methods=['GET'])
def get_status():
    metrics = network_analyzer.get_realtime_metrics()
    return jsonify({
        'status': 'Running' if metrics['is_running'] else 'Stopped',
        'sniffer_thread': 'Active' if metrics['is_running'] else 'Inactive'
    })


@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    metrics = network_analyzer.get_realtime_metrics()
    return jsonify(metrics)


@app.route('/api/config', methods=['GET'])
def get_config():
    config = supabase_service.load_baseline_config()
    return jsonify(config)


@app.route('/api/config', methods=['POST'])
def update_config():
    try:
        new_config = request.get_json()

        if not new_config:
            return jsonify({'error': 'No configuration data provided'}), 400

        required_fields = ['traffic_threshold', 'connection_rate', 'protocol_blacklist']
        for field in required_fields:
            if field not in new_config:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        success = supabase_service.save_baseline_config(new_config)

        if success:
            network_analyzer.update_config(new_config)
            return jsonify({
                'message': 'Configuration updated successfully',
                'config': new_config
            })
        else:
            return jsonify({'error': 'Failed to save configuration'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    try:
        limit = request.args.get('limit', default=50, type=int)
        alerts = supabase_service.get_recent_alerts(limit)
        return jsonify(alerts)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/metrics/reset', methods=['POST'])
def reset_metrics():
    try:
        network_analyzer.reset_metrics()
        return jsonify({'message': 'Metrics reset successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

    print(f"Starting PySecureNet Analyzer API on port {port}")
    print(f"App ID: {APP_ID}, User ID: {USER_ID}")

    app.run(host='0.0.0.0', port=port, debug=debug)
