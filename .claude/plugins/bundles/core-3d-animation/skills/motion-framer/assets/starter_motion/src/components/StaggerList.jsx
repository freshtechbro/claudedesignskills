import { motion } from 'framer-motion'

const container = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2
    }
  }
}

const item = {
  hidden: { opacity: 0, x: -20 },
  visible: {
    opacity: 1,
    x: 0,
    transition: { duration: 0.5 }
  }
}

export default function StaggerList() {
  const items = [
    { id: 1, title: 'First Item', description: 'Animates first' },
    { id: 2, title: 'Second Item', description: 'Follows with a delay' },
    { id: 3, title: 'Third Item', description: 'Then this one' },
    { id: 4, title: 'Fourth Item', description: 'And finally this' },
  ]

  return (
    <motion.ul
      variants={container}
      initial="hidden"
      animate="visible"
      style={{
        listStyle: 'none',
        maxWidth: '600px',
        margin: '0 auto'
      }}
    >
      {items.map((listItem) => (
        <motion.li
          key={listItem.id}
          variants={item}
          whileHover={{ scale: 1.02, x: 10 }}
          style={{
            background: 'rgba(255, 255, 255, 0.1)',
            backdropFilter: 'blur(10px)',
            border: '1px solid rgba(255, 255, 255, 0.2)',
            borderRadius: '12px',
            padding: '20px',
            marginBottom: '15px',
            cursor: 'pointer',
          }}
        >
          <h4 style={{ fontSize: '1.2rem', marginBottom: '5px' }}>
            {listItem.title}
          </h4>
          <p style={{ opacity: 0.8 }}>{listItem.description}</p>
        </motion.li>
      ))}
    </motion.ul>
  )
}
