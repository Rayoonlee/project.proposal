import { supabase } from '../lib/supabase'
import { LogOut, Shield } from 'lucide-react'
import './Header.css'

export default function Header({ session }) {
  const handleSignOut = async () => {
    await supabase.auth.signOut()
  }

  return (
    <header className="header">
      <div className="header-content">
        <div className="header-brand">
          <Shield className="brand-icon" />
          <div>
            <h1>PySecureNet Analyzer</h1>
            <p>Network Security Analysis System</p>
          </div>
        </div>

        <div className="header-user">
          <span className="user-email">{session?.user?.email}</span>
          <button onClick={handleSignOut} className="logout-button">
            <LogOut size={18} />
            Sign Out
          </button>
        </div>
      </div>
    </header>
  )
}
