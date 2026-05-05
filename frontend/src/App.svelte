<script>
  import { onMount } from 'svelte'
  import { currentSession, loading, error, successMessage, isSessionActive } from './lib/stores'
  import { api } from './lib/api'
  import Dashboard from './components/Dashboard.svelte'
  import Session from './components/Session.svelte'
  import History from './components/History.svelte'
  import Exercises from './components/Exercises.svelte'
  import Navigation from './components/Navigation.svelte'
  import Toast from './components/Toast.svelte'

  let currentPage = 'dashboard'
  let backendConnected = false
  let isInitializing = true // NEW: Prevents UI flashing during the initial check

  onMount(async () => {
    try {
      await api.getHealth()
      backendConnected = true

      // NEW: Check for an ongoing session right when the app loads
      try {
        const session = await api.getCurrentSession()
        currentSession.set(session)

        // If there is an active workout or a draft, jump straight to the workout tab
        if (session && (session.status === 'active' || session.status === 'draft')) {
          currentPage = 'session'
        }
      } catch (sessionErr) {
        // api.js throws an error if no session is found, which is completely normal.
        currentSession.set(null)
      }

    } catch (err) {
      console.error('Backend connection failed:', err)
      backendConnected = false
    } finally {
      isInitializing = false
    }
  })

  function handleNavigate(event) {
    currentPage = event.detail
  }
</script>

<div class="min-h-screen flex flex-col bg-zinc-950 text-zinc-100 font-sans selection:bg-zinc-800 selection:text-zinc-100">

  {#if !backendConnected && !isInitializing}
    <div class="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div class="bg-zinc-900 border border-white/10 rounded-2xl p-6 max-w-md w-full shadow-2xl">
        <h2 class="text-xl font-bold mb-2 text-rose-500">Backend Offline</h2>
        <p class="text-zinc-400 text-sm mb-4">
          Make sure the FastAPI backend is running on http://localhost:5100
        </p>
        <div class="bg-black/50 p-3 rounded-lg border border-white/5 font-mono text-xs text-zinc-300">
          python main.py
        </div>
      </div>
    </div>
  {/if}

  <header class="sticky top-0 z-30 bg-zinc-950/80 backdrop-blur-xl border-b border-white/5">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 bg-zinc-100 rounded-lg flex items-center justify-center shadow-[0_0_15px_rgba(255,255,255,0.2)]">
            <span class="text-black font-bold text-sm">HP</span>
          </div>
          <h1 class="text-xl font-bold text-zinc-100 tracking-tight">Hypertrophy</h1>
        </div>
        {#if $isSessionActive}
          <div class="px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-[10px] font-bold tracking-widest uppercase flex items-center gap-2">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
            Active
          </div>
        {/if}
      </div>
    </div>
  </header>

  <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
    {#if !isInitializing}
      {#if currentPage === 'dashboard'}
        <Dashboard on:navigate={handleNavigate} />
      {:else if currentPage === 'session'}
        <Session on:navigate={handleNavigate} />
      {:else if currentPage === 'history'}
        <History on:navigate={handleNavigate} />
      {:else if currentPage === 'exercises'}
        <Exercises on:navigate={handleNavigate} />
      {/if}
    {/if}
  </main>

  <Navigation {currentPage} on:navigate={handleNavigate} />
  <Toast />

  {#if $loading || isInitializing}
    <div class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-40 transition-opacity">
      <div class="bg-zinc-900 border border-white/10 rounded-2xl px-6 py-4 flex items-center gap-4 shadow-2xl">
        <div class="w-5 h-5 border-2 border-zinc-500 border-t-zinc-100 rounded-full animate-spin"></div>
        <span class="text-zinc-300 text-sm font-medium tracking-wide">
          {isInitializing ? 'Connecting...' : 'Syncing...'}
        </span>
      </div>
    </div>
  {/if}
</div>

<style>
  :global(body) {
    background-color: #09090b; /* zinc-950 */
    margin: 0;
  }
</style>
