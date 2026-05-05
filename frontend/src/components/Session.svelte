<script>
  import { onMount } from 'svelte'
  import {
    currentSession,
    sessionLogs,
    sessionStats,
    loading,
    isSessionActive,
  } from '../lib/stores'
  import { api } from '../lib/api'
  import { showSuccess, showError } from '../lib/stores'
  import SetLogger from './SetLogger.svelte'

  let exercises = []
  let selectedExercise = null
  let selectedMuscles = []
  let plannedTemplate = []
  let generationWarnings = [] // NEW: Store warnings from generation
  let isGenerating = false
  let selectValue = ''

  const muscleGroups = ['Chest', 'Back', 'Legs', 'Shoulders', 'Biceps', 'Triceps', 'Core', 'Forearms']

  onMount(async () => {
    await loadSession()
    await loadExercises()
  })

  async function loadSession() {
    loading.set(true)
    try {
      const session = await api.getCurrentSession()
      currentSession.set(session)

      if (session.planned_template) {
        try {
          plannedTemplate = JSON.parse(session.planned_template)
        } catch {
          plannedTemplate = []
        }
      }

      if (session.status === 'active') {
        const logs = await api.getSessionLogs(session.id)
        sessionLogs.set(logs)
      }
    } catch (err) {
      currentSession.set(null)
      sessionLogs.set([])
      plannedTemplate = []
    } finally {
      loading.set(false)
    }
  }

  async function loadExercises() {
    try {
      exercises = await api.getExercises()
    } catch (err) {
      showError('Failed to load exercises')
    }
  }

  function toggleMuscle(muscle) {
    if (selectedMuscles.includes(muscle)) {
      selectedMuscles = selectedMuscles.filter(m => m !== muscle)
    } else {
      selectedMuscles = [...selectedMuscles, muscle]
    }
  }

  // --- PHASE 1: Generate Plan ---
  async function generatePlan() {
    if (selectedMuscles.length === 0) return

    loading.set(true)
    isGenerating = true
    try {
      const result = await api.generateWorkout(selectedMuscles)

      // Extract warnings and valid recommendations
      generationWarnings = result.recommendations
        .filter(r => r.warning)
        .map(r => r.warning)

      const validRecommendations = result.recommendations.filter(r => !r.warning)

      // FIX: Use dynamic target_sets from backend
      const template = validRecommendations.map(ex => ({
        ...ex,
        target_sets: ex.target_sets || 3,
        target_reps: '8-12',
      }))

      const session = await api.saveDraft(template)
      currentSession.set(session)
      plannedTemplate = template
      selectedMuscles = []
    } catch (err) {
      showError(err.message)
    } finally {
      loading.set(false)
      isGenerating = false
    }
  }

  // --- PHASE 2: Edit Draft ---
  function removeExerciseFromDraft(index) {
    plannedTemplate = plannedTemplate.filter((_, i) => i !== index)
  }

  function addExerciseToDraft() {
    if (!selectValue) return
    const exId = parseInt(selectValue)
    const exercise = exercises.find(e => e.id === exId)

    if (exercise && !plannedTemplate.find(p => p.id === exId)) {
      plannedTemplate = [...plannedTemplate, { ...exercise, target_sets: 3, target_reps: '8-12' }]
    }
    selectValue = ''
  }

  // --- PHASE 3: Activation & Empty Start ---
  async function activateSession() {
    if (!$currentSession) return
    loading.set(true)
    try {
      await api.saveDraft(plannedTemplate)
      const session = await api.activateSession($currentSession.id)
      currentSession.set(session)
      sessionLogs.set([])
      generationWarnings = [] // Clear warnings on start
      showSuccess('Workout started!')
    } catch (err) {
      showError(err.message)
    } finally {
      loading.set(false)
    }
  }

  async function startEmptyWorkout() {
    loading.set(true)
    try {
      const draft = await api.saveDraft([])
      const session = await api.activateSession(draft.id)
      currentSession.set(session)
      sessionLogs.set([])
      plannedTemplate = []
      generationWarnings = [] // Clear warnings
      showSuccess('Workout started!')
    } catch (err) {
      showError(err.message)
    } finally {
      loading.set(false)
    }
  }

  async function deleteDraft() {
    if (!$currentSession) return
    loading.set(true)
    try {
      await api.deleteSession($currentSession.id)
      currentSession.set(null)
      plannedTemplate = []
      selectedMuscles = []
      generationWarnings = [] // Clear warnings
    } catch (err) {
      showError('Failed to delete draft')
    } finally {
      loading.set(false)
    }
  }

  // --- PHASE 4: Execution & Ad-Hoc ---
  function addAdHocExercise() {
    if (!selectValue) return
    const exId = parseInt(selectValue)
    const exercise = exercises.find(e => e.id === exId)

    if (exercise) {
      if (!plannedTemplate.find(p => p.id === exId)) {
        plannedTemplate = [...plannedTemplate, { ...exercise, target_sets: 3, target_reps: '8-12' }]
      }
      selectedExercise = exercise
    }
    selectValue = ''
  }

  async function handleSetLogged(event) {
    const { reps, weight, rpe } = event.detail
    if (!selectedExercise || !$currentSession) return

    loading.set(true)
    try {
      await api.logSet({
        session_id: $currentSession.id,
        exercise_id: selectedExercise.id,
        reps,
        weight,
        rpe: rpe || null,
      })
      const logs = await api.getSessionLogs($currentSession.id)
      sessionLogs.set(logs)
    } catch (err) {
      showError(err.message)
    } finally {
      loading.set(false)
    }
  }

  async function deleteLog(logId) {
    if (!$currentSession) return
    loading.set(true)
    try {
      await api.deleteSetLog($currentSession.id, logId)
      const logs = await api.getSessionLogs($currentSession.id)
      sessionLogs.set(logs)
    } catch (err) {
      showError('Failed to delete set')
    } finally {
      loading.set(false)
    }
  }

  async function finishSession() {
    if (!$currentSession) return
    loading.set(true)
    try {
      await api.finishSession($currentSession.id)
      currentSession.set(null)
      sessionLogs.set([])
      selectedExercise = null
      plannedTemplate = []
      showSuccess('Workout finished!')
    } catch (err) {
      showError('Failed to finish session')
    } finally {
      loading.set(false)
    }
  }

  function getSetsLoggedForExercise(exerciseId) {
    return $sessionLogs.filter(log => log.exercise_id === exerciseId).length
  }

  function getExerciseById(id) {
    return exercises.find(e => e.id === id)
  }
