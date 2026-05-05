<script>
  import { createEventDispatcher } from 'svelte'
  import { isSessionActive } from '../lib/stores'

  export let currentPage = 'dashboard'
  const dispatch = createEventDispatcher()

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: '📊' },
    { id: 'session', label: 'Workout', icon: '🏋️' },
    { id: 'history', label: 'History', icon: '📝' },
    { id: 'exercises', label: 'Exercises', icon: '🔨' },
  ]

  function navigate(page) {
    currentPage = page
    dispatch('navigate', page)
  }
</script>

<nav class="fixed bottom-0 left-0 right-0 bg-zinc-950/80 backdrop-blur-xl border-t border-white/5 z-40 pb-[env(safe-area-inset-bottom)]">
  <div class="max-w-7xl mx-auto px-2">
    <div class="flex justify-around items-center h-16">
      {#each navItems as item (item.id)}
        <button
          on:click={() => navigate(item.id)}
          class="relative flex-1 h-full flex flex-col items-center justify-center transition-all duration-300 {currentPage === item.id
            ? 'text-zinc-100'
            : 'text-zinc-600 hover:text-zinc-400'}"
        >
          <div class="text-xl mb-1 transition-transform {currentPage === item.id ? 'scale-110' : 'scale-100 grayscale opacity-60'}">
            {item.icon}
          </div>
          <div class="text-[10px] font-bold tracking-widest uppercase">{item.label}</div>

          {#if item.id === 'session' && $isSessionActive}
            <div class="absolute top-2 right-[30%] w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse shadow-[0_0_8px_rgba(16,185,129,0.8)]"></div>
          {/if}
        </button>
      {/each}
    </div>
  </div>
</nav>

<div class="h-24"></div>
