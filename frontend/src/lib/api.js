const API_BASE = `http://${window.location.hostname}:5100`

export const api = {
  // Exercises
  async getExercises(muscleGroup = null) {
    const url = new URL(`${API_BASE}/exercises`)
    if (muscleGroup) url.searchParams.append('muscle_group', muscleGroup)
    const res = await fetch(url)
    if (!res.ok) throw new Error('Failed to fetch exercises')
    return res.json()
  },

  async getExercise(id) {
    const res = await fetch(`${API_BASE}/exercises/${id}`)
    if (!res.ok) throw new Error('Exercise not found')
    return res.json()
  },

  async createExercise(data) {
    const res = await fetch(`${API_BASE}/exercises`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
    if (!res.ok) throw new Error('Failed to create exercise')
    return res.json()
  },

  async updateExercise(id, data) {
    const res = await fetch(`${API_BASE}/exercises/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
    if (!res.ok) throw new Error('Failed to update exercise')
    return res.json()
  },

  async deleteExercise(id) {
    const res = await fetch(`${API_BASE}/exercises/${id}`, {
      method: 'DELETE',
    })
    if (!res.ok) throw new Error('Failed to delete exercise')
    return res.json()
  },
  async deleteSession(sessionId) {
    const res = await fetch(`${API_BASE}/session/${sessionId}`, {
      method: 'DELETE',
    })
    if (!res.ok) throw new Error('Failed to delete session')
    return res.json()
  },
  // Status/Fatigue
  async getStatus() {
    const res = await fetch(`${API_BASE}/status`)
    if (!res.ok) throw new Error('Failed to fetch status')
    return res.json()
  },

  async getMuscleFatigue(muscleGroup) {
    const res = await fetch(`${API_BASE}/status/${muscleGroup}`)
    if (!res.ok) throw new Error('Failed to fetch muscle fatigue')
    return res.json()
  },

  async resetMuscleFatigue(muscleGroup) {
    const res = await fetch(`${API_BASE}/status/reset/${muscleGroup}`, {
      method: 'POST',
    })
    if (!res.ok) throw new Error('Failed to reset fatigue')
    return res.json()
  },

  // Sessions
async saveDraft(template) {
    const res = await fetch(`${API_BASE}/session/draft`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(template),
    })
    if (!res.ok) throw new Error('Failed to save draft')
    return res.json()
  },

  async activateSession(sessionId) {
    const res = await fetch(`${API_BASE}/session/activate/${sessionId}`, {
      method: 'POST',
    })
    if (!res.ok) throw new Error('Failed to activate session')
    return res.json()
  },

  async getCurrentSession() {
    const res = await fetch(`${API_BASE}/session/current`)
    if (!res.ok) throw new Error('No active session')
    return res.json()
  },

  async logSet(data) {
    const res = await fetch(`${API_BASE}/session/log-set`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
    if (!res.ok) throw new Error('Failed to log set')
    return res.json()
  },

  async getSessionLogs(sessionId) {
    const res = await fetch(`${API_BASE}/session/${sessionId}/logs`)
    if (!res.ok) throw new Error('Failed to fetch session logs')
    return res.json()
  },

  async deleteSetLog(sessionId, logId) {
    const res = await fetch(`${API_BASE}/session/${sessionId}/logs/${logId}`, {
      method: 'DELETE',
    })
    if (!res.ok) throw new Error('Failed to delete set log')
    return res.json()
  },

  async finishSession(sessionId) {
    const res = await fetch(`${API_BASE}/session/finish/${sessionId}`, {
      method: 'POST',
    })
    if (!res.ok) throw new Error('Failed to finish session')
    return res.json()
  },

  // Planning
  async generateWorkout(priorityGroups) {
    const url = new URL(`${API_BASE}/session/generate`)
    priorityGroups.forEach(group => {
      url.searchParams.append('priority_groups', group)
    })
      const res = await fetch(url, {method: 'POST'})
    if (!res.ok) throw new Error('Failed to generate workout')
    return res.json()
  },

  // History & Analytics
  async getWorkoutHistory(limit = 20) {
    const url = new URL(`${API_BASE}/workouts/history`)
    url.searchParams.append('limit', limit)
    const res = await fetch(url)
    if (!res.ok) throw new Error('Failed to fetch history')
    return res.json()
  },

  async getWorkoutDetail(sessionId) {
    const res = await fetch(`${API_BASE}/workouts/${sessionId}`)
    if (!res.ok) throw new Error('Failed to fetch workout detail')
    return res.json()
  },

  async getVolumeTrends(muscleGroup = null, days = 30) {
    const url = new URL(`${API_BASE}/analytics/volume`)
    if (muscleGroup) url.searchParams.append('muscle_group', muscleGroup)
    url.searchParams.append('days', days)
    const res = await fetch(url)
    if (!res.ok) throw new Error('Failed to fetch volume trends')
    return res.json()
  },

  async getFatigueTrend(muscleGroup) {
    const res = await fetch(
      `${API_BASE}/analytics/fatigue-trend?muscle_group=${muscleGroup}`
    )
    if (!res.ok) throw new Error('Failed to fetch fatigue trend')
    return res.json()
  },

  async getHealth() {
    const res = await fetch(`${API_BASE}/health`)
    if (!res.ok) throw new Error('Backend not available')
    return res.json()
  },
}
