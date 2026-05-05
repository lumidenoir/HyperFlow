<script>
  import { error, successMessage } from '../lib/stores'
  import { fly } from 'svelte/transition'
</script>

{#if $error}
  <div transition:fly={{ y: 50, duration: 300 }} class="fixed bottom-24 left-1/2 -translate-x-1/2 z-50 w-full max-w-sm px-4 pointer-events-none">
    <div class="bg-zinc-900/90 backdrop-blur-xl border border-rose-500/20 p-4 rounded-2xl shadow-2xl flex items-center gap-3">
      <span class="text-rose-500 bg-rose-500/10 rounded-full w-6 h-6 flex items-center justify-center text-xs">✕</span>
      <span class="text-sm font-medium text-zinc-200 tracking-tight leading-snug">{$error}</span>
    </div>
  </div>
{/if}

{#if $successMessage}
  <div transition:fly={{ y: 50, duration: 300 }} class="fixed bottom-24 left-1/2 -translate-x-1/2 z-50 w-full max-w-sm px-4 pointer-events-none">
    <div class="bg-zinc-900/90 backdrop-blur-xl border border-emerald-500/20 p-4 rounded-2xl shadow-2xl flex items-center gap-3">
      <span class="text-emerald-400 bg-emerald-500/10 rounded-full w-6 h-6 flex items-center justify-center text-xs">✓</span>
      <span class="text-sm font-medium text-zinc-200 tracking-tight leading-snug">{$successMessage}</span>
    </div>
  </div>
{/if}
