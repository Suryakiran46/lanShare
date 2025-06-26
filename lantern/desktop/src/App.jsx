import './App.css'
import Sidebar from './components/sidebar'
import ChatSide from './components/chatSide'
function App() {

  return (
    <div className="flex gap-1 h-screen">
      <Sidebar />
      <ChatSide />
    </div>
  )
}

export default App
