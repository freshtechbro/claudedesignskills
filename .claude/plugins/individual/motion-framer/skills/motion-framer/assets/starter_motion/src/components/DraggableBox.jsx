import { motion } from 'framer-motion'
import { useState } from 'react'

export default function DraggableBox() {
  const [isDragging, setIsDragging] = useState(false)

  return (
    <div style={{
      height: '300px',
      position: 'relative',
      background: 'rgba(255, 255, 255, 0.05)',
      borderRadius: '16px',
      border: '2px dashed rgba(255, 255, 255, 0.3)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center'
    }}>
      <motion.div
        drag
        dragConstraints={{
          left: -100,
          right: 100,
          top: -100,
          bottom: 100
        }}
        dragElastic={0.1}
        whileDrag={{
          scale: 1.1,
          cursor: 'grabbing',
          boxShadow: '0 20px 40px rgba(0, 0, 0, 0.4)'
        }}
        onDragStart={() => setIsDragging(true)}
        onDragEnd={() => setIsDragging(false)}
        style={{
          width: '150px',
          height: '150px',
          background: isDragging
            ? 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'
            : 'rgba(255, 255, 255, 0.2)',
          borderRadius: '16px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          cursor: 'grab',
          userSelect: 'none',
          fontWeight: 'bold',
          fontSize: '1.1rem',
        }}
      >
        {isDragging ? 'Dragging!' : 'Drag me'}
      </motion.div>
    </div>
  )
}
