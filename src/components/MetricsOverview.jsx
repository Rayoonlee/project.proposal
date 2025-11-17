import { Activity, Wifi, TrendingUp, AlertTriangle } from 'lucide-react'
import './MetricsOverview.css'

export default function MetricsOverview({ metrics, loading }) {
  const cards = [
    {
      icon: Activity,
      label: 'Total Packets',
      value: metrics?.total_packets || 0,
      color: 'blue'
    },
    {
      icon: Wifi,
      label: 'Active Hosts',
      value: metrics?.active_hosts || 0,
      color: 'green'
    },
    {
      icon: TrendingUp,
      label: 'Connection Rate',
      value: metrics?.connection_rate || 0,
      color: 'amber'
    },
    {
      icon: AlertTriangle,
      label: 'Anomalies',
      value: metrics?.anomaly_count || 0,
      color: 'red'
    }
  ]

  if (loading) {
    return (
      <div className="metrics-container">
        <p className="loading-text">Loading metrics...</p>
      </div>
    )
  }

  return (
    <div className="metrics-container">
      <div className="metrics-grid">
        {cards.map((card, idx) => {
          const Icon = card.icon
          return (
            <div key={idx} className={`metric-card metric-${card.color}`}>
              <div className="metric-icon">
                <Icon size={24} />
              </div>
              <div className="metric-content">
                <p className="metric-label">{card.label}</p>
                <p className="metric-value">{card.value.toLocaleString()}</p>
              </div>
            </div>
          )
        })}
      </div>

      <div className="metrics-info">
        <h3>Real-Time Network Metrics</h3>
        <p>
          Last updated: {metrics?.timestamp ? new Date(metrics.timestamp).toLocaleTimeString() : 'N/A'}
        </p>
      </div>
    </div>
  )
}
