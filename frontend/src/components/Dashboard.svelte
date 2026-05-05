<script>
  import { onMount } from 'svelte'
  import { muscleStatus, loading } from '../lib/stores'
  import { api } from '../lib/api'

  let fatigue = {}
  let fatigueRecovery = {}
  let recentWorkouts = []

  const muscleGroups = ['Chest', 'Back', 'Legs', 'Shoulders', 'Biceps', 'Triceps', 'Core', 'Forearms']

  onMount(async () => {
    await loadDashboard()
  })

  async function loadDashboard() {
    loading.set(true)
    try {
      const status = await api.getStatus()
      fatigue = status
      muscleStatus.set(status)

      // Get last 3 workouts
      recentWorkouts = await api.getWorkoutHistory(3)

      for (const muscle of muscleGroups) {
        try {
          const recovery = await api.getFatigueTrend(muscle)
          fatigueRecovery[muscle] = recovery
        } catch (err) {}
      }
    } catch (err) {
      console.error('Failed to load dashboard:', err)
    } finally {
      loading.set(false)
    }
  }

  function isRedZoned(muscle) { return (fatigue[muscle] || 0) >= 10.0 }

  function getFatigueColor(value) {
    if (value < 3) return 'text-emerald-400'
    if (value < 6) return 'text-amber-400'
    if (value < 9) return 'text-orange-500'
    return 'text-rose-500'
  }

  function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric'
    })
  }

  function formatTime(minutes) {
    if (!minutes) return '-';
    if (minutes < 60) return `${minutes}m`;
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return `${hours}h ${mins}m`;
  }
</script>

<div class="space-y-10 pb-24 px-2 sm:px-0 text-zinc-100 font-sans tracking-tight">

  <section>
    <div class="flex justify-between items-end mb-6 px-1">
      <div>
        <h2 class="text-2xl font-semibold tracking-tight">Recovery Status</h2>
        <p class="text-xs text-zinc-500 mt-1 uppercase tracking-widest font-medium">Live Fatigue Tracking</p>
      </div>
      <button
        on:click={loadDashboard}
        class="text-xs bg-zinc-800/50 hover:bg-zinc-700/50 text-zinc-300 px-3 py-1.5 rounded-full border border-white/5 transition-all active:scale-95"
      >
        Sync
      </button>
    </div>

    <div class="grid grid-cols-2 md:grid-cols-4 md:gap-4 gap-3">
      {#each muscleGroups as muscle (muscle)}
        {@const f = fatigue[muscle] || 0}
        {@const isRed = isRedZoned(muscle)}
        {@const recovery = fatigueRecovery[muscle]}

        <div class="bg-zinc-900/40 backdrop-blur-md border border-white/5 rounded-2xl p-4 flex flex-col relative overflow-hidden transition-all hover:bg-zinc-900/60 min-h-[120px]">

          <div class="absolute top-4 right-4 flex items-center justify-center">
            <span class="relative flex h-2.5 w-2.5">
              {#if isRed}
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-500 opacity-75"></span>
                <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-rose-500"></span>
              {:else}
                <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500/80 shadow-[0_0_8px_rgba(16,185,129,0.5)]"></span>
              {/if}
            </span>
          </div>

          <h3 class="font-medium text-sm text-zinc-200 mb-1">{muscle}</h3>

          <div class="my-auto">
            <div class="flex items-baseline gap-1">
              <span class="text-3xl font-bold {getFatigueColor(f)}">{f.toFixed(1)}</span>
              <span class="text-sm text-zinc-600 font-medium">/ 10</span>
            </div>
          </div>

          <div class="mt-auto">
            {#if isRed}
              <p class="text-[10px] text-rose-400/80 font-medium leading-tight mt-1">
                Needs rest
                {#if recovery?.estimated_recovery_hours > 0}
                  <span class="text-zinc-500 block">~{recovery.estimated_recovery_hours}h left</span>
                {/if}
              </p>
            {:else}
              <p class="text-[10px] text-emerald-400/70 font-medium mt-1">Can train</p>
            {/if}
          </div>
        </div>
      {/each}
    </div>
  </section>

  <section>
    <div class="mb-5 px-1">
      <h2 class="text-2xl font-semibold tracking-tight">Recent Activity</h2>
    </div>

    {#if recentWorkouts.length === 0}
      <div class="bg-zinc-900/30 border border-zinc-800/50 border-dashed rounded-2xl p-8 flex flex-col items-center justify-center text-center">
        <span class="text-2xl mb-2 opacity-50">📉</span>
        <p class="text-sm text-zinc-500">No recent workouts found.</p>
      </div>
    {:else}
      <div class="space-y-3">
        {#each recentWorkouts as workout}
          <div class="group bg-zinc-900/40 backdrop-blur-md border border-white/5 rounded-2xl p-4 flex items-center justify-between transition-all hover:bg-zinc-800/60 cursor-default">

            <div class="flex items-center gap-4">
              <div class="w-10 h-10 rounded-xl bg-zinc-800/80 border border-zinc-700/50 flex flex-col items-center justify-center">
                <span class="text-[10px] text-zinc-500 uppercase font-bold leading-none mb-0.5">
                  {new Date(workout.date).toLocaleDateString('en-US', { month: 'short' })}
                </span>
                <span class="text-sm text-zinc-200 font-bold leading-none">
                  {new Date(workout.date).getDate()}
                </span>
              </div>

              <div>
                <h3 class="font-medium text-zinc-200 text-sm">{formatDate(workout.date)}</h3>

                <div class="flex items-center gap-2 mt-0.5">
                  <p class="text-xs text-zinc-500">{workout.total_sets || 0} sets</p>
                  <span class="w-1 h-1 rounded-full bg-zinc-700"></span>
                  <p class="text-xs text-zinc-500">{formatTime(workout.duration_minutes)}</p>
                </div>
              </div>
            </div>

            <div class="text-right">
              <span class="text-sm font-semibold text-zinc-300">{workout.total_volume || 0}</span>
              <span class="text-xs text-zinc-600 block">lbs vol</span>
            </div>

          </div>
        {/each}
      </div>
    {/if}
  </section>
</div>