</script>

<div class="space-y-8 pb-24 text-zinc-100 font-sans tracking-tight">
  {#if !$currentSession}
    <div class="bg-zinc-900/40 backdrop-blur-md border border-white/5 rounded-2xl p-6">
      <h2 class="text-xl font-semibold tracking-tight mb-2">Plan Your Workout</h2>
      <p class="text-xs text-zinc-400 mb-6 leading-relaxed">
        Select target muscles. We'll generate a volume-matched plan based on your live fatigue.
      </p>

      <div class="grid grid-cols-2 md:grid-cols-3 gap-3 mb-8">
        {#each muscleGroups as muscle}
          {@const isSelected = selectedMuscles.includes(muscle)}
          <button
            on:click={() => toggleMuscle(muscle)}
            class="p-3 rounded-xl border text-sm font-medium transition-all active:scale-95 {isSelected
              ? 'border-transparent bg-zinc-100 text-zinc-900 shadow-[0_0_15px_rgba(255,255,255,0.1)]'
              : 'border-white/5 bg-zinc-900/50 text-zinc-400 hover:bg-zinc-800'}"
          >
            {muscle}
          </button>
        {/each}
      </div>

      <div class="flex gap-3 flex-col">
        <button
          on:click={generatePlan}
          disabled={selectedMuscles.length === 0 || isGenerating}
          class="w-full py-3.5 bg-zinc-100 text-zinc-900 font-semibold rounded-xl hover:bg-white transition-all disabled:opacity-50 disabled:cursor-not-allowed active:scale-[0.98]"
        >
          {isGenerating ? 'Analyzing Fatigue...' : 'Generate Plan'}
        </button>
        <button on:click={startEmptyWorkout} class="w-full py-3.5 bg-transparent border border-white/5 text-zinc-400 font-semibold rounded-xl hover:bg-zinc-900 hover:text-zinc-300 transition-all active:scale-[0.98]">
          Start Empty Workout
        </button>
      </div>
    </div>

  {:else if $currentSession.status === 'draft'}
    <div class="bg-zinc-900/40 backdrop-blur-md border border-white/5 rounded-2xl p-6 relative overflow-hidden">
      <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-amber-500/50 to-transparent"></div>

      <h2 class="text-xl font-semibold tracking-tight mb-1">Review Draft</h2>
      <p class="text-xs text-zinc-500 mb-6">Modify exercises before starting the clock.</p>

      {#if generationWarnings.length > 0}
        <div class="mb-6 space-y-2">
          {#each generationWarnings as warning}
            <div class="bg-rose-500/10 border border-rose-500/20 px-4 py-3 rounded-xl flex items-start gap-3">
              <span class="text-rose-400 mt-0.5 leading-none">⚠️</span>
              <p class="text-sm font-medium tracking-tight text-rose-400/90 leading-snug">{warning}</p>
            </div>
          {/each}
        </div>
      {/if}

      {#if plannedTemplate.length === 0}
        <div class="bg-zinc-900/30 border border-zinc-800/50 border-dashed rounded-xl p-8 text-center mb-6">
          <p class="text-sm text-zinc-500">No exercises added yet.</p>
        </div>
      {:else}
        <div class="space-y-2 mb-8">
          {#each plannedTemplate as exercise, idx}
            <div class="flex justify-between items-center bg-zinc-900/60 p-3.5 rounded-xl border border-white/5 group">
              <div>
                <h4 class="font-medium text-zinc-200 text-sm">{exercise.name}</h4>
                <p class="text-[11px] text-zinc-500 mt-1 uppercase tracking-widest font-semibold">
                  {exercise.target_sets} Sets <span class="text-zinc-700 mx-1">|</span> {exercise.target_reps} Reps
                </p>
              </div>
              <button
                on:click={() => removeExerciseFromDraft(idx)}
                class="text-zinc-600 hover:text-rose-400 p-2 rounded-lg transition-colors"
              >
                ✕
              </button>
            </div>
          {/each}
        </div>
      {/if}

      <div class="mb-8 p-4 bg-zinc-900/40 rounded-xl border border-white/5">
        <label class="block text-[10px] font-bold text-zinc-500 uppercase tracking-widest mb-3">
          Add Exercise
        </label>
        <div class="flex gap-2">
          <select bind:value={selectValue} class="flex-1 bg-zinc-950 border border-white/10 rounded-lg px-3 text-sm text-zinc-300 focus:outline-none focus:border-zinc-500">
            <option value="">Choose exercise...</option>
            {#each exercises as exercise}
              {#if !plannedTemplate.find(e => e.id === exercise.id)}
                <option value={exercise.id}>{exercise.name}</option>
              {/if}
            {/each}
          </select>
          <button on:click={addExerciseToDraft} disabled={!selectValue} class="px-4 py-2 bg-zinc-800 hover:bg-zinc-700 text-zinc-200 text-sm font-medium rounded-lg transition-colors disabled:opacity-50">
            Add
          </button>
        </div>
      </div>

      <div class="flex gap-3">
        <button on:click={activateSession} class="flex-[2] py-3.5 bg-zinc-100 text-zinc-900 font-semibold rounded-xl hover:bg-white transition-all active:scale-[0.98]">
          Start Workout
        </button>
        <button on:click={deleteDraft} class="flex-1 py-3.5 bg-rose-500/10 border border-rose-500/20 text-rose-400 font-semibold rounded-xl hover:bg-rose-500/20 transition-all active:scale-[0.98]">
          Discard
        </button>
      </div>
    </div>

  {:else if $currentSession.status === 'active'}
    <div class="bg-zinc-900/40 backdrop-blur-md border border-white/5 rounded-2xl p-5 mb-6 flex justify-between items-center relative overflow-hidden">
      <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-emerald-500/50 to-transparent"></div>

      <div>
        <h2 class="text-lg font-semibold text-zinc-100">Workout in Progress</h2>
        <p class="text-xs text-zinc-500 mt-1 font-mono">{new Date($currentSession.date).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</p>
      </div>
      <div class="bg-emerald-500/10 border border-emerald-500/20 px-4 py-2 rounded-xl text-center">
        <span class="block text-lg font-bold text-emerald-400 leading-none">{$sessionStats.totalSets}</span>
        <span class="text-[9px] uppercase tracking-widest text-emerald-500/70 font-bold">Sets</span>
      </div>
    </div>

    {#if plannedTemplate.length > 0}
      <div class="mb-8">
        <h3 class="text-[11px] font-bold text-zinc-500 uppercase tracking-widest mb-3 px-1">Today's Agenda</h3>
        <div class="space-y-3">
          {#each plannedTemplate as exercise}
            {@const setsDone = getSetsLoggedForExercise(exercise.id)}
            {@const isComplete = setsDone >= exercise.target_sets}
            {@const isExpanded = selectedExercise?.id === exercise.id}

            <div class="bg-zinc-900/40 border border-white/5 rounded-2xl overflow-hidden transition-all {isExpanded ? 'ring-1 ring-zinc-700 bg-zinc-900/80 shadow-lg' : ''}">
              <button
                on:click={() => { selectedExercise = isExpanded ? null : exercise }}
                class="w-full p-4 flex justify-between items-center hover:bg-zinc-800 transition-all text-left group active:scale-[0.99]"
              >
                <div>
                  <h4 class="font-medium text-sm transition-colors {isExpanded ? 'text-white' : 'text-zinc-200 group-hover:text-white'}">{exercise.name}</h4>
                  <p class="text-[11px] text-zinc-500 mt-1 uppercase tracking-widest font-semibold">
                    Target: {exercise.target_sets} × {exercise.target_reps}
                  </p>
                </div>
                <div class="px-3 py-1 rounded-lg text-[11px] font-bold uppercase tracking-widest {isComplete ? 'bg-emerald-500/10 text-emerald-400' : 'bg-zinc-800 text-zinc-400'}">
                  {setsDone} / {exercise.target_sets}
                </div>
              </button>

              {#if isExpanded}
                <div class="border-t border-white/5 p-4 bg-zinc-950/50">
                  <SetLogger {exercise} on:logged={handleSetLogged} />
                </div>
              {/if}
            </div>
          {/each}
        </div>
      </div>
    {/if}

    <div class="bg-zinc-900/30 rounded-xl border border-white/5 p-4 mb-8">
      <h3 class="text-[10px] font-bold text-zinc-500 uppercase tracking-widest mb-3">Add Ad-hoc Exercise</h3>
      <div class="flex gap-2">
        <select bind:value={selectValue} class="flex-1 bg-zinc-950 border border-white/10 rounded-lg px-3 text-sm text-zinc-300 focus:outline-none">
          <option value="">Choose exercise...</option>
          {#each exercises as exercise}
            <option value={exercise.id}>{exercise.name}</option>
          {/each}
        </select>
        <button
          on:click={addAdHocExercise}
          disabled={!selectValue}
          class="px-4 py-2 bg-zinc-100 text-black text-sm font-bold uppercase tracking-widest rounded-lg transition-colors disabled:opacity-50"
        >
          Add
        </button>
      </div>
    </div>

    {#if $sessionLogs.length > 0}
      <div class="mb-8">
        <h3 class="text-[11px] font-bold text-zinc-500 uppercase tracking-widest mb-3 px-1">Completed Sets</h3>
        <div class="space-y-2 max-h-64 overflow-y-auto pr-1 no-scrollbar">
          {#each [...$sessionLogs].reverse() as log (log.id)}
            {@const exercise = getExerciseById(log.exercise_id)}
            <div class="flex justify-between items-center p-3.5 bg-zinc-900/60 rounded-xl border border-white/5">
              <div>
                <p class="font-medium text-zinc-200 text-sm">{exercise?.name || 'Unknown'}</p>
                <p class="text-[11px] font-semibold text-zinc-500 mt-1 uppercase tracking-widest">
                  {log.reps} × {log.weight} lbs {#if log.rpe}<span class="text-zinc-700 mx-1">|</span> RPE {log.rpe}{/if}
                </p>
              </div>
              <button on:click={() => deleteLog(log.id)} class="text-zinc-600 hover:text-rose-400 p-2 transition-colors">
                ✕
              </button>
            </div>
          {/each}
        </div>
      </div>
    {/if}

    <button on:click={finishSession} class="w-full py-4 bg-rose-500/10 border border-rose-500/20 text-rose-400 font-bold rounded-xl hover:bg-rose-500/20 transition-all active:scale-[0.98]">
      Finish Workout
    </button>
  {/if}
</div>

<style>
  .no-scrollbar::-webkit-scrollbar { display: none; }
  .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
</style>
