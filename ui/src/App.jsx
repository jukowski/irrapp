import './App.css'
import { Header } from './components/Header'
import { Sidebar } from './components/Sidebar'
import { CountryFilter } from './components/CountryFilter'

function App() {

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <Sidebar />
      <main className="pt-16">
        <div className="p-6 space-y-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-800">Welcome to IRR</h1>
            <p className="text-gray-600 mt-2">Click the hamburger menu to toggle the sidebar.</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <CountryFilter />
          </div>
        </div>
      </main>
    </div>
  )
}

export default App
