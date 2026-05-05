<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { activeSession, plannedExercises } from '$lib/store';
    import { fetchAPI } from '$lib/api';

    let currentExerciseIndex = 0;

    // Form binds
    let reps = 10;
    let weight = 0;
    let rpe = 8;

    let isSaving = false;
    let completedSets = [];

    $: currentExercise = $plannedExercises[currentExerciseIndex];
    $: sessionActive = $activeSession !== null;

    onMount(() => {
        if (!sessionActive || $plannedExercises.length === 0) {
            goto('/'); // Redirect home if refreshed or lost state
        }
    });

    async function logSet() {
        if (!currentExercise) return;
        isSaving = true;

        const payload = {
            session_id: $activeSession.id,
            exercise_id: currentExercise.id,
            reps,
            weight,
            rpe
        };

        try {
            await fetchAPI('/session/log-set', {
                method: 'POST',
                body: JSON.stringify(payload)
            });

            // Add to local UI array so user sees what they just did
            completedSets = [...completedSets, { ...payload, name: currentExercise.name }];
        } catch (e) {
            alert("Failed to log set!");
        } finally {
            isSaving = false;
        }
    }

    function nextExercise() {
        if (currentExerciseIndex < $plannedExercises.length - 1) {
            currentExerciseIndex++;
        }
    }

    async function finishWorkout() {
        if (!confirm("End session and calculate fatigue?")) return;

        try {
            await fetchAPI(`/session/finish/${$activeSession.id}`, { method: 'POST' });
            activeSession.set(null);
            plannedExercises.set([]);
            goto('/');
        } catch (e) {
            alert("Failed to finalize workout.");
        }
    }
</script>

{#if currentExercise}
    <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold text-white">Active Session</h1>
        <button on:click={finishWorkout} class="bg-red-500/20 text-red-400 px-4 py-2 rounded-lg font-medium hover:bg-red-500/30">Finish</button>
    </div>

    <div class="bg-blue-900/20 border border-blue-800/50 rounded-xl p-6 mb-6">
        <h2 class="text-3xl font-bold text-blue-400 mb-1">{currentExercise.name}</h2>
        <p class="text-gray-400 text-sm mb-6">Primary: {currentExercise.primary_muscle}</p>

        <div class="grid grid-cols-3 gap-4 mb-6">
            <div>
                <label class="block text-xs text-gray-500 mb-1">Reps</label>
                <input type="number" bind:value={reps} class="w-full bg-gray-900 border border-gray-700 rounded p-3 text-white text-center text-xl font-mono" />
            </div>
            <div>
                <label class="block text-xs text-gray-500 mb-1">Weight</label>
                <input type="number" bind:value={weight} step="2.5" class="w-full bg-gray-900 border border-gray-700 rounded p-3 text-white text-center text-xl font-mono" />
            </div>
            <div>
                <label class="block text-xs text-gray-500 mb-1">RPE</label>
                <input type="number" bind:value={rpe} min="1" max="10" class="w-full bg-gray-900 border border-gray-700 rounded p-3 text-white text-center text-xl font-mono" />
            </div>
        </div>

        <button
            on:click={logSet}
            disabled={isSaving}
            class="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-4 rounded-lg text-lg transition-colors"
        >
            {isSaving ? 'Saving...' : 'Log Set'}
        </button>
    </div>

    <div class="flex justify-between items-center bg-gray-900 p-4 rounded-lg border border-gray-800">
        <span class="text-gray-400">Exercise {currentExerciseIndex + 1} of {$plannedExercises.length}</span>
        <button
            on:click={nextExercise}
            disabled={currentExerciseIndex >= $plannedExercises.length - 1}
            class="text-white font-medium disabled:opacity-30"
        >
            Next Exercise &rarr;
        </button>
    </div>

    {#if completedSets.length > 0}
        <div class="mt-8">
            <h3 class="text-sm font-semibold text-gray-500 mb-3 uppercase tracking-wider">Logged Sets</h3>
            <div class="space-y-2">
                {#each [...completedSets].reverse() as set, i}
                    <div class="flex justify-between p-3 bg-gray-900 rounded border border-gray-800 text-sm">
                        <span class="font-medium text-gray-300">{set.name}</span>
                        <span class="text-gray-400 font-mono">{set.reps} reps @ {set.weight} <span class="text-xs">RPE {set.rpe}</span></span>
                    </div>
                {/each}
            </div>
        </div>
    {/if}
{/if}
