new Vue({
    el: '#app',
    data: {
        matches: []
    },
    created() {
        this.fetchMatches();
    },
    methods: {
        fetchMatches() {
            fetch('https://api.example.com/matches') // 替换为实际的API URL
                .then(response => response.json())
                .then(data => {
                    this.matches = data;
                })
                .catch(error => console.error('Error fetching matches:', error));
        }
    }
});
