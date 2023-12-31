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
        
        // console.log(`Start Time for setupId ${setupId}:`, startTime);

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
      "job_name": "CI_5G_robot_AVQL_Regression_Tests_CIT_RFP_rexIO",
      "ip": "127.0.0.1",
      "URL": "",
      "comment": "Placeholder for localhost"
    },
    {
      "setup": "VM0 - Regression CIT RFP",
      "setup_id": 2,
      "job_name": "CI_5G_robot_AVQL_Regression_Tests_CIT_RFP_rexIO/",
      "ip": "10.83.204.180",
      "URL": "http://janusz.emea.nsn-net.net:8080/job/CI_5G_robot_AVQL_Regression_Tests_CIT_RFP_rexIO/",
      "comment": ""
    },
    {
      "setup": "VM0 - Regression CRT RFP",
      "setup_id": 3,
      "job_name": "CI_5G_robot_AVQL_Regression_Tests_CRT_RFP_rexIO/",
      "ip": "10.83.204.180",
      "URL": "http://janusz.emea.nsn-net.net:8080/job/CI_5G_robot_AVQL_Regression_Tests_CRT_RFP_rexIO/",
      "comment": ""
    },
    {
      "setup": "VM0 - Regression Tests stabi branch",
      "setup_id": 4,
      "job_name": "CI_5G_robot_AVQL_Regression_Tests_stabi_branch_rexIO/",
      "ip": "10.83.204.180",
      "URL": "http://janusz.emea.nsn-net.net:8080/job/CI_5G_robot_AVQL_Regression_Tests_stabi_branch_rexIO/",
      "comment": "raz na tydzień"
    },
    {
      "setup": "VM1 - Smoke Tests",
      "setup_id": 5,
      "job_name": "CI_5G_robot_AVQL_Smoke_Tests_rexIO/",
      "ip": "10.83.204.184",
      "URL": "http://janusz.emea.nsn-net.net:8080/job/CI_5G_robot_AVQL_Smoke_Tests_rexIO/",
      "comment": ""
    },
    {
      "setup": "VM2 - Acceptance Tests",
      "setup_id": 6,
      "job_name": "CI_5G_robot_AVQL_Acceptance_Tests_rexIO/",
      "ip": "10.83.204.181",
      "URL": "http://janusz.emea.nsn-net.net:8080/job/CI_5G_robot_AVQL_Acceptance_Tests_rexIO/",
      "comment": ""
    },
    {
      "setup": "VM2 - Acceptance Tests 23R4",
      "setup_id": 7,
      "job_name": "CI_5G_robot_AVQL_Acceptance_Tests_rexIO_23R4/",
      "ip": "10.83.204.181",
      "URL": "http://janusz.emea.nsn-net.net:8080/job/CI_5G_robot_AVQL_Acceptance_Tests_rexIO_23R4/",
      "comment": ""
    },
    {
      "setup": "VM2 - Acceptance Tests stabi branch",
      "setup_id": 8,
      "job_name": "CI_5G_robot_AVQL_Acceptance_Tests_stabi_branch_rexIO/",
      "ip": "10.83.204.181",
      "URL": "http://janusz.emea.nsn-net.net:8080/job/CI_5G_robot_AVQL_Acceptance_Tests_stabi_branch_rexIO/",
      "comment": "Raz na tydzień"
    },
    {
      "setup": "VM4 - Regression BIST Tests",
      "setup_id": 9,
      "job_name": "CI_5G_robot_AVQL_Regression_BIST_Tests/",
      "ip": "10.83.207.224",
      "URL": "http://janusz.emea.nsn-net.net:8080/job/CI_5G_robot_AVQL_Regression_BIST_Tests/",
      "comment": ""
    },
    {
      "setup": "VM5 - Regression CIT Linux",
      "setup_id": 10,
      "job_name": "CI_5G_robot_AVQL_Regression_Tests_CIT_Linux_rexIO/",
      "ip": "10.83.204.232",
      "URL": "http://janusz.emea.nsn-net.net:8080/job/CI_5G_robot_AVQL_Regression_Tests_CIT_Linux_rexIO/",
      "comment": ""
    },
    {
      "setup": "VM5 - Regression CRT Linux",
      "setup_id": 11,
      "job_name": "CI_5G_robot_AVQL_Regression_Tests_CRT_Linux_rexIO/",
      "ip": "10.83.204.232",
      "URL": "http://janusz.emea.nsn-net.net:8080/job/CI_5G_robot_AVQL_Regression_Tests_CRT_Linux_rexIO/",
      "comment": "17 buildów, raz na parę dni"
    },
    {
      "setup": "VM5 - Regression Tests Linux stabi",
      "setup_id": 12,
      "job_name": "CI_5G_robot_AVQL_Regression_Tests_Linux_stabi_rexIO/",
      "ip": "10.83.204.232",
      "URL": "http://janusz.emea.nsn-net.net:8080/job/CI_5G_robot_AVQL_Regression_Tests_Linux_stabi_rexIO/",
      "comment": "17 buildów raz na tydzień"
    },
    {
      "setup": "VM7 - Startup Reliability Tests",
      "setup_id": 13,
      "job_name": "CI_5G_robot_AVQL_Startup_Reliability_Tests_rexIO/",
      "ip": "10.83.206.68",
      "URL": "http://janusz.emea.nsn-net.net:8080/job/CI_5G_robot_AVQL_Startup_Reliability_Tests_rexIO/",
      "comment": "Raz na 12 godzin"
    },
    {
      "setup": "VM12 - Regression CRT Alarms",
      "setup_id": 14,
      "job_name": "CI_5G_robot_AVQL_Regression_Tests_CRT_Alarms_rexIO/",
      "ip": "10.83.204.109",
      "URL": "http://janusz.emea.nsn-net.net:8080/job/CI_5G_robot_AVQL_Regression_Tests_CRT_Alarms_rexIO/",
      "comment": "od 5 sierpnia raz na parę dni"
    },
    {
      "setup": "VM14 - Smoke Tests - A101",
      "setup_id": 15,
      "job_name": "CI_5G_robot_AVQL_Smoke_Tests_rexIO_A101/",
      "ip": "10.83.204.100",
      "URL": "http://janusz.emea.nsn-net.net:8080/job/CI_5G_robot_AVQL_Smoke_Tests_rexIO_A101/",
      "comment": ""
    },
    {
      "setup": "VM15 - Acceptance Tests - A101",
      "setup_id": 16,
      "job_name": "CI_5G_robot_AVQL_Acceptance_Tests_rexIO_A101/",
      "ip": "10.83.207.3",
      "URL": "http://janusz.emea.nsn-net.net:8080/job/CI_5G_robot_AVQL_Acceptance_Tests_rexIO_A101/",
      "comment": ""
    },
    {
      "setup": "VM17 - DEBUG",
      "setup_id": 17,
      "job_name": "CI_5G_robot_AVQL_Acceptance_Tests_rexIO_A101/",
      "ip": "10.83.207.37",
      "URL": "http://janusz.emea.nsn-net.net:8080/job/CI_5G_robot_AVQL_Acceptance_Tests_rexIO_A101/",
      "comment": ""
    },
    {
      "setup": "VM22 - DEBUG",
      "setup_id": 18,
      "job_name": "CI_5G_robot_AVQL_Acceptance_Tests_rexIO_A101/",
      "ip": "10.83.204.93",
      "URL": "http://janusz.emea.nsn-net.net:8080/job/CI_5G_robot_AVQL_Acceptance_Tests_rexIO_A101/",
      "comment": ""
    },
    {
      "setup": "Local laptop",
      "setup_id": 19,
      "job_name": "CI_5G_robot_AVQL_Acceptance_Tests_rexIO_A101/",
      "ip": "10.83.204.93",
      "URL": "http://janusz.emea.nsn-net.net:8080/job/CI_5G_robot_AVQL_Acceptance_Tests_rexIO_A101/",
      "comment": "local setup"
    }
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

