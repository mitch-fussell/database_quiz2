document.addEventListener('DOMContentLoaded', function() {
    const playerSelect = document.getElementById('playerSelect');
    const playerInfo = document.getElementById('playerInfo');

    fetch('/players')
        .then(response => response.json())
        .then(players => {
            playerSelect.innerHTML = '<option value="">Select a player</option>';
            players.forEach(player => {
                const option = document.createElement('option');
                option.value = player.id;
                option.textContent = player.name;
                playerSelect.appendChild(option);
            });
        });

    playerSelect.addEventListener('change', function() {
        const selected = playerSelect.options[playerSelect.selectedIndex];
        if (selected.value) {
            playerInfo.textContent = `Selected Player: ${selected.textContent}`;
        } else {
            playerInfo.textContent = '';
        }
    });
});
