<script>
  import { onMount } from 'svelte'
  import { loading } from '../lib/stores'
  import { api } from '../lib/api'
  import { showSuccess, showError } from '../lib/stores'

  let exercises = []
  let showNewForm = false
  let editingId = null
  let selectedMuscleFilter = null

  let formData = {
    name: '',
    primary_muscle: 'Chest',
    secondary_muscle: '',
    fatigue_rating: 1.5,
    notes: '',
  }

  const muscleGroups = [
    'Chest',
    'Back',
    'Legs',
    'Shoulders',
    'Biceps',
    'Triceps',
    'Core',
    'Forearms'
  ]

  onMount(async () => {
    await loadExercises()
  })

  async function loadExercises() {
    loading.set(true)
    try {
      const data = await api.getExercises()
      exercises = data
    } catch (err) {
      showError('Failed to load exercises')
    } finally {
      loading.set(false)
    }
  }

  async function saveExercise() {
    if (!formData.name || !formData.primary_muscle) {
      showError('Name and primary muscle are required')
      return
    }

    loading.set(true)
    try {
      if (editingId) {
        await api.updateExercise(editingId, formData)
        showSuccess('Exercise updated')
      } else {
        await api.createExercise(formData)
        showSuccess('Exercise created')
      }
      resetForm()
      await loadExercises()
    } catch (err) {
      showError(err.message)
    } finally {
      loading.set(false)
    }
  }

  async function deleteExercise(id) {
    if (!confirm('Delete this exercise?')) return

    loading.set(true)
    try {
      await api.deleteExercise(id)
      showSuccess('Exercise deleted')
      await loadExercises()
    } catch (err) {
      showError('Failed to delete exercise')
    } finally {
      loading.set(false)
    }
  }

  function editExercise(exercise) {
    editingId = exercise.id
    formData = { ...exercise }
    showNewForm = true
  }

  function resetForm() {
    showNewForm = false
    editingId = null
    formData = {
      name: '',
      primary_muscle: 'Chest',
      secondary_muscle: '',
      fatigue_rating: 1.5,
      notes: '',
    }
  }

  function getFilteredExercises() {
    if (!selectedMuscleFilter) return exercises
    return exercises.filter(
      e =>
        e.primary_muscle === selectedMuscleFilter ||
        e.secondary_muscle === selectedMuscleFilter
    )
  }
</script>

