<script>
  import { createEventDispatcher } from 'svelte'

  export let exercise

  const dispatch = createEventDispatcher()

  let reps = 8
  let weight = 14
  let rpe = 7
  let notes = ''
  let isSubmitting = false

  async function logSet() {
    if (!reps || !weight) return

    isSubmitting = true
    dispatch('logged', {
      reps: parseInt(reps),
      weight: parseFloat(weight),
      rpe: rpe ? parseInt(rpe) : null,
      notes,
    })

    // Reset form for next set
    reps = 8
    weight = 14
    rpe = 7
    notes = ''
    isSubmitting = false
  }

  function incrementReps(delta) {
    reps = Math.max(1, Math.min(100, reps + delta))
  }

  function incrementWeight(delta) {
    weight = Math.max(0, Math.round((weight + delta) * 100) / 100)
  }
</script>

<div class="pt-2 pb-1 text-zinc-100">
  <div class="grid grid-cols-2 gap-4 mb-6">
    <div>
      <label class="block text-[10px] font-bold text-zinc-500 uppercase tracking-widest mb-3 text-center">Reps</label>
      <div class="flex items-center justify-center gap-2">
        <button on:click={() => incrementReps(-1)} class="w-10 h-10 rounded-xl bg-zinc-800 text-zinc-300 text-lg font-medium hover:bg-zinc-700 active:scale-95 transition-all">
          −
        </button>
        <input
          type="number"
          bind:value={reps}
          min="1"
          max="100"
          class="w-16 bg-transparent text-center text-3xl font-black text-white focus:outline-none"
        />
        <button on:click={() => incrementReps(1)} class="w-10 h-10 rounded-xl bg-zinc-800 text-zinc-300 text-lg font-medium hover:bg-zinc-700 active:scale-95 transition-all">
          +
        </button>
      </div>
    </div>

    <div>
      <label class="block text-[10px] font-bold text-zinc-500 uppercase tracking-widest mb-3 text-center">LBS</label>
      <div class="flex items-center justify-center gap-2">
        <button on:click={() => incrementWeight(-5)} class="w-10 h-10 rounded-xl bg-zinc-800 text-zinc-300 text-xs font-bold hover:bg-zinc-700 active:scale-95 transition-all">
          −5
        </button>
        <input
          type="number"
          bind:value={weight}
          step="2.5"
          min="0"
          class="w-20 bg-transparent text-center text-3xl font-black text-white focus:outline-none"
        />
        <button on:click={() => incrementWeight(5)} class="w-10 h-10 rounded-xl bg-zinc-800 text-zinc-300 text-xs font-bold hover:bg-zinc-700 active:scale-95 transition-all">
          +5
        </button>
      </div>
    </div>
  </div>

  <div class="mb-8">
    <label class="block text-[10px] font-bold text-zinc-500 uppercase tracking-widest mb-3">
      RPE <span class="text-zinc-700 normal-case tracking-normal ml-1">(Optional)</span>
    </label>
    <div class="flex gap-1.5 justify-between">
      {#each [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] as rpeValue}
        <button
          on:click={() => (rpe = rpeValue)}
          class="flex-1 py-2 rounded-lg text-xs font-bold transition-all active:scale-95 {rpe === rpeValue
            ? 'bg-zinc-100 text-black shadow-[0_0_10px_rgba(255,255,255,0.2)]'
            : 'bg-zinc-950 border border-white/5 text-zinc-500 hover:text-zinc-300'}"
        >
          {rpeValue}
        </button>
      {/each}
    </div>
  </div>

  <div class="flex gap-3">
    <div class="flex-1 bg-zinc-950 rounded-xl border border-white/5 px-4 py-3 flex flex-col justify-center">
      <span class="text-[9px] font-bold text-zinc-600 uppercase tracking-widest">Vol</span>
      <span class="text-lg font-black text-zinc-100">{reps * weight}</span>
    </div>

    <button
      on:click={logSet}
      disabled={isSubmitting || !reps || weight === null}
      class="flex-[2] bg-zinc-100 text-zinc-900 font-bold text-sm uppercase tracking-widest rounded-xl hover:bg-white transition-all active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed"
    >
      {isSubmitting ? '...' : 'Log Set'}
    </button>
  </div>
</div>

<style>
  input[type='number'] {
    appearance: textfield;
    -moz-appearance: textfield;
  }
  input[type='number']::-webkit-outer-spin-button,
  input[type='number']::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }
</style>
