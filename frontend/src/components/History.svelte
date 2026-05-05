<script>
  import { onMount } from 'svelte'
  import { loading } from '../lib/stores'
  import { api } from '../lib/api'
  import { showError } from '../lib/stores'

let workouts = []
  let selectedWorkout = null
  let selectedWorkoutDetail = null
  let exercises = []

onMount(async () => {
    // NEW: Load both history and exercises at the same time
    await Promise.all([
      loadHistory(),
      loadExercises()
    ])
  })
async function loadExercises() {
    try {
      exercises = await api.getExercises()
    } catch (err) {
      console.error("Failed to load exercises for mapping", err)
    }
  }

  function getExerciseName(id) {
    const ex = exercises.find(e => e.id === id)
    return ex ? ex.name : `Exercise #${id}`
  }
  async function loadHistory() {
    loading.set(true)
    try {
      const data = await api.getWorkoutHistory(30)
      workouts = data
    } catch (err) {
      showError('Failed to load workout history')
    } finally {
      loading.set(false)
    }
  }

  async function loadWorkoutDetail(id) {
    loading.set(true)
    try {
      const detail = await api.getWorkoutDetail(id)
      selectedWorkout = id
      selectedWorkoutDetail = detail
    } catch (err) {
      showError('Failed to load workout details')
    } finally {
      loading.set(false)
    }
  }
  async function deleteWorkoutSession(id) {
    if (!confirm('Are you sure you want to delete this entire workout? This cannot be undone.')) return;

    loading.set(true)
    try {
      await api.deleteSession(id)
      selectedWorkout = null
      selectedWorkoutDetail = null
      await loadHistory() // Refresh the list
    } catch (err) {
      showError('Failed to delete workout')
    } finally {
      loading.set(false)
    }
  }

  function formatDate(dateString) {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  function formatTime(minutes) {
    if (!minutes) return '-'
    if (minutes < 60) return `${minutes}m`
    const hours = Math.floor(minutes / 60)
    const mins = minutes % 60
    return `${hours}h ${mins}m`
  }
</script>

<div class="space-y-8 pb-24 text-zinc-100 font-sans tracking-tight">
  {#if selectedWorkoutDetail}
    <div class="bg-zinc-900/40 backdrop-blur-md border border-white/5 rounded-2xl p-6 relative overflow-hidden">
      <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-blue-500/50 to-transparent"></div>

      <div class="flex justify-between items-center mb-6">
        <button
          on:click={() => { selectedWorkout = null; selectedWorkoutDetail = null }}
          class="text-zinc-400 hover:text-white flex items-center gap-2 text-sm font-medium transition-colors"
        >
          <span class="text-lg leading-none mb-0.5">←</span> Back
        </button>

        <button
          on:click={() => deleteWorkoutSession(selectedWorkoutDetail.id)}
          class="bg-rose-500/10 text-rose-400 px-3 py-1.5 rounded-lg text-xs font-bold uppercase tracking-widest hover:bg-rose-500/20 transition-colors"
        >
          Delete
        </button>
      </div>

      <h2 class="text-2xl font-semibold tracking-tight text-zinc-100 mb-6">
        {formatDate(selectedWorkoutDetail.date)}
      </h2>

      <div class="grid grid-cols-2 gap-3 mb-8">
        <div class="bg-zinc-900/60 border border-white/5 p-4 rounded-xl">
          <p class="text-[10px] font-bold text-zinc-500 uppercase tracking-widest">Total Sets</p>
          <p class="text-2xl font-black text-zinc-100 mt-1">{selectedWorkoutDetail.total_sets}</p>
        </div>
        <div class="bg-zinc-900/60 border border-white/5 p-4 rounded-xl">
          <p class="text-[10px] font-bold text-zinc-500 uppercase tracking-widest">Total Volume</p>
          <p class="text-2xl font-black text-zinc-100 mt-1">{selectedWorkoutDetail.total_volume} <span class="text-xs text-zinc-600 tracking-widest">LBS</span></p>
        </div>
        <div class="bg-zinc-900/60 border border-white/5 p-4 rounded-xl">
          <p class="text-[10px] font-bold text-zinc-500 uppercase tracking-widest">Duration</p>
          <p class="text-2xl font-black text-zinc-100 mt-1">{formatTime(selectedWorkoutDetail.duration_minutes)}</p>
        </div>
        <div class="bg-zinc-900/60 border border-white/5 p-4 rounded-xl">
          <p class="text-[10px] font-bold text-zinc-500 uppercase tracking-widest">Exercises</p>
          <p class="text-2xl font-black text-zinc-100 mt-1">{selectedWorkoutDetail.exercises_count}</p>
        </div>
      </div>

      {#if selectedWorkoutDetail.notes}
        <div class="bg-zinc-950 border border-white/5 p-4 rounded-xl mb-8">
          <p class="text-[10px] font-bold text-zinc-500 uppercase tracking-widest mb-2">Notes</p>
          <p class="text-sm text-zinc-300 leading-relaxed">{selectedWorkoutDetail.notes}</p>
        </div>
      {/if}

      <h3 class="text-[11px] font-bold text-zinc-500 uppercase tracking-widest mb-4 px-1">Sets Performed</h3>
      <div class="space-y-2">
        {#each selectedWorkoutDetail.logs as log (log.id)}
          <div class="flex justify-between items-center p-4 bg-zinc-900/60 border border-white/5 rounded-xl group">
            <div>
              <p class="font-medium text-zinc-200 text-sm">{getExerciseName(log.exercise_id)}</p>
              <p class="text-[11px] font-semibold text-zinc-500 mt-1 uppercase tracking-widest">
                {log.reps} × {log.weight} lbs
                {#if log.rpe}<span class="text-zinc-700 mx-1">|</span> RPE {log.rpe}{/if}
              </p>
            </div>
            <div class="text-right">
              <p class="font-bold text-zinc-100">{log.reps * log.weight}</p>
              <p class="text-[9px] font-bold text-zinc-600 uppercase tracking-widest">Vol</p>
            </div>
          </div>
        {/each}
      </div>
    </div>

  {:else}
    <div class="mb-6 px-1">
      <h2 class="text-2xl font-semibold tracking-tight text-zinc-100">Workout History</h2>
    </div>

    {#if workouts.length === 0}
      <div class="bg-zinc-900/30 border border-zinc-800/50 border-dashed rounded-2xl p-8 flex flex-col items-center justify-center text-center">
        <span class="text-3xl mb-3 opacity-50">📋</span>
        <p class="text-sm text-zinc-500">No workouts yet. Go start lifting!</p>
      </div>
    {:else}
      <div class="space-y-3">
        {#each workouts as workout (workout.id)}
          <button
            on:click={() => loadWorkoutDetail(workout.id)}
            class="w-full bg-zinc-900/40 backdrop-blur-md border border-white/5 rounded-2xl p-5 flex justify-between items-center hover:bg-zinc-800/60 transition-all text-left group active:scale-[0.99]"
          >
            <div>
              <h3 class="font-medium text-zinc-200">{formatDate(workout.date)}</h3>
              <div class="flex items-center gap-2 mt-1.5">
                <p class="text-xs font-semibold text-zinc-500 uppercase tracking-widest">{workout.total_sets || 0} Sets</p>
                <span class="w-1 h-1 rounded-full bg-zinc-700"></span>
                <p class="text-xs font-semibold text-zinc-500 uppercase tracking-widest">{workout.total_volume || 0} LBS</p>
                <span class="w-1 h-1 rounded-full bg-zinc-700"></span>
                <p class="text-xs font-semibold text-zinc-500 uppercase tracking-widest">{formatTime(workout.duration_minutes)}</p>
              </div>
            </div>
            <span class="text-zinc-600 group-hover:text-zinc-300 transition-colors">→</span>
          </button>
        {/each}
      </div>

      <button on:click={loadHistory} class="w-full mt-6 py-3.5 bg-transparent border border-white/5 text-zinc-400 font-semibold rounded-xl hover:bg-zinc-900 transition-all active:scale-[0.98]">
        Refresh Data
      </button>
    {/if}
  {/if}
</div>