<div class="space-y-8 pb-24 text-zinc-100 font-sans tracking-tight">
  <div class="flex justify-between items-center px-1">
    <h2 class="text-2xl font-semibold tracking-tight text-zinc-100">Exercises</h2>
    {#if !showNewForm}
      <button on:click={() => (showNewForm = true)} class="bg-zinc-100 text-zinc-900 px-4 py-2 rounded-xl text-sm font-bold active:scale-95 transition-all">
        + New
      </button>
    {/if}
  </div>

  {#if showNewForm}
    <div class="bg-zinc-900/40 backdrop-blur-md border border-white/5 rounded-2xl p-6">
      <h3 class="font-semibold text-xl text-zinc-100 mb-6">
        {editingId ? 'Edit Exercise' : 'New Exercise'}
      </h3>

      <div class="space-y-5">
        <div>
          <label class="block text-[10px] font-bold text-zinc-500 uppercase tracking-widest mb-2">Exercise Name *</label>
          <input type="text" bind:value={formData.name} placeholder="e.g., Barbell Bench Press" class="w-full bg-zinc-950 border border-white/10 rounded-xl px-4 py-3 text-sm text-zinc-200 placeholder-zinc-700 focus:outline-none focus:border-zinc-500 transition-colors" />
        </div>

        <div>
          <label class="block text-[10px] font-bold text-zinc-500 uppercase tracking-widest mb-2">Primary Muscle *</label>
          <select bind:value={formData.primary_muscle} class="w-full bg-zinc-950 border border-white/10 rounded-xl px-4 py-3 text-sm text-zinc-200 focus:outline-none focus:border-zinc-500 transition-colors appearance-none">
            {#each muscleGroups as muscle}
              <option value={muscle}>{muscle}</option>
            {/each}
          </select>
        </div>

        <div>
          <label class="block text-[10px] font-bold text-zinc-500 uppercase tracking-widest mb-2">Secondary Muscle</label>
          <select bind:value={formData.secondary_muscle} class="w-full bg-zinc-950 border border-white/10 rounded-xl px-4 py-3 text-sm text-zinc-200 focus:outline-none focus:border-zinc-500 transition-colors appearance-none">
            <option value="">None</option>
            {#each muscleGroups as muscle}
              <option value={muscle}>{muscle}</option>
            {/each}
          </select>
        </div>

        <div>
          <label class="block text-[10px] font-bold text-zinc-500 uppercase tracking-widest mb-2">Fatigue Rating (0.1 - 10.0)</label>
          <input type="number" bind:value={formData.fatigue_rating} min="0.1" max="10" step="0.1" class="w-full bg-zinc-950 border border-white/10 rounded-xl px-4 py-3 text-sm text-zinc-200 focus:outline-none focus:border-zinc-500 transition-colors" />
        </div>

        <div>
          <label class="block text-[10px] font-bold text-zinc-500 uppercase tracking-widest mb-2">Notes</label>
          <textarea bind:value={formData.notes} placeholder="Optional notes..." class="w-full bg-zinc-950 border border-white/10 rounded-xl px-4 py-3 text-sm text-zinc-200 placeholder-zinc-700 focus:outline-none focus:border-zinc-500 transition-colors h-24 resize-none" />
        </div>

        <div class="flex gap-3 pt-4">
          <button on:click={saveExercise} class="flex-[2] py-3.5 bg-zinc-100 text-zinc-900 font-bold rounded-xl hover:bg-white transition-all active:scale-[0.98]">
            {editingId ? 'Save Updates' : 'Create Exercise'}
          </button>
          <button on:click={resetForm} class="flex-1 py-3.5 bg-zinc-800 text-zinc-300 font-bold rounded-xl hover:bg-zinc-700 transition-all active:scale-[0.98]">
            Cancel
          </button>
        </div>
      </div>
    </div>
  {/if}

  <div class="px-1">
    <div class="flex gap-2 overflow-x-auto pb-2 no-scrollbar snap-x">
      <button
        on:click={() => (selectedMuscleFilter = null)}
        class="snap-start shrink-0 px-4 py-2 rounded-xl text-[11px] font-bold uppercase tracking-widest transition-all {selectedMuscleFilter === null ? 'bg-zinc-100 text-zinc-900' : 'bg-zinc-900/50 text-zinc-500 border border-white/5 hover:bg-zinc-800'}"
      >
        All
      </button>
      {#each muscleGroups as muscle}
        <button
          on:click={() => (selectedMuscleFilter = muscle)}
          class="snap-start shrink-0 px-4 py-2 rounded-xl text-[11px] font-bold uppercase tracking-widest transition-all {selectedMuscleFilter === muscle ? 'bg-zinc-100 text-zinc-900' : 'bg-zinc-900/50 text-zinc-500 border border-white/5 hover:bg-zinc-800'}"
        >
          {muscle}
        </button>
      {/each}
    </div>
  </div>

  {#if getFilteredExercises().length === 0}
    <div class="bg-zinc-900/30 border border-zinc-800/50 border-dashed rounded-2xl p-8 flex flex-col items-center justify-center text-center">
      <p class="text-sm text-zinc-500">No exercises found.</p>
    </div>
  {:else}
    <div class="space-y-3">
      {#each getFilteredExercises() as exercise (exercise.id)}
        <div class="bg-zinc-900/40 backdrop-blur-md border border-white/5 rounded-2xl p-5 flex justify-between items-start group">
          <div class="flex-1">
            <h3 class="font-medium text-zinc-200 mb-2">
              {exercise.name}
            </h3>
            <div class="flex gap-2 flex-wrap mb-3">
              <span class="px-2 py-0.5 rounded-md bg-zinc-800 border border-zinc-700 text-[10px] font-bold uppercase tracking-widest text-zinc-400">{exercise.primary_muscle}</span>
              {#if exercise.secondary_muscle}
                <span class="px-2 py-0.5 rounded-md bg-zinc-900 border border-zinc-800 text-[10px] font-bold uppercase tracking-widest text-zinc-500">{exercise.secondary_muscle}</span>
              {/if}
            </div>

            {#if exercise.notes}
              <p class="text-xs text-zinc-500 leading-relaxed mb-2 max-w-sm">
                {exercise.notes}
              </p>
            {/if}
            <p class="text-[10px] font-bold uppercase tracking-widest text-zinc-600 mt-3">
              Fatigue Multiplier: <span class="text-zinc-400">{exercise.fatigue_rating}</span>
            </p>
          </div>

          <div class="flex flex-col gap-2 ml-4">
            <button on:click={() => editExercise(exercise)} class="w-10 h-10 rounded-xl bg-zinc-800/50 hover:bg-zinc-700 text-zinc-400 flex items-center justify-center transition-colors">
              ✎
            </button>
            <button on:click={() => deleteExercise(exercise.id)} class="w-10 h-10 rounded-xl bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 flex items-center justify-center transition-colors">
              ✕
            </button>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .no-scrollbar::-webkit-scrollbar { display: none; }
  .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
</style>
