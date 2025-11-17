import { AlertCircle, AlertTriangle, Info, CheckCircle } from 'lucide-react'
import './AlertsPanel.css'

export default function AlertsPanel({ alerts, loading }) {
  const getSeverityIcon = (severity) => {
    switch (severity) {
      case 'critical':
        return <AlertCircle className="severity-icon critical" />
      case 'high':
        return <AlertTriangle className="severity-icon high" />
      case 'medium':
        return <AlertTriangle className="severity-icon medium" />
      default:
        return <Info className="severity-icon low" />
    }
  }

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical':
        return 'critical'
      case 'high':
        return 'high'
      case 'medium':
        return 'medium'
      default:
        return 'low'
    }
  }

  if (loading) {
    return (
      <div className="alerts-panel">
        <p className="loading-text">Loading alerts...</p>
      </div>
    )
  }

  if (alerts.length === 0) {
    return (
      <div className="alerts-panel">
        <div className="no-alerts">
          <CheckCircle size={48} />
          <h3>No Alerts</h3>
          <p>Your network is operating normally. No anomalies detected.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="alerts-panel">
      <div className="alerts-list">
        {alerts.map((alert) => (
          <div key={alert.id} className={`alert-item alert-${getSeverityColor(alert.severity)}`}>
            <div className="alert-header">
              <div className="alert-title-group">
                {getSeverityIcon(alert.severity)}
                <div>
                  <h4 className="alert-type">{alert.alert_type.replace(/_/g, ' ')}</h4>
                  <p className="alert-source">Source IP: {alert.source_ip}</p>
                </div>
              </div>
              <span className={`severity-badge severity-${alert.severity}`}>
                {alert.severity.toUpperCase()}
              </span>
            </div>

            {alert.description && (
              <p className="alert-description">{alert.description}</p>
            )}

            <p className="alert-time">
              {new Date(alert.timestamp).toLocaleString()}
            </p>
          </div>
        ))}
      </div>

      <div className="alerts-summary">
        <h3>Alert Summary</h3>
        <p>Showing {alerts.length} recent alerts</p>
      </div>
    </div>
  )
}
