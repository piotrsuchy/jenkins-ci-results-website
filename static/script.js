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
    $(`#testNameElement_${setup_id}`).text("Nothing");
    $(`#scopeNameElement_${setup_id}`).text("Nothing");
    $(`#testNameElement_${setup_id}`).closest('tr').find('.test-duration').text("-");
    $(`#testNameElement_${setup_id}`).closest('tr').find('.scope-duration').text("-");
}

function updateDuration() {
    document.querySelectorAll(".test-duration").forEach(td => {
        const startTime = td.getAttribute('data-start-time');
        if (startTime) {  
            td.innerText = computeDuration(startTime);
        }
    });

    document.querySelectorAll(".scope-duration").forEach(td => {
        const startTime = td.getAttribute('data-start-time');
        if (startTime) {  
            td.innerText = computeDuration(startTime);
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
    }
  ]
};


for (const pipeline of setupsConfig.pipelines) {
    allSetupIds.push(pipeline.setup_id);  // Assuming 'setup' is the unique identifier for each pipeline
}

setInterval(function(){
    $.getJSON("/current_test_data", function(data) {
        console.log("Received data:", data);

        // Reset all rows by default
        allSetupIds.forEach(id => {
            resetRow(id);
        });

        // Update rows for running setups
        for (let entry of data) {
            $(`#testNameElement_${entry.setup_id}`).text(entry.test_name || "Nothing");
            $(`#scopeNameElement_${entry.setup_id}`).text(entry.scope_name || "Nothing");
            $(`#testNameElement_${entry.setup_id}`).closest('tr').find('.test-duration').attr('data-start-time', entry.test_start_time);
            $(`#testNameElement_${entry.setup_id}`).closest('tr').find('.scope-duration').attr('data-start-time', entry.scope_start_time);
        }
    });
}, 3000);

setInterval(updateDuration, 1000);