let startTimesDict = {}

function updateStartTimesDict() {
    allSetupIds.forEach(setupId => {
        $.getJSON(`/api/get_start_times/${setupId}`)
            .done(function(times) {
                console.log(`Times for setupId ${setupId}:`, times);
                // It's okay for one of these to be null
                startTimesDict[setupId] = [times.setup_start_time, times.teardown_start_time];
            })
            .fail(function(jqxhr, textStatus, error) {
                const err = textStatus + ", " + error;
                console.error(`Request Failed for setupId ${setupId}: `, err);
            });
    });
}


// Call updateStartTimesDict every 2 seconds
setInterval(updateStartTimesDict, 2000);


setInterval(function() {
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

                let testName;
                if (entry.scope_status === 'running') {
                    testName = entry.test_name;
                    $(`#testNameElement_${entry.setup_id}`).closest('tr').find('.test-duration').attr('data-start-time', entry.test_start_time);
                    $(`#testNameElement_${entry.setup_id}`).text(entry.test_name);
                } else if (entry.scope_status === 'startup' || entry.scope_status === 'teardown') {
                    fetchStartTimes(entry.setup_id, entry.scope_status);
                } else {
                    testName = "Nothing";
                    $(`#testNameElement_${entry.setup_id}`).text(testName);
                    $(`#testNameElement_${entry.setup_id}`).closest('tr').find('.test-duration').attr('data-start-time', '');
                }
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

function fetchStartTimes(setupId, status) {
    $.getJSON(`/api/get_start_times/${setupId}`, function(times) {
        let testName = status === 'startup' ? "Suite Startup" : "Suite Teardown";
        let startTimeIndex = status === 'startup' ? 0 : 1;
        let startTimes = [times.setup_start_time, times.teardown_start_time];
        let testStartTime = startTimes[startTimeIndex];

        console.log('Fetching start times: ', testStartTime)

        $(`#testNameElement_${setupId}`).text(testName);
        $(`#testNameElement_${setupId}`).closest('tr').find('.test-duration').attr('data-start-time', testStartTime || '');
    }).fail(function(jqxhr, textStatus, error) {
        console.error(`Failed to fetch start times for setupId ${setupId}:`, textStatus, error);
    });
}


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


// setInterval(updateDuration, 1000);

// Function to log the startTimesDict to the console
function logStartTimesDict() {
    console.log('Current startTimesDict:', startTimesDict);
}

// Call logStartTimesDict every 5 seconds
setInterval(logStartTimesDict, 5000);
