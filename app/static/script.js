function computeDuration(startTime) {
    const start = new Date(startTime);
    const now = new Date();
    const diffMs = now - start;
    const diffSecs = Math.floor(diffMs / 1000);
    const mins = Math.floor(diffSecs / 60);
    const secs = diffSecs % 60;
    return `${mins} mins ${secs} secs`;
}

function resetRow(setup_id) {
    $(`#testNameElement_${setup_id}`).text("Not running");
    $(`#scopeNameElement_${setup_id}`).text("Not running");
    $(`#progressElement_${setup_id}`).text("0/0")
    $(`#testNameElement_${setup_id}`).closest('tr').find('.test-duration').text("---");
    $(`#testNameElement_${setup_id}`).closest('tr').find('.scope-duration').text("---");
}

let runningSetups = new Set(); // Define runningSetups at the top level of your script

function updateDuration() {
    console.log("Updating durations...");
    document.querySelectorAll(".test-duration, .scope-duration").forEach(td => {

        const startTime = td.getAttribute('data-start-time');
        const setupId = td.closest('tr').getAttribute('data-setup-id');
        
        console.log(`Start Time for setupId ${setupId}:`, startTime);
        
        if (runningSetups.has(parseInt(setupId))) {
            const duration = computeDuration(startTime);
            console.log(`Computed Duration for setupId ${setupId}:`, duration);
            
            // If duration is falsy (e.g. empty string, null, undefined), set to '-' as a fallback
            td.innerText = duration || '-';
            console.log(`Updated Duration Element for setupId ${setupId}:`, td);
        } else {
            console.log(`Setup ID ${setupId} is not in the runningSetups set.`);
        }
    });
}



// Extracting all the setup_ids from the setups_config.json
const allSetupIds = [];
const setupsConfig = {
  "pipelines": [
    {
      "setup": "LOCALHOST",
      "setup_id": 1,
      "job_name": "CI_robot_AVQL_Regression_Tests_CIT_RFP_rexIO",
      "ip": "127.0.0.1",
      "URL": "",
      "comment": "Placeholder for localhost"
    },
  ]
};


for (const pipeline of setupsConfig.pipelines) {
    allSetupIds.push(pipeline.setup_id);  // Assuming 'setup' is the unique identifier for each pipeline
}

function showPopup(setupId) {
    fetch(`/jenkins_data/${setupId}`)
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.text();
    })
    .then(data => {
        try {
            return JSON.parse(data);
        } catch (e) {
            throw new Error("Failed to parse JSON");
        }
    })
    .then(data => {
        let buildsContent = document.getElementById(`buildsContent_${setupId}`);
        buildsContent.innerHTML = ""; // Clear previous data

        data.forEach(build => {
            let buildInfo = `
                <h3>URL: <a href="${build.url}" target="_blank">${build.url}</a></h3>
                <p>Tests: ${build.passed_tests} / ${build.total_tests}</p>
                <p>Date: ${formatDate(build.timestamp)}</p>
                <p>Duration: ${formatDuration(build.duration)}</p>
                <hr>
            `;
            buildsContent.innerHTML += buildInfo;
        });

        document.getElementById(`myPopup_${setupId}`).style.display = "block";
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}


function closePopup(setupId) {
    document.getElementById(`myPopup_${setupId}`).style.display = "none";
}

// ... [rest of the JavaScript code remains unchanged]


function formatDate(timestamp) {
    const date = new Date(timestamp * 1000);
    const hours = padNumber(date.getHours());
    const minutes = padNumber(date.getMinutes());
    const seconds = padNumber(date.getSeconds());
    return `${date.getDate()}.${date.getMonth() + 1}.${date.getFullYear()} ${hours}:${minutes}:${seconds}`;
}

function padNumber(num) {
    return num < 10 ? '0' + num : num;
}

function formatDuration(duration) {
    const hours = Math.floor(duration / 3600);
    const minutes = Math.floor((duration % 3600) / 60);
    const seconds = Math.floor(duration % 60);
    return `${padNumber(hours)}:${padNumber(minutes)}:${padNumber(seconds)}`;
}

setInterval(function(){
    $.getJSON("/api/current_test_data", function(data) {
        console.log("Received data:", data);

        let currentlyRunningSetups = new Set();

        if (data.length === 0) {
            // If there are no entries in the data, reset all the rows
            runningSetups.forEach(setup_id => {
                resetRow(setup_id);
            });
            runningSetups = new Set();
        } else {
            for (let entry of data) {
                currentlyRunningSetups.add(entry.setup_id);

                // Update scope name and its duration
                $(`#scopeNameElement_${entry.setup_id}`).text(entry.scope_name || "Nothing");
                $(`#scopeNameElement_${entry.setup_id}`).closest('tr').find('.scope-duration').attr('data-start-time', entry.scope_start_time);

                // Update test name and its duration based on the scope status
                let testName, testStartTime;
                if (entry.scope_status === 'running') {
                    testName = entry.test_name || "Suite Startup";
                    testStartTime = entry.test_start_time || entry.scope_start_time;
                } else if (entry.scope_status === 'startup') {
                    testName = "Suite Startup";
                    testStartTime = "TBA"
                } else if (entry.scope_status === 'teardown') {
                    testName = "Suite Teardown";
                    testStartTime = "TBA"
                } else {
                    testName = "Nothing";
                    testStartTime = '';
                }

                $(`#testNameElement_${entry.setup_id}`).text(testName);
                $(`#testNameElement_${entry.setup_id}`).closest('tr').find('.test-duration').attr('data-start-time', testStartTime);
            }

            runningSetups.forEach(setup_id => {
                if (!currentlyRunningSetups.has(setup_id)) {
                    resetRow(setup_id);
                }
            });

            runningSetups = currentlyRunningSetups;
        }

        updateDuration();
    });
}, 1000);



setInterval(function () {
    fetch('/api/get_progress_state')
        .then(response => response.json())
        .then(all_progress => {
            for (const [setup_id, progress] of Object.entries(all_progress)) {
		let [completed, total] = progress.split('/').map(Number); // converts string to numbers
		let percentage = total === 0 ? 0 : Math.round((completed / total) * 100);
                document.getElementById(`progressElement_${setup_id}`).textContent = `${progress} (${percentage}%)`;
            }
        })
        .catch(error => console.error('Error fetching progress:', error));

}, 1000);


setInterval(updateDuration, 1000);
