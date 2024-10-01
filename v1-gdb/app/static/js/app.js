// search and filter functionality
$(document).ready(function() {
    // Function to fetch records from backend and display them
    function fetchRecords() {
        $.ajax({
            url: '/get_records', // Backend route to fetch records
            method: 'GET',
            dataType: 'json',
            success: function(data) {
                displayRecords(data); // Function to display records
            },
            error: function(_xhr, _status, error) {
                console.error('Error fetching records:', error);
            }
        });
    }

    // Function to display records
    function displayRecords(records) {
        var recordsList = $('#recordsList');
        recordsList.empty(); // Clear existing records

        records.forEach(function(record) {
            // Create HTML elements to display each record
            var listItem = $('<li>').text(record.title);
            recordsList.append(listItem);
        });
    }

    // Function to filter records based on search input
    $('#searchInput').on('input', function() {
        var searchKeyword = $(this).val().toLowerCase();
        var filteredRecords = records.filter(function(record) {
            return record.title.toLowerCase().includes(searchKeyword);
        });
        displayRecords(filteredRecords); // Update displayed records
    });

    // Initial fetch of records when the page loads
    fetchRecords();
});


// handles checkbox selected downloads and deletes
$(document).ready(function() {
    var selectedRecords = []; // Array to store selected record IDs

    // Function to handle checkbox click event
    $('.recordCheckbox').on('change', function() {
        var recordId = $(this).val();
        if ($(this).is(':checked')) {
            selectedRecords.push(recordId); // Add record ID to selection array
        } else {
            selectedRecords = selectedRecords.filter(function(id) {
                return id !== recordId; // Remove record ID from selection array
            });
        }
    });

    // Function to handle download button click event
    $('#downloadButton').on('click', function() {
        if (selectedRecords.length === 0) {
            alert('Please select at least one record.');
        } else {
            // Send selected record IDs to backend for download
            $.ajax({
                url: '/download_records', // Backend route for downloading records
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(selectedRecords),
                success: function(_response) {
                    // Handle download response
                },
                error: function(_xhr, _status, error) {
                    console.error('Error downloading records:', error);
                }
            });
        }
    });
});
