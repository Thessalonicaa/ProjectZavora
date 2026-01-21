<template>
  <div class="beams-bg">
    <canvas ref="canvas" :width="width" :height="height" class="beams-canvas"></canvas>
    <!-- Multiple Gradient Overlays for Better Effect -->
    <div class="beams-gradient-overlay"></div>
    <div class="beams-glow-overlay"></div>
    <div class="beams-accent-overlay"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

const props = defineProps({
  beamWidth: { type: Number, default: 3 },
  beamHeight: { type: Number, default: 25 },
  beamNumber: { type: Number, default: 20 },
  lightColor: { type: String, default: '#ff3c03' },
  speed: { type: Number, default: 2 },
  noiseIntensity: { type: Number, default: 1.75 },
  scale: { type: Number, default: 0.2 },
  rotation: { type: Number, default: 30 },
  width: { type: Number, default: 1920 },
  height: { type: Number, default: 1080 }
})

const canvas = ref(null)
let ctx, beams = []

function random(min, max) { return Math.random() * (max - min) + min }

function drawBeams() {
  ctx.clearRect(0, 0, props.width, props.height)
  beams.forEach(b => {
    ctx.save()
    // Enhanced opacity animation with sine wave
    ctx.globalAlpha = 0.2 + Math.sin(Date.now()/600 + b.idx) * 0.15
    ctx.translate(b.x, b.y)
    ctx.rotate((props.rotation * Math.PI/180) + Math.sin(Date.now()/1200 + b.idx) * 0.08)
    
    // Draw beam with gradient effect
    ctx.beginPath()
    ctx.moveTo(0, 0)
    ctx.lineTo(0, props.beamHeight * props.scale * (1 + Math.sin(Date.now()/800 + b.idx) * props.noiseIntensity))
    ctx.lineWidth = props.beamWidth
    ctx.strokeStyle = props.lightColor
    ctx.shadowColor = props.lightColor
    ctx.shadowBlur = 20
    ctx.shadowOffsetX = 0
    ctx.shadowOffsetY = 0
    ctx.lineCap = 'round'
    ctx.stroke()
    
    // Additional glow layer
    ctx.globalAlpha = 0.05 + Math.sin(Date.now()/500 + b.idx) * 0.03
    ctx.lineWidth = props.beamWidth * 3
    ctx.stroke()
    
    ctx.restore()
  })
}

function animate() {
  drawBeams()
  requestAnimationFrame(animate)
}

onMounted(() => {
  ctx = canvas.value.getContext('2d')
  beams = Array.from({ length: props.beamNumber }).map((_, i) => ({
    idx: i,
    x: random(0, props.width),
    y: random(0, props.height)
  }))
  animate()
})

watch(() => [props.beamNumber, props.beamWidth, props.beamHeight, props.lightColor, props.scale, props.rotation], () => {
  beams = Array.from({ length: props.beamNumber }).map((_, i) => ({
    idx: i,
    x: random(0, props.width),
    y: random(0, props.height)
  }))
})
</script>

<style scoped>
.beams-bg {
  position: fixed;
  top: 0; left: 0;
  width: 100vw; height: 100vh;
  z-index: 0;
  pointer-events: none;
  opacity: 0.4;
  overflow: hidden;
  background: linear-gradient(135deg, rgba(0,0,0,0.5) 0%, rgba(15,23,42,0.8) 50%, rgba(0,0,0,0.5) 100%);
}

.beams-canvas {
  width: 100vw;
  height: 100vh;
  filter: blur(2px) brightness(1.15) drop-shadow(0 0 60px #ff3c03dd);
  mix-blend-mode: lighten;
  transition: filter 0.6s ease;
  opacity: 0.85;
}

/* Primary Gradient Overlay */
.beams-gradient-overlay {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 1;
  background: radial-gradient(ellipse 100% 80% at 50% 30%, rgba(255,60,3,0.15) 0%, rgba(255,60,3,0.06) 50%, transparent 100%),
    linear-gradient(135deg, rgba(255,60,3,0.1) 0%, rgba(255,140,0,0.08) 50%, rgba(255,60,3,0.1) 100%);
  mix-blend-mode: screen;
  opacity: 0.8;
  filter: blur(10px) brightness(1.25);
  animation: gradientPulse 8s ease-in-out infinite;
}

/* Glow Overlay */
.beams-glow-overlay {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 1;
  background: radial-gradient(ellipse 120% 100% at 50% 50%, rgba(255,100,30,0.08) 0%, transparent 70%);
  mix-blend-mode: screen;
  opacity: 0.6;
  filter: blur(30px) brightness(1.15);
  animation: glowPulse 6s ease-in-out infinite reverse;
}

/* Accent Overlay */
.beams-accent-overlay {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 1;
  background: 
    radial-gradient(circle at 20% 50%, rgba(255,60,3,0.05) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(255,140,0,0.05) 0%, transparent 50%),
    linear-gradient(180deg, rgba(255,60,3,0.03) 0%, transparent 50%, rgba(255,140,0,0.03) 100%);
  mix-blend-mode: lighten;
  opacity: 0.7;
  filter: blur(15px);
  animation: accentPulse 10s ease-in-out infinite;
}

/* Animations */
@keyframes gradientPulse {
  0%, 100% {
    opacity: 0.7;
    filter: blur(10px) brightness(1.2);
  }
  50% {
    opacity: 0.9;
    filter: blur(12px) brightness(1.3);
  }
}

@keyframes glowPulse {
  0%, 100% {
    opacity: 0.5;
    filter: blur(30px) brightness(1.1);
  }
  50% {
    opacity: 0.7;
    filter: blur(25px) brightness(1.2);
  }
}

@keyframes accentPulse {
  0%, 100% {
    opacity: 0.6;
  }
  50% {
    opacity: 0.8;
  }
}

/* Responsive Design */
@media (max-width: 900px) {
  .beams-bg, .beams-canvas {
    width: 100vw !important;
    height: 100vh !important;
  }
  
  .beams-canvas {
    filter: blur(2px) brightness(1.1) drop-shadow(0 0 40px #ff3c03cc);
  }
  
  .beams-gradient-overlay {
    opacity: 0.7;
    filter: blur(8px) brightness(1.2);
  }
  
  .beams-glow-overlay {
    opacity: 0.5;
    filter: blur(25px) brightness(1.1);
  }
}

/* Mobile Optimization */
@media (max-width: 600px) {
  .beams-bg {
    opacity: 0.35;
  }
  
  .beams-canvas {
    opacity: 0.8;
    filter: blur(1.5px) brightness(1.1) drop-shadow(0 0 30px #ff3c03cc);
  }
}
</style>
