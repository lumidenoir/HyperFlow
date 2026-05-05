import { writable, derived } from 'svelte/store'

// Current active session
export const currentSession = writable(null)

// All exercises
export const exercises = writable([])

// Muscle fatigue status
export const muscleStatus = writable({})

// UI state
export const loading = writable(false)
export const error = writable(null)
export const successMessage = writable(null)

// Current session logs (sets logged in this session)
export const sessionLogs = writable([])

// Derived store for checking if session is active
export const isSessionActive = derived(currentSession, $session => $session !== null)

// Derived store for session statistics
export const sessionStats = derived(sessionLogs, $logs => {
  if (!$logs || $logs.length === 0) {
    return {
      totalSets: 0,
      totalVolume: 0,
      exerciseCount: 0,
      averageRPE: 0,
    }
  }

  const totalSets = $logs.length
  const totalVolume = $logs.reduce((sum, log) => sum + (log.reps * log.weight), 0)
  const exerciseCount = new Set($logs.map(log => log.exercise_id)).size
  const logsWithRPE = $logs.filter(log => log.rpe)
  const averageRPE = logsWithRPE.length > 0
    ? (logsWithRPE.reduce((sum, log) => sum + log.rpe, 0) / logsWithRPE.length).toFixed(1)
    : 0

  return {
    totalSets,
    totalVolume: Math.round(totalVolume),
    exerciseCount,
    averageRPE,
  }
})

// Helper function to show success message
export function showSuccess(message) {
  successMessage.set(message)
  setTimeout(() => successMessage.set(null), 2000)
}

// Helper function to show error
export function showError(message) {
  error.set(message)
  setTimeout(() => error.set(null), 4000)
}
