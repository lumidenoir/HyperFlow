<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { fetchAPI } from '$lib/api';
    import { activeSession, plannedExercises } from '$lib/store';

    let muscleStatus = {};
    let priorityGroups = ['Chest', 'Triceps']; // Default selection
    let isGenerating = false;

    const availableMuscles = ['Chest', 'Back', 'Legs', 'Shoulders', 'Biceps', 'Triceps', 'Core'];

    onMount(async () => {
        try {
            muscleStatus = await fetchAPI('/status');
        } catch (e) {
            console.error("Make sure FastAPI is running!", e);
        }
    });

    function togglePriority(muscle) {
        if (priorityGroups.includes(muscle)) {
            priorityGroups = priorityGroups.filter(m => m !== muscle);
        } else {
            priorityGroups = [...priorityGroups, muscle];
        }
    }

    async function startWorkout() {
        if (priorityGroups.length === 0) return alert("Select at least one muscle group!");

        isGenerating = true;
        try {
            // 1. Generate the plan
            const planRes = await fetchAPI(`/session/generate?` + new URLSearchParams(priorityGroups.map(g => ['priority_groups', g])));
            plannedExercises.set(planRes.recommendations || []);

            // 2. Start the backend session
            const session = await fetchAPI('/session/start', { method: 'POST' });
            activeSession.set(session);

            // 3. Move to execution screen
            goto('/workout');
        } catch (e) {
            alert("Failed to start session. " + e.message);
        } finally {
            isGenerating = false;
        }
    }
</script>

<header class="mb-8 border-b border-gray-800 pb-4">
    <h1 class="text-3xl font-bold tracking-tight text-white">Hypertrophy Planner</h1>
</header>

<section class="mb-8">
    <h2 class="text-lg font-semibold mb-4 text-gray-300">Current Fatigue Levels</h2>
    <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
        {#each Object.entries(muscleStatus) as [muscle, fatigue]}
            <div class="p-3 rounded-lg border border-gray-800 bg-gray-900 flex flex-col">
                <span class="text-sm font-medium text-gray-400">{muscle}</span>
                <span class="text-xl font-bold {fatigue > 8 ? 'text-red-400' : fatigue > 4 ? 'text-yellow-400' : 'text-green-400'}">
                    {fatigue.toFixed(1)} <span class="text-xs text-gray-500 font-normal">/ 10</span>
                </span>
            </div>
        {/each}
    </div>
</section>

<section class="mb-8 bg-gray-900 border border-gray-800 p-5 rounded-xl">
    <h2 class="text-lg font-semibold mb-4 text-white">Plan Today's Session</h2>
    <div class="flex flex-wrap gap-2 mb-6">
        {#each availableMuscles as muscle}
            <button
                class="px-4 py-2 rounded-full text-sm font-medium transition-colors border {priorityGroups.includes(muscle) ? 'bg-blue-600 border-blue-500 text-white' : 'bg-transparent border-gray-700 text-gray-400 hover:border-gray-500'}"
                on:click={() => togglePriority(muscle)}
            >
                {muscle}
            </button>
        {/each}
    </div>

    <button
        on:click={startWorkout}
        disabled={isGenerating}
        class="w-full bg-white text-black font-bold py-3 rounded-lg hover:bg-gray-200 transition-colors disabled:opacity-50"
    >
        {isGenerating ? 'Analyzing Fatigue...' : 'Generate & Start Workout'}
    </button>
</section>
