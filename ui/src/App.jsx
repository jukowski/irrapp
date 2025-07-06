import './App.css'
import { Header } from './components/Header'
import { Sidebar } from './components/Sidebar'

function App() {

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <Sidebar />
      <main className="pt-16">
        <div className="p-6">
          <h1 className="text-2xl font-bold text-gray-800">Welcome to IRR</h1>
          <p className="text-gray-600 mt-2">Click the hamburger menu to toggle the sidebar.</p>
        </div>
      </main>
    </div>
  )
}

export default App
