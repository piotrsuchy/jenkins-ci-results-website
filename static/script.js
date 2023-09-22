function computeDuration(startTime) {
    const start = new Date(startTime);
    const now = new Date();
    const diffMs = now - start;
    const diffSecs = Math.floor(diffMs / 1000);
    const mins = Math.floor(diffSecs / 60);
    const secs = diffSecs % 60;
    return `${mins} mins ${secs} secs`;
}

function updateDuration() {
    document.querySelectorAll(".test-duration").forEach(td => {
        const startTime = td.getAttribute('data-start-time');
        td.innerText = computeDuration(startTime);
    });

    document.querySelectorAll(".scope-duration").forEach(td => {
        const startTime = td.getAttribute('data-start-time');
        td.innerText = computeDuration(startTime);
    });
}

setInterval(function(){
    $.getJSON("/current_test_data", function(data) {
        for (let entry of data) {
            $(`#testNameElement_${entry.setup_id}`).text(entry.test_name);
            $(`#scopeNameElement_${entry.setup_id}`).text(entry.scope_name);

            // Update start times for duration computation. 
            // We use `.closest('tr')` to ensure we are only updating the duration in the same row.
            $(`#testNameElement_${entry.setup_id}`).closest('tr').find('.test-duration').attr('data-start-time', entry.test_start_time);
            $(`#testNameElement_${entry.setup_id}`).closest('tr').find('.scope-duration').attr('data-start-time', entry.scope_start_time);
        }
    });
}, 10000);



setInterval(updateDuration, 1000)