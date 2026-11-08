import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import HoverCard from './components/HoverCard'
import DraggableBox from './components/DraggableBox'
import StaggerList from './components/StaggerList'
import './App.css'

function App() {
  const [showModal, setShowModal] = useState(false)

  return (
    <div className="app">
      <header className="header">
        <motion.h1
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          Motion Starter
        </motion.h1>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2, duration: 0.5 }}
        >
          Framer Motion animation examples
        </motion.p>
      </header>

      <main className="main">
        <section className="section">
          <h2>Hover Animations</h2>
          <div className="grid">
            <HoverCard title="Card 1">
              Hover over me to see the animation
            </HoverCard>
            <HoverCard title="Card 2">
              Different hover effects
            </HoverCard>
            <HoverCard title="Card 3">
              Smooth transitions
            </HoverCard>
          </div>
        </section>

        <section className="section">
          <h2>Drag Interaction</h2>
          <DraggableBox />
        </section>

        <section className="section">
          <h2>Staggered List</h2>
          <StaggerList />
        </section>

        <section className="section">
          <h2>Exit Animations</h2>
          <motion.button
            className="modal-button"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setShowModal(!showModal)}
          >
            {showModal ? 'Close' : 'Open'} Modal
          </motion.button>

          <AnimatePresence mode="wait">
            {showModal && (
              <motion.div
                key="modal"
                className="modal-backdrop"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                onClick={() => setShowModal(false)}
              >
                <motion.div
                  className="modal"
                  initial={{ opacity: 0, scale: 0.9, y: 20 }}
                  animate={{ opacity: 1, scale: 1, y: 0 }}
                  exit={{ opacity: 0, scale: 0.9, y: -20 }}
                  transition={{ type: 'spring', stiffness: 300, damping: 30 }}
                  onClick={(e) => e.stopPropagation()}
                >
                  <h3>Modal Title</h3>
                  <p>This modal animates in and out smoothly with AnimatePresence.</p>
                  <motion.button
                    className="close-button"
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    onClick={() => setShowModal(false)}
                  >
                    Close
                  </motion.button>
                </motion.div>
              </motion.div>
            )}
          </AnimatePresence>
        </section>
      </main>

      <footer className="footer">
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
        >
          Built with Framer Motion
        </motion.p>
      </footer>
    </div>
  )
}

export default App
