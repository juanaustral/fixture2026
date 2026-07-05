import { motion, type Variants, type HTMLMotionProps } from 'framer-motion'
import { type ReactNode } from 'react'

// Page transition: fade + slide up
const pageVariants: Variants = {
  initial: { opacity: 0, y: 12 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -12 },
}

export function PageTransition({ children, ...props }: { children: ReactNode } & HTMLMotionProps<'div'>) {
  return (
    <motion.div
      variants={pageVariants}
      initial="initial"
      animate="animate"
      exit="exit"
      transition={{ duration: 0.3, ease: 'easeOut' }}
      {...props}
    >
      {children}
    </motion.div>
  )
}

// Stagger container for card grids
const staggerContainerVariants: Variants = {
  hidden: {},
  visible: {
    transition: {
      staggerChildren: 0.06,
      delayChildren: 0.05,
    },
  },
}

export function StaggerContainer({ children, className, ...props }: { children: ReactNode; className?: string } & HTMLMotionProps<'div'>) {
  return (
    <motion.div
      variants={staggerContainerVariants}
      initial="hidden"
      animate="visible"
      className={className}
      {...props}
    >
      {children}
    </motion.div>
  )
}

// Individual stagger item
const staggerItemVariants: Variants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.35, ease: 'easeOut' },
  },
}

export function StaggerItem({ children, className, ...props }: { children: ReactNode; className?: string } & HTMLMotionProps<'div'>) {
  return (
    <motion.div variants={staggerItemVariants} className={className} {...props}>
      {children}
    </motion.div>
  )
}

// Simple fade-in
export function FadeIn({ children, className, delay = 0, ...props }: { children: ReactNode; className?: string; delay?: number } & HTMLMotionProps<'div'>) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.4, ease: 'easeOut', delay }}
      className={className}
      {...props}
    >
      {children}
    </motion.div>
  )
}
