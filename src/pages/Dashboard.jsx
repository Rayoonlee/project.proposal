import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'
import MetricsOverview from '../components/MetricsOverview'
import AlertsPanel from '../components/AlertsPanel'
import ConfigPanel from '../components/ConfigPanel'
import Header from '../components/Header'
import './Dashboard.css'

export default function Dashboard({ session }) {
  const [metrics, setMetrics] = useState(null)
  const [alerts, setAlerts] = useState([])
  const [config, setConfig] = useState(null)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('overview')

  useEffect(() => {
    loadData()
    const interval = setInterval(loadData, 5000)
    return () => clearInterval(interval)
  }, [])

  const loadData = async () => {
    try {
      const { data: metricsData } = await supabase
        .from('network_metrics')
        .select('*')
        .order('timestamp', { ascending: false })
        .limit(1)

      if (metricsData?.length > 0) {
        setMetrics(metricsData[0])
      }

      const { data: alertsData } = await supabase
        .from('network_alerts')
        .select('*')
        .order('timestamp', { ascending: false })
        .limit(20)

      if (alertsData) {
        setAlerts(alertsData)
      }

      const { data: configData } = await supabase
        .from('network_configs')
        .select('*')
        .limit(1)

      if (configData?.length > 0) {
        setConfig(configData[0])
      }

      setLoading(false)
    } catch (err) {
      console.error('Error loading data:', err)
      setLoading(false)
    }
  }

  return (
    <div className="dashboard">
      <Header session={session} />

      <main className="dashboard-content">
        <div className="tabs">
          <button
            className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
            onClick={() => setActiveTab('overview')}
          >
            Overview
          </button>
          <button
            className={`tab ${activeTab === 'alerts' ? 'active' : ''}`}
            onClick={() => setActiveTab('alerts')}
          >
            Alerts
          </button>
          <button
            className={`tab ${activeTab === 'config' ? 'active' : ''}`}
            onClick={() => setActiveTab('config')}
          >
            Configuration
          </button>
        </div>

        <div className="tab-content">
          {activeTab === 'overview' && (
            <MetricsOverview metrics={metrics} loading={loading} />
          )}
          {activeTab === 'alerts' && (
            <AlertsPanel alerts={alerts} loading={loading} />
          )}
          {activeTab === 'config' && (
            <ConfigPanel config={config} onConfigUpdate={() => loadData()} />
          )}
        </div>
      </main>
    </div>
  )
}
