import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'
import { Save, RotateCcw } from 'lucide-react'
import './ConfigPanel.css'

export default function ConfigPanel({ config, onConfigUpdate }) {
  const [formData, setFormData] = useState({
    traffic_threshold: 1000,
    connection_rate: 100,
    protocol_blacklist: 'ICMP,IGMP'
  })
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState(null)

  useEffect(() => {
    if (config) {
      setFormData({
        traffic_threshold: config.traffic_threshold || 1000,
        connection_rate: config.connection_rate || 100,
        protocol_blacklist: config.protocol_blacklist || 'ICMP,IGMP'
      })
    }
  }, [config])

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: name === 'protocol_blacklist' ? value : parseInt(value) || value
    }))
  }

  const handleSave = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage(null)

    try {
      const { data: { user } } = await supabase.auth.getUser()

      if (config?.id) {
        await supabase
          .from('network_configs')
          .update(formData)
          .eq('id', config.id)
      } else {
        await supabase
          .from('network_configs')
          .insert([{
            ...formData,
            user_id: user.id
          }])
      }

      setMessage({ type: 'success', text: 'Configuration saved successfully!' })
      setTimeout(() => {
        setMessage(null)
        onConfigUpdate()
      }, 2000)
    } catch (err) {
      setMessage({ type: 'error', text: `Error: ${err.message}` })
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    if (config) {
      setFormData({
        traffic_threshold: config.traffic_threshold || 1000,
        connection_rate: config.connection_rate || 100,
        protocol_blacklist: config.protocol_blacklist || 'ICMP,IGMP'
      })
    }
  }

  return (
    <div className="config-panel">
      <div className="config-card">
        <h2>Network Configuration</h2>
        <p className="config-description">
          Configure baseline security settings for network analysis and anomaly detection.
        </p>

        <form onSubmit={handleSave} className="config-form">
          <div className="form-group">
            <label htmlFor="traffic_threshold">Traffic Threshold (packets)</label>
            <input
              id="traffic_threshold"
              type="number"
              name="traffic_threshold"
              value={formData.traffic_threshold}
              onChange={handleChange}
              min="100"
              step="100"
              disabled={loading}
            />
            <p className="field-help">Maximum packets per host before triggering an alert</p>
          </div>

          <div className="form-group">
            <label htmlFor="connection_rate">Connection Rate (connections/min)</label>
            <input
              id="connection_rate"
              type="number"
              name="connection_rate"
              value={formData.connection_rate}
              onChange={handleChange}
              min="10"
              step="10"
              disabled={loading}
            />
            <p className="field-help">Maximum connections per minute threshold</p>
          </div>

          <div className="form-group">
            <label htmlFor="protocol_blacklist">Protocol Blacklist</label>
            <input
              id="protocol_blacklist"
              type="text"
              name="protocol_blacklist"
              value={formData.protocol_blacklist}
              onChange={handleChange}
              placeholder="ICMP,IGMP,..."
              disabled={loading}
            />
            <p className="field-help">Comma-separated protocol names to block</p>
          </div>

          {message && (
            <div className={`message message-${message.type}`}>
              {message.text}
            </div>
          )}

          <div className="form-actions">
            <button type="submit" className="btn-save" disabled={loading}>
              <Save size={18} />
              {loading ? 'Saving...' : 'Save Configuration'}
            </button>
            <button
              type="button"
              className="btn-reset"
              onClick={handleReset}
              disabled={loading}
            >
              <RotateCcw size={18} />
              Reset
            </button>
          </div>
        </form>
      </div>

      <div className="config-info">
        <h3>Configuration Guide</h3>
        <div className="info-section">
          <h4>Traffic Threshold</h4>
          <p>Triggers an alert when a single host exceeds this packet count. Helps detect potential data exfiltration or DDoS attacks.</p>
        </div>

        <div className="info-section">
          <h4>Connection Rate</h4>
          <p>Monitors the total number of new connections per minute. Useful for detecting connection-based attacks.</p>
        </div>

        <div className="info-section">
          <h4>Protocol Blacklist</h4>
          <p>Specifies which network protocols should trigger immediate alerts. Common choices include ICMP (ping) and IGMP (multicast).</p>
        </div>
      </div>
    </div>
  )
}
