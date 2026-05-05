<script>
  export let value = 0
  export let max = 10

  $: percentage = Math.min((value / max) * 100, 100)
  $: color = value < 3 ? '#10b981' : value < 6 ? '#f59e0b' : value < 9 ? '#ef6f0b' : '#dc2626'
</script>

<div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3 overflow-hidden">
  <div
    style="width: {percentage}%; background-color: {color}; transition: width 0.3s ease"
    class="h-full rounded-full"
  />
</div>

<style>
  div {
    background: linear-gradient(90deg, #f3f4f6 0%, #e5e7eb 100%);
  }
</style>
