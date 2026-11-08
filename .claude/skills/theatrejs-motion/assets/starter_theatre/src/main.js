import { getProject, types } from '@theatre/core'
import studio from '@theatre/studio'

// Studio is dev-only. Vite exposes import.meta.env.DEV; the fallback covers
// non-Vite bundlers. Keep Studio out of production builds.
if (import.meta.env?.DEV ?? process.env.NODE_ENV !== 'production') {
  studio.initialize()
}

const project = getProject('Theatre Starter')
const sheet = project.sheet('Intro')

const box = document.querySelector('.box')

const boxObj = sheet.object('Box', {
  x: types.number(0, { range: [-300, 300] }),
  y: types.number(0, { range: [-300, 300] }),
  opacity: types.number(1, { range: [0, 1] }),
  rotation: types.number(0, { range: [-180, 180] }),
  scale: types.number(1, { range: [0, 3] }),
})

boxObj.onValuesChange(({ x, y, opacity, rotation, scale }) => {
  box.style.transform =
    `translate(${x}px, ${y}px) rotate(${rotation}deg) scale(${scale})`
  box.style.opacity = opacity
})

// Wait for any loaded state before playing, then loop the sequence.
project.ready.then(() => {
  sheet.sequence.play({ iterationCount: Infinity, range: [0, 3] })
})
