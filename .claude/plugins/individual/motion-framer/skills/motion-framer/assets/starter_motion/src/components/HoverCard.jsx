import { motion } from 'framer-motion'

export default function HoverCard({ title, children }) {
  return (
    <motion.div
      className="hover-card"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{
        scale: 1.05,
        boxShadow: '0 20px 40px rgba(0, 0, 0, 0.3)',
        transition: { duration: 0.2 }
      }}
      whileTap={{ scale: 0.98 }}
      style={{
        background: 'rgba(255, 255, 255, 0.1)',
        backdropFilter: 'blur(10px)',
        border: '1px solid rgba(255, 255, 255, 0.2)',
        borderRadius: '16px',
        padding: '30px',
        cursor: 'pointer',
      }}
    >
      <h3 style={{ fontSize: '1.5rem', marginBottom: '10px' }}>{title}</h3>
      <p style={{ opacity: 0.9 }}>{children}</p>
    </motion.div>
  )
}
